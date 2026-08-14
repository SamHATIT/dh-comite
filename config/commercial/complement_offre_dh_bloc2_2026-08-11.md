# Complément à intégrer dans offre_dh.md — DEC-2026-0805-01 (rédigé le 11/08)

**Statut : rédigé, PAS ENCORE FUSIONNÉ dans `/workspace/config/offre_dh.md`.**
L'écriture directe dans ce fichier a été refusée par la permission de l'hôte pendant
cette ronde. Contenu prêt à copier tel quel dès qu'un CoS, Sam, ou une prochaine ronde
avec l'autorisation d'écriture pourra le faire. Rien de ce qui suit n'est encore
"canonique" tant que ce n'est pas dans offre_dh.md.

---

## Complément DEC-2026-0805-01 (11/08) — segment grands comptes et plafonds Bloc II

Le 04/08 le Commercial avait demandé d'intégrer ici le segment grands comptes et les
plafonds d'usage Bloc II. Deux études sont venues depuis (grands comptes du 08/08,
revue tarifaire Financier/Commercial du 09/08) et changent ce qui peut être écrit sans
inventer :

### Segment grands comptes — mode conseil (DEOS)

DEOS (gouvernance des délégations IA, vendu au comité de direction, pas à l'IT) reste
**sur devis**, sous le tier Enterprise. Grille à l'étude : 1 200 €/direction gouvernée/mois,
minimum 3 directions (43 200 à 86 400 €/an) — **non arbitrée**, en attente de Sam depuis le
09/08 (DEC-2026-0809-02, attente_sam). Aucun prix DEOS ne doit être prononcé par le
Commercial avant cet arbitrage (DH-CRO-002).

**« Mode supervision » exclu du périmètre.** La demande du 05/08 envisageait aussi un mode
supervision grands comptes. L'étude du 08/08 (`config/commercial/deos_grands_comptes_2026-08-08.md`
§4.6) a constaté qu'il rouvrirait la frontière « Team s'arrête avant la production », refermée
trois jours plus tôt par une règle absolue : DEC-2026-0808-07, aucun déploiement en
production. DEOS n'en a structurellement pas besoin (il gouverne des décisions, il ne déploie
rien chez le client). Le mode supervision ne doit apparaître dans aucun document commercial.

### Plafonds d'usage Bloc II

- **Free : 20 échanges** — plafond technique déjà en place (`HISTORY_TURNS_MAX`,
  `sophie_concierge_service.py`, vérifié 09/08). Recommandation non tranchée de la revue du
  09/08 : borner dans le temps (ex. 14 jours) plutôt que par session, la vitrine n'ayant pas
  besoin de permanence — **à décider par Sam**.
- **Pro : 2 SDS/mois inclus**, pas 3 — la demande du 04/08 portait le chiffre 3, corrigé ici à
  la valeur réellement observée (`config/commercial/offre_revue_2026-08-09.md` §2.4, §4.2). La
  même revue déconseille un forfait fixe (coût réel d'un SDS variant de 4,74 à 21,79 € selon le
  projet, ×6,8 d'écart) et recommande un système de crédits — **non arbitré**, question posée à
  Sam séparément ce jour (DEC-2026-0811-09).
- **Team : à fixer.** Aucune limite chiffrée n'existe ni n'a été recommandée à ce stade — la
  revue du 09/08 signale seulement l'absence de coût jetons instrumenté pour Team comme réserve
  à instruire si Sam le demande.

*Ce qui n'est pas encore dans offre_dh.md reste au conditionnel ici : la grille DEOS et le
modèle de quota Pro sont des options documentées, pas des prix ou plafonds engagés.*
