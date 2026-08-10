#!/bin/bash
# Verifie qu'aucun chemin absolu ne traine dans les pages du comite.
#
# POURQUOI CE CONTROLE EXISTE — trois fois le meme defaut le 10/08 :
#   · le matin, les liens des rapports (href="/rapport/...")
#   · le soir, le bouton d'arbitrage (fetch('/api/arbitrer'))
#   · cinq minutes plus tard, les apercus de l'index (src="01-seuils.html")
#
# nginx sert le comite sous /comite/ via proxy_pass vers 127.0.0.1:8090/.
# Un chemin commencant par / sort donc du comite et retombe ailleurs — sans
# aucune erreur visible, ce qui rend le defaut particulierement couteux.
#
#   bash bin/verifier_chemins.sh
set -uo pipefail
cd "$(dirname "$0")/.."
ECARTS=0

echo "── Chemins absolus dans les pages HTML ──"
for motif in 'href="/' "src=\"/" "fetch('/" 'fetch("/' 'action="/'; do
  R=$(grep -rn --include=*.html --include=*.py "$motif" web/ 2>/dev/null \
      | grep -viE 'https?://|//fonts|//cdn' | head -5)
  if [ -n "$R" ]; then
    echo "$R" | sed 's|^|  |' | cut -c1-110
    ECARTS=$((ECARTS+1))
  fi
done

if [ "$ECARTS" -eq 0 ]; then
  echo "  aucun — tous les chemins sont relatifs."
else
  echo
  echo "  Ces chemins sortiront du prefixe /comite/ et echoueront SILENCIEUSEMENT."
  echo "  Les rendre relatifs, ou les adapter a la route du service."
fi
exit "$ECARTS"
