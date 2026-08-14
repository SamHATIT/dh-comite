# Tri des 61 décisions accordées — proposition, rien n'est écrit

> **Établi le 11/08 à la demande de Sam. Aucune écriture en base.**
> Chaque lot est à valider séparément.

## Ce que le stock contient réellement

Sur 61 décisions au statut `accordee`, une quinzaine seulement relèvent d'un travail
en attente. Le reste est du classement en retard. **La métrique du Chief of Staff est
donc faussée à la source** — indépendamment de toute manipulation, son stock ne peut
pas décroître tant qu'il contient des règles sans état terminal.

## LOT A — déjà faites, à clôturer (10)

Toutes portent la clôture dans leur propre intitulé et le texte décrit un fait vérifié.

| Décision | Objet | Preuve disponible |
| --- | --- | --- |
| DEC-2026-0808-09 | B1 — affirmations de sécurité inexactes retirées du site | texte de remplacement en ligne |
| DEC-2026-0808-12 | B4 — engagement Anthropic sur l'entraînement, preuve au dossier | documentation citée |
| DEC-2026-0808-13 | SMTP — diagnostic corrigé, le service n'était pas cassé | courriel retrouvé |
| DEC-2026-0809-06 | mot de passe du comité régénéré | connexion rétablie |
| DEC-2026-0810-01 | étude de marché SH Conseil retrouvée et classée | fichier classé |
| DEC-2026-0810-20 | B2 — chiffrement des identifiants clients vérifié | vérification datée |
| DEC-2026-0810-31 | rectification de DEC-2026-0810-28, vue `v_deos_signaux` confirmée | audit Fable |
| DEC-2026-0810-04 | curseur `ecrire_base` du Commercial | **résolu le 11/08 : passé au niveau 3, canal `sf-lead`** |
| DEC-2026-0810-06 | « il n'y a personne pour exécuter » | **résolu le 11/08 : 14 curseurs rouverts** |
| DEC-2026-0810-23 | tableau de bord périmé après exécution manuelle | cause identifiée — *à confirmer : corrigée ou seulement diagnostiquée ?* |

**Contrainte à respecter** : `CHECK (statut <> 'clos' OR preuve IS NOT NULL)`. Chaque
clôture doit porter sa preuve. Utiliser `deos-decisions status <id> clos --par <agent>
--preuve '<json>'`, jamais un UPDATE direct.

## LOT B — doctrines, pas des actions (12)

Elles énoncent une règle permanente. Aucun état ne les termine ; elles resteront
indéfiniment dans la file.

DEC-2026-0809-09 (nous ne vendons pas de la conformité) · DEC-2026-0810-12 (écart de
qualité d'Emma en local, constat mesuré) · DEC-2026-0810-14, -15, -16, -17 (composition
de l'équipe : quatre décisions du même jour sur le même sujet) · DEC-2026-0810-19 (dépôt
git du client) · DEC-2026-0810-21 (benchmark comité, résultat tranché) · DEC-2026-0810-24
(les gabarits sont un vocabulaire) · DEC-2026-0810-25 (source des prospects : Salesforce)
· DEC-2026-0810-26 (tout est dans Salesforce) · DEC-2026-0810-27 (les prospects
n'existaient nulle part — résolu depuis par l'injection des 112).

**Deux voies, à trancher par Sam :**
- **(a) Sans migration** : clore avec une preuve `{"nature":"doctrine","report":"<fichier>"}`
  et recopier le texte dans un registre de doctrine (`config/doctrine_dh.md`). Le texte
  reste consultable, la file se vide. Aucun changement de schéma.
- **(b) Avec migration** : ajouter `doctrine` à la contrainte `decisions_statut_check`.
  Plus propre à long terme, mais c'est une modification de schéma en production.

*Recommandation : (a). La voie (b) se justifiera quand le registre de doctrine aura fait
la preuve de son usage.*

## LOT C — doublons à fusionner (4 groupes)

| À conserver | À rattacher | Motif |
| --- | --- | --- |
| DEC-2026-0804-05 | DEC-2026-0714-01 | même interface web globale, 28 j et 7 j d'écart ; la seconde se déclare « suite » de la première |
| DEC-2026-0810-02 | DEC-2026-0810-03 | compte d'organisation ; la seconde se déclare « complément » |
| DEC-2026-0809-13 | DEC-2026-0809-12 | prix du Pro et adaptation par marché, même sujet |
| DEC-2026-0809-10 | DEC-2026-0809-11 | carte bancaire à l'inscription, dispositif précisé |

## LOT D — incohérence à trancher, la seule qui appelle une décision de Sam

**Le prix du Pro existe en trois versions.** `DEC-2026-0809-13` fixe 79 € avec un tarif
de lancement possible à 59 €. `config/offre_dh.md` — le document canonique, dont la règle
dit qu'« aucune promesse hors de ce tableau » n'est permise — affiche **49 €**.

Trois semaines avant l'ouverture, c'est le seul point du registre qui bloque autre chose
que du classement : la page de tarification, le parcours Stripe et l'argumentaire
commercial en dépendent tous.

## LOT E — échéances qui courent

| Décision | Échéance | Reste |
| --- | --- | ---: |
| DEC-2026-0806-14 | démonstration DEOS au DSI du Crédit Logement, dernière semaine d'août | ~2 semaines |
| DEC-2026-0804-02 | huit chantiers O2, produit prêt au 31/08 | 20 jours |

## Effet attendu

61 → environ 39 après lots A et B, dont 4 fusions supplémentaires en lot C. Le stock
résiduel — une trentaine — décrit enfin du travail réel, et la métrique du Chief of Staff
redevient interprétable.
