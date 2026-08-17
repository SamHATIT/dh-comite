#!/usr/bin/env python3
"""Preflight — vérifie qu'une direction a les MOYENS de tenir son mandat.

POURQUOI CE SCRIPT (17/08) : six pannes en douze jours, toutes de la même famille.
Backlog non monté, dépôt en lecture seule, route inexistante, clé absente, direction
absente des rondes, canal imposé sans outil derrière. Dans les trois premiers cas,
c'est l'agent lui-même qui a fini par trouver la panne — après plusieurs jours
d'apparente inaction que le comité a lus comme de la négligence.

Le point commun : le mandat était écrit dans la fiche de l'agent, la capacité vivait
ailleurs (docker-compose.yml, .env, table curseurs), et rien ne rapprochait les deux.
Ce script est ce rapprochement, exécuté AVANT la ronde plutôt que découvert après.

Un agent NOT_READY ne rentre pas dans la ronde. Et son alerte part au Chief of Staff,
jamais à lui-même : voir la règle du paradoxe, ci-dessous et dans docs/PREFLIGHT.md.

    preflight.py delivery              une direction        → JSON, sortie 0 ou 1
    preflight.py --toutes              les directions actives
    preflight.py --toutes --dormantes  y compris les fonctions en veille
    preflight.py delivery --texte      sortie lisible par un humain
    preflight.py --lister              ce que déclare config/preflight.yaml
    preflight.py --autotest            vérifie le parseur et la règle du paradoxe

Sortie : JSON Lines, un objet par direction, au format fixé par LOT-05.
Codes   : 0 toutes READY · 1 au moins une NOT_READY · 2 erreur d'usage ou de config.

CE SCRIPT N'ÉCRIT RIEN — ni en base, ni sur la plateforme. Ses seuls accès en écriture
sont des fichiers témoins créés puis supprimés dans les montages déclarés `rw`, et
jamais dans une zone de la plateforme (invariant I1, appliqué par ZONES_PLATEFORME).
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import date

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHEMIN_CONFIG = os.path.join(RACINE, "config", "preflight.yaml")

# CADENCE (arbitrage de Sam, 17/08, SPEC §8.4 — point ouvert n° 4, clos) : le Preflight
# tourne AVANT CHAQUE RONDE, pas une fois par jour. Une passe complète sur les quatre
# directions actives coûte 0,8 s ; le compromis qui justifiait une passe quotidienne
# n'existait pas. Conséquence sur ces délais : ils sont un budget de temps par ronde,
# pas par jour. Les relever ferait payer chaque ronde, alors garder l'API à 5 s.
DELAI_OUTIL = 10      # secondes — au-delà, un outil qui ne rend pas la main est suspect
DELAI_SQL = 15
DELAI_API = 5         # « délai court » (LOT-05) : le Preflight ne doit pas retarder la ronde

# ── Invariant I1, rendu mécanique ────────────────────────────────────────────────
# Le Preflight teste l'écriture en écrivant vraiment (os.access ment sur un montage
# read-only quand on tourne en root : les bits de permission sont satisfaits, c'est le
# système de fichiers qui refuse). Ce test réel ne doit JAMAIS viser la plateforme.
# Un préfixe listé ici ne peut pas être testé en écriture, quoi qu'en dise la config.
ZONES_PLATEFORME = (
    "/repo", "/backlog", "/prodlogs", "/var/www",
    "/root/workspace/digital-humans-production",
)

AXES_DEFAUT = ["observer", "ecrire_base", "agir_production",
               "envoyer_externe", "engager_depense", "modifier_dispositif"]

CLE_VALIDE = re.compile(r"^[a-z][a-z0-9_-]*$")


# ═════════════════════════════════════════════════════════════════════════════════
#  La règle du paradoxe — un seul point de construction des échecs
# ═════════════════════════════════════════════════════════════════════════════════
#
# « Tu n'as pas les moyens de travailler → voici une tâche → travaille pour obtenir
#   les moyens. » C'est ce que produit une alerte Preflight assignée à l'agent qu'elle
# bloque : il ne peut pas se débloquer seul, par définition. Un montage manquant se
# répare dans docker-compose.yml, une clé dans .env, un curseur dans la table — trois
# endroits hors de sa portée.
#
# Toute alerte est donc assignée au Chief of Staff, qui décide QUI corrige. C'est la
# seule fonction du fichier qui fabrique un échec : il n'existe aucun chemin de code
# permettant d'assigner une alerte à la direction concernée. --autotest le vérifie.
#
# Exception unique, et elle est spécifiée (SPEC §4.2) : si c'est le CoS lui-même qui
# est NOT_READY, l'alerte remonte au CEO, qui prend sa place momentanément et alerte
# Sam. La règle tient dans les deux cas : jamais l'agent que l'alerte bloque.

OWNER_ALERTE = "chief-of-staff"
OWNER_SUPPLEANCE = "ceo"


def echec(direction, controle, detail, next_action):
    """Fabrique une alerte Preflight. Seul constructeur — voir la règle du paradoxe."""
    owner = OWNER_SUPPLEANCE if direction == OWNER_ALERTE else OWNER_ALERTE
    return {"controle": controle, "detail": detail,
            "next_action": next_action, "next_owner": owner}


# ═════════════════════════════════════════════════════════════════════════════════
#  Lecture de la configuration
# ═════════════════════════════════════════════════════════════════════════════════
#
# POURQUOI UN PARSEUR DE REPLI : le conteneur dh-comite est bâti sur ubuntu:24.04 avec
# postgresql-client, jq et python3 (arrivé par python3-matplotlib). PyYAML n'y est pas
# garanti, et rebâtir l'image pour une dépendance de confort supposerait de redémarrer
# le comité — un effet de bord plus coûteux que le problème. On utilise donc PyYAML
# s'il est là, et à défaut un parseur du sous-ensemble strictement employé par
# preflight.yaml. `--autotest` compare les deux lectures quand PyYAML est présent :
# l'équivalence est vérifiée, pas supposée.

class ErreurConfig(Exception):
    pass


def _sans_commentaire(ligne):
    """Retire un commentaire # hors chaîne quotée."""
    dehors, quote = [], None
    for c in ligne:
        if quote:
            dehors.append(c)
            if c == quote:
                quote = None
        elif c in "\"'":
            quote = c
            dehors.append(c)
        elif c == "#":
            break
        else:
            dehors.append(c)
    return "".join(dehors).rstrip()


def _scalaire(texte):
    t = texte.strip()
    if len(t) >= 2 and t[0] == t[-1] and t[0] in "\"'":
        return t[1:-1]
    if t.startswith("[") and t.endswith("]"):
        dedans = t[1:-1].strip()
        return [_scalaire(x) for x in dedans.split(",")] if dedans else []
    if t in ("", "null", "~"):
        return None
    if t in ("true", "True"):
        return True
    if t in ("false", "False"):
        return False
    if re.fullmatch(r"-?\d+", t):
        return int(t)
    if re.fullmatch(r"-?\d+\.\d+", t):
        return float(t)
    return t


_PAIRE = re.compile(r"^[A-Za-z_][A-Za-z0-9_.-]*\s*:(\s|$)")


def _lignes(texte):
    out = []
    for num, brute in enumerate(texte.splitlines(), 1):
        if "\t" in brute:
            raise ErreurConfig(f"ligne {num} : tabulation interdite en YAML")
        sans = _sans_commentaire(brute)
        if not sans.strip():
            continue
        out.append((len(sans) - len(sans.lstrip(" ")), sans.strip(), num))
    return out


def _parse(L, i, indent):
    return (_parse_liste if L[i][1].startswith("- ") else _parse_map)(L, i, indent)


def _parse_liste(L, i, indent):
    items = []
    while i < len(L) and L[i][0] == indent and L[i][1].startswith("- "):
        reste, num = L[i][1][2:].strip(), L[i][2]
        if not reste:                                   # « - » puis bloc indenté
            i += 1
            if i < len(L) and L[i][0] > indent:
                valeur, i = _parse(L, i, L[i][0])
                items.append(valeur)
            else:
                items.append(None)
        elif _PAIRE.match(reste):                       # « - clé: valeur » + suite
            sous, i = [(indent + 2, reste, num)], i + 1
            while i < len(L) and L[i][0] > indent:
                sous.append(L[i])
                i += 1
            valeur, _ = _parse_map(sous, 0, indent + 2)
            items.append(valeur)
        else:                                           # scalaire
            items.append(_scalaire(reste))
            i += 1
    return items, i


def _parse_map(L, i, indent):
    d = {}
    while i < len(L) and L[i][0] == indent:
        ligne, num = L[i][1], L[i][2]
        if ligne.startswith("- "):
            break
        if not _PAIRE.match(ligne):
            raise ErreurConfig(f"ligne {num} : hors du sous-ensemble YAML accepté "
                               f"(attendu « clé: valeur ») : {ligne[:60]}")
        cle, _, reste = ligne.partition(":")
        cle, reste = cle.strip(), reste.strip()
        if reste:
            d[cle] = _scalaire(reste)
            i += 1
        else:
            i += 1
            if i < len(L) and L[i][0] > indent:
                d[cle], i = _parse(L, i, L[i][0])
            elif i < len(L) and L[i][0] == indent and L[i][1].startswith("- "):
                d[cle], i = _parse_liste(L, i, indent)   # liste alignée sur sa clé
            else:
                d[cle] = None
    return d, i


def yaml_minimal(texte):
    L = _lignes(texte)
    if not L:
        return {}
    valeur, i = _parse(L, 0, L[0][0])
    if i != len(L):
        raise ErreurConfig(f"ligne {L[i][2]} : indentation incohérente")
    return valeur


def charger_config(chemin=CHEMIN_CONFIG):
    with open(chemin, encoding="utf-8") as fh:
        texte = fh.read()
    try:
        import yaml
        conf = yaml.safe_load(texte)
    except ImportError:
        conf = yaml_minimal(texte)
    if not isinstance(conf, dict) or "directions" not in conf:
        raise ErreurConfig(f"{chemin} : clé « directions » absente")
    return conf


# ═════════════════════════════════════════════════════════════════════════════════
#  Accès en LECTURE à la base du comité
# ═════════════════════════════════════════════════════════════════════════════════

def sql_lecture(requete):
    """Exécute un SELECT sur la base du comité. Renvoie (lignes, erreur).

    Le Preflight ne fait que lire : aucun appel de ce fichier n'écrit en base. Les
    seules valeurs interpolées dans une requête sont des clés de config validées par
    CLE_VALIDE, jamais une saisie libre.
    """
    dsn = os.environ.get("COMITE_DB_DSN", "")
    if not dsn:
        return None, "COMITE_DB_DSN absente de l'environnement"
    try:
        r = subprocess.run(["psql", dsn, "-tA", "-F", "|", "-c", requete],
                           capture_output=True, text=True, timeout=DELAI_SQL)
    except FileNotFoundError:
        return None, "psql introuvable dans le conteneur"
    except subprocess.TimeoutExpired:
        return None, f"base injoignable (pas de réponse en {DELAI_SQL} s)"
    if r.returncode != 0:
        derniere = [x for x in r.stderr.strip().splitlines() if x]
        return None, (derniere[-1][:160] if derniere else "psql en échec")
    return [x for x in r.stdout.splitlines() if x], None


# ═════════════════════════════════════════════════════════════════════════════════
#  Les huit contrôles
# ═════════════════════════════════════════════════════════════════════════════════

def _absolu(chemin):
    return chemin if os.path.isabs(chemin) else os.path.join(RACINE, chemin)


def _sous_plateforme(chemin):
    reel = os.path.abspath(chemin)
    return any(reel == z or reel.startswith(z + "/") for z in ZONES_PLATEFORME)


def _test_ecriture(dossier):
    """Écrit puis supprime un témoin. Renvoie None si OK, sinon le motif.

    On écrit vraiment : sur un montage read-only, os.access(W_OK) répond vrai en root
    alors que l'écriture échoue en EROFS. C'est exactement le cas qui a rendu trois
    feux verts du 13/08 inexécutables sans que personne ne le voie (14/08).
    """
    if _sous_plateforme(dossier):
        return "refus interne : test d'écriture interdit sous la plateforme (I1)"
    temoin = os.path.join(dossier, f".preflight-{os.getpid()}")
    try:
        with open(temoin, "w", encoding="utf-8") as fh:
            fh.write("preflight")
        os.unlink(temoin)
        return None
    except OSError as e:
        return f"{e.strerror or e}"


def controle_tools(direction, spec):
    echecs = []
    for outil in spec.get("outils") or []:
        chemin = _absolu(outil["chemin"])
        nom = outil["chemin"]
        if not os.path.exists(chemin):
            echecs.append(echec(direction, "tools", f"{nom} n'existe pas",
                                f"rétablir {nom} ou retirer la capacité de la fiche"))
            continue
        if not os.access(chemin, os.X_OK):
            echecs.append(echec(direction, "tools", f"{nom} n'est pas exécutable",
                                f"chmod +x {nom}"))
            continue
        if not outil.get("verifier_aide", True):
            continue
        # « répond à --help sans effet de bord ». Définition posée par l'incident du
        # 17/08 : `sf-lead --help` déposait le texte littéral « --help » dans la file
        # Salesforce. Depuis, il imprime son usage et sort en 2 — un code non nul qui
        # signale un refus propre, pas une panne. On n'exige donc PAS un code 0 : on
        # exige que le processus rende la main, sans planter.
        try:
            r = subprocess.run([chemin, "--help"], capture_output=True, text=True,
                               timeout=DELAI_OUTIL)
        except subprocess.TimeoutExpired:
            echecs.append(echec(direction, "tools",
                                f"{nom} ne rend pas la main sur --help ({DELAI_OUTIL} s)",
                                f"vérifier {nom} : il attend une entrée ou boucle"))
            continue
        except OSError as e:
            echecs.append(echec(direction, "tools", f"{nom} ne démarre pas : {e}",
                                f"vérifier l'interpréteur de {nom}"))
            continue
        if r.returncode in (126, 127):
            echecs.append(echec(direction, "tools",
                                f"{nom} ne s'exécute pas (code {r.returncode})",
                                f"vérifier les droits et le shebang de {nom}"))
        elif "Traceback (most recent call last)" in r.stderr:
            echecs.append(echec(direction, "tools", f"{nom} lève une exception sur --help",
                                f"corriger {nom} avant la prochaine ronde"))
    return echecs, []


def controle_credentials(direction, spec):
    """Présence, jamais valeur. Aucune clé n'est imprimée par ce script."""
    echecs = []
    for cred in spec.get("credentials") or []:
        if "variable" in cred:
            nom = cred["variable"]
            if not (os.environ.get(nom) or "").strip():
                echecs.append(echec(direction, "credentials",
                                    f"{nom} absente ou vide dans l'environnement",
                                    f"renseigner {nom} dans .env puis relancer le conteneur"))
        elif "fichier" in cred:
            chemin, cle = cred["fichier"], cred["cle"]
            try:
                with open(chemin, encoding="utf-8", errors="replace") as fh:
                    trouve = any(l.startswith(cle + "=") and l.split("=", 1)[1].strip()
                                 for l in fh)
            except OSError as e:
                echecs.append(echec(direction, "credentials",
                                    f"{chemin} illisible ({e.strerror or e}) — clé {cle}",
                                    f"vérifier le montage de {chemin}"))
                continue
            if not trouve:
                echecs.append(echec(direction, "credentials",
                                    f"{cle} absente ou vide dans {chemin}",
                                    f"renseigner {cle} dans {chemin}"))
    return echecs, []


def controle_permissions(direction, spec, axes):
    """Les six axes existent en base pour la clé que lira le garde-fou.

    Le garde-fou pretooluse-guard.sh lit DH_DIRECTION, cherche la ligne, et retombe
    sur le niveau 1 (Observe) s'il ne la trouve pas — silencieusement, et c'est un
    défaut délibéré côté garde-fou (mieux vaut tout refuser que tout permettre). Mais
    côté direction, cela produit une fonction muette dont personne ne sait qu'elle est
    muette : le Juridique le 06/08, le Financier le 14/08. On vérifie donc ici.
    """
    cle = spec.get("curseurs_direction") or direction
    if not CLE_VALIDE.match(cle):
        return [echec(direction, "permissions", f"clé de curseur invalide : {cle!r}",
                      "corriger config/preflight.yaml")], []
    lignes, err = sql_lecture(
        f"SELECT type_tache FROM curseurs WHERE direction = '{cle}'")
    if err:
        return [echec(direction, "permissions", f"curseurs illisibles : {err}",
                      "rétablir l'accès à la base du comité")], []

    presents = set(lignes)
    manquants = [a for a in axes if a not in presents]
    if not manquants:
        return [], []

    detail = f"curseurs absents pour « {cle} » : {', '.join(manquants)}"
    action = f"créer les curseurs manquants de « {cle} » (arbitrage de Sam : colonne maj_par)"

    # Cas de la bascule Growth : les lignes existent sous les anciennes clés, mais pas
    # sous celle que lit le garde-fou. La direction n'est pas « sans réglage » — elle
    # est sous un réglage que personne n'a voulu : Observe partout, par défaut.
    composantes = spec.get("curseurs_composantes") or []
    if composantes and len(manquants) == len(axes):
        couvertes = []
        for comp in composantes:
            if not CLE_VALIDE.match(comp):
                continue
            l2, e2 = sql_lecture(
                f"SELECT type_tache FROM curseurs WHERE direction = '{comp}'")
            if not e2 and set(axes) <= set(l2):
                couvertes.append(comp)
        if couvertes:
            detail = (f"« {cle} » n'a aucun curseur ; les réglages vivent encore sous "
                      f"{', '.join(couvertes)}. Le garde-fou lit DH_DIRECTION et "
                      f"retombera sur Observe pour les six axes.")
            action = (f"reporter les curseurs de {', '.join(couvertes)} sur « {cle} », "
                      f"ou faire tourner la ronde sous les anciennes clés")
    return [echec(direction, "permissions", detail, action)], []


def controle_mounts(direction, spec):
    echecs = []
    for m in spec.get("mounts") or []:
        # Le chemin déclaré peut être relatif à la racine du dépôt (« . »,
        # « file-salesforce ») ou absolu s'il s'agit d'un point de montage du
        # conteneur (/repo, /prodlogs). On résout, mais on affiche le déclaré :
        # c'est celui qu'on retrouvera dans docker-compose.yml.
        declare, mode = m["chemin"], (m.get("mode") or "ro")
        chemin = _absolu(declare)
        if not os.path.isdir(chemin):
            echecs.append(echec(direction, "mounts", f"{declare} non monté",
                                f"monter {declare} dans docker-compose.yml puis recréer le conteneur"))
            continue
        if mode == "ro":
            # On ne teste PAS l'écriture d'un montage read-only : les zones concernées
            # sont celles de la plateforme, et I1 interdit d'y écrire — y compris un
            # fichier témoin, y compris pour vérifier qu'on ne peut pas.
            try:
                os.listdir(chemin)
            except OSError as e:
                echecs.append(echec(direction, "mounts",
                                    f"{declare} monté mais illisible ({e.strerror or e})",
                                    f"vérifier les droits de {declare}"))
        else:
            motif = _test_ecriture(chemin)
            if motif:
                echecs.append(echec(direction, "mounts",
                                    f"{declare} non monté en écriture ({motif})",
                                    f"monter {declare} en rw dans docker-compose.yml"))
    return echecs, []


def controle_apis(direction, spec):
    """Requêtes GET uniquement, délai court. Un service optionnel n'est pas bloquant."""
    echecs, avertissements = [], []
    for api in spec.get("apis") or []:
        nom, url = api.get("nom") or api["url"], api["url"]
        try:
            requete = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(requete, timeout=DELAI_API):
                pass
            continue
        except urllib.error.HTTPError:
            continue        # 401, 403, 404 : le service répond, c'est ce qu'on teste
        except Exception as e:
            motif = f"{nom} ne répond pas ({type(e).__name__})"
        if api.get("optionnel"):
            avertissements.append(f"api {motif} — déclaré optionnel, non bloquant")
        else:
            echecs.append(echec(direction, "apis", motif,
                                f"rétablir {nom} ou le déclarer optionnel dans preflight.yaml"))
    return echecs, avertissements


def controle_budget(direction, spec):
    """Budget restant sur la période.

    I3 — aucun indicateur auto-déclaré : la consommation n'est PAS lue dans un rapport
    d'agent mais dans les fichiers de sortie de `claude -p --output-format json`, écrits
    par l'outil, que l'agent évalué ne rédige pas. Même source que bin/couts.py.

    Le plafond, lui, n'est pas tranché (SPEC §8.1 — coût cible du comité). Tant qu'il
    vaut null, le contrôle reporte la consommation constatée et se déclare INDETERMINE.
    Il ne fabrique pas un seuil pour avoir l'air de conclure.
    """
    budget = spec.get("budget") or {}
    prefixe = budget.get("traces")
    mois = date.today().strftime("%Y-%m")
    consomme, n = 0.0, 0
    dossier = os.path.join(RACINE, "rondes")
    if prefixe and os.path.isdir(dossier):
        for nom in os.listdir(dossier):
            if not (nom.startswith(prefixe + "-") and nom.endswith(".json")):
                continue
            if f"-{mois}-" not in nom:
                continue
            try:
                with open(os.path.join(dossier, nom), encoding="utf-8") as fh:
                    cout = json.load(fh).get("total_cost_usd")
            except Exception:
                continue
            if cout:
                consomme += float(cout)
                n += 1

    plafond = budget.get("plafond_usd_mois")
    if plafond is None:
        return [], [f"budget INDETERMINE — {consomme:.2f} USD constatés sur {mois} "
                    f"({n} exécutions). Plafond non tranché : SPEC §8.1."]
    if consomme >= float(plafond):
        return [echec(direction, "budget",
                      f"plafond atteint : {consomme:.2f} / {plafond} USD sur {mois}",
                      "arbitrer le relèvement ou suspendre la cadence (SPEC §1.3)")], []
    return [], [f"budget : {consomme:.2f} / {plafond} USD consommés sur {mois}"]


def controle_policy(direction, spec, canaux):
    """Le canal imposé désigne-t-il un outil qui existe ?

    Sixième panne de la série : des curseurs annonçant des canaux qui n'existent pas.
    Une direction lit « passe par tel canal » et n'a rien pour le faire — consigne
    inapplicable, qu'aucun contrôle ne rattrapait.

    curseurs.canal_impose contient de la PROSE, pas un identifiant : constaté le 17/08
    sur la sauvegarde du 11/08. On reconnaît le canal par motifs, et l'on n'échoue que
    sur ce qu'on a su reconnaître. Un canal non reconnu produit un avertissement — on
    ne bloque pas une ronde sur une phrase qu'on n'a pas su lire.
    """
    echecs, avertissements = [], []
    cle = spec.get("curseurs_direction") or direction
    if not CLE_VALIDE.match(cle):
        return [], []
    lignes, err = sql_lecture(
        "SELECT type_tache || '|' || replace(coalesce(canal_impose, ''), '|', '/') "
        f"FROM curseurs WHERE direction = '{cle}' AND coalesce(canal_impose, '') <> ''")
    if err:
        return [echec(direction, "policy", f"canaux imposés illisibles : {err}",
                      "rétablir l'accès à la base du comité")], []

    for ligne in lignes:
        axe, _, prose = ligne.partition("|")
        bas = prose.lower()
        reconnus = [c for c in (canaux or [])
                    if any(m.lower() in bas for m in (c.get("motifs") or []))]
        if not reconnus:
            avertissements.append(
                f"policy : canal imposé de l'axe {axe} non résolu en outil "
                f"(« {prose[:70].strip()}… ») — vérification impossible, "
                f"ajouter un motif dans config/preflight.yaml si c'en est un")
            continue
        for canal in reconnus:
            cible = canal.get("outil")
            if not cible:
                continue        # canal reconnu mais non exécutable : rien à vérifier
            chemin = _absolu(cible)
            if not (os.path.exists(chemin) and os.access(chemin, os.X_OK)):
                echecs.append(echec(direction, "policy",
                                    f"canal imposé « {canal['nom']} » (axe {axe}) "
                                    f"désigne {cible}, absent ou non exécutable",
                                    f"rétablir {cible}, ou lever le canal imposé"))
    return echecs, avertissements


def controle_evidence(direction, spec):
    """Un moyen de PROUVER le travail, au moins un.

    Cas d'école du 08/08 : le Juridique, créé le 02/08, n'avait aucun périmètre
    d'écriture dans deos-state. Ses rapports étaient refusés en silence — « 0 rapport
    legal » pendant cinq jours. Il travaillait ; rien n'arrivait. Un mandat sans moyen
    de preuve produit un agent que l'on croit inactif.
    """
    moyens = spec.get("evidence") or []
    if not moyens:
        return [echec(direction, "evidence", "aucun moyen de preuve déclaré",
                      "déclarer un dépôt ou une table dans config/preflight.yaml")], []
    motifs, ok = [], False
    for m in moyens:
        t = m.get("type")
        if t == "table":
            table = m["table"]
            if not CLE_VALIDE.match(table):
                motifs.append(f"table {table!r} : nom invalide")
                continue
            _, err = sql_lecture(f"SELECT 1 FROM {table} LIMIT 1")
            if err:
                motifs.append(f"table {table} : {err}")
            else:
                ok = True
        elif t in ("depot", "fichier"):
            declare = m["chemin"]
            chemin = _absolu(declare)
            cible = chemin if os.path.isdir(chemin) else os.path.dirname(chemin)
            if not os.path.isdir(cible):
                motifs.append(f"{declare} : absent")
                continue
            motif = _test_ecriture(cible)
            if motif:
                motifs.append(f"{declare} : non inscriptible ({motif})")
            else:
                ok = True
        else:
            motifs.append(f"type de preuve inconnu : {t!r}")
    if ok:
        return [], ([f"evidence : moyen(s) indisponible(s) — {' ; '.join(motifs)}"]
                    if motifs else [])
    return [echec(direction, "evidence",
                  f"aucun moyen de preuve utilisable — {' ; '.join(motifs)}",
                  "ouvrir un espace d'écriture ou un scope deos-state à cette direction")], []


CONTROLES = ["tools", "credentials", "permissions", "mounts",
             "apis", "budget", "policy", "evidence"]


def verifier(direction, conf):
    spec = conf["directions"][direction]
    axes = conf.get("axes_curseurs") or AXES_DEFAUT
    canaux = conf.get("canaux") or []

    resultats = [
        controle_tools(direction, spec),
        controle_credentials(direction, spec),
        controle_permissions(direction, spec, axes),
        controle_mounts(direction, spec),
        controle_apis(direction, spec),
        controle_budget(direction, spec),
        controle_policy(direction, spec, canaux),
        controle_evidence(direction, spec),
    ]
    echecs = [e for lot, _ in resultats for e in lot]
    avertissements = [a for _, lot in resultats for a in lot]

    # Filet : la règle du paradoxe ne doit pas pouvoir être contournée par un ajout
    # futur de contrôle. Si une alerte se retrouvait assignée à la direction qu'elle
    # bloque, on préfère une erreur bruyante à une alerte qui n'ira nulle part.
    for e in echecs:
        if e["next_owner"] == direction:
            raise AssertionError(
                f"règle du paradoxe violée : alerte {e['controle']} assignée à {direction}")

    return {
        "direction": direction,
        "statut": "NOT_READY" if echecs else "READY",
        "echecs": echecs,
        "avertissements": avertissements,
        "points_ouverts": spec.get("points_ouverts") or [],
        "etat": spec.get("etat"),
        "cadence": spec.get("cadence"),
        "controles": CONTROLES,
        "date": date.today().isoformat(),
    }


# ═════════════════════════════════════════════════════════════════════════════════
#  Sorties
# ═════════════════════════════════════════════════════════════════════════════════

def rendre_texte(r):
    lignes = [f"── {r['direction']}  [{r['etat']}/{r['cadence']}]  {r['statut']}"]
    if r["statut"] == "READY":
        lignes.append("   les huit contrôles passent.")
    for e in r["echecs"]:
        lignes.append(f"   ✗ {e['controle']:<12} {e['detail']}")
        lignes.append(f"     → {e['next_action']}  [{e['next_owner']}]")
    for a in r["avertissements"]:
        lignes.append(f"   · {a}")
    for p in r["points_ouverts"]:
        lignes.append(f"   ? {p}")
    return "\n".join(lignes)


def autotest(conf):
    """Vérifie ce qui peut l'être sans base ni conteneur."""
    ok = True

    # 1. Le parseur de repli lit-il la config comme PyYAML ?
    with open(CHEMIN_CONFIG, encoding="utf-8") as fh:
        texte = fh.read()
    interne = yaml_minimal(texte)
    try:
        import yaml
        if interne != yaml.safe_load(texte):
            print("✗ le parseur de repli diverge de PyYAML sur preflight.yaml")
            ok = False
        else:
            print("✓ parseur de repli identique à PyYAML sur preflight.yaml")
    except ImportError:
        print("· PyYAML absent : équivalence non vérifiable ici, parseur de repli utilisé")

    # 2. La règle du paradoxe : aucune alerte assignée à l'agent qu'elle bloque.
    for direction in conf["directions"]:
        e = echec(direction, "tools", "témoin", "témoin")
        if e["next_owner"] == direction:
            print(f"✗ règle du paradoxe : {direction} s'assignerait sa propre alerte")
            ok = False
    print("✓ règle du paradoxe : aucune direction ne reçoit sa propre alerte")
    if echec("chief-of-staff", "tools", "t", "t")["next_owner"] != OWNER_SUPPLEANCE:
        print("✗ suppléance du CoS non appliquée (SPEC §4.2)")
        ok = False
    else:
        print(f"✓ suppléance : une alerte sur le CoS va au {OWNER_SUPPLEANCE} (SPEC §4.2)")

    # 3. Cohérence de la config : canaux résolus, clés valides, contrôles couverts.
    for canal in conf.get("canaux") or []:
        cible = canal.get("outil")
        if cible and not os.path.exists(_absolu(cible)):
            print(f"✗ canal « {canal['nom']} » désigne {cible}, absent du dépôt")
            ok = False
        if not (canal.get("motifs") or []):
            print(f"✗ canal « {canal.get('nom')} » sans motif : jamais reconnaissable")
            ok = False
    for direction, spec in conf["directions"].items():
        if not CLE_VALIDE.match(spec.get("curseurs_direction") or direction):
            print(f"✗ {direction} : clé de curseur invalide")
            ok = False
        for m in spec.get("mounts") or []:
            if (m.get("mode") or "ro") == "rw" and _sous_plateforme(_absolu(m["chemin"])):
                print(f"✗ {direction} : {m['chemin']} déclaré rw sous la plateforme (I1)")
                ok = False
    print("✓ config : canaux résolus, clés valides, aucun montage rw sous la plateforme")
    return ok


def main():
    ap = argparse.ArgumentParser(
        description="Preflight — mandat ↔ capacité, huit contrôles par direction.")
    ap.add_argument("directions", nargs="*", help="directions à vérifier")
    ap.add_argument("--toutes", action="store_true", help="toutes les directions actives")
    ap.add_argument("--dormantes", action="store_true",
                    help="avec --toutes : inclut les fonctions en veille")
    ap.add_argument("--texte", action="store_true", help="sortie lisible plutôt que JSON")
    ap.add_argument("--lister", action="store_true", help="liste ce que déclare la config")
    ap.add_argument("--autotest", action="store_true", help="vérifie parseur et invariants")
    ap.add_argument("--config", default=CHEMIN_CONFIG)
    a = ap.parse_args()

    try:
        conf = charger_config(a.config)
    except (OSError, ErreurConfig) as e:
        print(f"config illisible : {e}", file=sys.stderr)
        return 2

    if a.autotest:
        return 0 if autotest(conf) else 1

    if a.lister:
        for nom, spec in conf["directions"].items():
            print(f"{nom:<18} {spec.get('etat'):<8} {spec.get('cadence')}")
        return 0

    if a.toutes:
        cibles = [n for n, s in conf["directions"].items()
                  if a.dormantes or s.get("etat") == "active"]
    else:
        cibles = a.directions
    if not cibles:
        ap.print_usage(sys.stderr)
        print("preflight : nommer une direction, ou --toutes", file=sys.stderr)
        return 2

    inconnues = [c for c in cibles if c not in conf["directions"]]
    if inconnues:
        print(f"direction inconnue : {', '.join(inconnues)} — voir --lister", file=sys.stderr)
        return 2

    bloquee = False
    for cible in cibles:
        r = verifier(cible, conf)
        bloquee = bloquee or r["statut"] == "NOT_READY"
        print(rendre_texte(r) if a.texte
              else json.dumps(r, ensure_ascii=False, separators=(",", ":")))
    return 1 if bloquee else 0


if __name__ == "__main__":
    sys.exit(main())
