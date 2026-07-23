const links = ["Dashboard", "Repositories", "Scan History", "Findings", "AI Chat", "Reports", "Settings"];

export function Nav() {
  return <nav style={{ display: "flex", gap: 16, flexWrap: "wrap", padding: "16px 0", borderBottom: "1px solid #27272a" }}>
    {links.map((link) => <a href={`/${link.toLowerCase().replaceAll(" ", "-")}`} key={link} style={{ color: "#a1a1aa", textDecoration: "none" }}>{link}</a>)}
  </nav>;
}

