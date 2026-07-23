import { PageShell } from "../components/page-shell";
"use client";

async function downloadPdf() {
  const api = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
  const findingsResponse = await fetch(`${api}/mvp/findings`);
  const findingsData = await findingsResponse.json();
  const response = await fetch(`${api}/mvp/reports/pdf`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ report_type: "technical", findings: findingsData.findings ?? [] }) });
  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a"); link.href = url; link.download = "security-report.pdf"; link.click(); URL.revokeObjectURL(url);
}

async function downloadReport(format: "markdown" | "json", reportType: "executive" | "technical") {
  const api = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
  const findingsData = await (await fetch(`${api}/mvp/findings`)).json();
  const report = await (await fetch(`${api}/mvp/reports`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ report_type: reportType, output_format: format, findings: findingsData.findings ?? [] }) })).json();
  const content = format === "json" ? JSON.stringify(report.content, null, 2) : report.content;
  const link = document.createElement("a"); link.href = URL.createObjectURL(new Blob([content], { type: format === "json" ? "application/json" : "text/markdown" })); link.download = `${reportType}-security-report.${format === "json" ? "json" : "md"}`; link.click();
}

export default function Reports() { return <PageShell title="Reports"><div style={{ display: "grid", gap: 16 }}>
  <section className="card"><h2>Executive report</h2><p>Security score, total findings, critical issues, risk summary, and recommended priorities.</p><button onClick={() => downloadReport("markdown", "executive")}>Download Markdown</button> <button onClick={() => downloadReport("json", "executive")}>Download JSON</button></section>
  <section className="card"><h2>Technical report</h2><p>All findings, AI explanations, remediation guidance, code snippets, and references.</p><button onClick={() => downloadReport("markdown", "technical")}>Download Markdown</button> <button onClick={() => downloadReport("json", "technical")}>Download JSON</button></section>
  <section className="card"><h2>Export format</h2><select defaultValue="pdf"><option value="pdf">PDF</option><option value="markdown">Markdown</option><option value="json">JSON</option></select><p><button onClick={downloadPdf}>Download PDF</button></p></section>
</div></PageShell>; }
