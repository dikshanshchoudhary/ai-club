# Product Roadmap

## Phase 1 — MVP

- Repository security scanning
- Alert investigation
- Cloud security assessment
- Executive dashboard
- GitHub and OpenAI integrations
- Semgrep, Trivy, Gitleaks, and Checkov

## Post-MVP

| Feature | Suggested priority | Main dependency |
|---|---:|---|
| PR review bot | High | GitHub webhook and review permissions |
| Auto-generated patches | High | Approval workflow and patch validation |
| Compliance dashboard | High | Control mappings and evidence storage |
| Threat hunting | Medium | SIEM/event connectors and indexed telemetry |
| Cloud posture management | Medium | AWS/Azure/GCP credentials and continuous jobs |
| SIEM integration | Medium | Sentinel, Splunk, Wazuh, or Elastic connector |
| Attack path visualization | Medium | Asset graph and MITRE relationship model |
| CVE trending | Low | Historical NVD/CISA KEV ingestion |
| Multi-tenant organizations | Low | Tenant isolation, billing, and stronger authorization |

Each feature should preserve the existing principles: least-privilege integrations, RAG-grounded analysis, audit logging, and explicit approval for state-changing actions.

