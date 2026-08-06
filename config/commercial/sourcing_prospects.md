# Sourcing de prospects — méthode et pistes
> Établi avec Sam, transmis le 06/08/2026. Ce document répond à la demande de
> « source de comptes cibles » (DEC-2026-0716-01). Il n'y a plus de source à
> demander : elle est ici. La suite est du travail de production.

## 1. Le principe : chercher la PREUVE d'un besoin, pas un profil

La prospection classique part d'un profil type (secteur, taille, code d'activité)
et espère tomber juste. On fait l'inverse : on cherche la **preuve publique et
datée** qu'une entreprise investit dans Salesforce EN CE MOMENT.

Une entreprise qui recrute un administrateur ou un développeur Salesforce
investit dans Salesforce, maintenant. C'est public, daté, vérifiable, et cent
fois mieux qualifié qu'une ligne dans une liste sectorielle.

## 2. Les sources de signaux — toutes publiques et légitimes

| Source | Signal | Ce qu'on en tire |
| --- | --- | --- |
| Offres d'emploi (France Travail en données ouvertes, sites d'entreprises, cabinets de recrutement) | Recrutement admin / dev / architecte Salesforce | Investissement en cours, taille de l'équipe, technologies citées, parfois le nom du responsable |
| Appels d'offres publics (BOAMP, TED) mentionnant Salesforce | Achat imminent, budget voté | Le signal le plus fort qui soit, avec le périmètre décrit |
| Annuaire des partenaires Salesforce | Intégrateurs et consultants | Canal PARTENARIAT, pas prospection directe — souvent le meilleur canal pour un fondateur seul |
| Communautés (Trailblazer, groupes utilisateurs francophones) | Questions posées, problèmes décrits | Le besoin exprimé par la personne elle-même |
| Publications sectorielles, communiqués, levées de fonds | Croissance, transformation annoncée | Contexte et calendrier |
| Concierge Sophie sur le site | Visiteurs ayant engagé la conversation | La seule source de leads ENTRANTS — la plus qualifiée |

## 3. Ce que le Commercial doit produire, sans demander d'arbitrage

**Étape 1 — l'ICP, à partir de ce que nous avons déjà.**
78 projets internes existent en base (`v_deos_projects`, `v_deos_executions`).
Analyse-les : quels secteurs, quelles tailles, quels cas d'usage reviennent,
quels types d'objets et d'automatisations. L'ICP se déduit de ce qu'on sait
faire, pas d'une intuition. Livrable : une fiche ICP d'une page.

**Étape 2 — un lot d'essai de 30 comptes.**
Pas 300. Trente, sourcés un par un, chacun avec :
  · le nom de l'entreprise et son secteur ;
  · LE SIGNAL, avec son URL et sa date — sans signal daté, le compte ne compte pas ;
  · le contact identifié si trouvable publiquement (fonction, pas coordonnées
    personnelles) ;
  · ce que Digital·Humans pourrait leur apporter, en une phrase ;
  · un score de qualification sur 10 selon le skill existant.

**Étape 3 — mesurer avant d'industrialiser.**
Sur ces 30, combien Sam appellerait-il volontiers ? Ce chiffre décide de la
suite. Si le rendement est bon, on industrialise avec la chaîne N8N existante.
S'il est faible, on change de source avant d'avoir perdu un mois.

## 4. Où saisir — Salesforce, décidé par Sam le 06/08

Sam a tranché : **tous les leads et prospects vont dans Salesforce**, y compris
ceux du concierge Sophie. Un lot d'essai se saisit donc en Leads Salesforce,
pas dans un fichier ni dans `deos_state`.

Ce que cela implique :
  · chaque compte sourcé devient un **Lead** dans l'org Digital·Humans ;
  · les champs personnalisés du brief CRM portent la qualification :
    `Source_DH__c` (d'où vient le signal), `Score_Qualification__c`,
    `Detail_Score__c`, `Tier_Vise__c` ;
  · la fiche s'enrichit au fil de la recherche : signal, contexte, contact,
    communication publique de l'entreprise sur le sujet ;
  · le comité y accède en lecture via l'utilisateur d'intégration.

Tant que l'org n'est pas prête à recevoir les Leads, saisis dans
`deos_state.pipeline_commercial` en respectant **exactement** les mêmes champs,
pour que la reprise soit mécanique. Ne crée pas de format parallèle.

## 5. Ce qui existe déjà et dort — à rebrancher, pas à reconstruire

Rappel de l'inventaire (`config/outils_disponibles.md`) : la chaîne complète
existe en workflows N8N désactivés — capture de leads, enrichissement,
scoring, relances. Il ne manque que la source d'entrée, qui est l'objet de ce
document, et une validation humaine avant tout envoi.

## 6. Les limites — à respecter sans exception

  · Pas d'aspiration massive de LinkedIn : contraire à ses conditions
    d'utilisation, et expose le compte de Sam.
  · Contacts professionnels publics uniquement. Aucune donnée personnelle
    au-delà de la fonction et de l'entreprise.
  · Chaque contact conserve sa SOURCE et sa DATE. Sans elles, il est
    inexploitable et juridiquement fragile.
  · Aucun envoi, aucune prise de contact sans validation de Sam. Le curseur
    commercial reste sur « conseille » avant le 01/09.
