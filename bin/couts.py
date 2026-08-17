#!/usr/bin/env python3
"""Suivi des coûts du dispositif — à partir des données déjà produites.

Pourquoi ce script plutôt qu'un outil externe : chaque exécution de
`claude -p --output-format json` enregistre DÉJÀ son coût exact, sa durée, ses
jetons et la répartition par modèle. Installer un runtime tiers pour obtenir
une information qu'on possède serait absurde.

Déclencheur : le 08/08, le plafond mensuel a sauté sans que personne l'ait vu
venir — 24 € d'Opus sur une journée, contre 8 € de Sonnet, pour quatre missions
de directeurs lancées à la main.

    couts.py            → 14 derniers jours
    couts.py 30         → 30 derniers jours
"""
import json, glob, sys, os
from datetime import datetime, timedelta, timezone
from collections import defaultdict

BASE = "/root/workspace/dh-comite"
# --help doit rendre l'aide, pas une trace. Le Preflight de LOT-05 controle que
# chaque outil declare repond a --help : ce script lisait argv[1] comme un nombre
# de jours et levait ValueError, ce qui le declarait EN PANNE et bloquait toutes
# les rondes du CEO (constate le 17/08). Un outil qui ne sait pas dire ce qu'il
# fait est indistinguable d'un outil casse.
if len(sys.argv) > 1 and sys.argv[1] in ("--help", "-h"):
    print(__doc__)
    sys.exit(0)
try:
    JOURS = int(sys.argv[1]) if len(sys.argv) > 1 else 14
except ValueError:
    print("usage: couts.py [nombre de jours]  (defaut 14)", file=sys.stderr)
    sys.exit(2)
DEPUIS = datetime.now(timezone.utc) - timedelta(days=JOURS)

par_jour, par_source, par_modele = defaultdict(float), defaultdict(float), defaultdict(float)
total, n = 0.0, 0

for f in glob.glob(f"{BASE}/*/*.json"):
    try:
        st = datetime.fromtimestamp(os.path.getmtime(f), timezone.utc)
        if st < DEPUIS:
            continue
        d = json.load(open(f, encoding="utf-8"))
        c = d.get("total_cost_usd")
        if not c:
            continue
    except Exception:
        continue

    nom = os.path.basename(f)
    # "directeur-delivery-2026-08-09.json" -> "directeur-delivery"
    source = nom.rsplit("-", 3)[0] if nom.count("-") >= 3 else nom.replace(".json", "")

    total += c; n += 1
    par_jour[st.strftime("%d/%m")] += c
    par_source[source] += c
    for m, u in (d.get("modelUsage") or {}).items():
        # Coût non ventilé par modèle dans la sortie : on impute au prorata
        # des jetons de sortie, qui dominent la facture.
        par_modele[m.replace("claude-", "").replace("-20251001", "")] += \
            c * (u.get("outputTokens", 0) or 0) / max(
                sum((v.get("outputTokens", 0) or 0) for v in d["modelUsage"].values()), 1)

if not n:
    print(f"Aucune exécution tracée sur {JOURS} jours."); sys.exit(0)

print(f"\n  COÛTS — {JOURS} derniers jours")
print(f"  {n} exécutions · {total:.2f} USD · {total/max(n,1):.2f} USD par exécution\n")

print("  Par jour")
for j in sorted(par_jour, key=lambda x: (x[3:], x[:2])):
    barre = "█" * max(1, int(par_jour[j] / max(max(par_jour.values()), .01) * 34))
    print(f"    {j}  {par_jour[j]:>7.2f}  {barre}")

print("\n  Par source")
for s, c in sorted(par_source.items(), key=lambda x: -x[1]):
    print(f"    {s:<32} {c:>7.2f}   {c/total*100:>4.1f} %")

print("\n  Par modèle (imputation au prorata des jetons de sortie)")
for m, c in sorted(par_modele.items(), key=lambda x: -x[1]):
    print(f"    {m:<32} {c:>7.2f}   {c/total*100:>4.1f} %")

# Projection : le plafond a saute le 08/08 a ~106 USD sur le mois.
jour_moyen = total / max(len(par_jour), 1)
print(f"\n  Rythme : {jour_moyen:.2f} USD/jour → {jour_moyen*30:.0f} USD sur 30 jours")
if jour_moyen * 30 > 120:
    print("  ⚠ Au-delà du plafond actuel de 150 USD si le rythme se maintient.")
print()
