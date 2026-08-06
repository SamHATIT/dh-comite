# Cartographie des capacités — 6 août 2026
> Établie par inventaire direct du serveur. Document de référence, à vérifier
> avant toute demande d'outil. Version complète illustrée : `config/DH_Cartographie_Capacites_2026-08-06.docx`

## Ce que chaque direction doit savoir

**N8N tourne en service systemd, pas en Docker.** 18 workflows, 1 354 exécutions,
10 actifs. Les 5 dormants attendent un repointage de modèle, pas une reconstruction.

**La chaîne de prospection existe presque entièrement** : Lead Capture et
LinkedIn Enrichment sont ACTIFS, Lead Scoring et Email Outreach dormants.
Il manque le maillon d'entrée (signaux publics) — désormais construit mais
inactif, et dont le débit réel reste à mesurer.

**Salesforce est prêt à recevoir les prospects** : 4 champs de qualification sur
le Lead, permission set de saisie, accès lecture seule du comité vérifié.

**Une capacité nouvelle arrive** : Gemini (texte, image, vidéo). Elle couvre le
besoin visuel du Marketing, aujourd'hui sans solution.

## L'ordre des actions, par rendement

1. Identifiant Anthropic dans N8N → repointer Veille Concurrence (30 min)
2. Brancher Gemini → génération de masse + visuels (1 h)
3. Retirer la clé en dur de « Blog - Veille Hebdo » (15 min, **sécurité**)
4. Repointer Lead Scoring et LinkedIn Enrichment (1 h)
5. Clé France Travail pour les signaux d'emploi (gratuite, à tester)
6. Search Console + API du blog (30 min)
7. Email-to-Case et Knowledge (3 h)

## Rappel de méthode

Cette cartographie doit être **vérifiée, pas crue**. Le 06/08, une conclusion
erronée sur N8N a failli faire corriger un document exact. Vérifiez sur le
serveur avant de retirer ou d'ajouter une demande.
