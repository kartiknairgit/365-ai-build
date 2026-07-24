import { useMemo, useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import {
  Background,
  Controls,
  Handle,
  Position,
  ReactFlow,
  type NodeProps,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import {
  Activity,
  ArrowLeftRight,
  Bot,
  Boxes,
  FileUp,
  Gauge,
  Info,
  Search,
  ShieldCheck,
  Wrench,
} from "lucide-react";
import { NavLink, Route, Routes } from "react-router-dom";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import {
  getJson,
  importTrace,
  type RunDetail,
  type RunSummary,
  type TraceEvent,
} from "./api";

const nav = [
  ["/", "Overview", Gauge],
  ["/runs", "Runs & traces", Activity],
  ["/agents", "Agents", Bot],
  ["/comparisons", "Comparisons", ArrowLeftRight],
  ["/imports", "Imports", FileUp],
  ["/about", "About", Info],
] as const;

function Status({ healthy }: { healthy: boolean }) {
  return (
    <span className={`status ${healthy ? "healthy" : "failed"}`}>
      {healthy ? "Completed" : "Needs attention"}
    </span>
  );
}

function State({ children }: { children: React.ReactNode }) {
  return <div className="state">{children}</div>;
}

function Overview() {
  const metrics = useQuery({
    queryKey: ["metrics"],
    queryFn: () =>
      getJson<Record<string, number | string | boolean>>("/api/v1/metrics"),
  });
  const runs = useQuery({
    queryKey: ["runs"],
    queryFn: () =>
      getJson<{ items: RunSummary[]; total: number }>(
        "/api/v1/runs?page_size=8",
      ),
  });
  if (metrics.isLoading || runs.isLoading)
    return <State>Loading operational summary…</State>;
  if (metrics.error || runs.error)
    return <State>Connect the local backend to view operational data.</State>;
  const m = metrics.data!;
  const cards = [
    ["Total runs", m.total_runs],
    ["Completion", `${Math.round(Number(m.completion_rate) * 100)}%`],
    ["Tool success", `${Math.round(Number(m.tool_call_success_rate) * 100)}%`],
    ["P95 latency", `${Math.round(Number(m.p95_latency_ms))} ms`],
  ];
  const chart = [
    {
      name: "Completed",
      value: Math.round(Number(m.completion_rate) * 100),
      color: "#22a06b",
    },
    {
      name: "Failed/incomplete",
      value: Math.round(Number(m.failure_rate) * 100),
      color: "#dc4c4c",
    },
    {
      name: "Human review",
      value: Math.round(Number(m.human_review_rate) * 100),
      color: "#d99412",
    },
  ];
  return (
    <>
      <Header
        eyebrow="System overview"
        title="Workflow operations"
        subtitle="Deterministic signals from validated local traces."
      />
      <section className="metric-grid">
        {cards.map(([label, value]) => (
          <article className="metric" key={String(label)}>
            <span>{label}</span>
            <strong>{String(value)}</strong>
          </article>
        ))}
      </section>
      <section className="two-column">
        <article className="panel chart-panel">
          <h2>Run health distribution</h2>
          <p className="sr-only">
            {chart.map((item) => `${item.name}: ${item.value}%`).join(", ")}
          </p>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={chart}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value">
                {chart.map((item) => (
                  <Cell key={item.name} fill={item.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </article>
        <article className="panel">
          <h2>Recent runs</h2>
          <div className="run-list">
            {runs.data!.items.map((run) => (
              <div className="run-row" key={run.run_id}>
                <div>
                  <strong>{run.workflow_name}</strong>
                  <small>
                    {run.run_id} · v{run.workflow_version}
                  </small>
                </div>
                <Status healthy={run.is_complete} />
              </div>
            ))}
          </div>
          {!runs.data!.items.length && (
            <State>
              No traces imported yet. Load a fictional fixture from Imports.
            </State>
          )}
        </article>
      </section>
    </>
  );
}

function Header({
  eyebrow,
  title,
  subtitle,
}: {
  eyebrow: string;
  title: string;
  subtitle: string;
}) {
  return (
    <header className="page-header">
      <p className="eyebrow">{eyebrow}</p>
      <h1>{title}</h1>
      <p>{subtitle}</p>
    </header>
  );
}

function EventNode({ data }: NodeProps) {
  const value = data as { label: string; status: string; kind: string };
  return (
    <div className={`flow-node ${value.status}`}>
      <Handle type="target" position={Position.Top} />
      <small>{value.kind}</small>
      <strong>{value.label}</strong>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

function WorkflowGraph({
  events,
  onSelect,
}: {
  events: TraceEvent[];
  onSelect: (event: TraceEvent) => void;
}) {
  const nodes = events.map((event, index) => ({
    id: event.event_id,
    type: "event",
    position: { x: (index % 4) * 210, y: Math.floor(index / 4) * 130 },
    data: {
      label: event.agent_name ?? event.tool_name ?? event.event_id,
      kind: event.event_type,
      status: event.status,
    },
  }));
  const edges = events
    .filter((event) => event.parent_event_id)
    .map((event) => ({
      id: `${event.parent_event_id}-${event.event_id}`,
      source: event.parent_event_id!,
      target: event.event_id,
      animated: event.event_type === "handoff",
    }));
  return (
    <div
      className="graph"
      aria-label={`Workflow graph with ${nodes.length} events`}
    >
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={{ event: EventNode }}
        onNodeClick={(_, node) => {
          const found = events.find((event) => event.event_id === node.id);
          if (found) onSelect(found);
        }}
        fitView
      >
        <Background />
        <Controls />
      </ReactFlow>
    </div>
  );
}

function Runs() {
  const [selectedRun, setSelectedRun] = useState("");
  const [selectedEvent, setSelectedEvent] = useState<TraceEvent | null>(null);
  const [search, setSearch] = useState("");
  const runs = useQuery({
    queryKey: ["runs"],
    queryFn: () =>
      getJson<{ items: RunSummary[] }>("/api/v1/runs?page_size=100"),
  });
  const detail = useQuery({
    queryKey: ["run", selectedRun],
    queryFn: () => getJson<RunDetail>(`/api/v1/runs/${selectedRun}`),
    enabled: Boolean(selectedRun),
  });
  const filtered = useMemo(
    () =>
      detail.data?.events.filter((event) =>
        JSON.stringify(event).toLowerCase().includes(search.toLowerCase()),
      ) ?? [],
    [detail.data, search],
  );
  return (
    <>
      <Header
        eyebrow="Trace explorer"
        title="Runs and execution evidence"
        subtitle="Reconstructed topology, chronology, and deterministic findings."
      />
      <div className="toolbar">
        <select
          aria-label="Select run"
          value={selectedRun}
          onChange={(event) => setSelectedRun(event.target.value)}
        >
          <option value="">Select a run</option>
          {runs.data?.items.map((run) => (
            <option key={run.run_id} value={run.run_id}>
              {run.workflow_name} · {run.run_id}
            </option>
          ))}
        </select>
        <label className="search">
          <Search size={16} />
          <input
            aria-label="Search trace"
            placeholder="Search event, agent, tool…"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
          />
        </label>
      </div>
      {!selectedRun && (
        <State>Select a run to inspect its workflow graph and timeline.</State>
      )}
      {detail.isLoading && <State>Reconstructing run…</State>}
      {detail.error && <State>Unable to load this run.</State>}
      {detail.data && (
        <>
          <section className="panel">
            <h2>Workflow topology</h2>
            <WorkflowGraph
              events={detail.data.events}
              onSelect={setSelectedEvent}
            />
            {selectedEvent && (
              <pre className="event-detail">
                {JSON.stringify(selectedEvent, null, 2)}
              </pre>
            )}
          </section>
          <section className="panel">
            <h2>Execution timeline</h2>
            <div className="timeline">
              {filtered.map((event) => (
                <details key={event.event_id}>
                  <summary>
                    <time>
                      {new Date(event.timestamp).toLocaleTimeString()}
                    </time>
                    <span className="event-type">{event.event_type}</span>
                    <strong>
                      {event.agent_name ?? event.tool_name ?? event.event_id}
                    </strong>
                    <Status
                      healthy={!["failed", "timed_out"].includes(event.status)}
                    />
                  </summary>
                  <pre>{JSON.stringify(event, null, 2)}</pre>
                </details>
              ))}
            </div>
            {detail.data.evaluation_flags.map((flag) => (
              <div className="flag" key={`${flag.rule}-${flag.event_id}`}>
                <ShieldCheck size={16} />
                <strong>{flag.rule.replaceAll("_", " ")}</strong>
                <span>{flag.explanation}</span>
              </div>
            ))}
          </section>
        </>
      )}
    </>
  );
}

function Agents() {
  const query = useQuery({
    queryKey: ["agents"],
    queryFn: () =>
      getJson<Array<Record<string, string | number>>>("/api/v1/agents"),
  });
  return (
    <>
      <Header
        eyebrow="Operational scorecards"
        title="Agent activity"
        subtitle="Evidence-based operations—not intelligence, quality, or safety scores."
      />
      {query.isLoading && <State>Loading agent evidence…</State>}
      <section className="card-grid">
        {query.data?.map((agent) => (
          <article className="panel agent-card" key={String(agent.agent_name)}>
            <Bot />
            <h2>{agent.agent_name}</h2>
            <dl>
              <div>
                <dt>Run participation</dt>
                <dd>{agent.participation_count}</dd>
              </div>
              <div>
                <dt>Median latency</dt>
                <dd>{agent.median_latency_ms} ms</dd>
              </div>
              <div>
                <dt>Tool success</dt>
                <dd>{Math.round(Number(agent.tool_success_rate) * 100)}%</dd>
              </div>
              <div>
                <dt>Retries</dt>
                <dd>{agent.retry_count}</dd>
              </div>
            </dl>
            <small>{agent.disclaimer}</small>
          </article>
        ))}
      </section>
      {query.data?.length === 0 && (
        <State>No agent participation observed.</State>
      )}
    </>
  );
}

function Comparisons() {
  const [baseline, setBaseline] = useState("");
  const [candidate, setCandidate] = useState("");
  const runs = useQuery({
    queryKey: ["runs"],
    queryFn: () =>
      getJson<{ items: RunSummary[] }>("/api/v1/runs?page_size=100"),
  });
  const comparison = useQuery({
    queryKey: ["comparison", baseline, candidate],
    queryFn: () =>
      getJson<Record<string, unknown>>(
        `/api/v1/comparisons?baseline_run_id=${encodeURIComponent(baseline)}&candidate_run_id=${encodeURIComponent(candidate)}`,
      ),
    enabled: Boolean(baseline && candidate),
  });
  const selector = (
    label: string,
    value: string,
    change: (value: string) => void,
  ) => (
    <label>
      {label}
      <select value={value} onChange={(event) => change(event.target.value)}>
        <option value="">Select run</option>
        {runs.data?.items.map((run) => (
          <option key={run.run_id} value={run.run_id}>
            {run.run_id}
          </option>
        ))}
      </select>
    </label>
  );
  return (
    <>
      <Header
        eyebrow="Regression analysis"
        title="Compare workflow runs"
        subtitle="Directional deterministic deltas; small samples do not imply statistical significance."
      />
      <div className="comparison-select">
        {selector("Baseline", baseline, setBaseline)}
        <ArrowLeftRight />
        {selector("Candidate", candidate, setCandidate)}
      </div>
      {comparison.isLoading && <State>Calculating deltas…</State>}
      {comparison.data && (
        <pre className="panel comparison-output">
          {JSON.stringify(comparison.data, null, 2)}
        </pre>
      )}
    </>
  );
}

function Imports() {
  const [file, setFile] = useState<File | null>(null);
  const mutation = useMutation({ mutationFn: importTrace });
  return (
    <>
      <Header
        eyebrow="Local data"
        title="Import trace JSONL"
        subtitle="Files remain local. Content is parsed as bounded JSON and never executed."
      />
      <section className="panel import-panel">
        <FileUp size={32} />
        <label>
          Trace file
          <input
            type="file"
            accept=".jsonl,.ndjson,application/x-ndjson"
            onChange={(event) => setFile(event.target.files?.[0] ?? null)}
          />
        </label>
        <button
          disabled={!file || mutation.isPending}
          onClick={() => file && mutation.mutate(file)}
        >
          {mutation.isPending ? "Validating…" : "Import safely"}
        </button>
        {mutation.isSuccess && (
          <pre>{JSON.stringify(mutation.data, null, 2)}</pre>
        )}
        {mutation.error && <p role="alert">{mutation.error.message}</p>}
      </section>
    </>
  );
}

function About() {
  return (
    <>
      <Header
        eyebrow="System boundaries"
        title="About this prototype"
        subtitle="A local observability and deterministic evaluation workbench."
      />
      <section className="panel prose">
        <h2>Human interpretation required</h2>
        <p>
          AgentOps Control Tower does not execute agents or tools, guarantee
          model quality or safety, or claim live provider pricing. Imported
          values remain local and inert. Seeded traces are fictional.
        </p>
        <h2>Architecture</h2>
        <p>
          FastAPI validates, quarantines, reconstructs, and stores traces in
          SQLite. React Query drives this React control plane; React Flow and
          Recharts provide accessible visual summaries.
        </p>
      </section>
    </>
  );
}

export function App() {
  return (
    <div className="app-shell">
      <aside>
        <div className="brand">
          <Boxes />
          <div>
            <strong>AgentOps</strong>
            <span>CONTROL TOWER</span>
          </div>
        </div>
        <nav aria-label="Primary">
          {nav.map(([path, label, Icon]) => (
            <NavLink key={path} to={path} end={path === "/"}>
              <Icon size={18} />
              {label}
            </NavLink>
          ))}
        </nav>
        <div className="local-badge">
          <Wrench size={15} />
          Local-only prototype
        </div>
      </aside>
      <main>
        <Routes>
          <Route path="/" element={<Overview />} />
          <Route path="/runs" element={<Runs />} />
          <Route path="/agents" element={<Agents />} />
          <Route path="/comparisons" element={<Comparisons />} />
          <Route path="/imports" element={<Imports />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </main>
    </div>
  );
}
