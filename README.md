# Secpol - Security Policy & Control Mapper

Secpol is a comprehensive, cross-framework security control mapping tool designed to help organizations reduce duplicate compliance work by mapping controls across dozens of regulatory, privacy, and security frameworks.

## Overview

Compliance and governance teams often duplicate effort when working with multiple frameworks. Secpol provides an intelligent, bidirectional mapping engine that translates controls between over 100 frameworks natively.

By identifying equivalent and related controls across frameworks, organizations can:
- Avoid duplicate assessments
- Streamline multi-framework audits
- Demonstrate control coverage across standards
- Accelerate AI governance and compliance programs

### Supported Frameworks (Included Data)
Secpol natively includes tens of thousands of mapping relationships powered by leading open-source meta-frameworks (like the Open Security Architecture and the Secure Controls Framework). Included out-of-the-box are:
- **Federal & Defense:** NIST 800-53, NIST 800-171, NIST CSF
- **International & Privacy:** ISO 27001, GDPR
- **Trust & Commercial:** SOC 2 (Trust Service Criteria, Types 1, 2, and 3), PCI-DSS
- **Healthcare:** HIPAA, HITRUST
- **AI Governance:** EU AI Act, NIST AI RMF, ISO 42001
- **Meta Frameworks:** Secure Controls Framework (SCF)

## Project Structure

```text
Secpol/
├── README.md
├── requirements.txt
├── data/
│   ├── nist80053_controls.csv
│   ├── iso27001_controls.csv
│   ├── scf_controls.csv
│   ├── [...other framework _controls.csv files...]
│   └── mappings.csv
├── mapper/
│   ├── __init__.py
│   ├── models.py
│   ├── loader.py
│   └── engine.py
└── cli.py
```

## Installation

```bash
git clone <repository_url>
cd Secpole-Compliance-Controls-Mapper
pip install -r requirements.txt
```

## Usage

Secpol operates via a powerful command-line interface (`cli.py`). All commands support outputting to `table` (default), `json`, or `csv` via the `--format` flag.

### Map a Single Control

Find all known mappings for a specific control across every available framework.

```bash
python cli.py map-control --framework NIST800-53 --control-id AC-2
```

### Map Entire Frameworks

Analyze the overlap between two distinct frameworks to conduct gap assessments.

```bash
python cli.py map-framework --source-framework NIST800-53 --target-framework SOC2 --format json
```

### Calculate Coverage

Calculate what percentage of a source framework is covered by a target framework.

```bash
python cli.py coverage --source-framework SCF --target-framework NIST800-53
```

Coverage now reports both a plain percentage and a **weighted** percentage
(equivalent=1.0, partial=0.5, related=0.25), plus how many controls are locally
defined versus known only through mappings.

### Gap Analysis

List the specific source controls that have **no** mapping to a target — the
inverse of coverage, and the actual audit deliverable.

```bash
python cli.py gap --source-framework NIST800-53 --target-framework SOC2
```

### Multi-Hop Mapping (transitive reach)

Frameworks are connected through pivots like the SCF. These commands walk chains
of mappings so you can reach a target framework even with no direct mapping.

```bash
# Show the shortest chain connecting a control to a framework
python cli.py trace --framework SOC2 --control-id CC6.3 --target-framework NIST-CSF

# List every target control reachable within N hops, with a confidence score
python cli.py map-transitive --framework NIST800-53 --control-id AC-2 \
    --target-framework ISO27001 --max-hops 3
```

Confidence is the product of edge strengths along the path, so a 3-hop chain of
`related` links scores far lower than a direct `equivalent` mapping.

### Excel Report

Generate a formatted `.xlsx` with an N×N coverage matrix and a detail sheet
(mapped controls + gaps) for every framework pair.

```bash
python cli.py report --frameworks "NIST800-53,SOC2,ISO27001" --output report.xlsx
```

## Data Sources & Extending the Tool

### Data Sources
Secpol's mapping intelligence is derived from over 26,000+ relationships extracted from:
- The Secure Controls Framework (SCF)
- The Open Security Architecture (OSA) Data Repository
- Official NIST, ISO, and AICPA crosswalk documents

### Add New Frameworks

Secpol dynamically discovers and loads frameworks. **No code changes are required to add a new framework.**

1. **Add Controls:** Create a CSV file in the `data/` directory. The file name must end with `_controls.csv`. The framework name will be automatically derived from the filename (e.g., `gdpr_controls.csv` -> `GDPR`).
   ```csv
   id,name,description
   Art.32,Security of processing,Taking into account the state of the art...
   ```

2. **Add Mappings:** Append your mappings in `data/mappings.csv`:
   ```csv
   NIST800-53,AC-2,GDPR,Art.32,related
   ```

*Note: The Secpol engine handles missing definitions gracefully. If you map to a target control that doesn't have a defined description in a `_controls.csv` file, the tool will still display the mapping relationship successfully.*

## Custom API Queries

Secpol can be imported and used natively in Python scripts to build GRC dashboards or automation:

```python
from mapper.engine import ControlMapper
from mapper.loader import load_controls, load_mappings
import glob
import os

# Dynamically load all frameworks
controls = []
for file_path in glob.glob("data/*_controls.csv"):
    framework = os.path.basename(file_path).replace("_controls.csv", "").upper().replace("_", "")
    controls += load_controls(file_path, framework)

mappings = load_mappings("data/mappings.csv")
mapper = ControlMapper(controls, mappings)

# Execute bidirectional mapping queries
results = mapper.map_control("EU-AIACT", "Article 17.1")
```

## Requirements
- Python 3.7+
- Dependencies: pydantic, pandas, tabulate, pyyaml

## License
MIT License
