# Dossier de conformité fournisseur Hostinger — état au 11/08

**Statut :** bloqué, en attente d'un élément que je n'ai pas les moyens
d'obtenir moi-même. Ce document prépare le travail pour qu'il démarre
immédiatement dès réception.

## Ce qu'il faut retenir

- Sam a rempli le formulaire du centre de confiance Hostinger le 08/08.
  Hostinger devait envoyer un **lien d'accès** aux documents protégés — le
  lien arrive par un canal auquel je n'ai pas accès (messagerie de Sam).
- **Rien n'a été reçu ni classé à ce jour** : aucune trace du dossier dans
  `/workspace/config/legal/`, `/repo` ou `/backlog` (recherche faite ce jour,
  aucun résultat).
- Cette mission ne peut pas avancer sans que Sam transmette le lien ou les
  documents. Ce n'est pas une tâche que je peux contourner : le centre de
  confiance d'un hébergeur est nominatif et lié au compte client.
- **Ce que ça ne change pas dans l'intervalle** : la formulation actuelle de
  `pages_legales_2026-08-06.md` reste correcte sans ces documents — elle
  s'appuie sur l'accord d'hébergement public (`sauvegardes.md`), pas sur le
  centre de confiance.

## Ce qui manque, précisément

D'après DEC-2026-0808-11, six pièces sont attendues :

1. Politique de contrôle cryptographique et de chiffrement
2. Politique de sécurité de l'information
3. Standard d'amélioration du système de management de la sécurité
4. Politique de protection des mots de passe
5. Certificat ISO/IEC 27001:2022
6. Liste des sous-traitants (utile pour compléter le registre RGPD — les
   sous-traitants ultérieurs d'Hostinger ne sont pas documentés aujourd'hui)

## Ce que je ferai dès réception, sans attendre de nouvelle demande

| Pièce | Vérification à faire | Pourquoi |
| --- | --- | --- |
| Certificat ISO/IEC 27001:2022 | Numéro de certificat, périmètre couvert (data centers concernés ?), date de validité, organisme certificateur | Une certification ISO 27001 ne couvre pas toujours tous les sites d'un hébergeur — vérifier que le périmètre inclut le serveur qui nous héberge |
| Politique de chiffrement | Confirmer si elle couvre le chiffrement **au repos** sur les VPS auto-gérés (le nôtre), ou seulement les services managés d'Hostinger | Notre lecture actuelle (`sauvegardes.md`) est que la sécurité du contenu d'un VPS nous incombe entièrement — à confronter à ce que dit ce document |
| Liste des sous-traitants | Croiser avec le registre des traitements en construction (point #32 de `conformite_donnees_2026-08-08.md`, aujourd'hui MANQUANT) | Un sous-traitant ultérieur non déclaré est un manquement RGPD art. 28 |
| Politique de sécurité de l'information / mots de passe | Aucune action de notre côté attendue — à archiver comme preuve si un client ou un audit le demande | Dossier de preuve, pas une obligation qui nous incombe directement |

## Ce qui manque et qui dépend de Sam

**Seule action requise :** transmettre le lien reçu d'Hostinger, ou les
documents une fois téléchargés. Cinq minutes de sa part suffisent à débloquer
les six vérifications ci-dessus.
