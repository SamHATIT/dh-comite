#!/bin/bash
# NON-RÉGRESSION DU GARDE-FOU — les douze cas.
# LOT-06, critère d'acceptation n°3. Attendu : 12/12.
#
# Un cas par règle que le garde-fou documente, et pour les deux dernières, un
# cas par CORRECTIF de faux positif : ce sont celles qui se perdent, parce
# qu'une règle absente ne se voit pas alors qu'une règle en trop se rapporte.
#
# Chaque cas nomme l'incident qui a motivé la règle. Un test qui vérifie un
# comportement sans dire pourquoi ce comportement est attendu se fait supprimer
# le jour où il gêne.
#
# Usage : bash tests/garde-fou.sh

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/commun.sh"

echo "Non-régression du garde-fou — 12 cas"
echo

# ── Interdictions absolues : la production ne se touche pas ────────────────────

# DH-DEL-001. Le comité observe la plateforme, il ne l'exploite pas. Invariant I1
# de la refonte : « ne jamais toucher à la plateforme ».
cas 1 DENY "DH-DEL-001 · systemctl est refusé" \
    delivery 'systemctl restart n8n'

cas 2 DENY "DH-DEL-001 · docker est refusé" \
    delivery 'docker ps -a'

cas 3 DENY "DH-DEL-001 · kill est refusé" \
    delivery 'kill -9 4242'

# DH-DEL-002. La production est en lecture seule via deos_ro. Les identifiants
# applicatifs donnent un accès en écriture : ils sont interdits, même pour un
# SELECT — c'est le compte qui est proscrit, pas la requête.
cas 4 DENY "DH-DEL-002 · identifiants applicatifs de production refusés" \
    delivery 'psql "$DEOS_RO_DSN" -U digital_humans -c "SELECT count(*) FROM projects"'

cas 5 DENY "DH-DEL-002 · écriture vers la base de production refusée" \
    delivery 'psql "$DEOS_RO_DSN" -c "UPDATE projects SET statut='"'"'clos'"'"' WHERE id=1"'

# DH-COS-002. Le registre ne se manipule que par deos-decisions, qui trace
# auteur, date, preuve et justification.
#
# CAS LE PLUS IMPORTANT DE LA SUITE depuis le LOT-06 : il est joué avec le
# Chief of Staff, dont le curseur ecrire_base est à 4. Le moteur de politique
# rend donc ALLOW — et l'interdiction absolue doit refuser quand même. C'est ce
# qui prouve qu'un ALLOW du moteur ne dispense d'aucune interdiction absolue.
# La sauvegarde du 11/08 le dit noir sur blanc pour le CoS : « aucune écriture
# SQL directe : elle est bloquée par DH-COS-002 même au niveau autonomie ».
cas 6 DENY "DH-COS-002 · SQL direct sur decisions refusé même au cran Autonomie" \
    chief-of-staff 'psql "$COMITE_DB_DSN" -c "UPDATE decisions SET statut='"'"'clos'"'"' WHERE id='"'"'DEC-X'"'"'"'

# R14. La promotion d'un skill est réservée à Sam : une direction propose dans
# .claude/skills-proposed/, elle ne pose jamais dans .claude/skills/.
cas 7 DENY "R14 · promotion de skill par copie refusée" \
    delivery 'cp /tmp/SKILL.md /workspace/.claude/skills/nouveau/SKILL.md'

cas_fichier 8 DENY "R14 · promotion de skill par l'outil d'édition refusée" \
    delivery Write '/workspace/.claude/skills/nouveau/SKILL.md'

# DH-FS-001 (14/08). Vérifié ce jour à la demande de Sam : le garde-fou bloquait
# le SQL et les envois externes, et laissait passer TOUTES les destructions de
# fichiers. `rm -rf /workspace` était autorisé. Une direction pouvait effacer la
# configuration entière du comité.
cas 9 DENY "DH-FS-001 · destruction dans une zone protégée refusée" \
    delivery 'rm -rf /workspace/config'

cas 10 DENY "DH-FS-001 · suppression en masse par find refusée" \
    delivery 'find /workspace/config -name "*.md" -delete'

# ── Faux positifs corrigés : ce qui doit PASSER ───────────────────────────────

# FIX-GUARD-001 (04/08). Sans limites de mot, « updated_at », « deleted » et
# « last_updated » déclenchaient le blocage : cinq rondes perdues le 04/08 sur
# de simples lectures. Le mot UPDATE ne doit se reconnaître qu'entier.
cas 11 ALLOW "FIX-GUARD-001 · « updated_at » ne déclenche pas le blocage SQL" \
    delivery 'psql "$DEOS_RO_DSN" -tA -c "SELECT updated_at FROM v_deos_executions LIMIT 5"'

# CORRECTIF DU 17/08. La règle de vidage par redirection cherchait un « > » et un
# chemin protégé n'importe où dans la commande, sans regarder de quel côté du
# chevron se trouvait le chemin. `cat /workspace/config/offre_dh.md > /tmp/copie.md`
# — une simple LECTURE — était refusé. Cinq faux positifs dans quatre directions
# le 17/08, dont le blocage du correctif de sécurité RAG validé par Sam le 13/08.
# On n'examine désormais que la CIBLE de la redirection.
cas 12 ALLOW "17/08 · lire une zone protégée et écrire ailleurs est autorisé" \
    delivery 'cat /workspace/config/offre_dh.md > /tmp/copie.md'

bilan "Non-régression du garde-fou"
