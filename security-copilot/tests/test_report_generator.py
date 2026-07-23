from agents.report_generator import SecurityReportAgent


def test_report_agent_creates_markdown_report_types():
    result = SecurityReportAgent().create([{"severity": "high"}], "executive", "markdown")
    assert result["status"] == "draft"
    assert result["content"].startswith("# Executive Security Report")


def test_report_agent_creates_html_output():
    result = SecurityReportAgent().create([], "compliance", "html")
    assert result["content"].startswith("<html>")


def test_report_agent_creates_json_and_executive_priorities():
    result = SecurityReportAgent().create([{"severity": "critical"}], "executive", "json")
    assert result["content"]["finding_count"] == 1
    markdown = SecurityReportAgent().create([{"severity": "critical"}], "executive", "markdown")["content"]
    assert "Recommended priorities" in markdown


def test_report_agent_renders_pdf_bytes():
    pdf = SecurityReportAgent().render_pdf([{"severity": "high", "title": "Demo finding"}])
    assert pdf.startswith(b"%PDF")
