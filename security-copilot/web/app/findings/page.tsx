import { PageShell } from "../components/page-shell";
import { useEffect, useState } from "react";

type Finding = {
  severity: string;
  cwe?: string;
  cve?: string;
  file?: string;
  file_path?: string;
  line?: number;
  line_number?: number;
  description?: string;
  title?: string;
  impact: string;
  explanation: string;
  fix: string;
  diff: string;
  references: string[];
  mitre?: string;
};

export default function Findings() {
  const [findings, setFindings] = useState<Finding[] | null>(null);
  const [message, setMessage] = useState("Loading live findings…");
  useEffect(() => { fetch(`${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}/mvp/findings`).then((response) => response.json()).then((data) => { setFindings(data.findings ?? []); setMessage(data.message ?? ""); }).catch(() => setMessage("Unable to load live findings.")); }, []);
  return <PageShell title="Findings">{findings === null ? <div className="card">{message}</div> : findings.length === 0 ? <div className="card">{message || "No findings are stored in PostgreSQL."}</div> : findings.map((finding) => <article className="card" key={`${finding.file_path}-${finding.line_number}-${finding.description}`} style={{ marginBottom: 16 }}>
    <div style={{ display: "flex", justifyContent: "space-between" }}><h2><a href={`/findings/${(finding as any).id}`}>{finding.description ?? finding.title ?? "Security finding"}</a></h2><strong style={{ color: "#f87171" }}>{finding.severity}</strong></div>
    <p><b>Location:</b> {finding.file_path ?? finding.file ?? "Unknown"}:{finding.line_number ?? finding.line ?? "?"}</p><p><b>CWE:</b> {finding.cwe ?? "N/A"} &nbsp; <b>CVE:</b> {finding.cve ?? "N/A"}</p>
    <h3>Impact</h3><p>{finding.impact ?? "Not provided by the scanner."}</p><h3>AI explanation</h3><p>{finding.explanation ?? "Not generated yet."}</p><h3>AI-generated fix</h3><p>{finding.fix ?? "Not generated yet."}</p>
    {finding.diff && <><h3>Code diff</h3><pre style={{ background: "#09090b", padding: 16, overflowX: "auto" }}>{finding.diff}</pre></>}
    <h3>References</h3><ul>{(finding.references ?? []).map((reference) => <li key={reference}>{reference}</li>)}</ul>{finding.mitre && <p><b>MITRE ATT&CK:</b> {finding.mitre}</p>}
  </article>)}</PageShell>;
}
