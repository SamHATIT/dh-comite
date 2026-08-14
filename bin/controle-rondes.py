#!/usr/bin/env python3
"""Controle de fin de ronde — detecte les rapports vides ou tues au plafond.

POURQUOI (14/08) : une ronde tuee au plafond produit un JSON marque
subtype=success, is_error=false. L echec n est QUE dans le fichier .err, que
rien ne lisait. C est ainsi que la ronde du Delivery du 14/08 a ete perdue :
14 secondes de reponse, une promesse de rapport, et un subagent tue a la
vingtieme minute apres avoir travaille. Personne ne l a vu.

Consequence de ce silence : le CEO a compte la ronde comme absente, la sante
globale est tombee a 25/100, et le brief de Sam portait en premiere ligne
"silence de Delivery face a une relance personnelle". Alors que le travail
avait eu lieu.

Ce script ne juge pas le CONTENU d un rapport — seulement son EXISTENCE.
Un rapport trop court ou dont le subagent a ete tue est signale, point.

Usage : controle-rondes.py [AAAA-MM-JJ]
Sortie : 0 si tout va bien, 1 si au moins une ronde est incomplete.
"""
import glob, json, os, sys
from datetime import date

SEUIL = 800          # en dessous, ce n est pas un rapport mais un accuse
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JOUR = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()

alertes = []
for f in sorted(glob.glob(os.path.join(BASE, "rondes", f"*-{JOUR}.json"))):
    agent = os.path.basename(f).replace(f"-{JOUR}.json", "")
    try:
        d = json.load(open(f, encoding="utf-8"))
        n = len(d.get("result") or "")
        tours = d.get("num_turns")
        duree = round((d.get("duration_ms") or 0) / 1000)
    except Exception as e:
        alertes.append((agent, 0, f"illisible : {e}", None, None))
        continue

    err = f.replace(".json", ".err")
    tue = (os.path.exists(err) and os.path.getsize(err) > 0
           and "Background tasks still running" in open(err, errors="replace").read())

    if n < SEUIL or tue:
        motif = "subagent TUE AU PLAFOND" if tue else "rapport trop court"
        alertes.append((agent, n, motif, tours, duree))

if not alertes:
    print(f"{JOUR} : toutes les rondes ont produit un rapport.")
    sys.exit(0)

print(f"═══ RONDES SANS RAPPORT EXPLOITABLE — {JOUR} ═══", file=sys.stderr)
for agent, n, motif, tours, duree in alertes:
    d = f", {duree} s" if duree is not None else ""
    t = f", {tours} tours" if tours is not None else ""
    print(f"  {agent:28} {n:>6} car{t}{d}  →  {motif}", file=sys.stderr)
print(file=sys.stderr)
print("  Un rapport tue au plafond n est PAS une absence : le travail a eu lieu.",
      file=sys.stderr)
print("  Relever CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS dans bin/rondes.sh, ou",
      file=sys.stderr)
print("  reduire le perimetre de la ronde concernee.", file=sys.stderr)

with open(os.path.join(BASE, "rondes", "ALERTES.log"), "a", encoding="utf-8") as fh:
    for agent, n, motif, *_ in alertes:
        fh.write(f"{JOUR}\t{agent}\t{n} car\t{motif}\n")
sys.exit(1)
