#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# Boucle d'évolution des skills — inspirée de SkillClaw (AMAP-ML), sans son
# proxy d'interception.
#
# POURQUOI PAS LE PROXY : SkillClaw intercepte tous les appels des agents pour
# en extraire des enseignements. Chez nous, tout est DÉJÀ sur disque — rondes,
# rapports, briefs, décisions. Pas besoin de mettre un intermédiaire sur le
# chemin des données, ce qui aurait posé un problème de cloisonnement le jour
# où des données clients y transitent.
#
# CE QU'ON GARDE : les trois étapes — résumer, agréger, réécrire — et la
# déduplication, qui est notre vrai problème (skills qui se recouvrent).
#
# CADENCE : hebdomadaire, le dimanche. Assez pour que des motifs émergent,
# assez rare pour ne rien coûter.
# ═══════════════════════════════════════════════════════════════════════════
set -uo pipefail
cd /workspace

TS=$(date -u +%F)
DEPUIS=$(date -u -d "7 days ago" +%F)
SORTIE="config/evolution/evolution_${TS}.md"
mkdir -p config/evolution

echo "[evolution] fenêtre : $DEPUIS → $TS"

CTX=$(mktemp)
{
  echo "# MATIÈRE DE LA SEMAINE ($DEPUIS → $TS)"
  echo ""
  echo "## Skills actuels — inventaire"
  for d in .claude/skills/*/; do
    n=$(basename "$d")
    desc=$(sed -n '/^description:/,/^---/p' "$d/SKILL.md" 2>/dev/null | head -4 | tr '\n' ' ' | cut -c1-200)
    echo "- **$n** : $desc"
  done
  echo ""
  echo "## Rondes de la semaine"
  find rondes -name '*.json' -newermt "$DEPUIS" 2>/dev/null | sort | while read -r f; do
    echo "### $(basename "$f" .json)"
    python3 -c "
import json,sys
try:
    d=json.load(open('$f'))
    for k in ('faits','alertes','escalades','donnees_manquantes','besoin_interface'):
        v=d.get(k)
        if v: print(f'{k}: ' + json.dumps(v, ensure_ascii=False)[:900])
except Exception as e: print('illisible')
" 2>/dev/null
    echo ""
  done
  echo "## Décisions de la semaine"
  psql "$COMITE_DB_DSN" -tA -c "SELECT id||' | '||statut||' | '||left(texte,400) FROM decisions WHERE date >= '$DEPUIS' ORDER BY id;" 2>/dev/null
} > "$CTX"

echo "[evolution] contexte : $(wc -c < "$CTX") octets"

cat > /tmp/mission_evo.md <<'MISSION'
MISSION — boucle d'évolution des skills.

Tu analyses une semaine de travail réel pour améliorer les skills des
directeurs. Tu ne produis PAS un rapport d'activité : tu cherches ce qui
DEVRAIT ÊTRE ÉCRIT quelque part et ne l'est pas.

TROIS ÉTAPES, dans cet ordre.

── 1. RÉSUMER — qu'est-ce qui s'est réellement passé ?

Pour chaque direction, relève les moments où quelque chose a coincé :
- une information cherchée qui n'était pas trouvable
- une erreur commise qui aurait pu être évitée par une consigne écrite
- une question posée à Sam dont la réponse aurait dû être connue
- un travail refait parce qu'on ignorait qu'il existait déjà

Ignore ce qui s'est bien passé. On ne cherche que les frictions.

── 2. AGRÉGER — qu'est-ce qui se répète ?

Une friction isolée est un incident. **Une friction qui revient est un skill
manquant.** Regroupe ce qui se ressemble, et compte les occurrences.

Signale aussi les RECOUVREMENTS entre skills existants : deux skills qui
disent la même chose se neutralisent — l'agent ne sait plus lequel charger.

── 3. PROPOSER — que faut-il écrire, modifier, ou supprimer ?

Pour chaque proposition :
- **CRÉER** un skill : quel manque, combien de fois constaté, ce qu'il
  contiendrait
- **ENRICHIR** un skill : lequel, quelle section, quel texte exact à ajouter
- **FUSIONNER** deux skills : lesquels, pourquoi, ce qui reste du fusionné
- **SUPPRIMER** : lequel, et pourquoi il ne sert plus

CONTRAINTES ABSOLUES :
- Tu ÉCRIS des propositions, tu ne modifies AUCUN fichier. Sam tranche.
- Chaque proposition porte le NOMBRE d'occurrences qui la motive. Une seule
  occurrence n'est pas une proposition, c'est une anecdote — ne la remonte pas.
- Cite la source : quelle ronde, quelle décision, quelle date.
- Si la semaine n'a rien produit qui mérite un changement, DIS-LE. Une
  semaine sans proposition est un résultat valable, pas un échec.
- Maximum cinq propositions. Au-delà, on ne les traite pas.

Écris ton analyse et restitue-la intégralement.
MISSION

{ cat /tmp/mission_evo.md; echo ""; cat "$CTX"; } | \
  claude -p --model opus --allowedTools Read,Grep,Glob > "$SORTIE" 2>/tmp/evolution.err

TAILLE=$(wc -c < "$SORTIE" 2>/dev/null || echo 0)
echo "[evolution] rendu : $TAILLE octets → $SORTIE"

if [ "$TAILLE" -lt 200 ]; then
  echo "$TS ALERTE : évolution non produite — $(tail -1 /tmp/evolution.err 2>/dev/null)" >> config/evolution/incidents.log
  exit 1
fi
rm -f "$CTX"
