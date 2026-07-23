import { PageShell } from "../components/page-shell";
"use client";
import { useEffect, useState } from "react";

export default function Repositories() {
  const [source, setSource] = useState("demo/vulnerable-repo");
  const [job, setJob] = useState<any>(null);
  const [message, setMessage] = useState("");
  const [repositories, setRepositories] = useState<any[]>([]);
  useEffect(() => { fetch(`${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}/mvp/repositories`).then((response) => response.json()).then((data) => setRepositories(data.repositories ?? [])).catch(() => undefined); }, []);
  const startScan = async () => {
    setMessage("Queueing scan…");
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}/jobs/live-repository-scan`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ source }) });
    const created = await response.json(); setJob(created); setMessage(`Job ${created.status}`);
  };
  useEffect(() => { if (!job?.job_id || ["completed", "failed"].includes(job.status)) return; const timer = setInterval(async () => { const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}/jobs/${job.job_id}`); const current = await response.json(); setJob(current); setMessage(`Job ${current.status}`); }, 1500); return () => clearInterval(timer); }, [job?.job_id, job?.status]);
  return <PageShell title="Repositories"><div className="card"><p>Scan a local repository path or Git URL.</p><input value={source} onChange={(event) => setSource(event.target.value)} style={{ width: "100%", padding: 10, background: "#09090b", color: "white" }} /><br /><br /><button onClick={startScan}>Scan</button><p>{message}</p>{job?.result && <p>Findings: {job.result.finding_count}. Stored: {String(job.result.stored)}.</p>}</div><div className="card" style={{ marginTop: 16 }}><h2>Connected repositories</h2>{repositories.length ? repositories.map((repository) => <p key={repository.id}>{repository.name} ({repository.provider})</p>) : <p>No repositories stored in PostgreSQL.</p>}</div></PageShell>;
}
