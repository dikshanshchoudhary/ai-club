"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { PageShell } from "../../components/page-shell";

export default function FindingDetail() {
  const params = useParams<{ id: string }>();
  const [data, setData] = useState<any>(null);
  useEffect(() => { fetch(`${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}/mvp/findings/${params.id}`).then((response) => response.json()).then(setData); }, [params.id]);
  if (!data) return <PageShell title="Finding"><div className="card">Loading live finding…</div></PageShell>;
  if (!data.finding) return <PageShell title="Finding"><div className="card">{data.message ?? "Finding not found."}</div></PageShell>;
  const finding = data.finding;
  return <PageShell title="Finding detail"><article className="card"><h2>{finding.title}</h2><p><b>Severity:</b> {finding.severity}</p><p><b>Tool:</b> {finding.tool} &nbsp; <b>Rule:</b> {finding.rule_id ?? "N/A"}</p><p><b>Location:</b> {finding.file_path ?? "Unknown"}:{finding.line_number ?? "?"}</p><h3>Description</h3><p>{finding.description ?? "Not provided."}</p><h3>Evidence</h3><pre>{JSON.stringify(finding.evidence, null, 2)}</pre><p><b>Status:</b> {finding.status}</p></article></PageShell>;
}
