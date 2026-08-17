-- LOT-01 — table tasks, statuts etendus, contrainte de blocage
-- Refonte DEOS Governance V2 · SPEC.md §1.1 et §1.2 · 17 aout 2026
--
-- QUOI. Cree la table tasks, etend le vocabulaire de statuts de decisions, et pose
-- en base la contrainte qui rend l'invariant I4 incontournable.
--
-- POURQUOI. Le comite savait enregistrer des decisions, pas les executer. Une
-- decision accordee restait un texte : rien ne portait le critere de fin, l'owner,
-- la preuve ni la reprise. La table tasks est l'unite d'execution qui manquait.
--
-- CE QUE CA REMPLACE. Le suivi d'execution se faisait dans le texte libre des
-- decisions et dans PageSuivi.md, regeneres a la main. Un blocage s'y ecrivait en
-- prose, sans champ obligatoire — donc sans reprise possible. Ce mode disparait :
-- a partir d'ici, un blocage sans suite est refuse par la base elle-meme.
--
-- IDEMPOTENCE. Le schema reel a derive de db/init/01_schema.sql (la colonne
-- decisions.demo est ecrite par bin/deos-decisions mais absente du fichier d'init).
-- Cette migration ne suppose donc aucun etat exact : elle est rejouable sans erreur
-- et decouvre les contraintes existantes au lieu de les nommer en dur.

BEGIN;

-- ---------------------------------------------------------------------------
-- 1. Table tasks — SPEC.md §1.2
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS tasks (
  id              text PRIMARY KEY,          -- TASK-2026-0817-01
  decision_id     text NOT NULL REFERENCES decisions(id),
  titre           text NOT NULL,
  critere_fin     text NOT NULL,             -- verifiable, pas declaratif
  owner           text NOT NULL,
  echeance        date,
  statut          text NOT NULL DEFAULT 'a_faire',
  attempt_count   integer NOT NULL DEFAULT 0,
  last_error      text,
  retry_at        timestamptz,
  blocker         text,
  next_action     text,
  next_owner      text,
  budget_usd      numeric(8,4) NOT NULL DEFAULT 0.50,
  consomme_usd    numeric(8,4) NOT NULL DEFAULT 0,
  evidence_type   text,                      -- commit | fichier | base | url
  evidence_ref    text,
  cree_le         timestamptz NOT NULL DEFAULT now(),
  cree_par        text NOT NULL,
  maj_le          timestamptz NOT NULL DEFAULT now()
);

COMMENT ON TABLE tasks IS
  'Unite d''execution rattachee a une decision. La decision est le contenant, '
  'la tache est ce qui se fait, se bloque, echoue et se prouve.';

COMMENT ON COLUMN tasks.critere_fin IS
  'Condition de fin VERIFIABLE, pas declarative. "le hook refuse un DELETE" et non '
  '"le hook est ameliore" : sans cela, la cloture redevient une affirmation.';
COMMENT ON COLUMN tasks.blocker IS
  'Obstacle EXTERNE constate. Rempli obligatoirement quand statut = blocked (I4).';
COMMENT ON COLUMN tasks.next_action IS
  'Action suivante concrete. C''est ce champ qui empeche une difficulte de terminer '
  'une session (I5) : une tache bloquee porte toujours ce qui doit arriver ensuite.';
COMMENT ON COLUMN tasks.next_owner IS
  'Qui porte next_action. Souvent une AUTRE fonction que owner : un agent prive de '
  'ses moyens ne peut pas se debloquer lui-meme (SPEC §3.1).';
COMMENT ON COLUMN tasks.attempt_count IS
  'Nombre de tentatives. Pilote le budget d''echec : 1re reprise directe, 2e exige '
  'de nommer la cause, 3e passe la main au Chief of Staff (SPEC §2.2).';
COMMENT ON COLUMN tasks.retry_at IS
  'Date de remise en file. Une tache failed dont retry_at est depasse revient '
  'automatiquement dans la file — c''est ce qui distingue un moteur d''execution '
  'd''un ordonnanceur (SPEC §2.3).';
COMMENT ON COLUMN tasks.budget_usd IS
  'Budget de la tache. Depassement tolere 10 %, au-dela escalade direction -> CEO '
  '-> Sam (SPEC §1.3).';
COMMENT ON COLUMN tasks.evidence_type IS
  'commit | fichier | base | url. Sans preuve, pas de cloture : un indicateur qui '
  'se calcule sur une donnee que l''evalue ecrit lui-meme mesure la declaration, '
  'pas le fait (I3).';

-- ---------------------------------------------------------------------------
-- 2. Contrainte blocage_avec_suite — invariant I4 rendu incontournable
-- ---------------------------------------------------------------------------
--
-- POURQUOI EN BASE ET PAS DANS LE CODE. Le registre est ecrit par plusieurs outils
-- (bin/deos-tasks, la boucle d'execution, psql a la main lors d'un incident). Un
-- controle applicatif n'est vrai que pour le chemin qui le traverse. Une tache
-- bloquee sans action suivante est invisible : personne ne la reprend, elle ne
-- reapparait dans aucune file, et elle ne repart jamais.

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint
    WHERE conname = 'blocage_avec_suite' AND conrelid = 'tasks'::regclass
  ) THEN
    ALTER TABLE tasks ADD CONSTRAINT blocage_avec_suite CHECK (
      statut NOT IN ('blocked','failed')
      OR (blocker IS NOT NULL AND next_action IS NOT NULL AND next_owner IS NOT NULL)
    );
  END IF;
END $$;

-- maj_le ne se met pas a jour tout seul. Sans ce declencheur le champ ment des la
-- premiere modification, et toute file « qu'est-ce qui a bouge depuis hier » (ronde
-- V2, question 2) devient fausse. Meme mecanique que trg_decisions_touch, mais la
-- fonction existante ecrit updated_at : le nom de colonne differe ici.
CREATE OR REPLACE FUNCTION touch_maj_le() RETURNS trigger AS $$
BEGIN NEW.maj_le := now(); RETURN NEW; END; $$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_tasks_touch ON tasks;
CREATE TRIGGER trg_tasks_touch BEFORE UPDATE ON tasks
  FOR EACH ROW EXECUTE FUNCTION touch_maj_le();

-- Index poses pour les acces que LOT-02 et LOT-04 feront a chaque tour :
--   --dues (retry_at depasse), file par owner, file par statut, taches d'une decision.
CREATE INDEX IF NOT EXISTS idx_tasks_retry_at   ON tasks (retry_at) WHERE retry_at IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_tasks_owner      ON tasks (owner);
CREATE INDEX IF NOT EXISTS idx_tasks_statut     ON tasks (statut);
CREATE INDEX IF NOT EXISTS idx_tasks_decision   ON tasks (decision_id);

-- ---------------------------------------------------------------------------
-- 3. Statuts etendus de decisions — SPEC.md §1.1
-- ---------------------------------------------------------------------------
--
-- La contrainte d'origine etait declaree en ligne dans db/init/01_schema.sql, donc
-- nommee automatiquement par PostgreSQL. On ne la nomme pas en dur : on retrouve
-- toute contrainte CHECK de decisions qui enumere les anciens statuts, quel que soit
-- son nom, et on la remplace. clos_avec_preuve n'est pas concernee : elle ne
-- mentionne pas attente_sam et reste en place.

DO $$
DECLARE c record;
BEGIN
  FOR c IN
    SELECT conname FROM pg_constraint
    WHERE conrelid = 'decisions'::regclass
      AND contype = 'c'
      AND pg_get_constraintdef(oid) LIKE '%attente_sam%'
  LOOP
    EXECUTE format('ALTER TABLE decisions DROP CONSTRAINT %I', c.conname);
  END LOOP;
END $$;

ALTER TABLE decisions ADD CONSTRAINT decisions_statut_check CHECK (
  statut IN (
    'attente_sam',      -- question ouverte adressee a Sam
    'accordee',         -- arbitree ; le CoS doit en tirer une tache sous 24 h
    'en_execution',     -- au moins une tache en cours
    'propose_cloture',  -- NOUVEAU : l'agent a fini et fourni sa preuve, en attente
    'blocked',          -- NOUVEAU : obstacle externe, l'action n'a pas pu etre tentee
    'failed',           -- NOUVEAU : l'action a ete tentee et a echoue
    'needs_decision',   -- NOUVEAU : attend un arbitrage humain
    'clos',             -- valide, avec preuve et constat de relecture
    'refusee',          -- ecartee, avec motif — c'est un jugement
    'obsolete'          -- NOUVEAU : n'a plus d'objet — c'est une peremption
  )
);

COMMENT ON CONSTRAINT decisions_statut_check ON decisions IS
  'Dix statuts. blocked et failed sont distincts : le premier n''a pas pu etre '
  'tente, le second l''a ete. obsolete et refusee sont distincts : peremption '
  'contre jugement — marquer refusee ce qui n''a plus d''objet salit le signal.';

-- ---------------------------------------------------------------------------
-- 4. Champs de blocage sur decisions — arbitrage de Sam du 17/08
-- ---------------------------------------------------------------------------
--
-- POURQUOI. SPEC §1.1 exige blocker / next_action / owner sur une decision
-- blocked, mais ne definissait ces champs qu'en §1.2, sur tasks. Incoherence
-- reconnue par Sam le 17/08 et tranchee dans ce sens : les colonnes vont sur
-- decisions.
--
-- LE MOTIF EST LE CAS FREQUENT, PAS LE CAS LIMITE. Une decision peut etre
-- bloquee alors qu'AUCUNE tache n'existe encore — c'est meme la situation
-- normale a la sortie du Recovery Sprint (LOT-09), qui trie une quarantaine de
-- decisions ouvertes dont beaucoup n'ont jamais produit de tache. Faire porter
-- la suite par les taches supposait qu'il y en ait une : sans ces colonnes,
-- LOT-03 ne peut pas appliquer sa propre regle.
--
-- NEXT_OWNER ET NON OWNER. SPEC §1.1 ecrit « owner », mais la contrainte de
-- §1.2 — qui fait foi, c'est elle qu'on implemente — dit next_owner. Sur
-- decisions, « owner » seul serait de surcroit ambigu avec la direction
-- porteuse. Le trio reste donc identique a celui de tasks : ce qui bloque, ce
-- qui vient ensuite, qui le porte.

ALTER TABLE decisions
  ADD COLUMN IF NOT EXISTS blocker       text,
  ADD COLUMN IF NOT EXISTS next_action   text,
  ADD COLUMN IF NOT EXISTS next_owner    text,
  ADD COLUMN IF NOT EXISTS attempt_count integer NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS last_error    text,
  ADD COLUMN IF NOT EXISTS retry_at      timestamptz;

COMMENT ON COLUMN decisions.next_owner IS
  'Qui porte next_action. Souvent une AUTRE fonction que celle qui a constate le '
  'blocage : un agent prive de ses moyens ne peut pas se debloquer lui-meme '
  '(SPEC §3.1). Meme role que tasks.next_owner.';
COMMENT ON COLUMN decisions.attempt_count IS
  'Tentatives au niveau de la decision. Une decision failed a ete tentee et a '
  'echoue, meme sans tache formalisee.';

-- Fin de la premiere transaction. Tout ce qui precede est ADDITIF : nouvelles
-- tables, nouvelles colonnes, elargissement d'un vocabulaire de statuts. Rien n'y
-- restreint l'existant, donc rien ne peut y echouer sur des donnees deja en place.
COMMIT;

-- ---------------------------------------------------------------------------
-- 5. La contrainte de blocage sur decisions — transaction separee, a dessein
-- ---------------------------------------------------------------------------
--
-- POURQUOI PAS DANS LA MEME TRANSACTION. C'est la seule etape qui RESTREINT
-- l'existant, donc la seule qui puisse echouer sur des donnees deja en base. Si
-- elle etait dans la transaction precedente, son echec annulerait aussi l'ajout
-- des colonnes blocker / next_action / next_owner — et l'operateur se verrait
-- demander de renseigner des colonnes qui n'existent pas. Impasse constatee en
-- validation le 17/08 : le conseil d'erreur etait litteralement inapplicable.
--
-- Consequence assumee : si cette transaction echoue, la migration est
-- partiellement appliquee. Ce n'est pas un etat casse — tout l'additif est en
-- place et coherent, seule la contrainte manque. Le rejeu apres correction la
-- pose, les sections precedentes etant rejouables sans effet.

BEGIN;

-- Poser la contrainte sur une table qui contient deja des lignes fautives echoue,
-- et PostgreSQL ne dit pas LESQUELLES : « is violated by some row ». Le cas se
-- presente si les sections 1-3 ont ete appliquees lors d'un passage anterieur et
-- que des decisions sont passees en blocked/failed entre-temps. On nomme donc les
-- lignes avant d'essayer.
--
-- On ne pose deliberement PAS la contrainte en NOT VALID. Ce serait tolerer
-- durablement les blocages sans suite existants — exactement ce que I4 interdit,
-- et exactement le defaut qu'on corrige. Une migration ne doit pas installer une
-- regle en s'exemptant de la faire respecter.
DO $$
DECLARE n integer; ids text;
BEGIN
  SELECT count(*), string_agg(id, ', ' ORDER BY id) INTO n, ids
    FROM decisions
   WHERE statut IN ('blocked','failed')
     AND (blocker IS NULL OR next_action IS NULL OR next_owner IS NULL);

  IF n > 0 THEN
    RAISE EXCEPTION 'LOT-01 : % decision(s) en blocked/failed sans suite : %', n, ids
      USING HINT = 'Renseigner blocker, next_action et next_owner sur ces decisions, '
                   'ou les ramener a un statut anterieur, puis rejouer la migration. '
                   'Un blocage sans action suivante est invisible : il ne repart jamais (I4).';
  END IF;
END $$;

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint
    WHERE conname = 'decisions_blocage_avec_suite' AND conrelid = 'decisions'::regclass
  ) THEN
    ALTER TABLE decisions ADD CONSTRAINT decisions_blocage_avec_suite CHECK (
      statut NOT IN ('blocked','failed')
      OR (blocker IS NOT NULL AND next_action IS NOT NULL AND next_owner IS NOT NULL)
    );
  END IF;
END $$;

COMMENT ON CONSTRAINT decisions_blocage_avec_suite ON decisions IS
  'Miroir exact de blocage_avec_suite sur tasks. I4 vaut au niveau de la '
  'decision aussi : une decision bloquee sans action suivante est invisible, '
  'personne ne la reprend, elle ne repart jamais.';

COMMIT;
