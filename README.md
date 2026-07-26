# 🛡️ AI Security Copilot

> An Agentic AI-powered Security Operations Platform that automates repository scanning, vulnerability assessment, cloud security analysis, threat intelligence, and AI-assisted remediation.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791)
![Qdrant](https://img.shields.io/badge/Qdrant-VectorDB-DC244C)
![License](https://img.shields.io/badge/License-MIT-green)

---

# 📌 Overview

AI Security Copilot is an **Agentic AI Security Operations Platform** designed to help developers, security analysts, and DevSecOps teams identify, analyse, and remediate security risks across software repositories and cloud infrastructure.

Unlike traditional security scanners, AI Security Copilot combines **Large Language Models (LLMs)** with **industry-standard security tools** to provide intelligent explanations, prioritised remediation guidance, and executive security reports.

---

# ✨ Key Features

## 🔍 Repository Security Analysis

- Source code scanning
- Dependency analysis
- Infrastructure as Code (IaC) scanning
- Secret detection
- Security misconfiguration detection

---

## 🤖 AI-Powered Security Assistant

- AI-generated vulnerability explanations
- Security recommendations
- Root cause analysis
- Risk prioritisation
- Executive summaries

---

## 🛡️ Multi-Agent Architecture

The platform consists of specialised AI agents:

- 🧠 Planner Agent
- 📂 Repository Agent
- 🚨 Alert Agent
- ☁️ Cloud Security Agent
- 📊 Risk Assessment Agent
- 🔎 Scanner Agent
- 🦠 Malware Analysis Agent
- 🎣 Phishing Detection Agent
- 🌐 Threat Intelligence Agent
- 🎯 Threat Hunting Agent
- 🔧 Remediation Agent
- 📝 Report Generator

Each agent performs a dedicated task while the Planner Agent coordinates workflows.

---

# 🔧 Security Tools

The platform integrates multiple open-source security tools:

| Tool | Purpose |
|-------|----------|
| Semgrep | Static Application Security Testing (SAST) |
| Trivy | Container & Dependency Scanning |
| Gitleaks | Secret Detection |
| Checkov | Infrastructure as Code Security |
| VirusTotal | Threat Intelligence |
| Qdrant | Vector Database for RAG |
| PostgreSQL | Findings Database |

---

# 🏗️ Architecture

```
                User
                  │
          React Dashboard
                  │
             FastAPI Backend
                  │
         Planner / Orchestrator
                  │
     ┌────────────┼────────────┐
     │            │            │
 Repository    Scanner      Cloud
   Agent        Agent       Agent
     │            │            │
 Risk Agent   Threat Intel  Alerts
     │
 Remediation Agent
     │
 Report Generator
                  │
      GPT / LLM Reasoning
                  │
    PostgreSQL + Qdrant
                  │
      Executive Reports
```

---

# ⚡ Technology Stack

## Frontend

- React
- TypeScript
- Tailwind CSS

## Backend

- FastAPI
- Python

## AI

- Large Language Models
- Retrieval Augmented Generation (RAG)
- Prompt Engineering

## Database

- PostgreSQL
- Qdrant

## DevOps

- Docker
- Docker Compose

---

# 🔐 Security Principles

AI Security Copilot follows a **Secure-by-Design** approach.

### Authentication

- JWT Authentication
- Role-Based Access Control (RBAC)

### AI Security

- Prompt Injection Protection
- Context Isolation
- Human-in-the-loop Approval
- Agent Permission Boundaries
- Output Validation
- Evidence-Grounded Responses

### Infrastructure Security

- HTTPS/TLS
- Encrypted Storage
- Audit Logging
- Read-only Tool Execution
- Least Privilege Access

---

# 📋 AI Security Risk Assessment

The project is designed following internationally recognised frameworks.

## OWASP LLM Top 10

✔ Prompt Injection

✔ Sensitive Information Disclosure

✔ Supply Chain Security

✔ Data Poisoning

✔ Improper Output Handling

✔ Excessive Agency

✔ Prompt Leakage

✔ Vector Database Security

✔ Misinformation

✔ Resource Exhaustion

---

## MITRE ATLAS

The system incorporates mitigations for:

- Prompt Injection
- Model Theft
- Credential Access
- Resource Exhaustion
- Supply Chain Compromise
- Adversarial Inputs
- Model Extraction

---

# 🚀 Workflow

1. User submits repository
2. Planner creates task graph
3. Security agents execute scans
4. AI correlates findings
5. Risk engine prioritises vulnerabilities
6. AI generates remediation
7. Executive report is created

---

# 📊 Generated Reports

AI Security Copilot produces:

- PDF Reports
- Markdown Reports
- JSON Reports

Reports include:

- Executive Summary
- Vulnerability Findings
- Severity Scores
- Risk Matrix
- Remediation Recommendations

---

# 📂 Project Structure

```
ai-security-copilot/

├── backend/
│   ├── agents/
│   ├── api/
│   ├── scanners/
│   ├── services/
│   ├── models/
│   └── database/
│
├── frontend/
│
├── docs/
│
├── docker/
│
├── scripts/
│
└── README.md
```

---

# ▶️ Getting Started

## Clone Repository

```bash
git clone https://github.com/dikshanshchoudhary/ai-club.git

cd ai-club
```

---

## Install Backend

```bash
pip install -r requirements.txt
```

---

## Run Backend

```bash
uvicorn app.main:app --reload
```

---

## Run Frontend

```bash
npm install

npm run dev
```

---

## Docker

```bash
docker compose up --build
```

---

# 📸 Screenshots

> Add screenshots here

- Dashboard
- Repository Scan
- AI Chat
- Risk Report
- Executive Report

---

# 📈 Future Roadmap

- Multi-Agent Collaboration
- Secure Autonomous Remediation
- SIEM Integration
- Cloud Security Posture Management
- Kubernetes Security
- Continuous AI Red Teaming
- Multi-LLM Support
- Enterprise SSO
- Compliance Reporting (ISO 27001, SOC 2, NIST)

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository

2. Create a feature branch

3. Commit your changes

4. Open a Pull Request

---

# 📚 References

- OWASP LLM Top 10
- MITRE ATLAS
- NIST AI Risk Management Framework
- NIST Cybersecurity Framework
- Semgrep Documentation
- Trivy Documentation
- Checkov Documentation
- Gitleaks Documentation

---

# 📄 License

This project is released under the **MIT License**.

---

# 👨‍💻 Author

**Dikshansh Choudhary**

B.Tech Computer Science & Engineering

KIET Group of Institutions

GitHub: https://github.com/dikshanshchoudhary

---

## ⭐ Support

If you found this project useful, consider giving it a **⭐ Star** on GitHub.
