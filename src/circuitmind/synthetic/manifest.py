"""Expected-results manifest rendering for synthetic project cases."""

import json
from pathlib import Path

from circuitmind.synthetic.spec import SyntheticProjectCase

MANIFEST_SCHEMA_VERSION = 1
MANIFEST_FILENAME = "manifest.json"


def write_case_manifest(
    case: SyntheticProjectCase,
    output_directory: Path,
) -> Path:
    """Write the deterministic expected-results manifest for a synthetic case."""

    output_directory.mkdir(parents=True, exist_ok=True)

    output_path = output_directory / MANIFEST_FILENAME

    payload = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "project_id": case.project.id,
        "expected_findings": [
            {
                "rule_id": finding.rule_id,
            }
            for finding in case.expected_findings
        ],
    }

    content = json.dumps(
        payload,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
    )

    output_path.write_text(
        content + "\n",
        encoding="utf-8",
        newline="\n",
    )

    return output_path
