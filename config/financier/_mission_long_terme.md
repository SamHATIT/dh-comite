PRÉCISION DE SAM — 09/08. À intégrer à ta projection, c'est ce qu'il attend
vraiment.

« Qu'il inclue aussi les gains sur le comité si le test de mardi se passe
bien. C'est ça que je veux dire : je veux voir le gain sur le LONG TERME. »

── CE QUI SE JOUE MARDI ──

Un serveur GPU sera testé (Packet.ai, RTX PRO 6000 96 Go, forfait 299 $/mois).
Deux modèles ouverts y seront évalués sur nos tâches réelles :
Gemma 4 31B et Qwen 3.6 27B, en quantification 8 bits.

**Ce qui peut basculer en local, si le test passe :**
- le comité hebdomadaire
- les rondes quotidiennes des six directions
- le brief quotidien
- les agents du BUILD — Diego, Raj, Zara, Elena — autorisés par l'avis
  juridique du 09/08 : ils ne voient que des métadonnées de structure

**Ce qui reste sur API, sans discussion** (arbitrage de Sam) : Sophie, Olivia,
Emma, Marcus, Jordan, Aisha. Ils sont exposés aux données clients.

── CE QUE TU DOIS PRODUIRE ──

**1. LA VENTILATION ACTUELLE.** À partir de `bin/couts.py 14`, sépare ce qui
peut basculer de ce qui ne peut pas. C'est le chiffre de départ, et il doit
être exact — pas une estimation.

**2. LE GAIN SUR DOUZE MOIS, en trois scénarios :**

- **Le test échoue** — tout reste sur API. Quelle facture sur 12 mois au
  rythme actuel, et à volume croissant ?
- **Le test passe partiellement** — seul le comité et les rondes basculent, le
  BUILD reste sur API.
- **Le test passe entièrement** — comité, rondes, brief et BUILD en local.

Pour chacun : coût cumulé sur 12 mois, économie contre le scénario de
référence, et **le mois où le forfait devient rentable**.

**3. LE POINT QUI COMPTE VRAIMENT — l'effet du volume.**

L'API croît avec l'usage. Le forfait ne bouge pas. Or l'usage VA croître :
plus d'exécutions BUILD, plus de directions, plus de contenu.

**Modélise ça.** Si le volume double sur douze mois, que devient l'écart ?
C'est là que se voit le gain de long terme, pas dans la comparaison du premier
mois.

**4. UN GRAPHIQUE QUI MONTRE LA DIVERGENCE.** Deux courbes de coût cumulé sur
douze mois — API contre forfait — avec le point de croisement marqué. C'est LE
graphique de ta position.

**5. CE QUE LE GAIN FINANCE.** Une économie n'a de sens que rapportée à ce
qu'elle permet. Si le local libère 3 000 $ sur l'année, qu'est-ce que ça
achète ? Un mois de développement ? Une campagne ? De la marge de manœuvre
avant les premiers clients ?

── RÉSERVES À NE PAS MASQUER ──

- Le test de mardi peut échouer. **Ta projection doit le dire**, pas supposer
  le succès.
- Le serveur est en **Californie** — sans importance pour le comité, mais
  contradictoire avec notre argument de souveraineté pour des données clients.
- Faire tourner du local coûte du **temps de Sam** : installation, surveillance,
  mises à jour. Chiffre-le à 800 € le jour.

Intègre tout ça au document que tu es en train d'écrire.

═══════════════════════════════════════════════════════════════════════════
AJOUT DE SAM — 09/08 au soir. Troisième hypothèse de prix.
═══════════════════════════════════════════════════════════════════════════

« Psychologiquement, aux US, on peut aller jusqu'à 99 $. C'est un prix
habituel quand tu vois leurs abonnements : téléphone, télé, internet, etc. »

C'est une observation de terrain que ta fourchette générique 79-149 $ ne
capture pas. **Le 99 est un ancrage culturel** sur le marché américain :
téléphone, télévision, internet, logiciels s'y terminent tous par 99. Un prix
à 79 $ n'y est pas perçu comme accessible mais comme **en dessous du
standard** — ce qui peut signaler un produit moins sérieux.

**CHIFFRE UNE HYPOTHÈSE C : 99 $/mois pour le marché américain**, avec la
même méthode que A et B.

**Le point qui devrait ressortir, à vérifier** : à 99 $, le revenu perçu
serait d'environ 91 €/mois — soit **PLUS que les 79 €** de la zone euro,
alors qu'on affiche un prix qui paraît normal localement. Le désavantage de
change de 8 % que tu as identifié se retournerait en avantage.

**Traite aussi la question qu'elle soulève** : si 99 $ passe aux États-Unis,
faut-il réexaminer le prix en zone euro ? Un écart de 12 € entre marchés se
justifie-t-il, et se voit-il quand un prospect compare les pages ?

**Et pour le Royaume-Uni** : l'équivalent culturel du 99 $ est-il 79 £, 89 £
ou 99 £ ? Si tu n'as pas de source, dis-le plutôt que de supposer.

Rappel : le prix reste une proposition. DH-CRO-002 — Sam tranche.
