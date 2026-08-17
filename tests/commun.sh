#!/bin/bash
# Socle commun aux suites de tests du garde-fou et du moteur de politique.
# LOT-06, 17/08/2026.
#
# POURQUOI CE FICHIER EXISTE
# --------------------------
# Le LOT-06 exige « aucune régression sur les douze cas de test du garde-fou
# existant ». Ces douze cas n'existaient nulle part dans le dépôt : ni script,
# ni liste. Le garde-fou avait été corrigé quatre fois (FIX-GUARD-001 le 04/08,
# le curseur le 06/08, DH-FS-001 le 14/08, la redirection le 17/08) sans qu'une
# seule de ces corrections soit protégée par un test. C'est ainsi qu'un
# correctif se perd et se re-diagnostique quelques jours plus tard depuis zéro.
#
# Les cas sont donc DÉRIVÉS du code du garde-fou et des incidents que ses
# commentaires citent, un cas par règle documentée. Ils sont écrits ici pour la
# première fois : à lire comme une reconstitution, pas comme un héritage.
#
# LES CURSEURS NE SONT PAS INVENTÉS
# ---------------------------------
# Ils viennent de config/curseurs_sauvegarde_2026-08-11.csv — la sauvegarde des
# 36 lignes réglées par Sam. Un test qui inventerait ses propres niveaux
# prouverait que le moteur sait lire un fichier, pas qu'il applique la
# gouvernance réelle.

set -uo pipefail

RACINE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# DH_CROCHET permet de rejouer la suite contre une sauvegarde .pre-<motif>.
# C'est ce qui rend la non-régression démontrable : une suite écrite en même
# temps que le code neuf ne prouve rien tant qu'on ne l'a pas vue passer sur le
# code ancien. Usage réservé aux tests ; le crochet réellement branché est
# désigné par .claude/settings.json.
CROCHET="${DH_CROCHET:-$RACINE/.claude/hooks/pretooluse-guard.sh}"
SAUVEGARDE_CURSEURS="$RACINE/config/curseurs_sauvegarde_2026-08-11.csv"

# Le crochet lit ce chemin en dur. On l'alimente, et on le SUPPRIME en sortant :
# sur le serveur, laisser un cache de test en place ferait travailler la ronde
# suivante sur des curseurs figés au lieu de ceux de la base.
CACHE=/tmp/curseurs.cache
nettoyer() { rm -f "$CACHE"; }
trap nettoyer EXIT

# direction|type_tache|niveau — le format que le crochet attend.
semer_curseurs() {
  tail -n +2 "$SAUVEGARDE_CURSEURS" | cut -d, -f2,3,4 | tr ',' '|' > "$CACHE"
  touch "$CACHE"   # fraîcheur : sans DSN, un cache périmé serait vidé par psql
}

REUSSIS=0
ECHOUES=0
declare -a ECHECS

# Lance le crochet et rend ALLOW ou DENY.
# usage : verdict_crochet <direction> <json d'entrée>
verdict_crochet() {
  local direction="$1" entree="$2"
  semer_curseurs
  local sortie
  sortie=$(printf '%s' "$entree" | DH_DIRECTION="$direction" bash "$CROCHET" 2>&1)
  if [ $? -eq 0 ]; then echo "ALLOW"; else echo "DENY|$sortie"; fi
}

# usage : cas <numero> <attendu ALLOW|DENY> <intitulé> <direction> <commande bash>
cas() {
  local numero="$1" attendu="$2" intitule="$3" direction="$4" commande="$5"
  local entree
  entree=$(jq -nc --arg c "$commande" '{tool_name:"Bash", tool_input:{command:$c}}')
  verifier "$numero" "$attendu" "$intitule" "$direction" "$entree"
}

# Même chose pour un outil d'édition de fichier (Write/Edit).
# usage : cas_fichier <numero> <attendu> <intitulé> <direction> <outil> <chemin>
cas_fichier() {
  local numero="$1" attendu="$2" intitule="$3" direction="$4" outil="$5" chemin="$6"
  local entree
  entree=$(jq -nc --arg t "$outil" --arg p "$chemin" \
             '{tool_name:$t, tool_input:{file_path:$p}}')
  verifier "$numero" "$attendu" "$intitule" "$direction" "$entree"
}

verifier() {
  local numero="$1" attendu="$2" intitule="$3" direction="$4" entree="$5"
  local brut obtenu detail
  brut=$(verdict_crochet "$direction" "$entree")
  obtenu="${brut%%|*}"
  detail="${brut#*|}"
  if [ "$obtenu" = "$attendu" ]; then
    REUSSIS=$((REUSSIS + 1))
    printf '  \033[32m✓\033[0m %-3s %s\n' "$numero" "$intitule"
  else
    ECHOUES=$((ECHOUES + 1))
    ECHECS+=("$numero $intitule — attendu $attendu, obtenu $obtenu")
    printf '  \033[31m✗\033[0m %-3s %s\n' "$numero" "$intitule"
    printf '      attendu %s, obtenu %s\n' "$attendu" "$obtenu"
    [ "$obtenu" = "DENY" ] && printf '      %s\n' "$(echo "$detail" | head -2)"
  fi
}

bilan() {
  local titre="$1" total=$((REUSSIS + ECHOUES))
  echo
  if [ "$ECHOUES" -eq 0 ]; then
    printf '\033[32m%s : %d/%d\033[0m\n' "$titre" "$REUSSIS" "$total"
    return 0
  fi
  printf '\033[31m%s : %d/%d\033[0m\n' "$titre" "$REUSSIS" "$total"
  for e in "${ECHECS[@]}"; do printf '  · %s\n' "$e"; done
  return 1
}
