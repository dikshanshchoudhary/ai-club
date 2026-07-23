import { Nav } from "./nav";

export function PageShell({ title, children }: { title: string; children: React.ReactNode }) {
  return <main style={{ maxWidth: 1200, margin: "0 auto", padding: 32 }}><p style={{ color: "#a1a1aa" }}>AI SECURITY COPILOT</p><h1>{title}</h1><Nav />{children}</main>;
}

