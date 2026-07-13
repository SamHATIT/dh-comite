-- GATE 4 §3 — vues lecture seule pour le comité (Security Filtering : pas de contenu client)
CREATE OR REPLACE VIEW v_deos_executions AS
SELECT e.id, e.project_id, p.name AS project_name, e.status::text AS status,
       e.execution_state, e.last_completed_phase, e.progress, e.current_agent,
       e.total_tokens_used, e.total_cost, e.duration_seconds,
       e.started_at, e.completed_at, e.created_at, e.state_updated_at
FROM executions e JOIN projects p ON p.id = e.project_id;

CREATE OR REPLACE VIEW v_deos_sections AS
SELECT d.id, d.execution_id, d.agent_id, d.deliverable_type,
       length(d.content) AS content_length,
       (d.content IS NULL OR length(btrim(d.content)) = 0) AS vide,
       d.created_at, d.updated_at
FROM agent_deliverables d;

CREATE OR REPLACE VIEW v_deos_projects AS
SELECT p.id, p.user_id, p.name, p.salesforce_product, p.status::text AS status,
       p.created_at, p.updated_at
FROM projects p;

CREATE OR REPLACE VIEW v_deos_build_phases AS
SELECT b.id, b.execution_id, b.phase_number, b.phase_name, b.status,
       b.agent_id, b.total_batches, b.completed_batches, b.elena_verdict
FROM build_phase_executions b;
