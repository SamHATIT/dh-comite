#!/usr/bin/env python3
"""Clot les decisions dont la preuve est VERIFIABLE MECANIQUEMENT.

POURQUOI (17/08) : constat de Sam — « on a valide plus de vingt decisions
depuis une semaine, pas une des taches n'est faite ». Verification faite, c'est
en partie inexact : le Delivery avait deja corrige DEC-2026-0810-09, commit
62674ed. Mais la decision etait toujours au statut accordee.

La cause est un defaut de circuit, pas de travail. Celui qui FAIT n'a pas le
droit de declarer termine — deos-decisions refuse un changement de statut
venant d'une direction, et son curseur ecrire_base est a Conseille. Celui qui
A le droit (CoS, CEO, Sam) ne fait pas le tour. Resultat : 40 decisions
accordees de plus de trois jours, dont une partie deja faite.

CE SCRIPT NE JUGE PAS LE TRAVAIL. Il verifie qu'une reference citee EXISTE :
un commit qui mentionne la decision, un fichier, une table. Si oui, il clot en
citant la preuve. Sinon il laisse ouvert.

IL EST DELIBEREMENT CONSERVATEUR. Fermer a tort est PIRE que laisser trainer :
une decision close sort du radar et personne n'y revient. Dans le doute, on
laisse ouvert et on le dit.

Usage : cloturer-prouvees.py [--appliquer]   (sans l option : simulation)
"""
import json, os, re, subprocess, sys

APPLIQUER = "--appliquer" in sys.argv
DEPOTS = ["/repo-delivery", "/repo"]


def sql(requete):
    r = subprocess.run(["psql", os.environ["COMITE_DB_DSN"], "-tAF", "|", "-c", requete],
                       capture_output=True, text=True, timeout=40)
    return [l.split("|") for l in r.stdout.strip().split("\n") if l]


def commits_citant(dec):
    """Cherche un commit dont le message cite la decision. C'est la preuve la
    plus forte : le travail est date, signe, et son contenu est lisible."""
    for depot in DEPOTS:
        if not os.path.isdir(os.path.join(depot, ".git")):
            continue
        r = subprocess.run(["git", "log", "--all", "--format=%H|%s", f"--grep={dec}"],
                           cwd=depot, capture_output=True, text=True, timeout=30)
        for ligne in r.stdout.strip().split("\n"):
            if "|" in ligne:
                h, sujet = ligne.split("|", 1)
                # verifier que le commit a bien touche des fichiers
                n = subprocess.run(["git", "show", "--stat", "--format=", h],
                                   cwd=depot, capture_output=True, text=True, timeout=20)
                if n.stdout.strip():
                    return depot, h[:8], sujet[:70]
    return None


def trace_en_base(dec):
    """Une decision reglee par une ecriture en base laisse une empreinte : une
    cle dans deos_state, une ligne ajoutee, un curseur modifie. On cherche la
    reference de la decision dans les valeurs stockees — c'est la meme logique
    que pour un commit, appliquee a un autre support.
    Ajoute le 17/08 : la version precedente ne voyait QUE Git, donc toute
    decision reglee autrement restait ouverte indefiniment."""
    # CORRECTIF DU 17/08, releve en simulation. La premiere version cherchait
    # la reference PARTOUT dans deos_state — et trouvait 35 candidats au lieu
    # de 6, presque tous faux. La cause : les cles rapport_*, brief et
    # calendrier_* sont des endroits ou l on PARLE des decisions, pas ou on les
    # APPLIQUE. Un brief qui mentionne DEC-2026-0813-04 ne prouve rien : il
    # prouve seulement que le CEO l a lue.
    # On exclut donc ces cles narratives et on ne garde que celles qui portent
    # un etat metier.
    NARRATIVES = ("rapport_", "brief", "calendrier_", "journal", "suivi_")
    try:
        r = sql(f"SELECT cle FROM deos_state WHERE valeur::text ILIKE '%{dec}%' LIMIT 5")
        for (cle,) in [(x[0],) for x in r]:
            if not any(cle.startswith(n) or cle == n.rstrip("_") for n in NARRATIVES):
                return ("deos_state", cle)
        r = sql(f"SELECT type_tache FROM curseurs WHERE justification ILIKE '%{dec}%' LIMIT 1")
        if r:
            return ("curseurs", r[0][0])
    except Exception:
        pass
    return None


def trace_fichier(dec):
    """Un fichier de configuration qui cite la decision. Moins fort qu un commit
    — le fichier peut ne pas etre versionne — mais c'est une empreinte reelle."""
    try:
        r = subprocess.run(["grep", "-rl", dec, "/workspace/config", "/workspace/.claude"],
                           capture_output=True, text=True, timeout=25)
        f = [x for x in r.stdout.strip().split("\n") if x]
        if f:
            return f[0].replace("/workspace/", "")
    except Exception:
        pass
    return None


def main():
    ouvertes = sql("SELECT id, origine, (now()::date - date::date) FROM decisions "
                   "WHERE statut = 'accordee' ORDER BY date")
    print(f"{len(ouvertes)} decision(s) accordee(s) a examiner")
    print()

    closes, laissees = [], []
    for dec, origine, age in ouvertes:
        p = commits_citant(dec)
        if p:
            depot, court, sujet = p
            closes.append((dec, origine, age, "commit", f"{court} — {sujet}"))
            continue
        b = trace_en_base(dec)
        if b:
            closes.append((dec, origine, age, "base", f"{b[0]} / {b[1]}"))
            continue
        # RETIRE LE 17/08 : la recherche par fichier produisait surtout du bruit.
        # config/evolution/evolution_2026-08-16.md ressortait pour QUATRE
        # decisions sans rapport, la fiche du Delivery pour une cinquieme. Ce
        # sont des documents qui LISTENT les decisions, pas qui les appliquent.
        # Le motif est general : tout document qui parle des decisions ressemble
        # a une preuve. Seul le commit porte un travail date et signe.
        laissees.append((dec, origine, age, "aucune empreinte"))

    if closes:
        print("EMPREINTE TROUVEE — a faire relire par le Chief of Staff :")
        for dec, origine, age, genre, ref in closes:
            print(f"  {dec}  {age:>2}j  {origine:<10} [{genre}] {ref[:56]}")
    print()
    print(f"{len(laissees)} sans empreinte — laissee(s) ouverte(s).")

    if not APPLIQUER:
        print()
        print("SIMULATION. Relancer avec --appliquer pour lancer la relecture.")
        return

    # ── RELECTURE PAR LE CHIEF OF STAFF ───────────────────────────────────
    # Ce script ne CLOT PLUS de lui-meme (correction du 17/08, demande de Sam).
    # Une empreinte prouve qu un travail a eu lieu, pas qu il fait ce que la
    # decision demandait. Verifier cela suppose de LIRE le commit et de juger —
    # aucune regle mecanique ne le fera.
    #
    # On separe donc les deux etages : la machine trouve les candidats, le
    # Chief of Staff les relit et tranche. C est aussi un controle CROISE —
    # celui qui relit n est pas celui qui a ecrit.
    print()
    print("Relecture par le Chief of Staff...")
    for dec, origine, age, genre, ref in closes:
        invite = f"""Tu verifies UNE decision, {dec}, et rien d autre.

Une empreinte a ete trouvee automatiquement : [{genre}] {ref}

Ta tache : lire la decision avec deos-decisions, lire ce que l empreinte
designe reellement (le commit avec git show, le fichier, la cle en base), et
dire si le travail demande est FAIT.

Attention : une empreinte prouve qu un travail a eu lieu, PAS qu il fait ce que
la decision demandait. C est exactement ce que tu dois trancher.

Si c est fait, clos la decision :
  deos-decisions status {dec} clos --par cos --preuve '{{"relu_par":"cos","empreinte":"{ref[:60]}","constat":"<ce que tu as verifie>"}}'

Si c est partiel ou hors sujet, LAISSE-LA ACCORDEE et dis en une ligne ce qui
manque. Ne clos jamais dans le doute : une decision close sort du radar et
personne n y revient. Laisser trainer est moins grave que fermer a tort.

Reponds en deux lignes maximum."""
        r = subprocess.run(
            ["claude", "-p", invite, "--model", "sonnet",
             "--allowedTools", "Bash,Read,Grep,Glob", "--output-format", "json"],
            capture_output=True, text=True, timeout=300,
            env={**os.environ, "DH_DIRECTION": "chief-of-staff"})
        try:
            d = json.loads(r.stdout)
            print(f"  {dec} : {(d.get('result') or '').strip()[:160]}")
        except Exception:
            print(f"  {dec} : relecture illisible")


if __name__ == "__main__":
    main()
