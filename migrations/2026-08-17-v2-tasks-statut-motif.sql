-- LOT-02 — vocabulaire de tasks.statut, et colonne motif sur decisions
-- Refonte DEOS Governance V2 · 17 aout 2026
--
-- QUOI. Ferme le vocabulaire de tasks.statut par une contrainte CHECK, et cree la
-- colonne decisions.motif avec reprise de l'existant.
--
-- POURQUOI DEUX CHOSES DANS UNE MEME MIGRATION. Ce sont les deux seuls elements de
-- DDL en attente, et LOT-02 est le premier lot a en disposer depuis la cloture de
-- LOT-01. Les separer produirait deux fichiers appliques dans la meme minute, sans
-- rien clarifier.
--
-- CE QUE CA REMPLACE. Pour tasks.statut : rien — l'absence de contrainte etait
-- deliberee, SPEC §1.2 donnant un defaut ('a_faire') sans enumerer le vocabulaire.
-- LOT-01 avait refuse de l'inventer et laisse le point a LOT-02, qui definit les
-- commandes et donc les etats. Pour decisions.motif : remplace le rangement du
-- motif dans porte_sur, colonne dont ce n'est pas l'objet.

BEGIN;

-- ---------------------------------------------------------------------------
-- 1. Vocabulaire de tasks.statut
-- ---------------------------------------------------------------------------
--
-- Six etats, tires des commandes de LOT-02 et de la boucle de SPEC §2 :
--
--   a_faire   creee, pas commencee            (defaut, impose par SPEC §1.2)
--   en_cours  demarree                        (deos-tasks start)
--   blocked   obstacle externe, non tentee     (impose par SPEC §1.2)
--   failed    tentee, echouee                  (impose par SPEC §1.2)
--   done      finie avec preuve, en attente    (deos-tasks done)
--   valide    relue et validee                 (deos-tasks valider)
--
-- MELANGE FRANCAIS/ANGLAIS ASSUME. blocked, failed et a_faire sont imposes mot pour
-- mot par SPEC §1.2 : les traduire casserait la contrainte blocage_avec_suite, qui
-- enumere 'blocked' et 'failed'. Le reste suit le nom de la commande qui le pose.
--
-- POURQUOI done ET valide SONT DISTINCTS. Meme separation que propose_cloture et
-- clos sur les decisions : celui qui fait le travail atteste, celui qui relit
-- valide. Un seul etat terminal ferait de la tache son propre juge — I3.

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint
    WHERE conname = 'tasks_statut_check' AND conrelid = 'tasks'::regclass
  ) THEN
    ALTER TABLE tasks ADD CONSTRAINT tasks_statut_check CHECK (
      statut IN ('a_faire','en_cours','blocked','failed','done','valide')
    );
  END IF;
END $$;

COMMENT ON CONSTRAINT tasks_statut_check ON tasks IS
  'Six etats. a_faire, blocked et failed sont imposes par SPEC §1.2 ; done et '
  'valide sont distincts pour la meme raison que propose_cloture et clos sur les '
  'decisions : on ne valide pas son propre travail.';

-- ---------------------------------------------------------------------------
-- 2. tasks.constat et tasks.valide_par
-- ---------------------------------------------------------------------------
--
-- POURQUOI. SPEC §1.1 definit l'etat valide comme « avec preuve ET CONSTAT DE
-- RELECTURE », et la commande valider de LOT-02 prend --constat. Mais SPEC §1.2
-- n'a pas donne de colonne pour le porter : la preuve est celle de l'executant,
-- le constat est celui du relecteur, et les deux ne disent pas la meme chose.
--
-- Sans ces colonnes, le constat n'avait que des mauvais rangements possibles —
-- next_action, evidence_ref — c'est-a-dire la faute meme que le point 3 de cette
-- migration repare sur decisions. Une colonne surchargee melange deux
-- informations et rend l'une des deux illisible sans deviner laquelle.

ALTER TABLE tasks ADD COLUMN IF NOT EXISTS constat    text;
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS valide_par text;

COMMENT ON COLUMN tasks.constat IS
  'Constat de relecture, ecrit par qui valide. Distinct de evidence_ref, qui est '
  'la preuve fournie par qui a execute : l''un atteste, l''autre relit.';

-- ---------------------------------------------------------------------------
-- 3. decisions.motif
-- ---------------------------------------------------------------------------
--
-- POURQUOI. LOT-03 rangeait le motif d'une decision obsolete dans porte_sur, ou
-- l'outil rangeait deja le motif d'un refus. porte_sur designe ce sur quoi une
-- decision porte : y mettre un motif melange deux informations dans une colonne,
-- et rend l'une des deux impossible a lire sans deviner laquelle. Dette signalee
-- par LOT-03 et accordee par Sam le 17/08.

ALTER TABLE decisions ADD COLUMN IF NOT EXISTS motif text;

COMMENT ON COLUMN decisions.motif IS
  'Motif d''un refus, d''une mise en obsolescence ou de toute sortie qui en exige '
  'un. Distinct de porte_sur, qui designe ce sur quoi la decision porte.';

-- REPRISE DE L'EXISTANT. Uniquement pour refusee et obsolete : ce sont les deux
-- seuls statuts pour lesquels porte_sur a servi de motif. Ailleurs, porte_sur veut
-- dire ce qu'il dit, et le recopier fabriquerait un motif la ou il n'y en a jamais
-- eu. porte_sur n'est PAS vide apres reprise : effacer une donnee pour reussir un
-- deplacement fait perdre ce qu'on n'avait pas prevu de relire.
UPDATE decisions
   SET motif = porte_sur
 WHERE statut IN ('refusee','obsolete')
   AND porte_sur IS NOT NULL
   AND motif IS NULL;

COMMIT;
