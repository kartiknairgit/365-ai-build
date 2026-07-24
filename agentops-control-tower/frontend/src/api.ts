const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export interface RunSummary {
  trace_id: string;
  run_id: string;
  workflow_name: string;
  workflow_version: string;
  event_count: number;
  is_complete: boolean;
  finding_count: number;
}

export interface TraceEvent {
  event_id: string;
  parent_event_id: string | null;
  sequence_number: number;
  timestamp: string;
  event_type: string;
  status: string;
  agent_name?: string;
  tool_name?: string;
  latency_ms?: number;
  input_summary?: string;
  output_summary?: string;
  error_message?: string;
}

export interface RunDetail {
  run_id: string;
  is_complete: boolean;
  events: TraceEvent[];
  findings: Array<{ code: string; event_id: string; explanation: string }>;
  evaluation_flags: Array<{
    rule: string;
    severity: string;
    event_id: string;
    explanation: string;
  }>;
}

export async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_URL}${path}`);
  if (!response.ok) throw new Error(`Request failed (${response.status})`);
  return response.json() as Promise<T>;
}

export async function importTrace(file: File) {
  const body = new FormData();
  body.append("file", file);
  const response = await fetch(`${API_URL}/api/v1/imports`, {
    method: "POST",
    body,
  });
  if (!response.ok) throw new Error(`Import failed (${response.status})`);
  return response.json();
}
