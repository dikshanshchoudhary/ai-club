# Technical Security Report — Demo

| Severity | Tool | Location | Finding |
|---|---|---|---|
| High | Semgrep | `vulnerable-repo/app.py:9` | Potential SQL injection |
| High | Gitleaks | `vulnerable-repo/app.py:4` | Credential-like literal |
| High | Checkov | `sample-terraform/main.tf` | Public bucket configuration |
| High | Checkov | `sample-k8s/deployment.yaml` | Privileged container |
| Medium | Trivy | `vulnerable-repo/requirements.txt` | Outdated dependencies |

