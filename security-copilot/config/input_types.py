from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class InputType:
    key: str
    category: str
    accepted_extensions: tuple[str, ...]
    value_kind: str


INPUT_TYPES = {
    item.key: item
    for item in [
        InputType("github_repository_url", "repository", (), "url"),
        InputType("windows_event_logs", "logs", (".evtx", ".json", ".xml"), "file"),
        InputType("sysmon", "logs", (".evtx", ".json", ".xml"), "file"),
        InputType("apache", "logs", (".log", ".txt", ".json"), "file"),
        InputType("nginx", "logs", (".log", ".txt", ".json"), "file"),
        InputType("cloudtrail", "logs", (".json", ".jsonl"), "file"),
        InputType("azure_logs", "logs", (".json", ".jsonl"), "file"),
        InputType("gcp_logs", "logs", (".json", ".jsonl"), "file"),
        InputType("splunk_alert", "alert", (".json",), "file"),
        InputType("sentinel_alert", "alert", (".json",), "file"),
        InputType("elastic_alert", "alert", (".json",), "file"),
        InputType("wazuh_alert", "alert", (".json",), "file"),
        InputType("terraform", "infrastructure", (".tf", ".tf.json"), "file"),
        InputType("dockerfile", "infrastructure", ("Dockerfile",), "file"),
        InputType("docker_compose", "infrastructure", (".yml", ".yaml"), "file"),
        InputType("kubernetes_yaml", "infrastructure", (".yml", ".yaml"), "file"),
        InputType("cloudformation", "infrastructure", (".json", ".yml", ".yaml"), "file"),
        InputType("helm", "infrastructure", (".yml", ".yaml", "Chart.yaml"), "file"),
        InputType("docker_image", "container", (), "image_reference"),
        InputType("oci_image", "container", (), "image_reference"),
        InputType("sbom", "container", (".json", ".xml", ".spdx", ".cdx"), "file"),
    ]
}


def describe_input(key: str) -> dict | None:
    item = INPUT_TYPES.get(key.lower())
    return asdict(item) if item else None

