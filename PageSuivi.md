# Page de suivi — Digital·Humans
Générée par le Chief of Staff · ronde du 2026-08-07T07:08Z
Source : `psql "$COMITE_DB_DSN"` (table `decisions`, 56 lignes) · `deos-state get brief/rapport_*` (dernier brief consolidé : 2026-08-06) · `find .claude/skills-proposed` · `deos-state get priorites_semaine/cash_suivi`.

**Note de fraîcheur importante** : au moment de cette ronde (07:00–07:08Z), la ronde automatisée du jour (`rondes.sh`, cron 07:00Z) est **en cours d'exécution en parallèle** — 5 process `claude -p` actifs (PID 1196–1220) depuis 07:00Z, fichiers `rondes/*-2026-08-07.json` encore à 0 octet (normal, pas un échec : ces fichiers ne s'écrivent qu'à la fin du process). Cette ronde manuelle s'appuie donc sur le **dernier brief et les derniers rapports disponibles, datés du 2026-08-06**, complétés par des vérifications directes en base que j'ai faites moi-même ce 07/08 (citées comme telles).

---

## §1 — Décisions (56 au total : 21 attente_sam · 19 accordée · 2 en_execution · 11 clos · 3 refusée)

### 1.1 Accordée / en_execution SANS preuve — cœur de l'audit (par ancienneté)

| id | quoi | origine | statut | âge | preuve | prochaine action |
|---|---|---|---|---|---|---|
| DEC-2026-0714-01 | Interface web globale de suivi du comité | sam | accordee | 24j | non | **PAS en retard malgré l'âge** : activité réelle confirmée hier (commits `7459e66`,`1231612`,`f41915b`,`edb16b0`,`eca5530` du 2026-08-06 20:29–20:56Z, « Actes I/II/III » du tableau de bord). Reprend via DEC-2026-0804-05. Aucune action requise. |
| DEC-2026-0716-01 | Source de comptes cibles (sourcing prospection) | ceo | accordee | 22j | non | Sam a répondu le 06/08 (méthode + doc `sourcing_prospects.md`, refus explicite de nouvelle sollicitation). **Compteur redémarré au 06/08, J1 aujourd'hui.** Si aucune preuve de sourcing dans le rapport Commercial du 08/08, j'escalade au CEO en nommant Commercial/Marketing porteurs — pas de nouvelle sollicitation de Sam. |
| DEC-2026-0716-05 | Cadrage livre blanc v1 | ceo | accordee | 22j | non | Sam a répondu le 06/08 (« envoyez-moi ce que vous avez, je complèterai — 1er jet sans attendre »). Compteur redémarré, J1. Porteur : Marketing. |
| DEC-2026-0802-01 | Démo phare Agentforce→DH→sandbox | sam | accordee | 5j | non | **EN RETARD.** 0 livrable depuis le 02/08. Statut déjà demandé par Sam le 06/08 (DEC-2026-0806-01, réponse attendue en ronde du 07/08 — en cours). Ne pas dupliquer la relance. |
| DEC-2026-0802-02 | BUILD — reprise sur incident sans redémarrer phase 1 | ceo | accordee | 5j | non | Arbitrage produit (règle posée), reste à appliquer techniquement par Delivery. Pas de relance dédiée aujourd'hui, à recroiser avec DEC-2026-0806-23. |
| DEC-2026-0802-03 | BUILD — travail incrémental (delta) | sam | accordee | 5j | non | Idem — règle posée, application technique à vérifier. |
| DEC-2026-0802-05 | Mission juridique — vente hors France | sam | accordee | 5j | non | **EN RETARD.** Aucun livrable Légal retrouvé depuis le 02/08 (`rapport_legal` **jamais alimenté** dans `deos_state` — confirmé ce jour). Statut déjà redemandé par le CEO le 06/08 (DEC-2026-0806-02, 1 relance, réponse attendue). Si silence persistant après cette 2e ronde sans réponse → escalade à Sam nommément (Légal ne rend pas compte malgré 2 demandes du CEO). |
| DEC-2026-0802-06 | Mission juridique — audit RGPD parcours | sam | accordee | 5j | non | Même situation que ci-dessus, même relance groupée (DEC-2026-0806-02). |
| DEC-2026-0802-07 | AI Act art. 50 — conformité | sam | en_execution | 5j | non | Progrès réel constaté (mentions_ia.md, pages légales, mention IA widget testée — fichiers vérifiés ce jour, cf. §Alertes). Statut déjà redemandé par Sam (DEC-2026-0806-03, en cours de ronde). |
| DEC-2026-0802-08 | Mission transverse Entracte (cadrage) | sam | accordee | 5j | non | Reprise et séquencée par DEC-2026-0803-02 ci-dessous — ne pas compter deux fois le retard. |
| DEC-2026-0803-01 | GO correctif bug BUILD phase2 (NoneType, exec 165) | ceo | accordee | 4j | non | **EN RETARD — ET DÉSACCORD FACTUEL À SIGNALER.** Vérification directe que j'ai faite ce jour (`psql "$DEOS_RO_DSN" -c "SELECT * FROM v_deos_build_phases WHERE execution_id=165"`) : phase2 toujours `failed`, `last_error` identique, `started_at=completed_at=2026-08-02T17:55:43Z`, **aucun changement depuis le 02/08**. Or DEC-2026-0806-23 (06/08, statut attente_sam) affirme *« le correctif du bug NoneType est appliqué »* — affirmation **non corroborée par la base**. Cf. alerte dédiée ci-dessous, à remonter à Sam sans délai [DH-COS-002]. |
| DEC-2026-0803-02 | Séquencement Entracte (arbitrage CEO 03/08) | ceo | en_execution | 4j | non | **EN RETARD**, confirmé stagnant par le rapport Marketing du 06/08 (« textes inchangés depuis le 03/08 »). Statut déjà redemandé (DEC-2026-0806-04, en cours de ronde). |
| DEC-2026-0803-03 | Série des 11 portraits — traitement visuel | sam | accordee | 4j | non | **EN RETARD**, aucune trace de production dans le rapport Marketing du 06/08. Porteur Marketing. Pas de relance Sam (déjà arbitré) — si rien au 09/08, escalade CEO nommant Marketing. |
| DEC-2026-0803-04 | Page LinkedIn Digital·Humans | sam | accordee | 4j | non | **EN RETARD**, même constat. Porteur Marketing, dépend en partie de DEC-2026-0716-01 (compte commercial). |
| DEC-2026-0803-05 | Identité visuelle des directeurs | sam | accordee | 4j | non | **EN RETARD**, question d'arbitrage (illustré vs photo-réaliste) toujours ouverte, aucune trace de décision de contenu. Porteur Marketing + validation Légal. |
| DEC-2026-0803-06 | Règle « toute proposition porte son coût » | sam | accordee | 4j | non | Règle de fonctionnement, pas un livrable — j'en vérifie l'application en continu (fait : les décisions du 06/08 citent systématiquement un coût). Pas de relance. |
| DEC-2026-0804-01 | Fiabilisation export logs backend (ré-arbitrage) | sam | accordee | 3j | non | **FRANCHIT LE SEUIL DE RETARD AUJOURD'HUI.** Delivery a livré une proposition chiffrée à 3 options le 05/08 (PROP-2026-0805-01, reco Option A), gravité élevée à « haute » le 06/08 (dégradation des logs qui s'aggrave, 6e ronde consécutive). **Relance émise aujourd'hui vers Sam** : le travail de préparation est fait, il ne reste qu'un choix. |
| DEC-2026-0804-02 | Suivi 8 chantiers O2 | sam | accordee | 3j | non | Modalité fixée par Sam lui-même (MAJ hebdo manuelle). Pas de relance — l'échéance est la sienne. |
| DEC-2026-0804-05 | Mission collective interface web (spec DSI) | sam | accordee | 3j | non | Activité réelle confirmée (commits du 06/08 sur le tableau de bord). Retard signalé par Marketing sur la consolidation DSI attendue le 05/08 — à recroiser au comité du 10/08, pas une relance CoS. |

### 1.2 attente_sam (21 — arbitrage ou accusé de réception de Sam attendu)

Tous datés du 05/08 ou 06/08 (âge 1–2 jours) : **sous le seuil de relance (3j)**, aucune action de ma part aujourd'hui sauf listing. Le volume (21) reflète la session d'arbitrage massive du 06/08, pas un nouvel engorgement — à surveiller si le rythme de traitement ne suit pas dans les 3 prochains jours.

| id | quoi (résumé) | âge |
|---|---|---|
| DEC-2026-0805-01 | MAJ offre canonique — grands comptes / plafonds Bloc II | 2j |
| DEC-2026-0806-01 à 04 | Demandes de statut de Sam (démo Agentforce, juridique, AI Act, Entracte) — réponses attendues dans la ronde du 07/08, actuellement en cours | 1j |
| DEC-2026-0806-05 | Amendement plan Raj (champs Lead créés manuellement) | 1j |
| DEC-2026-0806-07 | Accès Salesforce du comité (Comite_RO) opérationnel | 1j |
| DEC-2026-0806-08 | Audit de sécurité des accès (mots de passe partagés) | 1j |
| DEC-2026-0806-09/10 | Offre intégrateur (12 identifiés) / base 149 partenaires Salesforce | 1j |
| DEC-2026-0806-11 | Stratégie d'approche à 3 moteurs (Team/Pro/Partenaires) | 1j |
| DEC-2026-0806-12 | Chemin critique réouverture du site | 1j |
| DEC-2026-0806-13 | Mentions IA — libellés définitifs | 1j |
| DEC-2026-0806-14 | Opportunité DSI Crédit Logement (dernière semaine d'août) | 1j |
| DEC-2026-0806-15 | Décision de démonstration (résiduelle, mode demo) — **anomalie de nettoyage** : 0806-16/17 (mêmes conditions) sont déjà `refusee` automatiquement, 0806-15 est resté `attente_sam`. Signalé, pas de correction de ma part (hors mon scope d'écriture sans preuve de statut réel). | 1j |
| DEC-2026-0806-18 | Veille concurrentielle N8N repointée Gemini — 1er rapport produit | 1j |
| DEC-2026-0806-19/20 | Pages légales prêtes / mention IA widget Sophie testée | 1j |
| DEC-2026-0806-21 | 5 workflows dormants repointés Gemini | 1j |
| DEC-2026-0806-22 | Consigne de présentation au CEO (format tableau de bord) | 1j |
| DEC-2026-0806-23 | Arbitrage budget BUILD — reprendre exec 165 | 1j — **voir alerte : affirmation non corroborée par la base** |

### 1.3 Clôturées / refusées cette semaine (rappel)
11 clos (dont **DEC-2026-0716-02 clôturé par moi aujourd'hui**, preuve : vues `v_deos_leads/prospects/veille` vérifiées lisibles par Commercial le 06/08 et re-vérifiées par moi ce jour), 3 refusées (dont 2 décisions de démonstration purgées automatiquement).

---

## §2 — Skills proposés par les directeurs
**File vide** : `find /workspace/.claude/skills-proposed -mindepth 1` → 0 résultat, vérifié ce jour 2026-08-07T07:0xZ. Aucun skill à faire valider par Sam. Signalé pour qu'une file vide ne soit jamais lue comme une file traitée.

---

## §3 — Priorités / OKR de la semaine (source : `deos-state get priorites_semaine`, alimenté par cos le 2026-08-03)

| rang | titre | responsable | activité cette semaine |
|---|---|---|---|
| 1 | BUILD : correctif phase2 + spec delta prêts pour le GO de Sam (O2/O4, checkpoint 15/08) | delivery | Mitigée : GO donné (0803-01) puis « repris » selon 0806-23, **mais la base ne montre aucun changement** (cf. alerte). |
| 2 | Purger le lot d'arbitrage prioritaire (attente_sam) | chief-of-staff | Active — 21 décisions arbitrées/créées le 06/08, 1 clôturée par moi aujourd'hui. |
| 3 | Jalons commerciaux du 15/08 (bibliothèque 15/15, trames) | commercial | Stagnante sur la bibliothèque (8/15 inchangé), mais activité annexe (partenaires, stratégie d'approche). |
| 4 | Conformité AI Act art. 50 — checklist réouverture Sophie | legal | Active le 06/08 (mentions_ia.md, pages légales, mention widget) — mais **jamais via le canal `rapport_legal`**, donc invérifiable par le cycle normal. |
| 5 | Séquence éditoriale (rang 3 prêt, carte 4 neutralisée) | marketing | Stagnante sur rangs 1–2 (publication LinkedIn non confirmée depuis le 16/07). |

Aucune priorité n'est totalement sans activité cette semaine → pas de pénalité "-10 priorité morte" au calcul du score.

---

## §4 — Cash (mandat DH-COS-003 : lecture/alerte uniquement, jamais d'estimation de ma part)

Source : `deos-state get cash_suivi`, dernière mise à jour **2026-08-06T07:06Z par cos**.

- **Solde déclaré : 0 EUR, déclaré par Sam le 2026-07-14 — inchangé depuis 24 jours.** Surveillance du solde toujours largement inactive : je le signale conformément à mon mandat, sans l'estimer.
- **Seuil d'alerte : 50 EUR, confirmé par Sam le 2026-08-06** (DEC-2026-0716-03, désormais **clos avec preuve** — bonne nouvelle : ce point était en risque d'oubli depuis 20 jours, il est résolu).
- Crédits API : plafond 100 USD, recharge auto active (mise en place par Sam le 02/08). Repère de consommation daté du 02/08 : ~20 % consommé (exécution 165 = 26,13 USD, travaux comité ≈ 15 USD). **Pas de donnée de consommation plus récente disponible** — à signaler, pas à extrapoler.
- Aucune échéance connue déclarée.

---

## §5 — Relances émises cette ronde (2026-08-07)

| destinataire | décision(s) | objet | pourquoi maintenant |
|---|---|---|---|
| **Sam** (direct, sans délai — [DH-COS-002]) | DEC-2026-0803-01 / DEC-2026-0806-23 | **« Fait » non prouvé** : DEC-2026-0806-23 affirme le correctif BUILD appliqué ; vérification directe en base (`v_deos_build_phases#165`, ce jour) montre 0 changement depuis le 02/08. À trancher : soit le correctif n'a pas été rejoué, soit l'affirmation est erronée — J-8 du checkpoint 15/08. | Risque opérationnel majeur sur un jalon commercial ; règle explicite : ce cas remonte à Sam directement. |
| **Sam** | DEC-2026-0804-01 | Choisir parmi les 3 options chiffrées de PROP-2026-0805-01 (reco Delivery : Option A) pour la fiabilisation des logs — dégradation en aggravation (6e ronde consécutive). | Franchit le seuil de 3 jours aujourd'hui ; le travail de préparation est fait, seule une décision manque. |
| **CEO** (info nombre seulement à Sam) | DEC-2026-0802-05, DEC-2026-0802-06 | Rappel du statut « aucun rapport Légal jamais reçu » — 2e ronde sans réponse après la relance CEO du 06/08 (DEC-2026-0806-02). Si le 08/08 reste muet, j'escalade nommément à Sam (Légal ne rend pas compte malgré 2 demandes du CEO). | Respect du protocole d'escalade en 2 temps. |
| — (aucune relance) | DEC-2026-0716-01, DEC-2026-0716-05 | Compteur redémarré au 06/08 après réponse de Sam — trop tôt (J1) pour relancer ; je ne redemande pas ce que Sam a déjà fourni. | Consigne du 06/08 |
| — (aucune relance, à surveiller) | DEC-2026-0803-03/04/05 | Portraits, page LinkedIn, identité visuelle — en retard (4j) mais création récente et dépendance à la levée du blocage AI Act (résolue le 06/08) ; je laisse un cycle avant d'escalader au CEO en nommant Marketing. | DH-COS-004 : pas de harcèlement, un signal d'abord. |

---

## §6 — Score d'exécution du jour

**Score = 28/100 — ROUGE**

Calcul (formule visible) : base 100
− 8 × 9 décisions en retard (>3j sans activité réelle constatée) : DEC-2026-0802-01, 0802-05, 0802-06, 0803-01, 0803-02, 0803-03, 0803-04, 0803-05, 0804-01 = **−72**
− 15 × 0 décision en risque d'oubli (>7j) — **aucune aujourd'hui** (les trois qui l'étaient hier — 0716-01/02/03 — ont toutes bougé : 03 clos, 02 clos, 01 recompté depuis la réponse de Sam du 06/08)
− 5 × 0 skill proposé sans traitement >14j (file vide)
− 10 × 0 priorité de semaine totalement sans activité
= **28, rouge (<60)**

**Lecture** : le score baisse fortement par rapport au 05/08 (39) non pas parce que la situation se dégrade, mais parce que la vague de décisions arbitrées entre le 02/08 et le 04/08 (9 décisions) franchit mécaniquement le seuil des 3 jours ce matin, en même temps. Deux faits positifs contrebalancent : (1) zéro décision en risque d'oubli aujourd'hui contre 3 hier — les plus anciens blocages ont tous été débloqués par Sam le 06/08 ; (2) une décision close avec preuve aujourd'hui (DEC-2026-0716-02). Le point de vigilance réel n'est pas le volume, c'est la **contradiction factuelle sur le correctif BUILD** (DEC-2026-0803-01/0806-23), à 8 jours du checkpoint.
