"use client";

import { useEffect, useState } from "react";
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export default function Dashboard() {
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => { const load = () => fetch(`${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}/mvp/dashboard/live`).then((response) => response.json()).then(setData).catch(() => setError("Unable to load live dashboard data.")); load(); const timer = setInterval(load, 5000); return () => clearInterval(timer); }, []);
  if (error) return <main style={{ maxWidth: 1200, margin: "0 auto", padding: 32 }}><h1>Executive security dashboard</h1><p>{error}</p></main>;
  if (!data) return <main style={{ maxWidth: 1200, margin: "0 auto", padding: 32 }}><h1>Executive security dashboard</h1><p>Loading live data…</p></main>;
  const dashboard = data.dashboard;
  if (!dashboard) return <main style={{ maxWidth: 1200, margin: "0 auto", padding: 32 }}><h1>Executive security dashboard</h1><p>{data.message ?? "No dashboard data available."}</p></main>;
  return <main style={{ maxWidth: 1200, margin: "0 auto", padding: 32 }}>
    <h1>Executive security dashboard</h1>
    <section style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16, marginTop: 24 }}>
      {[['Risk score', `${dashboard.risk_score}/100`], ['Open findings', dashboard.total_findings], ['Critical findings', dashboard.critical_findings], ['Repositories', dashboard.repositories]].map(([label, value]) => <div className="card" key={label}><div style={{ color: "#a1a1aa" }}>{label}</div><h2>{value}</h2></div>)}
    </section>
    <section className="card" style={{ marginTop: 16 }}><h2>Database status</h2><p>Live source: {dashboard.data_source}</p><p>Completed scans: {dashboard.completed_scans}</p></section>
  </main>;
}
