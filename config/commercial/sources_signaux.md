# Sources de signaux publics — inventaire testé
> Établi le 06/08/2026 par test direct de chaque source. Complète
> `sourcing_prospects.md`. Chaque ligne a été appelée réellement.

## Le principe, rappelé

On ne cherche pas un profil type. On cherche la **preuve publique et datée**
qu'une organisation investit dans Salesforce **maintenant**. Sans URL ni date,
le signal ne compte pas.

## Ce qui est construit et fonctionne

| Source | Ce qu'elle donne | Débit mesuré | État |
| --- | --- | --- | --- |
| **APEC** | Recrutements Salesforce cadres, France | **731 offres, 16 signaux qualifiés** au 1er passage | **Collecteur construit**, inactif |
| **BOAMP** | Marchés publics mentionnant Salesforce | ~1 signal pertinent par an — trop rare | Collecteur construit, inactif |

## Ce qui est testé et prometteur, à construire

| Source | Ce qu'elle donne | Accès | Priorité |
| --- | --- | --- | --- |
| **France Travail** | Offres d'emploi, tout le marché français — bien plus large que l'APEC | Clé gratuite sur francetravail.io | **Haute** |
| **HelloWork** | Flux RSS d'offres par mot-clé, sans clé | Flux RSS direct | **Haute** — la plus simple |
| **Welcome to the Jungle** | Entreprises et leurs offres, API publique | API ouverte | Moyenne |
| **Salesforce Ben** | Veille sectorielle, mouvements du marché | Flux RSS | Moyenne — nourrit le Marketing |

## Ce qui demande une décision avant de s'y engager

| Source | Ce qu'elle donnerait | La réserve |
| --- | --- | --- |
| **AppExchange** | Éditeurs et intégrateurs partenaires Salesforce | Pas d'API publique. Consultation manuelle possible, automatisation à cadrer |
| **Annuaire partenaires Salesforce** | Intégrateurs français — canal **partenariat**, pas prospection | Idem |
| **Trailblazer Community** | Questions posées par des utilisateurs réels — le besoin exprimé par la personne elle-même | Contenu communautaire : consultation oui, extraction automatisée à cadrer |
| **Pages carrières des entreprises** | Le signal à sa source, sans intermédiaire | Parfaitement légitime. Demande un collecteur par entreprise — utile en ciblage fin, pas en volume |

## Ce qui est écarté, et pourquoi

**LinkedIn en automatisé.** L'aspiration est contraire aux conditions
d'utilisation, quel que soit l'outil employé — Playwright ou autre. Le risque
n'est pas judiciaire (les données publiques ne relèvent pas du pénal) mais
opérationnel : LinkedIn détecte ces schémas et **bannit le compte**. Or ce
compte porte la séquence éditoriale de lancement, les onze portraits d'agents
et la crédibilité professionnelle de Sam. Le bannissement tomberait au pire
moment.

Consulter LinkedIn soi-même et noter les entreprises reste évidemment normal.
C'est l'automatisation à grande échelle qui pose problème, pas la lecture.

**Et surtout : ce n'est pas nécessaire.** L'APEC donne le même signal,
publiquement, avec 16 résultats qualifiés au premier essai. Une entreprise qui
recrute publie presque toujours ailleurs que sur LinkedIn.

## Deux enseignements du premier passage

**Le bruit est le vrai ennemi.** Sans filtre sur l'intitulé du poste, l'APEC
remonte des commerciaux ascenseurs et le BOAMP des marchés de traiteur. Le mot
« Salesforce » apparaît quelque part sans que le sujet soit Salesforce. Le
filtre doit porter sur le **titre**, pas sur le corps.

**Les diffuseurs masquent les employeurs.** Hellowork, Meteojob, Handicap Job,
Direct Emploi apparaissent comme « entreprises » alors qu'ils diffusent pour
un tiers. Ils sont marqués « employeur à identifier » avec un score minoré :
le signal reste vrai, mais il demande une recherche.

## Le constat stratégique du premier passage

Sur 16 signaux, **9 sont des ESN** — Akkodis, Capgemini, mc2i, SYD Groupe.
Elles recrutent des consultants Salesforce parce qu'elles ont des projets à
livrer et des difficultés à embaucher. C'est précisément le problème que
Digital·Humans résout, et c'est le **canal partenariat** que l'analyse
stratégique désignait comme le plus prometteur pour un fondateur seul en
première année.

Les clients finaux existent aussi — Safran Electronics & Defense et sa
transformation CRM en est un.

**Conséquence pour le Commercial** : deux approches distinctes à préparer.
Un discours partenaire pour les ESN, un discours client pour les autres.
