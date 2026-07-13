-- GATE 4 §3 — schéma dh_comite
CREATE TABLE deos_state (
  cle         text PRIMARY KEY,
  valeur      jsonb NOT NULL,
  maj_par     text NOT NULL,
  updated_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE decisions (
  id          text PRIMARY KEY,
  date        timestamptz NOT NULL DEFAULT now(),
  origine     text NOT NULL,
  texte       text NOT NULL,
  options     jsonb,
  recommandation text,
  statut      text NOT NULL DEFAULT 'attente_sam'
              CHECK (statut IN ('attente_sam','accordee','refusee','en_execution','clos')),
  validation_par text,
  porte_sur   text,
  preuve      jsonb,
  trace_instruction_id text,
  updated_at  timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT clos_avec_preuve CHECK (statut <> 'clos' OR preuve IS NOT NULL)
);

-- append-only : DELETE interdit (DH-COS-002)
CREATE FUNCTION decisions_no_delete() RETURNS trigger AS $$
BEGIN
  RAISE EXCEPTION 'decisions est append-only : DELETE interdit (DH-COS-002)';
END; $$ LANGUAGE plpgsql;

CREATE TRIGGER trg_decisions_no_delete
  BEFORE DELETE ON decisions
  FOR EACH ROW EXECUTE FUNCTION decisions_no_delete();

CREATE FUNCTION touch_updated_at() RETURNS trigger AS $$
BEGIN NEW.updated_at := now(); RETURN NEW; END; $$ LANGUAGE plpgsql;

CREATE TRIGGER trg_deos_state_touch BEFORE UPDATE ON deos_state
  FOR EACH ROW EXECUTE FUNCTION touch_updated_at();
CREATE TRIGGER trg_decisions_touch BEFORE UPDATE ON decisions
  FOR EACH ROW EXECUTE FUNCTION touch_updated_at();
