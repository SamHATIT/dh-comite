# Piste — WanGP en local pour la production vidéo des onze agents

> **Date :** 2026-08-10 · **Source : Sam** (capture du dépôt WanGP, transmise le 10/08 au soir)
> **Statut : à tester, pas une décision.** Aucune génération n'a été lancée.

---

## Pourquoi ça compte ici

La campagne des onze agents (`campagne_onze_agents_scripts.md`, §7) est bloquée par trois
manques d'outillage déclarés par le Marketing. **WanGP en couvre deux et rend le troisième
sans objet.**

| # | Manque déclaré | Ce que WanGP apporte |
| --- | --- | --- |
| 1 | Aucune capacité vidéo ; besoin de **8 s en image-vers-vidéo** pour figer le clair-obscur sur une image de référence | Wan et LTX-2 font exactement de l'image-vers-vidéo. C'est le cas d'usage central de l'outil |
| 2 | Aucune capacité voix ; besoin de **onze timbres distinguables** | Qwen3 TTS et Chatterbox sont embarqués dans la même interface |
| 3 | Clé Gemini non vérifiable, tarif inconnu, dépend du Delivery | **Sans objet** : exécution locale, aucune clé tierce, aucun tarif par génération |

## Ce qui rend la piste sérieuse

Le §6 de la campagne construit toute sa structure de coût sur l'évitement du visage et de la
synchronisation labiale — les deux postes les plus chers de la vidéo générative. **Le parti
pris silhouette et contre-jour était une contrainte budgétaire déguisée en choix
artistique.** En local, la contrainte tombe : le facteur de 4 à 6 tentatives par plan
(hypothèse non sourcée du §6.3) cesse d'être un risque financier et devient du temps machine.

## Ce qu'il faut vérifier avant d'y croire

1. **Le GPU est loué à l'heure, pas possédé.** « Gratuit » est faux : c'est du temps machine
   facturé. Référence à comparer — le pipeline BUILD complet a coûté 3 $ le 10/08. Mesurer
   le coût d'un spot de 8 s avant d'extrapoler à onze.
2. **La qualité au niveau d'une communication de marque n'est pas acquise.** Un rendu
   suffisant pour une démonstration technique ne l'est pas forcément pour la page LinkedIn
   d'une entreprise qui vend de la rigueur à des établissements financiers.
3. **Onze timbres réellement distinguables** est une exigence plus dure qu'une synthèse
   vocale correcte. À tester sur trois voix avant de valider le principe.
4. **Licences des modèles pour un usage commercial** — Wan, LTX-2, Chatterbox n'ont pas
   toutes les mêmes conditions. À vérifier avant toute diffusion publique.

## Séquence proposée

Un seul spot, Sophie, de bout en bout : image de référence → 8 s en image-vers-vidéo → une
voix. Mesurer le coût GPU réel et le nombre de tentatives. **C'est le test que le §7 réclame
depuis le 09/08 : la capacité de production n'a jamais été vérifiée, même pour un usage
ponctuel.** Rien ne part en production avant la revue Juridique du concept Entracte, et le
Delivery n'entre qu'après le 15 août.

## Dépendance

Prochaine session GPU (protocole en attente, `Journee_10_aout_tests_GPU`). À y ajouter comme
poste distinct des tests BUILD.

---

## Protocole de comparaison Wan / LTX-2

**Demandé par Sam le 10/08.** Les deux modèles sont dans WanGP, donc comparables à interface,
machine et quantification identiques — condition rarement réunie, elle rend la mesure honnête.

**Entrées gelées, strictement identiques pour les deux** : une image de référence unique
(Sophie, clair-obscur établi), un prompt unique, une durée de 8 s, même quantification, même
graine si l'outil l'expose.

### Critères, par ordre de poids

| # | Critère | Comment on le mesure | Pourquoi celui-là |
| --- | --- | --- | --- |
| 1 | **Coût GPU par plan retenu** | (durée de génération × tentatives jusqu'à un plan utilisable) × tarif horaire | La métrique qui décide. Un modèle rapide qui rate beaucoup coûte plus qu'un modèle lent qui passe |
| 2 | **Tenue du contre-jour et de la silhouette** | jugement binaire sur 6 générations : le clair-obscur de l'image de référence survit-il ? | C'est l'identité visuelle de la campagne. Un modèle qui « éclaire » la scène est disqualifié, quelle que soit sa netteté |
| 3 | **Fidélité à l'image de référence** | dérive du cadrage, de la lumière et de la silhouette entre l'image d'entrée et la première frame | Onze spots doivent partager un registre. Une dérive forte interdit la série |
| 4 | **Stabilité temporelle sur 8 s** | scintillement, déformation des contours, morphing en fin de plan | Le format est court mais la silhouette est le seul sujet : sa déformation se voit immédiatement |
| 5 | Nombre de tentatives jusqu'au premier plan utilisable | comptage | Vérifie ou infirme le facteur 4 à 6 du §6.3, jamais sourcé |
| 6 | VRAM et faisabilité | pic mesuré | Conditionne la possibilité de co-charger un TTS dans la même session |

**Le mouvement lent et l'absence de visage jouent contre les classements publics.** Les
comparatifs de vidéo générative se départagent sur les visages, la synchronisation labiale et
l'action rapide — trois choses que cette campagne évite par construction. **Un classement
externe ne dira rien d'utile ici.** Seul le test sur les plans réels tranche.

**Livrable** : un tableau à six lignes, deux colonnes, et une recommandation nommée. Pas
d'impression, pas d'adjectif.
