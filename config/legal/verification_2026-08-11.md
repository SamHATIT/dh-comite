# Vérification du 11/08 — l'avis défavorable du 08/08 tient toujours

**Statut :** constat vérifié, aucune décision à trancher ici. Ce document
actualise l'audit `conformite_donnees_2026-08-08.md` (missions DEC-2026-0802-06
et DEC-2026-0808-01) avec l'état réel des trois sites et du code, relevé ce
jour.

## Ce qu'il faut retenir

- **Aucune régression, mais aucune correction non plus.** Les trois défauts
  bloquants identifiés le 08/08 sont exactement dans le même état trois jours
  plus tard.
- `digital-humans.fr` sert toujours la page « Entracte » sur toutes les routes
  testées — y compris `/mentions-legales`, `/cgv`, `/privacy`,
  `/confidentialite`. Le site n'expose aujourd'hui aucun parcours client ni
  aucun widget IA : l'exposition AI Act art. 50 est donc nulle **tant qu'il
  reste en pause**, mais rien n'est publié pour autant.
- `samhatit-consulting.cloud` et `deos.cloud` sont en ligne, mais leurs pages
  légales n'existent toujours pas : sur le premier les liens de pied de page
  sont **morts** (`href="#"`), sur le second ils sont **absents** du pied de
  page.
- Le contournement du chiffrement (B2) signalé le 08/08 est **toujours présent
  dans le code**, aux mêmes lignes.

## 1. Les trois sites, relevé du 11/08 à l'instant

| Site | Accessible | Mentions légales | Confidentialité | Preuve |
| --- | --- | --- | --- | --- |
| digital-humans.fr | Oui (HTTP 200), mais **Entracte** sur toute route | Inaccessible — la page renvoie l'Entracte | Inaccessible — idem | `curl` sur `/`, `/mentions-legales`, `/cgv`, `/privacy`, `/confidentialite` : les cinq réponses sont identiques, page « Entracte » |
| samhatit-consulting.cloud | Oui, site réel | **Lien mort** : `<a href="#" data-i18n="foot.legal">Mentions légales</a>` | **Lien mort** : `<a href="#" data-i18n="foot.privacy">Confidentialité</a>` | Ligne 335-336 du HTML servi, relevé ce jour |
| deos.cloud | Oui, site réel | **Absent** du pied de page | **Absent** du pied de page | Pied de page relevé : `© MMXXVI · DEOS · Une solution SH Conseil · contact@deos.cloud` — aucun lien légal |

`/mentions-legales` et `/privacy` renvoient un **404** direct sur ces deux
derniers sites (vérifié par requête directe) : les pages n'existent nulle
part, pas seulement en pied de page.

Aucun widget de chat n'est exposé sur `samhatit-consulting.cloud` ni
`deos.cloud` — confirmation que ce sont des vitrines statiques, comme constaté
le 08/08 (§4 de `conformite_donnees_2026-08-08.md`).

**Conséquence pour DEC-2026-0808-01** : l'audit du 08/08 avait classé les deux
sites NON CONFORME. Ce n'est pas corrigé. La mission n'a pas de nouvelle
information à produire — elle demande un correctif (Sam a le brouillon des
pages, il ne les a pas encore publiées), pas un nouvel audit.

## 2. Le code, relevé du 11/08

`backend/app/api/routes/projects.py` lit et écrit toujours
`project_credentials.encrypted_value` en clair, sans passer par
`encrypt_credential` / `decrypt_credential` — écriture lignes 256, 264, 279,
285 ; lecture lignes 356, 360, 446. Identique à la description de
DEC-2026-0810-09.

Le go de Sam sur l'option (a) (correctif de code cette semaine) a été donné le
10/08. Le correctif n'est **pas encore livré** au 11/08 — ce n'est pas une
alerte de ma part, c'est un fait daté qui revient au Delivery, porteur de
DEC-2026-0809-05 / DEC-2026-0810-09.

## Conclusion pour l'avis juridique

**L'avis défavorable du 08/08 à l'ouverture des inscriptions reste
intégralement valable au 11/08**, pour les mêmes deux raisons (B2 en clair,
B3 non prouvé — B3 déjà reconfirmé ce jour dans DEC-2026-0811-03). L'avis
favorable-sous-réserve à la réouverture en vitrine de `digital-humans.fr`
reste également valable : les réserves (publier les pages corrigées, mention
IA du widget) ne sont pas levées, mais rien ne s'est aggravé — le site est
simplement resté en pause.

**Ce que je ne peux pas faire depuis mon périmètre** : publier les pages sur
les trois sites, ou corriger le code — ce sont des actions Sam / Delivery. Ma
part (vérifier, dater, chiffrer les manques) est faite.

## Sources

- `curl` direct sur les cinq URL de digital-humans.fr, ce jour.
- `curl` direct sur samhatit-consulting.cloud et deos.cloud, ce jour, HTML
  inspecté ligne par ligne pour le pied de page.
- Lecture de `/repo/backend/app/api/routes/projects.py`, ce jour.
- `config/legal/conformite_donnees_2026-08-08.md` pour l'état de référence.
