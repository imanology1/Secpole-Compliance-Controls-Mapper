import pandas as pd
from .models import Control, Mapping


def load_controls(path: str, framework: str):
    """Load controls from a CSV file.

    Requires columns: id, name. `description` is optional. Rows with a blank
    id are skipped rather than creating a phantom control.
    """
    df = pd.read_csv(path, dtype=str).fillna("")
    missing = {"id", "name"} - set(df.columns)
    if missing:
        raise ValueError(f"{path}: missing required column(s): {', '.join(sorted(missing))}")

    controls = []
    for _, row in df.iterrows():
        cid = str(row["id"]).strip()
        if not cid:
            continue
        controls.append(
            Control(
                framework=framework,
                id=cid,
                name=str(row["name"]).strip(),
                description=str(row.get("description", "")).strip(),
            )
        )
    return controls


def load_mappings(path: str):
    """Load control mappings from a CSV file.

    Requires: source_framework, source_id, target_framework, target_id.
    `relationship` is optional and defaults to "related".
    """
    df = pd.read_csv(path, dtype=str).fillna("")
    required = {"source_framework", "source_id", "target_framework", "target_id"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path}: missing required column(s): {', '.join(sorted(missing))}")

    mappings = []
    for _, row in df.iterrows():
        rel = str(row.get("relationship", "") or "related").strip()
        mappings.append(
            Mapping(
                source_framework=str(row["source_framework"]).strip(),
                source_id=str(row["source_id"]).strip(),
                target_framework=str(row["target_framework"]).strip(),
                target_id=str(row["target_id"]).strip(),
                relationship=rel,
            )
        )
    return mappings
