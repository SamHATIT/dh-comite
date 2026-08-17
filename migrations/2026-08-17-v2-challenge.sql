-- LOT-11 — tables challenges, avis et propositions
-- Refonte DEOS Governance V2 · SPEC.md §4bis · 17 aout 2026
--
-- QUOI. Cree les trois tables sur lesquelles reposent les mecanismes de challenge :
-- challenges (obligation hebdomadaire et contradictions du Strategic Challenge),
-- avis (boucle d'intelligence collective) et propositions (Strategic Yield sur ses
-- quatre etapes, avec rappel et mise en veille).
--
-- AJOUT AU CONTRAT DU LOT, ET POURQUOI. LOT-11 ne liste que bin/challenge.py,
-- config/activation.yaml et docs/CHALLENGE.md. Mais son §4 demande « un champ
-- rappele_le et un statut en_veille SUR LA PROPOSITION », et ses criteres 4 et 5
-- exigent de suivre une proposition dans le temps puis de la rappeler au bout de
-- 14 jours. Rien de cela ne survit a la fin d'un processus. Sans table, le garde-fou
-- redevient une consigne et le Strategic Yield un calcul sur rien — c'est-a-dire
-- exactement ce que la refonte supprime. La migration est un fichier NEUF : elle ne
-- partage aucun fichier avec LOT-10, l'autre lot de la vague D (bin/health.py).
--
-- POURQUOI PAS DANS decisions. Deux raisons, aucune n'est de gout.
--   1. Une proposition n'est PAS un point bloquant (LOT-11 §4 : « rien n'attend
--      derriere »). La ranger en attente_sam la ferait entrer dans la file
--      d'arbitrage. Le 10/08, huit fausses entrees attente_sam ont ete reclassees
--      pour ce motif exact : une file d'arbitrage qui se remplit de non-bloquants
--      cesse d'etre lue, et les vraies questions se perdent avec.
--   2. Le vocabulaire de decisions.statut appartient a LOT-03. Y ajouter en_veille
--      modifierait un objet partage pour un besoin qui n'est pas le sien.
--
-- CE QUE CA REMPLACE. Rien : ces objets n'existaient pas. La dimension CHALLENGE du
-- mandat (SPEC §4bis) n'avait aucun support — une hypothese formulee en ronde vivait
-- dans le texte du compte rendu, donc nulle part.

BEGIN;

-- ---------------------------------------------------------------------------
-- 0. touch_maj_le() — creee par LOT-01, recreee ici SEULEMENT si absente
-- ---------------------------------------------------------------------------
--
-- La fonction appartient a la migration de LOT-01. On ne la redefinit pas : deux
-- migrations qui reecrivent la meme fonction rendent le comportement dependant de
-- l'ordre d'application, et cet ordre a deja produit un defaut (voir
-- docs/APPLICATION_MIGRATIONS.md). On se contente de la creer si elle manque, pour
-- que ce fichier reste applicable seul sur une base ou LOT-01 n'est pas passe.

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_proc WHERE proname = 'touch_maj_le') THEN
    CREATE FUNCTION touch_maj_le() RETURNS trigger AS $f$
    BEGIN NEW.maj_le := now(); RETURN NEW; END; $f$ LANGUAGE plpgsql;
  END IF;
END $$;

-- ---------------------------------------------------------------------------
-- 1. challenges — l'obligation hebdomadaire et la contradiction
-- ---------------------------------------------------------------------------
--
-- DEUX NATURES DANS UNE TABLE, ET C'EST VOULU. SPEC §4bis pose deux obligations de
-- meme famille : une hypothese testable (challenge hebdomadaire) et une
-- contradiction argumentee (« une direction doit pouvoir contredire le CEO et Sam,
-- avec ses preuves et une alternative »). Dans les deux cas la regle est la meme :
-- contester ne suffit pas, il faut apporter de quoi trancher. Les separer en deux
-- tables dupliquerait le garde-fou, et un garde-fou duplique se corrige a moitie.
--
-- LE GARDE-FOU EST EN BASE, PAS SEULEMENT DANS L'OUTIL. Meme raisonnement que la
-- contrainte blocage_avec_suite de LOT-01 : le registre est ecrit par plusieurs
-- chemins — l'outil, un psql a la main pendant une ronde — c'est-a-dire exactement
-- au moment ou la discipline cede. Un controle applicatif n'est vrai que pour le
-- chemin qui le traverse.
--
-- POURQUOI btrim() ET PAS SEULEMENT NOT NULL. Une chaine vide, un espace ou un
-- tiret satisfont NOT NULL. Le champ serait rempli et l'hypothese resterait
-- intestable : on aurait mecanise la forme sans mecaniser rien.

CREATE TABLE IF NOT EXISTS challenges (
  id                   text PRIMARY KEY,        -- CHA-2026-0817-01
  direction            text NOT NULL,
  nature               text NOT NULL DEFAULT 'hypothese'
                       CHECK (nature IN ('hypothese','contradiction')),
  cycle                text NOT NULL DEFAULT 'hebdomadaire'
                       CHECK (cycle IN ('hebdomadaire','mensuel')),

  -- nature = hypothese : les trois champs exiges par SPEC §4bis
  hypothese            text,
  cout_experimentation text,
  critere_refutation   text,
  opportunite          text,                    -- 2e question, facultative

  -- nature = contradiction : qui est contredit, sur quoi, avec quelles preuves
  cible                text,                    -- ceo | sam
  sujet                text,
  preuve               text,
  alternative          text,

  -- Regime d'activation AU MOMENT DE LA SOUMISSION. Voir le commentaire de colonne :
  -- c'est ce qui rend l'essai reellement sans consequence.
  activation           text NOT NULL DEFAULT 'essai'
                       CHECK (activation IN ('actif','essai')),

  statut               text NOT NULL DEFAULT 'soumis'
                       CHECK (statut IN ('soumis','retenu','ecarte')),
  motif                text,                    -- pourquoi retenu ou ecarte
  statue_par           text,
  semaine              text NOT NULL DEFAULT to_char(now(), 'IYYY-"W"IW'),
  soumis_le            timestamptz NOT NULL DEFAULT now(),
  maj_le               timestamptz NOT NULL DEFAULT now(),

  CONSTRAINT challenge_testable CHECK (
    nature <> 'hypothese'
    OR (length(btrim(coalesce(hypothese,'')))            > 0
    AND length(btrim(coalesce(cout_experimentation,''))) > 0
    AND length(btrim(coalesce(critere_refutation,'')))   > 0)
  ),

  CONSTRAINT contradiction_argumentee CHECK (
    nature <> 'contradiction'
    OR (cible IN ('ceo','sam')
    AND length(btrim(coalesce(sujet,'')))       > 0
    AND length(btrim(coalesce(preuve,'')))      > 0
    AND length(btrim(coalesce(alternative,''))) > 0)
  )
);

COMMENT ON TABLE challenges IS
  'Dimension CHALLENGE du mandat (SPEC §4bis). Deux natures, un meme principe : '
  'contester ne suffit pas, il faut apporter de quoi trancher.';

COMMENT ON CONSTRAINT challenge_testable ON challenges IS
  'Un challenge qui ne produit pas une hypothese TESTABLE n''est pas rendu. Sans '
  'formulation refutable c''est une opinion, sans cout c''est un voeu, sans critere '
  'de refutation on ne saura jamais si elle etait fausse. Meme mecanique que '
  'blocage_avec_suite : une obligation verifiable, pas une consigne.';

COMMENT ON COLUMN challenges.activation IS
  'Regime au moment de la soumission, jamais recalcule. Un challenge rendu pendant '
  'l''essai ne doit compter dans aucun indicateur, y compris apres bascule de '
  'l''interrupteur en actif : sinon l''essai deviendrait retroactivement une note.';

COMMENT ON COLUMN challenges.semaine IS
  'Semaine ISO de soumission (2026-W34), posee par defaut pour que l''obligation '
  'HEBDOMADAIRE soit verifiable sans recalculer une date a chaque lecture.';

CREATE INDEX IF NOT EXISTS idx_challenges_direction ON challenges (direction);
CREATE INDEX IF NOT EXISTS idx_challenges_semaine   ON challenges (semaine);

-- ---------------------------------------------------------------------------
-- 2. propositions — le Strategic Yield sur ses quatre etapes
-- ---------------------------------------------------------------------------
--
--   soumise ──► acceptee ──► experimentee ──► resultat ──► impact
--      │            ▲
--      ├──► refusee │
--      └──► en_veille ──┘   (reprenable : une reponse tardive la fait repartir)
--
-- QUI JUGE : SAM (SPEC §8, tranche le 17/08). La contrainte reponse_de_sam le pose
-- en base et pas seulement dans l'outil, parce que c'est l'invariant I3 dans son cas
-- le plus direct : le CEO est mesure par le Strategic Yield, il ne peut pas ecrire
-- lui-meme l'acceptation qui le note.
--
-- LA PREUVE A PARTIR DE L'EXPERIMENTATION, meme motif. « Experimentee », « resultat »
-- et « impact » sont des faits ; sans reference verifiable ce sont des declarations
-- de la partie evaluee.

CREATE TABLE IF NOT EXISTS propositions (
  id              text PRIMARY KEY,             -- PROP-2026-0817-01
  origine         text NOT NULL DEFAULT 'ceo',
  texte           text NOT NULL,
  -- Droit du CEO de sortir du backlog : droit de PROPOSITION, pas d'initiative
  -- (SPEC §8, tranche le 17/08). La colonne rend le cas comptable ; elle
  -- n'autorise rien de plus que les autres.
  hors_backlog    boolean NOT NULL DEFAULT false,
  statut          text NOT NULL DEFAULT 'soumise'
                  CHECK (statut IN ('soumise','acceptee','refusee',
                                    'experimentee','resultat','impact','en_veille')),
  soumise_le      timestamptz NOT NULL DEFAULT now(),
  repondue_le     timestamptz,
  repondue_par    text,
  motif           text,                         -- motif du refus, ou de l'acceptation
  rappele_le      timestamptz,                  -- LOT-11 §4 : le rappel unique
  experimentee_le timestamptz,
  -- Qui a enregistre la derniere etape. Le CEO peut le faire — c'est son mandat —
  -- mais on veut pouvoir relire QUI a declare quoi : la preuve dit que le fait
  -- existe, cette colonne dit qui l'a porte au registre.
  etape_par       text,
  evidence_type   text CHECK (evidence_type IN ('commit','fichier','base','url')),
  evidence_ref    text,
  resultat        text,
  impact          text,
  maj_le          timestamptz NOT NULL DEFAULT now(),

  CONSTRAINT reponse_de_sam CHECK (
    repondue_par IS NULL OR repondue_par = 'sam'
  ),

  CONSTRAINT reponse_tracee CHECK (
    statut NOT IN ('acceptee','refusee')
    OR (repondue_par IS NOT NULL AND repondue_le IS NOT NULL)
  ),

  -- On ne met pas en veille ce qu'on n'a pas rappele. C'est la moitie de la regle
  -- qui protege le CEO : sans elle, « sans reponse » deviendrait silencieusement
  -- « sortie du calcul », et l'indicateur mesurerait la disponibilite de Sam.
  CONSTRAINT veille_apres_rappel CHECK (
    statut <> 'en_veille' OR rappele_le IS NOT NULL
  ),

  CONSTRAINT etape_prouvee CHECK (
    statut NOT IN ('experimentee','resultat','impact')
    OR (evidence_type IS NOT NULL AND length(btrim(coalesce(evidence_ref,''))) > 0)
  ),

  CONSTRAINT resultat_avant_impact CHECK (
    statut <> 'impact' OR length(btrim(coalesce(impact,''))) > 0
  )
);

COMMENT ON TABLE propositions IS
  'Propositions strategiques suivies sur quatre etapes (SPEC §4bis). Le CEO n''est '
  'PAS mesure au volume : ce sont les taux de passage d''une etape a la suivante '
  'qui font le Strategic Yield.';

COMMENT ON CONSTRAINT reponse_de_sam ON propositions IS
  'Sam juge de l''acceptation (arbitrage du 17/08). En base et pas seulement dans '
  'l''outil : I3 — un indicateur ne se calcule pas sur une donnee que la partie '
  'evaluee peut ecrire elle-meme.';

COMMENT ON COLUMN propositions.rappele_le IS
  'Date du rappel UNIQUE, apres 14 jours sans reponse. Une proposition sans reponse '
  'n''est pas un refus : sans ce champ, l''indicateur mesurerait la disponibilite de '
  'Sam plutot que la qualite des propositions.';

CREATE INDEX IF NOT EXISTS idx_propositions_statut ON propositions (statut);

-- ---------------------------------------------------------------------------
-- 3. avis — la boucle d'intelligence collective
-- ---------------------------------------------------------------------------
--
-- Une proposition du CEO est challengee par chaque direction SUR SON AXE PROPRE,
-- puis synthetisee, arbitree par Sam, executee, mesuree (LOT-11 §3). Les avis
-- vivent dans leur propre table plutot que dans un champ jsonb de propositions :
-- un avis a un auteur, une date et un garde-fou qui lui est propre.
--
-- LE GARDE-FOU DE L'AVIS. Un avis defavorable sans alternative arrete une
-- proposition sans rien mettre a la place — c'est la version collective du blocage
-- sans suite (I4). D'ou alternative_si_defavorable.
--
-- UN AVIS PAR DIRECTION ET PAR PROPOSITION. La cle primaire composee empeche
-- qu'une direction pese deux fois dans la meme synthese.

CREATE TABLE IF NOT EXISTS avis (
  proposition_id text NOT NULL REFERENCES propositions(id),
  direction      text NOT NULL,
  axe            text NOT NULL,
  verdict        text NOT NULL CHECK (verdict IN ('favorable','reserve','defavorable')),
  preuve         text NOT NULL,
  alternative    text,
  activation     text NOT NULL DEFAULT 'essai'
                 CHECK (activation IN ('actif','essai')),
  donne_le       timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (proposition_id, direction),

  CONSTRAINT alternative_si_defavorable CHECK (
    verdict <> 'defavorable' OR length(btrim(coalesce(alternative,''))) > 0
  ),
  CONSTRAINT avis_motive CHECK (length(btrim(preuve)) > 0)
);

COMMENT ON TABLE avis IS
  'Boucle d''intelligence collective : une direction, un axe, un verdict motive. '
  'Un avis defavorable sans alternative est la version collective du blocage sans '
  'suite — refuse par alternative_si_defavorable.';

-- ---------------------------------------------------------------------------
-- 4. Append-only — le meme mecanisme que sur decisions (DH-COS-002)
-- ---------------------------------------------------------------------------
--
-- POURQUOI ICI AUSSI. Le Strategic Yield se calcule sur ces lignes. Un indicateur
-- dont on peut supprimer les lignes genantes mesure ce qu'on a bien voulu garder :
-- il suffirait d'effacer trois propositions refusees pour ameliorer un taux
-- d'acceptation. C'est I3 par un autre chemin — non pas ecrire son resultat, mais
-- effacer ce qui le contredit.
--
-- Une proposition qu'on veut retirer se refuse ou se met en veille ; elle ne
-- disparait pas.

CREATE OR REPLACE FUNCTION challenge_no_delete() RETURNS trigger AS $$
BEGIN
  RAISE EXCEPTION 'table % : append-only. Un indicateur dont on peut supprimer les lignes genantes mesure ce qu''on a bien voulu garder.', TG_TABLE_NAME;
END; $$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_challenges_no_delete ON challenges;
CREATE TRIGGER trg_challenges_no_delete BEFORE DELETE ON challenges
  FOR EACH ROW EXECUTE FUNCTION challenge_no_delete();

DROP TRIGGER IF EXISTS trg_propositions_no_delete ON propositions;
CREATE TRIGGER trg_propositions_no_delete BEFORE DELETE ON propositions
  FOR EACH ROW EXECUTE FUNCTION challenge_no_delete();

DROP TRIGGER IF EXISTS trg_avis_no_delete ON avis;
CREATE TRIGGER trg_avis_no_delete BEFORE DELETE ON avis
  FOR EACH ROW EXECUTE FUNCTION challenge_no_delete();

-- maj_le ne se met pas a jour tout seul : sans declencheur, le champ ment des la
-- premiere modification (constat de LOT-01 sur tasks).
DROP TRIGGER IF EXISTS trg_challenges_touch ON challenges;
CREATE TRIGGER trg_challenges_touch BEFORE UPDATE ON challenges
  FOR EACH ROW EXECUTE FUNCTION touch_maj_le();

DROP TRIGGER IF EXISTS trg_propositions_touch ON propositions;
CREATE TRIGGER trg_propositions_touch BEFORE UPDATE ON propositions
  FOR EACH ROW EXECUTE FUNCTION touch_maj_le();

COMMIT;
