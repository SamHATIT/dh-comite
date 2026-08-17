#!/bin/bash
# RÉPÉTITION DU RECOVERY SPRINT — bin/recovery.py sur une base jetable.
# LOT-09, 18/08/2026. Attendu : 14/14.
#
# POURQUOI CETTE SUITE EXISTE
# ---------------------------
# Le tri porte sur quarante décisions réelles, et deux de ses erreurs possibles
# sont irréversibles en pratique : clore à tort (la décision sort du radar et
# personne n'y revient) et prendre un document qui PARLE d'une décision pour la
# preuve qu'elle est traitée. Aucune des deux ne se voit à la relecture du code.
# On les met donc sous test avant de toucher à la base réelle.
#
# CE QU'ELLE PROUVE, ET CE QU'ELLE NE PROUVE PAS
# ----------------------------------------------
# Elle prouve la mécanique : la détection d'empreintes, l'exclusion des sources
# narratives, le fait que le verdict est lu en base et non dans le compte rendu
# du relecteur, la reprise en plusieurs passes, et les trois critères du lot.
# Elle ne prouve RIEN sur la qualité du jugement du Chief of Staff : le
# relecteur est simulé ici. C'est précisément la moitié du travail qu'aucun
# test ne peut porter — d'où les deux étages.
#
# LE RELECTEUR SIMULÉ N'EST PAS UN TRI
# ------------------------------------
# Il applique des issues plausibles pour éprouver le circuit d'écriture. Il ne
# constitue pas un classement des vraies décisions et sa sortie n'a pas
# vocation à être recopiée dans docs/RECOVERY_2026-08.md : la trace se produit
# au moment du tri réel, par --trace.
#
# USAGE
#   COMITE_DB_DSN=<dsn d'une base jetable> bash tests/recovery.sh
#
# GARDE-FOU : le nom de la base doit contenir « repetition ». La suite crée des
# décisions et des tâches ; la lancer par distraction sur dh_comite polluerait
# le registre avec quarante fausses lignes, et decisions est append-only.

set -uo pipefail

RACINE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DSN="${COMITE_DB_DSN:-}"
[ -n "$DSN" ] || { echo "REFUS: COMITE_DB_DSN requis (base jetable)"; exit 2; }
case "$DSN" in *repetition*) ;; *)
  echo "REFUS: la base cible doit contenir « repetition » dans son nom."
  echo "       Cette suite écrit des décisions et des tâches."; exit 2;; esac

export COMITE_DB_DSN="$DSN"
export PATH="$RACINE/bin:$PATH"

REUSSIS=0; ECHOUES=0
cas() {  # cas "<intitulé>" "<attendu>" "<obtenu>"
  if [ "$2" = "$3" ]; then REUSSIS=$((REUSSIS+1)); printf '  ok   %s\n' "$1"
  else ECHOUES=$((ECHOUES+1)); printf '  ÉCHEC %s\n       attendu [%s], obtenu [%s]\n' "$1" "$2" "$3"; fi
}
contient() {  # contient "<intitulé>" "<motif>" "<texte>"
  if grep -q -- "$2" <<<"$3"; then REUSSIS=$((REUSSIS+1)); printf '  ok   %s\n' "$1"
  else ECHOUES=$((ECHOUES+1)); printf '  ÉCHEC %s\n       motif absent : %s\n' "$1" "$2"; fi
}
q() { psql "$COMITE_DB_DSN" -tA -c "$1"; }

BAC=$(mktemp -d); trap 'rm -rf "$BAC"' EXIT
export DH_RACINE="$BAC"
mkdir -p "$BAC/docs"

# ── Le décor ────────────────────────────────────────────────────────────────
#
# Neuf décisions, chacune posée pour éprouver UN cas. Les identifiants et les
# intitulés sont ceux de la file réelle du 17/08 (PageSuivi.md §1.1) : un jeu
# d'essai inventé prouverait que le script sait lire une table, pas qu'il sait
# trier ce stock-là.

psql "$COMITE_DB_DSN" -q -v ON_ERROR_STOP=1 <<'SQL'
DELETE FROM tasks;
ALTER TABLE decisions DISABLE TRIGGER trg_decisions_no_delete;
DELETE FROM decisions;
ALTER TABLE decisions ENABLE TRIGGER trg_decisions_no_delete;
DELETE FROM deos_state;

INSERT INTO decisions (id, date, origine, texte, statut) VALUES
 -- empreinte commit : le correctif de journalisation uvicorn, commit réel c3e534c
 ('DEC-2026-0804-01', now() - interval '13 days', 'sam',
  'Fiabilisation export logs backend', 'accordee'),
 -- empreinte commit également, mais partielle : le commit prépare, il ne déploie pas
 ('DEC-2026-0810-23', now() - interval '6 days', 'sam',
  'Tableau de bord périmé après exécution manuelle', 'accordee'),
 -- citée UNIQUEMENT par des sources narratives : le piège des 35 candidats
 ('DEC-2026-0802-02', now() - interval '14 days', 'sam',
  'BUILD reprend depuis la phase 1 au lieu de reprendre où il en est', 'accordee'),
 -- empreinte en base sur une clé métier
 ('DEC-2026-0810-04', now() - interval '7 days', 'sam',
  'Curseur ecrire_base du Commercial', 'accordee'),
 -- citée par une décision plus récente : signal de doublon
 ('DEC-2026-0809-12', now() - interval '8 days', 'sam',
  'Prix du Pro et adaptation par marché', 'accordee'),
 ('DEC-2026-0809-13', now() - interval '7 days', 'sam',
  'Prix du Pro à 79 € — complète DEC-2026-0809-12', 'accordee'),
 -- aucune empreinte : les six questions, sans raccourci
 ('DEC-2026-0806-09', now() - interval '10 days', 'sam',
  'Offre intégrateur à concevoir', 'accordee'),
 ('DEC-2026-0811-05', now() - interval '5 days', 'delivery',
  'Supervision N8N hors service', 'accordee'),
 ('DEC-2026-0813-03', now() - interval '4 days', 'cos',
  'Pages légales absentes sur les 3 sites', 'accordee'),
 -- hors périmètre : le tri ne porte que sur les accordées
 ('DEC-2026-0806-12', now() - interval '10 days', 'sam',
  'Chemin critique — réouverture du site', 'en_execution');

-- Sources NARRATIVES. Elles citent les décisions et n'en prouvent aucune :
-- un brief prouve que le CEO a lu la décision, pas qu'elle est traitée.
INSERT INTO deos_state (cle, valeur, maj_par) VALUES
 ('priorites_semaine', '{"rang1":"DEC-2026-0802-02","rang2":"DEC-2026-0810-23"}', 'cos'),
 ('brief', '{"texte":"DEC-2026-0802-02 relancée pour la cinquième fois"}', 'ceo'),
 ('rapport_delivery', '{"lu":["DEC-2026-0802-02","DEC-2026-0806-09"]}', 'delivery'),
 -- clé MÉTIER : elle porte un état, pas un récit
 ('curseur_commercial', '{"ecrire_base":3,"origine":"DEC-2026-0810-04"}', 'ceo');
SQL

# Dépôt d'essai : deux commits qui citent une décision et touchent un fichier.
# La vérification « le commit a touché des fichiers » compte : un commit vide
# porte un message, pas un travail.
DEPOT="$BAC/depot"; mkdir -p "$DEPOT"; git -C "$DEPOT" init -q
git -C "$DEPOT" config user.email t@t; git -C "$DEPOT" config user.name t
echo un > "$DEPOT/a"; git -C "$DEPOT" add a
git -C "$DEPOT" commit -qm "journalisation uvicorn passée en INFO (DEC-2026-0804-01)"
echo deux > "$DEPOT/b"; git -C "$DEPOT" add b
git -C "$DEPOT" commit -qm "diagnostic du tableau de bord périmé (DEC-2026-0810-23)"
export RECOVERY_DEPOTS="$DEPOT"

# ── 1. Le classement mécanique ──────────────────────────────────────────────

SIM=$(python3 "$RACINE/bin/recovery.py" --journal "$BAC/j.json" 2>&1)

cas "1 · le tri ne porte que sur les accordées (9, pas la en_execution)" \
    "9" "$(python3 -c "import json;print(len(json.load(open('$BAC/j.json'))['decisions']))")"

contient "2 · un commit citant la décision est une empreinte" \
    "DEC-2026-0804-01" "$(sed -n '/candidate deja faite/,/^$/p' <<<"$SIM")"

# LE CAS QUI COMPTE. DEC-2026-0802-02 est citée par priorites_semaine, par le
# brief et par un rapport de direction — trois fois plus « documentée » que
# celles qui ont un commit. Si elle ressort candidate, la détection reproduit
# le défaut du 17/08 : 35 preuves trouvées, 6 réelles.
contient "3 · trois citations narratives ne font pas une empreinte" \
    "DEC-2026-0802-02" "$(sed -n '/sans empreinte/,$p' <<<"$SIM")"

contient "4 · une clé métier de deos_state est une empreinte" \
    "DEC-2026-0810-04" "$(sed -n '/candidate deja faite/,/^$/p' <<<"$SIM")"

contient "5 · une décision citée par une plus récente est signalée comme doublon" \
    "DEC-2026-0809-12" "$(sed -n '/candidate doublon/,/^$/p' <<<"$SIM")"

cas "6 · la simulation n'écrit rien en base" \
    "9" "$(q "SELECT count(*) FROM decisions WHERE statut='accordee';")"

# ── 2. Le verdict se lit en base, pas dans le compte rendu ──────────────────
#
# Un relecteur qui ANNONCE une clôture sans l'écrire doit laisser une trace
# « sans decision ». C'est l'invariant I3 appliqué à l'outil qui mesure : sinon
# le rapport du tri devient l'autoportrait du relecteur.

cat > "$BAC/menteur.sh" <<'EOF'
#!/bin/bash
echo "J'ai clos la décision, tout était fait."
echo "QUESTION: 2"
echo "MOTIF: déjà réalisée, close"
EOF
chmod +x "$BAC/menteur.sh"

RECOVERY_RELECTEUR="$BAC/menteur.sh" python3 "$RACINE/bin/recovery.py" --appliquer \
  --journal "$BAC/j.json" --decision DEC-2026-0806-09 >"$BAC/menteur.out" 2>&1

contient "7 · un relecteur qui n'écrit rien est tracé « sans decision »" \
    "sans decision" "$(cat "$BAC/menteur.out")"
cas "8 · et l'écart avec sa déclaration est conservé" \
    "annonce la question 2, la base montre sans decision" \
    "$(python3 -c "import json;print(json.load(open('$BAC/j.json'))['decisions']['DEC-2026-0806-09']['passages'][-1].get('ecart',''))")"

# ── 3. Le tri complet, avec un relecteur qui écrit ─────────────────────────

cat > "$BAC/relecteur.sh" <<'EOF'
#!/bin/bash
# Relecteur simulé : une issue plausible par cas, écrite avec les vrais outils.
D=$(grep -o 'DEC-2026-[0-9]\{4\}-[0-9]\{2\}' <<<"$1" | head -1)
case "$D" in
  DEC-2026-0809-12) deos-decisions status "$D" obsolete --par cos \
      --motif "fusionnée dans DEC-2026-0809-13, même sujet à un jour d'écart" >/dev/null
      echo "QUESTION: 1"; echo "MOTIF: doublon, fusionnée dans 0809-13" ;;
  DEC-2026-0804-01) deos-decisions status "$D" clos --par cos \
      --preuve '{"relu_par":"cos","empreinte":"commit","constat":"le commit fait ce que la décision demandait"}' >/dev/null
      echo "QUESTION: 2"; echo "MOTIF: commit lu, il couvre la demande" ;;
  DEC-2026-0810-23) deos-tasks add --decision "$D" --titre "fournir la preuve de réalisation" \
      --critere-fin "la décision est en propose_cloture avec preuve" --owner delivery --par cos >/dev/null
      echo "QUESTION: 2"; echo "MOTIF: commit de diagnostic seulement, preuve demandée au porteur" ;;
  DEC-2026-0810-04) deos-tasks add --decision "$D" --titre "documenter le canal sf-lead" \
      --critere-fin "config/outils_disponibles.md cite le canal" --owner commercial --par cos >/dev/null
      echo "QUESTION: 3"; echo "MOTIF: curseur ouvert, documentation restante" ;;
  DEC-2026-0811-05) deos-decisions status "$D" blocked --par delivery \
      --blocker "port du conteneur n8n injoignable depuis le comité" \
      --next-action "ouvrir le port ou exposer une vue de supervision" --next-owner sam >/dev/null
      echo "QUESTION: 4"; echo "MOTIF: bloquée par l'infrastructure, pas par le Delivery" ;;
  DEC-2026-0802-02) deos-decisions status "$D" needs_decision --par delivery \
      --question "périmètre étroit sur la phase 1, ou refonte complète de la reprise ?" >/dev/null
      echo "QUESTION: 5"; echo "MOTIF: périmètre jamais tranché, question posée à Sam" ;;
  *) deos-tasks add --decision "$D" --titre "premier pas concret" \
      --critere-fin "un commit cite $D" --owner delivery --echeance 2026-08-25 --par cos >/dev/null
     echo "QUESTION: 6"; echo "MOTIF: encore pertinente, une tâche posée" ;;
esac
EOF
chmod +x "$BAC/relecteur.sh"

RECOVERY_RELECTEUR="$BAC/relecteur.sh" python3 "$RACINE/bin/recovery.py" --appliquer \
  --journal "$BAC/j.json" >"$BAC/tri.out" 2>&1

RAP=$(python3 "$RACINE/bin/recovery.py" --rapport --journal "$BAC/j.json" 2>&1)

contient "9 · chaque décision de départ a reçu un traitement" \
    "9 de depart · 9 traitees · 0 sans decision" "$RAP"
cas "10 · aucune décision restée accordée sans tâche" \
    "0" "$(q "SELECT count(*) FROM decisions d WHERE d.statut='accordee'
              AND NOT EXISTS (SELECT 1 FROM tasks t WHERE t.decision_id=d.id);")"
contient "11 · le critère 2 est reporté comme tenu" "2. accordees sans tache ..................... 0" "$RAP"

# needs_decision ouvre une entrée liée en attente_sam : la question posée à Sam
# est une décision de plus, et elle n'est pas dans la file active.
cas "12 · needs_decision a bien posé la question à Sam" \
    "1" "$(q "SELECT count(*) FROM decisions WHERE statut='attente_sam' AND texte ILIKE '%DEC-2026-0802-02%';")"

# ── 4. Reprise et trace ─────────────────────────────────────────────────────

# Une seconde passe ne doit rien relire : le tri se reprend en plusieurs fois
# sans repayer les précédentes ni revenir sur ce que le CoS a tranché.
RECOVERY_RELECTEUR="$BAC/relecteur.sh" python3 "$RACINE/bin/recovery.py" --appliquer \
  --journal "$BAC/j.json" >"$BAC/passe2.out" 2>&1
cas "13 · une seconde passe ne relit aucune décision déjà traitée" \
    "0 decision(s) — relecture par le Chief of Staff" "$(head -1 "$BAC/passe2.out")"

python3 "$RACINE/bin/recovery.py" --trace "$BAC/docs/RECOVERY.md" --journal "$BAC/j.json" >/dev/null 2>&1
cas "14 · la trace porte une ligne par décision de départ" \
    "9" "$(grep -c '^| DEC-2026' "$BAC/docs/RECOVERY.md")"

echo
echo "$REUSSIS réussis, $ECHOUES échoués"
[ "$ECHOUES" -eq 0 ]
