"""Single source of truth for framework naming.

Control-definition files are named `<slug>_controls.csv`. The raw slug
(uppercased, underscores stripped) does not always match the framework name
used inside data/mappings.csv. This module centralizes that translation so
the CLI, the API, and any scripts all agree — previously the mapping was
duplicated as an if/elif ladder in three separate places (bug #4).

To onboard a framework whose file slug differs from its mapping name, add one
entry to FILE_SLUG_TO_FRAMEWORK below. No other code changes required.
"""

import glob
import os

# Maps the derived file slug (basename minus _controls.csv, uppercased,
# underscores removed) to the canonical framework name used in mappings.csv.
# Anything not listed here is used as-is.
FILE_SLUG_TO_FRAMEWORK = {
    "NIST80053": "NIST800-53",
    "NIST800171": "NIST800-171",
    "NISTCSF": "NIST-CSF",
    "EUAIACT": "EU-AIACT",
    "NISTAIRMF": "NIST-AIRMF",
}


def framework_from_filename(path: str) -> str:
    """Derive the canonical framework name from a *_controls.csv path."""
    slug = os.path.basename(path).replace("_controls.csv", "").upper().replace("_", "")
    return FILE_SLUG_TO_FRAMEWORK.get(slug, slug)


def discover_control_files(data_dir: str = "data"):
    """Yield (path, framework_name) for every control file in data_dir.

    Skips any nested subdirectories (e.g. a stray data/data/) so duplicate
    copies can't silently double-load.
    """
    pattern = os.path.join(data_dir, "*_controls.csv")
    for path in sorted(glob.glob(pattern)):
        yield path, framework_from_filename(path)
