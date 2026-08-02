# Page de suivi — Digital·Humans

Ronde Chief of Staff du 2026-07-16T07:02Z (source : `deos-decisions:list` +
psql direct sur `decisions`, `deos-state:list`, `deos-state get
brief|okr_h2|cash_suivi|rapport_cos`, `find .claude/skills-proposed`, `git
log`). Ronde précédente : 2026-07-15T07:01:07Z (`rapport_cos` en mémoire).

## §1 Décisions

| id | quoi (≤60c) | origine | statut | âge | preuve | prochaine action |
|---|---|---|---|---|---|---|
| DEC-2026-0713-01 | Test étape 1 : validation du socle | sam | clos | 3j | oui | aucune — clôturée avec preuve |
| DEC-2026-0714-01 | Interface web globale de suivi du comité : tableaux de bord par domaine | sam | en_execution | 2j (≈1,58j sans activité) | non | aucune relance (sous le seuil de 3j) — dernière activité prouvée le 14/07 17:12 UTC (commits c7067b0/bb1c3d1/a0bbb23) ; **à surveiller** : franchit le seuil de relance le 17/07 en fin d'après-midi si aucune preuve d'ici là |
| DEC-2026-0714-02 | DA-2026-0714-01 (brief) : fiabilisation export logs | ceo | refusée | 2j | oui | aucune — refusée par Sam avec preuve |
| DEC-2026-0714-03 | DA-2026-0714-02 (brief) : activation calendrier rapports directeurs | ceo | clos | 2j | oui | aucune — clôturée avec preuve |
| DEC-2026-0714-04 | DA-2026-0714-03 (brief) : confirmer hypothèse déploiement + test fumée | ceo | clos | 2j | oui | aucune — clôturée avec preuve |
| DEC-2026-0714-05 | Session validation inputs 14/07 : OKR H2, objectifs commerciaux, calendrier éditorial, comptes/onboarding, Postmark, fiches agents, cash_suivi | sam | clos | 2j | oui | aucune — clôturée avec preuve |
| DEC-2026-0716-01 | DA-2026-0715-01 : source de comptes cibles régime A (liste réelle / outil / ajuster le KPI) | ceo | attente_sam | 0j (nouvelle) | non | obtenir arbitrage Sam — bloque l'objectif hebdo 0/5 |
| DEC-2026-0716-02 | DA-2026-0715-02 : branchement lecture comité source concierge Sophie | ceo | attente_sam | 0j (nouvelle, mais sujet signalé sans décision depuis le 14/07) | non | obtenir arbitrage Sam — signalé 2 jours sans décision avant sa création |
| DEC-2026-0716-03 | DA-2026-0715-03 : fixer le seuil d'alerte cash (seuil_alerte_solde) | ceo | attente_sam | 0j (nouvelle) | non | obtenir arbitrage Sam — condition d'activation de la surveillance cash |
| DEC-2026-0716-04 | DA-2026-0715-04 : valider portrait Sophie CONT-2026-0715-01 + statut fiche source + format hook | ceo | attente_sam | 0j (nouvelle) | non | obtenir arbitrage Sam — bloque la publication [DH-CMO-001] |
| DEC-2026-0716-05 | DA-2026-0715-05 : cadrer le livre blanc v1 (sujet, plan, responsable, jalons) | ceo | attente_sam | 0j (nouvelle) | non | obtenir arbitrage Sam — échéance 30/11, 0 avancement |

**Décisions ouvertes (non terminales) : 6/11** — DEC-2026-0714-01
(`en_execution`, ≈1,58j sans activité) + 5 nouvelles `attente_sam`
(DEC-2026-0716-01 à 05). Aucune décision en retard (>3j sans activité) ni
en risque d'oubli (>7j) à ce jour. Aucune relance émise cette ronde.

**Écart de traçabilité corrigé cette ronde** : les 5 `decisions_attendues`
du brief CEO du 2026-07-15 (DA-2026-0715-01 à 05, destinataire Sam)
n'existaient pas dans la table `decisions` — créées ce jour en statut
`attente_sam` (DEC-2026-0716-01 à 05). Source : `deos-state get
brief#decisions_attendues` (maj 2026-07-15T07:32:37Z) vs `deos-decisions
list` du 2026-07-16. Point d'attention : DA-2026-0715-02 (concierge
Sophie) était déjà signalée sans décision associée depuis le 14/07 par le
rapport commercial (2 constats consécutifs) — ce n'est pas un sujet neuf
pour Sam, seule sa formalisation en décision date d'aujourd'hui.

Aucun nouveau brief CEO n'a été produit depuis le 2026-07-15T07:32:37Z au
moment de cette ronde (07:02 UTC) ; le rapprochement s'appuie donc sur le
dernier brief disponible (`briefs/brief-2026-07-15.md`).

## §2 Skills proposés

Aucun skill proposé à ce jour — `.claude/skills-proposed/` reste vide
(aucun sous-dossier directeur). Source : `find
/workspace/.claude/skills-proposed -mindepth 1` (2026-07-16T07:02Z, 0
résultat). Inchangé depuis les rondes du 14 et du 15/07.

## §3 Priorités / OKR de la semaine

**Toujours absent au niveau hebdomadaire (3e ronde consécutive).** La clé
`priorites_semaine` n'a jamais été alimentée dans `deos_state`. À signaler
à Sam ; aucune estimation ne sera produite par le CoS à sa place.

Cadre semestriel disponible (clé `okr_h2`, scénario NOMINAL, validé par
Sam le 14/07) : O1 Revenu (11 clients signés au 31/12 dont 3 Team, MRR
≥ 4 800 €), O2 Lancement (produit prêt 31/08, lancement payant septembre),
O3 Visibilité (13 contenus avant fin octobre, livre blanc v1 au 30/11), O4
Qualité (0 incident visible client, exécutions réussies ≥ 95 %), O5
Gouvernance (0 décision oubliée, brief à l'heure ≥ 95 %). Ce cadre H2 ne
remplace pas une déclinaison hebdomadaire — signalé comme écart tant que
`priorites_semaine` reste vide (cf. DEC-2026-0716-05 pour le livre blanc,
seul chantier O3 déjà tracé en décision).

Priorités du jour du dernier brief disponible (2026-07-15) : (1) débloquer
l'amont commercial (comptes cibles + concierge Sophie) — désormais tracé
via DEC-2026-0716-01/02 ; (2) fixer le seuil d'alerte cash — tracé via
DEC-2026-0716-03 ; (3) valider les livrables marketing en attente — tracé
via DEC-2026-0716-04 ; (4) définir les priorités de la semaine — toujours
sans décision associée, reste un angle mort de gouvernance côté comité ;
(5) cadrer le livre blanc — tracé via DEC-2026-0716-05.

## §4 Cash

**Surveillance cash alimentée mais toujours sans seuil d'alerte —
inchangé depuis le 14/07 (3e ronde consécutive).** Déclaré par Sam le
14/07 : solde 0 €, MRR réel 0 €, compte professionnel en cours
d'ouverture (source : `deos-state get cash_suivi`, maj_par sam,
2026-07-14 — aucune mise à jour depuis). `seuil_alerte_solde` est `null`
et `echeances_connues` est vide : aucune alerte ne peut être déclenchée
par le CoS. Ce point est désormais tracé par une décision explicite
(**DEC-2026-0716-03**, `attente_sam`) plutôt que par un simple signalement
répété — à surveiller pour éviter qu'il ne devienne un cas de relance
sans décision initiale de Sam.

## §5 Relances émises

Aucune relance émise cette ronde. La seule décision non terminale
antérieure (DEC-2026-0714-01, `en_execution`) est à ≈1,58 jour sans
activité prouvée, sous le seuil de 3 jours [DH-COS-004] — à re-vérifier
dès la prochaine ronde, une relance sera émise si aucune preuve n'apparaît
d'ici le 17/07 en fin de journée. Les 5 décisions nouvellement créées
(DEC-2026-0716-01 à 05) sont en `attente_sam` : par définition du cycle
(attente_sam → accordée/refusée → en_execution → close), elles n'entrent
dans le champ des relances qu'une fois accordées/en exécution ; aucune
relance n'est donc due sur ces 5 décisions à ce stade.

## Score d'exécution

**100/100 — vert.** Calcul : base 100 − 8×0 (décisions en retard >3j : 0/1
décision éligible accordée/en_execution) − 15×0 (décisions en risque
d'oubli >7j) − 5×0 (skills proposés en attente >14j, file vide) − 10×0
(priorité de semaine sans activité à mi-semaine — critère non applicable,
`priorites_semaine` jamais définie) = 100.

Point de vigilance non chiffré dans le score : 5 nouvelles décisions
`attente_sam` créées ce jour attendent l'arbitrage de Sam, dont une
(DA-2026-0715-02, concierge Sophie) sans réponse depuis 2 jours avant même
sa formalisation en décision.
