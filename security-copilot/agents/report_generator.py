from dataclasses import dataclass
from io import BytesIO
import html
import json

from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet


@dataclass
class SecurityReportAgent:
    """Generate reviewable security reports in portable text formats."""

    def create(self, findings: list[dict], report_type: str = "technical", output_format: str = "markdown") -> dict:
        report_type = report_type.lower()
        output_format = output_format.lower()
        if report_type not in {"executive", "technical", "compliance"}:
            return {"status": "unsupported_report_type", "report_type": report_type}
        if output_format not in {"markdown", "html", "json", "pdf"}:
            return {"status": "unsupported_format", "output_format": output_format}
        markdown = self._markdown(findings, report_type)
        if output_format == "markdown":
            content = markdown
        elif output_format == "html":
            content = f"<html><body><pre>{html.escape(markdown)}</pre></body></html>"
        elif output_format == "json":
            content = {"report_type": report_type, "finding_count": len(findings), "findings": findings}
        else:
            content = {"status": "ready", "mime_type": "application/pdf"}
        return {"report_type": report_type, "format": output_format, "content": content, "status": "draft"}

    def _markdown(self, findings: list[dict], report_type: str) -> str:
        title = f"{report_type.title()} Security Report"
        lines = [f"# {title}", "", f"Finding count: {len(findings)}", ""]
        if report_type == "executive":
            critical = sum(1 for finding in findings if finding.get("severity") == "critical")
            lines.extend(["## Risk summary", "", "Prioritize critical findings, credential exposure, and internet-facing issues.", "", f"Critical issues: {critical}", "", "## Recommended priorities", "", "1. Contain critical exposures", "2. Rotate compromised credentials", "3. Apply and verify fixes", ""])
        else:
            lines.extend(["## Technical analysis", "", "Includes scanner evidence, AI explanations, remediation guidance, code snippets, and references.", ""])
        for index, finding in enumerate(findings, 1):
            lines.extend([f"## Finding {index}", "", f"```json\n{json.dumps(finding, indent=2)}\n```", ""])
        return "\n".join(lines)

    def render_pdf(self, findings: list[dict], report_type: str = "technical") -> bytes:
        buffer = BytesIO()
        document = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=48, leftMargin=48, topMargin=48, bottomMargin=48)
        styles = getSampleStyleSheet()
        story = [Paragraph(f"{report_type.title()} Security Report", styles["Title"]), Spacer(1, 12), Paragraph(f"Total findings: {len(findings)}", styles["BodyText"]), Spacer(1, 12)]
        for index, finding in enumerate(findings, 1):
            title = str(finding.get("title") or finding.get("description") or "Security finding")
            severity = str(finding.get("severity", "unknown"))
            location = str(finding.get("file") or finding.get("file_path") or "unknown location")
            story.extend([Paragraph(f"{index}. {html.escape(title)}", styles["Heading2"]), Paragraph(f"Severity: {html.escape(severity)} | Location: {html.escape(location)}", styles["BodyText"]), Spacer(1, 8)])
        document.build(story)
        return buffer.getvalue()


def generate_report(findings: list[dict], report_type: str = "technical", output_format: str = "markdown") -> dict:
    return SecurityReportAgent().create(findings, report_type, output_format)
