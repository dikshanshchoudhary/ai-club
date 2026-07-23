import argparse
import json
from pathlib import Path

from agents.threat_intelligence import ThreatIntelligenceAgent
from workflows.cloud_assessment import run as cloud_audit
from workflows.investigate_alert import run as investigate_alert
from workflows.scan_repository import run as scan_repository


def main() -> None:
    parser = argparse.ArgumentParser(prog="security", description="AI Security Copilot CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan", help="Scan a repository")
    scan.add_argument("target", nargs="?", default="repo")

    investigate = subparsers.add_parser("investigate", help="Investigate an alert JSON file")
    investigate.add_argument("alert_file")

    cloud = subparsers.add_parser("cloud", help="Assess cloud posture")
    cloud.add_argument("action", choices=["audit"])
    cloud.add_argument("--provider", default="aws")
    cloud.add_argument("--scope", default="default")

    explain = subparsers.add_parser("explain", help="Explain a CVE")
    explain.add_argument("identifier")

    args = parser.parse_args()
    if args.command == "scan":
        result = scan_repository(args.target)
    elif args.command == "investigate":
        payload = json.loads(Path(args.alert_file).read_text(encoding="utf-8"))
        result = investigate_alert(payload.get("source", "siem"), payload.get("events", []), payload.get("alert"))
    elif args.command == "cloud":
        result = cloud_audit(args.provider, args.scope)
    else:
        result = ThreatIntelligenceAgent().lookup_cve(args.identifier)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()

