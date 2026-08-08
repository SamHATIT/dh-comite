# Conformité des données clients — avis préalable à la mise en ligne

> **Date :** 2026-08-08
> **Auteur :** Directeur Juridique Digital·Humans
> **Commande :** Sam, 08/08 — condition du GO conditionnel de mise en ligne
> **Nature :** préparation de mise en conformité. **Ce document n'est pas un conseil
> juridique.** Les points marqués ⚖️ doivent être validés par un avocat.

---

## AVIS — réponse à la question posée

Sam a posé une condition claire : « dès que le Juridique valide que tout est OK,
on met en live ». Je suis le dernier verrou, je dois donc répondre sans
approximation.

**AVIS : DÉFAVORABLE en l'état, pour une mise en ligne AVEC parcours client
(inscription, upload, abonnement).**

**AVIS : FAVORABLE SOUS RÉSERVE pour une réouverture VITRINE de
digital-humans.fr** (contenu public, concierge Sophie avec sa mention IA, aucune
inscription ouverte), une fois publiées les trois pages légales du 06/08.

Ce n'est pas une réserve de principe. Six constats bloquants sont établis
ci-dessous **par preuve technique**, pas par précaution. Deux d'entre eux
n'étaient pas connus avant cet audit :

| # | Constat bloquant | Gravité | Preuve |
|---|---|---|---|
| B1 | **La politique de confidentialité en ligne affirme des mesures de sécurité qui n'existent pas** (coffre à secrets, sauvegardes chiffrées) | Critique | §2.3 |
| B2 | **Les identifiants Salesforce des clients sont stockés en clair en base**, dans des colonnes nommées `encrypted_*` | Critique | §2.1 |
| B3 | **L'isolement des contextes clients n'est pas prouvable** avec les accès du comité | Bloquant | §1.3 |
| B4 | L'engagement « Zero Data Retention » d'Anthropic est **affirmé publiquement sans preuve** au dossier | Bloquant | §2.4 |
| B5 | Les pages légales du 06/08 **ne sont pas publiées** — le site sert toujours l'entracte, et la version précédente contient des champs `[À COMPLÉTER]` | Bloquant | §3.1 |
| B6 | Les deux sites vitrines **n'ont aucune mention légale accessible** (LCEN) | Bloquant | §4 |

Le point A de la mission — le cloisonnement — appelle une réponse nuancée que je
donne d'emblée : **la règle de Sam est respectée sur sa première moitié et
non prouvée sur la seconde.** Le RAG commun ne contient effectivement aucune
donnée client (prouvé). L'isolement des contextes clients entre eux ne l'est pas
(non prouvable avec mes accès).

---

## 1. LE CLOISONNEMENT DES DONNÉES CLIENTS

Règle posée par Sam : « le RAG commun ne contient rien de propre à chaque client,
mais les contextes clients doivent être isolés. »

J'ai traité les deux moitiés séparément, parce qu'elles n'ont pas le même statut
probatoire.

### 1.1 Ce que contient réellement le RAG commun — **CONFORME, PROUVÉ**

**Verdict : le RAG commun ne contient aucune donnée client.** C'est établi, pas
supposé.

Le corpus est une base vectorielle ChromaDB, en `PersistentClient` local (pas de
serveur séparé), de **91 866 chunks répartis en 6 collections thématiques**.

| Collection | Contenu | Source de la preuve |
|---|---|---|
| `business`, `operations`, `technical` | Documentation Salesforce | `agents_registry.yaml` (champ `rag_collections` de chaque agent) |
| `apex` | Apex Reference Guide | `RAG_V2_JOURNAL.md`, 12/07 |
| `lwc` | Documentation LWC | idem |
| `china_collection` | Hyperforce / SFOA Chine, isolation `region=cn` | `refonte/sources/timeline.yaml` |

**Origine documentée de l'ingestion** (`RAG_V2_JOURNAL.md` 12–14/07 et
`refonte/sections/rag.html`) : Winter/Spring/Summer '26 Release Notes (PDF
officiels Salesforce), Shield Platform Encryption, AgentScript spec (TDX 2026),
Headless 360, Hyperforce/SFOA. Batch `sf_docs_2026_04_23`, idempotent.

Toutes ces sources sont de la **documentation Salesforce publique**. Le pipeline
d'ingestion est manuel, par lots tracés, alimenté depuis le CDN
`resources.docs.salesforce.com`. Aucun chemin d'ingestion automatique depuis les
projets clients n'apparaît dans la chaîne documentée.

> **Réserve d'honnêteté.** Cette preuve est *documentaire et structurelle*, pas
> une inspection du contenu des 91 866 chunks. Je n'ai pas accès à ChromaDB. La
> preuve directe consisterait à lister les collections et à échantillonner leurs
> métadonnées (§1.4, test T1). Elle est facile à produire et je la recommande,
> mais l'absence de chemin d'ingestion client est déjà un argument fort.

### 1.2 Où vivent les contextes clients

Les données propres à chaque client vivent à **quatre endroits distincts**, que
j'ai identifiés par lecture du schéma de production (rôle `deos_ro`) :

| Contexte | Table / stockage | Rattachement au client |
|---|---|---|
| Documents importés | `project_documents` (+ fichier sur disque, `file_path`) | `project_id` → `projects.user_id` |
| Conversations projet | `project_conversations` | `project_id`, `execution_id` |
| Code et livrables générés | `execution_artifacts`, `outputs`, `agent_deliverables`, `document_fusion` | `project_id` / `execution_id` |
| Identifiants Salesforce | `project_credentials`, `project_environments` | `project_id` |
| Conversations visiteurs (Sophie) | `chat_logs` | **aucun rattachement** — `session_uuid` + `ip_hash` |

Point structurant : `project_documents` porte une colonne **`collection_name`**
et un `chunk_count`. Les documents importés par un client sont donc **découpés et
vectorisés dans une collection ChromaDB nommée**, distincte des 6 collections du
corpus commun. L'architecture nomme d'ailleurs explicitement la route
`documents → P3 RAG isolation` (`architecture.md`).

**Le mécanisme d'isolement est donc : une collection ChromaDB par périmètre,
désignée par `project_documents.collection_name`, plus un filtrage applicatif par
`project_id` en base.**

### 1.3 La preuve de l'isolement — **NON PROUVABLE avec mes accès**

C'est le point que Sam a demandé de ne pas traiter par l'intention. Je le traite
donc par ce que j'ai pu tester, et je dis où je bute.

**Ce que j'ai pu prouver — et qui va dans le mauvais sens :**

**a) Aucune sécurité au niveau de la base.** Testé directement :

```sql
SELECT c.relname, c.relrowsecurity, c.relforcerowsecurity
FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public' AND c.relkind = 'r';
-- Résultat : 46 tables, relrowsecurity = f pour TOUTES

SELECT * FROM pg_policies;
-- Résultat : 0 ligne
```

**Row Level Security n'est activée sur aucune des 46 tables, et il n'existe
aucune policy.** Le cloisonnement en base ne repose donc sur **aucun mécanisme
technique** : il repose entièrement sur la discipline du code applicatif à
toujours filtrer par `project_id`. Une requête qui oublie la clause `WHERE`
retourne les données de tous les clients, sans obstacle.

**b) L'intégrité référentielle existe, et c'est le point positif.** 22 clés
étrangères rattachent les tables de contenu à `projects` ou `users`
(`project_documents_project_id_fkey`, `project_conversations_project_id_fkey`,
`outputs_project_id_fkey`, etc.). La structure *permet* le cloisonnement. Elle ne
l'*impose* pas.

**c) ChromaDB n'a pas de couche d'authentification.** C'est un `PersistentClient`
local (`refonte/sections/rag.html`) : un fichier sur disque ouvert par le
processus backend. Il n'y a pas de notion d'utilisateur ni de permission par
collection. L'isolement entre collections client repose donc **uniquement** sur
le fait que le code demande la bonne collection.

**Ce que je n'ai pas pu vérifier, et pourquoi :**

| Question ouverte | Pourquoi je ne peux pas trancher |
|---|---|
| `collection_name` est-il unique par projet, ou partagé ? | Le rôle `deos_ro` n'a **aucun droit** sur `project_documents` — seules 10 vues `v_deos_*` lui sont ouvertes, et aucune n'expose les documents. Vérifié : `information_schema.table_privileges` ne retourne que ces 10 vues en `SELECT`. |
| Les requêtes RAG sont-elles bornées à la collection du projet ? | Le code (`app/services/rag_service.py`) **n'est pas accessible** depuis le conteneur du comité. `/opt/digital-humans/` est vide ici ; la plateforme tourne ailleurs. |
| Un agent peut-il interroger la collection d'un autre client ? | Même cause. C'est la question centrale, et elle est hors de ma portée. |

**Verdict : À CORRIGER — l'isolement des contextes clients n'est pas prouvable
en l'état.** Conformément à la consigne de Sam, je qualifie donc ce point comme
**bloquant avant toute inscription ouvrant l'upload de documents.**

Je nuance sur un point, par honnêteté : « non prouvable » ne veut pas dire
« défaillant ». L'existence d'une route dédiée nommée *RAG isolation* et d'une
colonne `collection_name` suggère que le sujet a été traité par la Delivery. Mais
un engagement contractuel de cloisonnement ne peut pas reposer sur une
présomption favorable — surtout sans RLS en filet de sécurité.

### 1.4 Le protocole de preuve à exécuter (Delivery, ~2 h)

Voici les quatre tests qui transforment la présomption en preuve. Je ne peux pas
les exécuter — ils exigent un accès au serveur de production et au code, que mon
curseur et mes droits m'interdisent. Ils sont écrits pour être rejoués et versés
au dossier.

**T1 — Le corpus commun est-il propre ?**
```python
import chromadb
c = chromadb.PersistentClient(path=os.environ["DH_CHROMA_PATH"])
for col in c.list_collections():
    print(col.name, col.count())
# Attendu : les 6 collections documentaires, et AUCUNE collection projet
# dont le contenu serait mêlé. Échantillonner 20 métadonnées par collection
# et vérifier que la source est bien un PDF Salesforce.
```

**T2 — Une collection par projet, sans collision.**
```sql
SELECT collection_name, count(*) AS docs, count(DISTINCT project_id) AS projets
FROM project_documents GROUP BY collection_name HAVING count(DISTINCT project_id) > 1;
-- Attendu : 0 ligne. Toute ligne retournée = deux clients dans la même
-- collection = défaut de cloisonnement caractérisé.
```

**T3 — La requête RAG est-elle bornée ?** Relire `rag_service.py` et prouver que
la collection interrogée est dérivée du `project_id` du contexte d'exécution, et
jamais d'un paramètre fourni par l'appelant. Verser l'extrait au dossier.

**T4 — Test d'intrusion applicatif.** Avec le compte du client A authentifié,
appeler les routes `documents` et `hitl` en substituant l'identifiant d'un projet
du client B. **Attendu : HTTP 403/404, jamais 200.** C'est le seul test qui prouve
l'isolement du point de vue de l'attaquant plutôt que du concepteur.

**Recommandation complémentaire, que je porte comme juriste :** activer la RLS
PostgreSQL sur les tables porteuses de `project_id`. Le filtrage applicatif est
une bonne pratique ; la RLS est une garantie. Devant un client qui auditera son
sous-traitant — et un DSI de banque le fera — « nous filtrons dans le code » est
une réponse nettement plus faible que « la base refuse la lecture croisée ».

---

## 2. CE QUE SAM SOULÈVE

### 2.1 Chiffrement — **À CORRIGER, constat critique**

**Ce qu'un client peut légitimement exiger.** Le RGPD n'impose pas le chiffrement
en toutes circonstances : l'article 32.1 exige des mesures « appropriées au
risque », et cite le chiffrement au point (a) comme mesure de référence. Pour un
sous-traitant qui détient **les identifiants d'accès aux orgs Salesforce de ses
clients**, le risque est élevé et le chiffrement au repos n'est pas une option de
confort. La CNIL le recommande explicitement pour les secrets d'authentification.

| Exigence client | État réel | Verdict |
|---|---|---|
| Chiffrement **en transit** (externe) | TLS sur les sites et les API fournisseurs | CONFORME |
| Chiffrement **en transit** (interne) | Postgres et Redis en `127.0.0.1`, Redis **sans mot de passe** | ACCEPTABLE (boucle locale), à documenter |
| Chiffrement **au repos** des identifiants Salesforce | **EN CLAIR** | **NON CONFORME** |
| Chiffrement **au repos** de la base | Non documenté, non prouvé | À DOCUMENTER |
| Chiffrement des **sauvegardes** | Non prouvé — et pourtant **affirmé publiquement** | **NON CONFORME** (§2.3) |
| Gestion des **clés** | Fichiers `.env`, rotation manuelle, **aucun coffre** | À CORRIGER |

**Le constat critique.** La documentation technique de la plateforme
(`refonte/sections/security.html`, section « Hardening — backlog ») porte cette
ligne :

> « Chiffrement at-rest des `project_credentials` (**actuellement clair en DB**) »

Or la même page décrit, deux lignes plus haut, les mêmes données comme
« SFDX credentials — Par projet, **chiffrées** ». Et le schéma de la table nomme
la colonne **`encrypted_value`**. La table `project_environments` va plus loin :
`encrypted_client_id`, `encrypted_client_secret`, `encrypted_private_key`,
`encrypted_refresh_token`, `encrypted_security_token`.

**Des colonnes nommées « encrypted_* » contiennent des secrets en clair.** C'est
le pire des cas : un nom qui inspire confiance à quiconque relit le schéma —
développeur, auditeur, client — et une réalité contraire. Le risque n'est pas
seulement juridique, il est opérationnel : personne ne corrige un problème que le
schéma déclare résolu.

Ce que cela expose concrètement : ces secrets ouvrent l'accès aux orgs Salesforce
des clients, donc aux données des clients **de nos clients**. Une compromission
de la base ne serait pas un incident Digital·Humans, mais un incident chez chacun
des clients, avec notification CNIL au titre de l'article 33 et information des
personnes au titre de l'article 34.

⚖️ **Ce point doit être corrigé avant toute connexion d'une org Salesforce d'un
client réel.** Il est bloquant pour le palier Team, pas pour une vitrine.

**Ce qui manque, par ordre :**
1. Chiffrement applicatif effectif des colonnes `encrypted_*` (a minima AES-GCM,
   clé hors base) — **et vérification que le nom des colonnes dit la vérité** ;
2. Un coffre à secrets (Vault, AWS Secrets Manager, Doppler). L'architecture le
   reconnaît elle-même comme non-goal assumé : « No real Vault / AWS Secrets
   Manager integration » ;
3. La traçabilité des accès aux secrets : `audit_logs` compte 22 colonnes mais,
   de l'aveu de la documentation, « les actions secrets (rotations, changements)
   ne sont pas tracées » ;
4. Le chiffrement au repos des sauvegardes — ou, à défaut, **le retrait immédiat
   de l'affirmation contraire de la politique de confidentialité**.

**Deux fragilités connexes relevées au passage** (hors mandat strict, mais elles
pèsent sur la même promesse de sécurité) : aucune limitation de débit sur
`/auth/login` (force brute), et pas de 2FA sur les comptes d'administration.

### 2.2 Mention au moment de l'import — **MANQUANTE**

Aucune mention n'existe au point d'import. L'article 13 du RGPD impose
l'information **au moment de la collecte**, et l'upload est précisément le moment
où un client peut déposer, sans y penser, des données personnelles de tiers
(salariés, prospects, clients finaux figurant dans un brief ou un export).

**Texte proposé, à afficher dans la zone de dépôt — pas dans une infobulle :**

**FR**
```
Vos documents sont traités pour produire vos livrables, et pour cela seulement.
Ils sont isolés de ceux des autres clients et ne rejoignent aucune base de
connaissances partagée. Leur contenu est transmis à notre fournisseur de modèles
d'IA pour le temps du traitement ; il ne sert jamais à entraîner un modèle.
Conservation : durée de votre abonnement, puis 30 jours. Vous pouvez les
supprimer à tout moment depuis votre espace.

Si un document contient des données personnelles concernant des tiers, vous
restez responsable de traitement : assurez-vous d'être fondé à nous les confier.
```

**EN**
```
Your documents are processed to produce your deliverables, and for nothing else.
They are isolated from other customers' documents and never join a shared
knowledge base. Their content is sent to our AI model provider for the duration
of processing only; it is never used to train a model.
Retention: for the duration of your subscription, then 30 days. You can delete
them at any time from your workspace.

If a document contains personal data about third parties, you remain the data
controller: please make sure you have a lawful basis to share it with us.
```

⚠️ **La première phrase du second paragraphe engage** : elle affirme
l'isolement. Elle ne doit être publiée qu'une fois les tests §1.4 passés.

### 2.3 Engagement de non-utilisation — **le point le plus grave**

C'est ici que j'ai trouvé le constat le plus sérieux de cet audit, et il ne
figurait dans aucune commande.

**La politique de confidentialité actuellement en ligne contient des
affirmations de sécurité fausses.** Source : `dh-mod28-legal-content.py`
(contenu publié, rédigé le 01/05/2026), section 8 « Sécurité » :

| Affirmation publiée | Réalité établie | Source de la réfutation |
|---|---|---|
| « Les secrets d'API sont gérés via **un coffre dédié** » | Secrets en fichiers `.env`, rotation manuelle, aucun coffre | `security.html` ; `architecture.md` : « No real Vault / AWS Secrets Manager integration » |
| « Les sauvegardes de la base de données sont **chiffrées au repos** » | Non prouvé ; le chiffrement at-rest est au backlog | `security.html`, section Hardening |

Une politique de confidentialité est une **information due aux personnes
concernées** au sens des articles 13 et 14 du RGPD. Y décrire des mesures de
sécurité inexistantes n'est pas une imprécision rédactionnelle : c'est une
information inexacte sur les mesures de l'article 32, opposable en cas de
contrôle comme en cas de violation de données. Et à l'égard de clients
professionnels, une allégation de sécurité non étayée relève aussi du terrain des
pratiques commerciales trompeuses.

**Correction : retirer ces deux affirmations aujourd'hui, ou les rendre vraies
avant publication.** Ne rien affirmer qu'on ne puisse démontrer. Une politique
sobre et exacte protège mieux qu'une politique flatteuse et fausse.

**Ce que les fournisseurs garantissent réellement — vérifié aux sources.**

**Anthropic — garantie contractuelle établie.** Les Commercial Terms of Service,
section B, disposent : « **Anthropic may not train models on Customer Content
from Services.** » C'est une obligation contractuelle, pas une politique
révocable. Le centre de confidentialité le confirme : « By default, we will not
use your inputs or outputs from our commercial products (e.g. Claude for Work,
Anthropic API…) to train our models. »

> ⚠️ **Exception à maîtriser :** ce même document précise que le retour explicite
> d'un utilisateur (bouton pouce haut/bas) **lève** la garantie — Anthropic
> conserve alors la conversation entière jusqu'à 5 ans et peut l'utiliser pour
> l'entraînement. **Action concrète : si la plateforme expose un jour un bouton
> de feedback vers l'API, cette garantie tombe.** À interdire par conception, ou
> à désactiver dans les paramètres d'organisation.

Rétention par défaut hors ZDR : suppression sous 30 jours ; jusqu'à 2 ans en cas
de violation des règles d'usage, et 7 ans pour les scores de classification.

**OpenAI — garantie établie, fournisseur non déclaré côté comité.** « Data sent
to the OpenAI API is not used to train or improve OpenAI models (unless you
explicitly opt in) », rétention par défaut 30 jours pour la surveillance des abus.

> **Correction à apporter à la commande.** La mission vise « nos fournisseurs
> (Anthropic, Google) ». **Google n'est pas dans la chaîne de traitement.** Les
> deux fournisseurs réels sont **Anthropic** (modèles de langage) et **OpenAI**
> (embeddings du RAG, modèle `3-large`). Preuves : `security.html` inventorie
> `OPENAI_API_KEY` ; `RAG_V2_JOURNAL.md` chiffre le coût d'embedding OpenAI ;
> `deployment.md` exige `OPENAI_API_KEY` « for RAG embeddings ». La politique de
> confidentialité en ligne cite bien OpenAI — mais **la version refondue du
> 06/08 l'a omis**, ce qui serait une régression si elle était publiée en l'état
> (article 13.1.e : les destinataires doivent être nommés).

### 2.4 L'affirmation « Zero Data Retention » — **À PROUVER, bloquant**

La politique en ligne affirme : « Anthropic PBC — **Engagement Zero Data
Retention activé** : aucune conservation des prompts et des réponses au-delà du
temps strict de traitement. »

C'est une affirmation vérifiable, et je n'ai trouvé **aucune preuve** de cet
accord au dossier. Or, d'après le centre de confidentialité d'Anthropic, le ZDR
n'est **pas** un réglage par défaut : il est accordé « **subject to Anthropic's
approval** », négocié avec l'équipe commerciale, et appliqué **par organisation**.

**Vérification que Sam peut faire seul, en deux minutes** — c'est le seul point
de ce rapport que je ne peux pas trancher et qui ne demande personne d'autre :

> Console Anthropic → **Settings → Privacy Controls → Data retention period**

- Si le ZDR y figure : archiver la capture au dossier, l'affirmation est fondée.
- **Sinon : retirer la phrase de la politique aujourd'hui.** Sans ZDR, la
  rétention réelle est de 30 jours — ce qui reste parfaitement défendable, à
  condition de l'écrire.

### 2.5 La case à cocher à l'inscription

**Principe.** La CNIL et le CEPD sont constants : une acceptation globale
mélangeant CGV et données n'est pas valable, et une case pré-cochée n'est pas un
consentement (RGPD art. 4.11 et art. 7). Il faut donc **séparer** ce qui est
accepté (le contrat) de ce qui est porté à connaissance (l'information données).

**Nuance importante, et elle simplifie les choses :** le traitement des données
du client repose sur l'**exécution du contrat** (art. 6.1.b), pas sur le
consentement. La politique de confidentialité n'a donc pas à être « acceptée » —
elle doit être **portée à connaissance**. Faire cocher une case de consentement
là où la base légale est contractuelle est une erreur fréquente qui fragilise le
dossier plutôt qu'elle ne le renforce.

**Formulation retenue — trois lignes, deux cases seulement obligatoires :**

**FR**
```
☐  J'ai lu et j'accepte les Conditions générales de vente et d'utilisation.        [obligatoire]

☐  J'ai pris connaissance de la Politique de confidentialité, qui décrit les
   données traitées, leur durée de conservation, les sous-traitants auxquels
   elles sont transmises et mes droits.                                            [obligatoire]

☐  Je souhaite recevoir les actualités de Digital·Humans par courriel.
   Je peux me désinscrire à tout moment.                                           [facultatif]
```

**EN**
```
☐  I have read and accept the Terms of Sale and Use.                               [required]

☐  I have read the Privacy Policy, which describes the data processed, how long
   it is kept, the sub-processors it is shared with, and my rights.                [required]

☐  I would like to receive Digital·Humans news by email.
   I can unsubscribe at any time.                                                  [optional]
```

**Ce que cela engage, et les règles à respecter :**
- Aucune case **pré-cochée** — y compris la troisième (art. 4.11 RGPD) ;
- Les deux premières sont **distinctes** : une seule case pour les deux serait
  une acceptation globale, contestable ;
- La troisième est **détachable** : refuser la newsletter ne peut pas empêcher
  l'inscription (art. 7.4 RGPD) ; si elle est cochée, **double opt-in**
  (courriel de confirmation) — la chaîne N8N `Lead Capture - Website` envoie déjà
  un courriel de vérification, la brique existe ;
- « CGV » et « Politique de confidentialité » sont des **liens cliquables** vers
  les pages réelles, ouvrables **avant** de cocher ;
- **Horodatage et conservation de la preuve** du consentement (art. 7.1) : date,
  heure, version des documents acceptés. Aucune table ne porte cette trace
  aujourd'hui — `users` ne contient aucun champ de consentement. **À créer.**

⚖️ **Cas particulier — l'article 8 des CGV.** Les CGV en ligne prévoient que le
client « renonce expressément » à son droit de rétractation et que « la case
correspondante doit être cochée lors de la souscription ». Cette case
conditionne la renonciation : **si elle n'existe pas dans le formulaire, la
renonciation est inopposable**, et un client personne physique conserverait
14 jours de rétractation (art. L221-18 C. consommation). Je n'ai pas pu vérifier
le formulaire (site en entracte). À vérifier avant ouverture, ou à retirer des
CGV.

Je signale au passage une incohérence entre les deux jeux de CGV : celles en
ligne (01/05) traitent le cas du consommateur ; celles du 06/08 (art. 11) posent
qu'aucun droit de rétractation ne s'applique, le service étant B2B. **La seconde
position n'est tenable que si l'inscription est effectivement fermée aux
personnes physiques agissant hors activité professionnelle** — ce qui suppose de
le contrôler à l'inscription, et pas seulement de l'écrire.

---

## 3. LISTE DE CONTRÔLE DU PARCOURS CLIENT

Chaque ligne est **VÉRIFIÉE** avec sa preuve, **MANQUANTE**, ou **NON VÉRIFIABLE**
par moi — avec, dans ce dernier cas, qui peut le faire.

### 3.1 Pages légales et information

| # | Point de contrôle | État | Preuve / action |
|---|---|---|---|
| 1 | Mentions légales conformes LCEN rédigées | ✅ VÉRIFIÉ | `pages_legales_2026-08-06.md` §1 — éditeur, SIREN, RNE, directeur de publication, hébergeur complet |
| 2 | Mentions légales **publiées** | ❌ **MANQUANT** | `digital-humans.fr` sert l'entracte ; `/privacy` renvoie l'entracte. Aucune page légale n'est accessible |
| 3 | Version en ligne exempte de placeholders | ❌ **MANQUANT** | Le contenu déployé (01/05) porte `SIRET : [À COMPLÉTER]` et `Adresse du siège : [À COMPLÉTER]`, **en FR et en EN** |
| 4 | CGV publiées | ❌ MANQUANT | Idem — inaccessibles |
| 5 | Politique de confidentialité publiée | ❌ MANQUANT | Idem |
| 6 | Politique exempte d'affirmations fausses | ❌ **MANQUANT** | §2.3 — coffre à secrets, sauvegardes chiffrées, ZDR |
| 7 | Liste des sous-traitants complète et exacte | ⚠️ À CORRIGER | Version 06/08 : **OpenAI omis** ; Stripe qualifié « Inc., États-Unis » alors que la version en ligne retient « Stripe Payments Europe Ltd., Irlande ». Trancher et harmoniser |
| 8 | Identité de l'éditeur cohérente entre les sites | ❌ **MANQUANT** | Trois dénominations : « Sam Hatit » (site), « Aïssam Hatit / Digital-Humans » (identité officielle), « SH Conseil » (pied de deos.cloud). Une seule est exacte |
| 9 | Adresse de contact cohérente | ⚠️ À CORRIGER | `hello@` (site) vs `contact@` et `privacy@` (version 06/08) |
| 10 | Bandeau cookies | ⚠️ NON VÉRIFIABLE | Aucun bandeau constaté, mais le site est en entracte. Si seuls des cookies strictement nécessaires sont déposés, aucun bandeau n'est requis — **à confirmer par un relevé réel après réouverture** |

> **Sur la décision DEC-2026-0806-19** (« pages légales prêtes à publier, zéro
> champ à compléter ») : elle est exacte **pour le document du 06/08**, et
> trompeuse si on la lit comme un état du site. Le site sert toujours l'ancienne
> version, avec ses placeholders. **Prêt à publier n'est pas publié** — et c'est
> l'état publié qui engage.

### 3.2 Inscription et compte

| # | Point de contrôle | État | Preuve / action |
|---|---|---|---|
| 11 | Case CGV, non pré-cochée | ⚠️ NON VÉRIFIABLE | Formulaire inaccessible (entracte). **Delivery** peut le confirmer sur l'environnement de recette. Libellé fourni §2.5 |
| 12 | Case politique de confidentialité, distincte | ⚠️ NON VÉRIFIABLE | Idem |
| 13 | Case de renonciation à rétractation (CGV art. 8) | ⚠️ NON VÉRIFIABLE | Idem — **conditionne l'opposabilité de la clause** |
| 14 | Preuve du consentement horodatée | ❌ **MANQUANT** | Schéma `users` vérifié : aucun champ de consentement ni de version acceptée. À créer |
| 15 | Double opt-in newsletter | ⚠️ NON VÉRIFIABLE | Brique existante (N8N `Lead Capture - Website`, courriel de vérification) |
| 16 | Mot de passe stocké haché | ✅ VÉRIFIÉ | `users.hashed_password` ; JWT HS256, expiration 30 min |
| 17 | Information art. 13 au moment de la collecte | ❌ MANQUANT | Dépend des lignes 2 à 6 |

### 3.3 Concierge Sophie (visiteurs)

| # | Point de contrôle | État | Preuve / action |
|---|---|---|---|
| 18 | Mention IA en en-tête du widget (AI Act art. 50.1) | ✅ PRÊTE, non déployée | Libellés arbitrés le 06/08 (`mentions_ia.md`). **Bloquant réouverture** tant que non intégrée |
| 19 | Minimisation des données visiteurs | ✅ VÉRIFIÉ, bonne pratique | `chat_logs` stocke `ip_hash` (haché) et non l'IP en clair |
| 20 | Finalité **prospection** déclarée | ❌ **MANQUANT** | `chat_logs.email_collected` et `intent` / `next_action` : les conversations alimentent le commercial. Or la politique affirme qu'« aucune donnée n'est cédée à des tiers à des fins commerciales » sans jamais déclarer la prospection comme finalité. **Traitement à part entière, à déclarer et à fonder** (intérêt légitime, avec balance des intérêts documentée) |
| 21 | Information préalable du visiteur | ❌ MANQUANT | Aucune mention avant la conversation |
| 22 | Durée de conservation appliquée | ⚠️ NON VÉRIFIABLE | 12 mois annoncés ; aucune purge automatique constatable. `deos_ro` n'a pas accès à `chat_logs` |

### 3.4 Traitement, journalisation, droits

| # | Point de contrôle | État | Preuve / action |
|---|---|---|---|
| 23 | Isolement des contextes clients | ❌ **NON PROUVÉ** | §1.3 — bloquant |
| 24 | RAG commun sans donnée client | ✅ VÉRIFIÉ | §1.1 |
| 25 | Non-entraînement garanti contractuellement | ✅ VÉRIFIÉ | Anthropic Commercial Terms §B ; OpenAI API. **Sous réserve du feedback** (§2.3) |
| 26 | Chiffrement au repos des identifiants | ❌ **NON CONFORME** | §2.1 |
| 27 | Journaux — données personnelles | ⚠️ À DOCUMENTER | `audit_logs` conserve `ip_address` **en clair** et `user_agent`. Durée non définie |
| 28 | Purge des journaux sur demande d'effacement | ❌ MANQUANT | Aucun mécanisme documenté. Les sauvegardes non plus |
| 29 | Traçabilité des accès aux secrets | ❌ MANQUANT | Documentation : « les actions secrets ne sont pas tracées » |
| 30 | Parcours d'exercice des droits | ⚠️ À DOCUMENTER | Adresse de contact annoncée ; aucune procédure ni délai internes, aucun responsable désigné |
| 31 | Suppression à la résiliation (30 j) | ⚠️ NON VÉRIFIABLE | Annoncée aux CGV art. 10 ; aucune automatisation constatable |
| 32 | Registre des traitements (art. 30) | ❌ **MANQUANT** | Aucun registre n'existe. Obligatoire dès lors que le traitement n'est pas occasionnel — c'est le cas |

### 3.5 Ce qui conditionne le GO, dans l'ordre

**Pour rouvrir en vitrine** (sans inscription) :
1. Intégrer la mention IA du widget Sophie (Delivery, ~1 h) ;
2. Publier les trois pages du 06/08, **après** avoir retiré les affirmations
   fausses de la section Sécurité et **réintégré OpenAI** aux sous-traitants ;
3. Déclarer la finalité de prospection du concierge ;
4. Harmoniser l'identité de l'éditeur.

**Pour ouvrir les inscriptions**, en plus :
5. Passer les tests d'isolement §1.4 (Delivery, ~2 h) ;
6. Chiffrer effectivement `project_credentials` et `project_environments` ;
7. Trancher le ZDR (Sam, 2 min) et aligner la politique ;
8. Poser les cases à cocher et la preuve de consentement horodatée ;
9. Afficher la mention d'import ;
10. Établir le registre des traitements.

---

## 4. LES DEUX SITES JAMAIS AUDITÉS (DEC-2026-0808-01)

Sam les juge moins à risque, « vitrines sans parcours client ni collecte ». J'ai
vérifié plutôt que supposé, comme demandé. **L'hypothèse est juste sur la
collecte, et fausse sur le risque.**

Les mentions légales sont dues au titre de la **LCEN article 6-III-1** pour tout
site édité à titre professionnel, **qu'il y ait ou non collecte de données**. Une
vitrine n'est pas dispensée. Sanction encourue : 1 an d'emprisonnement et
75 000 € d'amende (LCEN art. 6-VI-2).

### 4.1 samhatit-consulting.cloud — **NON CONFORME**

| Rubrique | Constat | Verdict |
|---|---|---|
| Mentions légales | Un lien « Mentions légales » figure en pied de page — son `href` vaut **`#`**. Il ne mène nulle part. `/mentions-legales` renvoie **HTTP 404** | **NON CONFORME** |
| Confidentialité | Lien présent, `href` = **`#`** également | **NON CONFORME** |
| Collecte | CTA « Réserver 30 minutes » (×2) et adresse de contact. **Il y a donc bien un début de parcours** : une prise de rendez-vous collecte nom, adresse et créneau | À DOCUMENTER |
| Cookies | Aucun bandeau constaté ; à confirmer par relevé | À VÉRIFIER |
| Mention IA | Aucun agent exposé — art. 50 non applicable | SANS OBJET |

**Le cas est plus défavorable qu'une simple absence : le site *affiche* des liens
légaux qui ne mènent nulle part.** Un visiteur — ou un contrôleur — constate une
apparence de conformité démentie au premier clic.

Le CTA de prise de rendez-vous contredit par ailleurs le postulat « sans
collecte ». Si la réservation passe par Calendly (le workflow N8N
`Meeting Booking - Calendly` existe), alors Calendly est un **sous-traitant** à
déclarer, et une information art. 13 est due au moment de la réservation.

### 4.2 deos.cloud — **NON CONFORME**

| Rubrique | Constat | Verdict |
|---|---|---|
| Mentions légales | **Aucune, et aucun lien.** Le pied de page se limite à « © MMXXVI · DEOS Une solution SH Conseil ↗ contact@deos.cloud » | **NON CONFORME** |
| Confidentialité | Aucune | **NON CONFORME** |
| Collecte | CTA « Demander un accès » (×2) pointant vers l'ancre `#contact` ; pas de formulaire, seulement une adresse | Risque faible |
| Cookies | Aucun bandeau constaté | À VÉRIFIER |
| Mention IA | Aucun agent exposé | SANS OBJET |

**Incohérence d'entité — à traiter en priorité.** Le pied de page attribue DEOS à
**« SH Conseil »**. C'est une **quatrième** dénomination, qui ne correspond à
aucune entité juridique documentée : l'identité officielle (synthèse du Guichet
Unique du 19/05/2026) est **Aïssam Hatit, entrepreneur individuel**, nom
commercial **Digital-Humans**, SIREN 343 172 490. « SH Conseil » n'apparaît nulle
part dans ce dossier.

Trois sites, trois façons de nommer l'éditeur, aucune conforme :

| Site | Éditeur affiché | Exact ? |
|---|---|---|
| digital-humans.fr (déployé) | « Sam Hatit », SIRET `[À COMPLÉTER]` | Non — prénom d'usage, SIRET manquant |
| samhatit-consulting.cloud | Aucun (lien mort) | Non |
| deos.cloud | « SH Conseil » | Non — entité non documentée |

⚖️ **Si « SH Conseil » désigne une entité réelle et distincte, il faut le dire :
cela changerait le responsable de traitement, les mentions légales et le
cocontractant des CGV.** Si c'est un nom d'usage sans existence juridique, il
doit disparaître des trois sites. Point à trancher par Sam avant toute
publication ; en cas de doute, un avocat.

### 4.3 Correctif proposé

La correction est légère : **une même page de mentions légales, dérivée du
gabarit du 06/08**, adaptée par site (nom de domaine, hébergeur, contact) et
réellement liée. Compter 30 minutes par site. À défaut de politique de
confidentialité complète, une section courte suffit pour une vitrine sans
collecte — mais elle devient obligatoire pour samhatit-consulting.cloud dès lors
qu'une prise de rendez-vous est proposée.

---

## 5. CE QUI DOIT PASSER PAR UN AVOCAT ⚖️

Je prépare une mise en conformité ; je ne délivre pas de conseil juridique.
Doivent être validés avant tout engagement :

1. **La clause de limitation de responsabilité** (CGV art. 6). Plafonner au
   montant des 12 derniers mois est usuel, mais dans un contexte où la plateforme
   déploie du code dans l'org de production du client, sa portée réelle mérite un
   examen ;
2. **Le DPA client**, qui doit refléter exactement la chaîne : client =
   responsable de traitement, Digital·Humans = sous-traitant, Anthropic et OpenAI
   = sous-traitants ultérieurs. C'est l'enjeu central avant la première vente ;
3. **L'identité de l'entité éditrice** — « SH Conseil » (§4.2) ;
4. **La position sur l'exemption éditoriale de l'article 50(4)** de l'AI Act ;
5. **Les transferts hors UE** vers Anthropic et OpenAI, et les garanties
   invoquées (CCT, cadre transatlantique) ;
6. **La renonciation au droit de rétractation** et la fermeture effective de
   l'offre aux non-professionnels (§2.5).

---

## 6. CE QUE JE N'AI PAS PU VÉRIFIER, ET QUI LE PEUT

Par honnêteté sur mes limites, et pour que personne n'attende de moi ce que je ne
peux pas produire :

| Question | Pourquoi je ne peux pas | Qui peut |
|---|---|---|
| Code de `rag_service.py`, bornage des requêtes | Source non montée dans le conteneur du comité ; `/opt/digital-humans/` vide ici | **Delivery** |
| Contenu réel de ChromaDB | Aucun accès à la base vectorielle | **Delivery** (test T1) |
| `collection_name` unique par projet | `deos_ro` n'a de droits que sur 10 vues `v_deos_*` | **Delivery** (test T2) |
| Formulaire d'inscription, cases à cocher | Site en entracte | **Delivery**, en recette |
| Bandeau et dépôt réel de cookies | Idem | **Delivery**, relevé navigateur |
| Existence d'un accord ZDR Anthropic | Console fournisseur, hors de ma portée | **Sam**, 2 min (§2.4) |
| Nature juridique de « SH Conseil » | Aucune source au dossier | **Sam** |
| Chiffrement des sauvegardes | Aucun accès à l'infrastructure | **Delivery** |

**Un mot sur le dispositif.** Mon curseur « Écrire en base » est réglé sur
*Conseille*, et « Agir sur la production » sur *Observe*. Aucun blocage du
garde-fou n'a été rencontré pendant cette ronde : tout ce qui précède a été
obtenu en lecture seule, dans mon périmètre. Les tests §1.4 sortent en revanche
de ce périmètre — ils demandent un accès au code et au serveur. **Je ne les
contourne pas, je les délègue nommément à la Delivery.**

---

## 7. SOURCES

**Textes**
- [RGPD — Règlement (UE) 2016/679](https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32016R0679) — art. 4.11, 6.1.b, 7, 13, 14, 30, 32, 33, 34
- [LCEN — Loi n° 2004-575 du 21 juin 2004](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000801164/) — art. 6-III-1, 6-VI-2
- [AI Act — Règlement (UE) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng) — art. 50
- [Code de la consommation, art. L221-18](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032226843) — rétractation

**Autorités**
- [CNIL — Information des personnes et transparence](https://www.cnil.fr/fr/conformite-rgpd-information-des-personnes-et-transparence)
- [CNIL — Sécurité : chiffrement](https://www.cnil.fr/fr/securite-chiffrer-garantir-lintegrite-ou-signer)
- [CNIL — Le registre des activités de traitement](https://www.cnil.fr/fr/RGPD-le-registre-des-activites-de-traitement)

**Fournisseurs — consultés le 08/08/2026**
- [Anthropic — Commercial Terms of Service, §B](https://www.anthropic.com/legal/commercial-terms) : « Anthropic may not train models on Customer Content from Services »
- [Anthropic — Is my data used for model training ?](https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training) : non par défaut ; exception du feedback explicite
- [Anthropic — How long do you store my organization's data ?](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data) : 30 jours ; 2 ans / 7 ans en cas de violation
- [Anthropic — Zero data retention](https://docs.anthropic.com/en/docs/build-with-claude/zero-data-retention) : soumis à approbation, par organisation
- [OpenAI — Data controls in the OpenAI platform](https://developers.openai.com/api/docs/guides/your-data) : pas d'entraînement sur les données API, rétention 30 jours

**Preuves techniques internes** (relevées le 08/08/2026)
- Production PostgreSQL, rôle `deos_ro` : `pg_class.relrowsecurity` (46 tables, RLS
  désactivée partout), `pg_policies` (0 ligne), `pg_attribute` (schémas),
  `information_schema.table_privileges` (10 vues)
- `/backlog/refonte/sections/security.html` — inventaire des secrets, backlog de
  durcissement, « clair en DB »
- `/backlog/refonte/sections/rag.html` — 91 866 chunks, 6 collections
- `/backlog/RAG_V2_JOURNAL.md` — origine du corpus, bascule v2 du 14/07
- `/backlog/architecture.md` — route `documents → P3 RAG isolation`, non-goals
- `/backlog/marketing-site/scripts/dh-mod28-legal-content.py` — contenu légal déployé
- `/workspace/config/legal/pages_legales_2026-08-06.md`, `mentions_ia.md`,
  `identite_legale.md`
- Relevés en ligne du 08/08 : `digital-humans.fr` (entracte),
  `samhatit-consulting.cloud` (liens légaux `href="#"`, `/mentions-legales` → 404),
  `deos.cloud` (aucune page légale)

---

*Rapport produit le 2026-08-08 par le Directeur Juridique Digital·Humans.*
*Il prépare une mise en conformité et ne constitue pas un conseil juridique.*
