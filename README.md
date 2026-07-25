# NIST-800-53-Control-Mapper

Cross-framework security control mapping tool that helps organizations reduce duplicate compliance work by mapping controls across NIST 800-53, ISO 27001, and SOC 2.

## Overview

Compliance teams often duplicate effort when working with multiple frameworks. This tool provides intelligent mapping between:

- **NIST 800-53** & **NIST 800-171** & **NIST CSF** (Federal security controls and frameworks)
- **ISO 27001** (International security standard)
- **SOC 2** (Trust Service Criteria, Types 1, 2, and 3)
- **HITRUST** (Healthcare Information Trust Alliance)
- **HIPAA** (Health Insurance Portability and Accountability Act)

**Recent Data Ingestions:**
- Extracted and integrated over **1,500 base controls** and **4,000+ cross-mappings** directly from the **Secure Controls Framework (SCF)** (version 2026.2).
- Ingested over **22,000 cross-compliance mappings** from the **Open Security Architecture (OSA)** project, heavily expanding mapping coverage for NIST 800-53 across dozens of other proprietary and open frameworks (PCI-DSS, CIS, COBIT, etc).

By identifying equivalent and related controls across frameworks, organizations can:
- Avoid duplicate assessments
- Streamline multi-framework audits
- Demonstrate control coverage across standards
- Accelerate compliance programs

## Project Structure

```
NIST-800-53-Control-Mapper/
├── README.md
├── requirements.txt
├── data/
│   ├── nist80053_controls.csv
│   ├── iso27001_controls.csv
│   ├── soc2_controls.csv
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
git clone https://github.com/imane2030/NIST-800-53-Control-Mapper.git
cd NIST-800-53-Control-Mapper
pip install -r requirements.txt
```

## Usage

### Map a Single Control

```bash
python cli.py map-control --framework NIST800-53 --control-id AC-2
```

Output:
```
| Source          | Target         | Target Name                    | Relationship |
|-----------------|----------------|--------------------------------|--------------|
| NIST800-53 AC-2 | ISO27001 A.9.2.1| User registration             | equivalent   |
| NIST800-53 AC-2 | SOC2 CC6.3     | Multi-factor authentication   | related      |
```

### Map Entire Framework

```bash
python cli.py map-framework --source-framework NIST800-53 --target-framework SOC2
```

## Data Format

### Control Definition (controls CSV)

```csv
id,name,description
AC-2,Account Management,"Manages information system accounts..."
```

### Mapping Definition (mappings.csv)

```csv
source_framework,source_id,target_framework,target_id,relationship
NIST800-53,AC-2,ISO27001,A.9.2.1,equivalent
NIST800-53,AC-2,SOC2,CC6.3,related
```

### Relationship Types

- **equivalent**: Controls serve the same purpose
- **related**: Controls address similar objectives
- **partial**: Source control partially satisfies target

## Example Use Cases

### 1. Multi-Framework Audit Planning

Identify which NIST controls satisfy SOC 2 requirements:

```bash
python cli.py map-framework --source-framework NIST800-53 --target-framework SOC2 > audit_coverage.md
```

### 2. Gap Analysis

Find ISO 27001 controls not covered by existing NIST implementation:

```bash
python cli.py map-framework --source-framework ISO27001 --target-framework NIST800-53
```

### 3. Control Rationalization

Consolidate overlapping controls across multiple compliance programs.

## Data Sources

Mapping data is derived from:
- NIST SP 800-53 Rev. 5 official documentation
- ISO/IEC 27001:2013 Annex A
- AICPA SOC 2 Trust Service Criteria
- NIST 800-53/ISO 27001 crosswalk documents
- Open Security Architecture (OSA) Data Repository
- Secure Controls Framework (SCF)
- Industry compliance mapping resources

## Extending the Tool

### Add New Framework

1. Create a CSV file in the `data/` directory. The file name must end with `_controls.csv`. The framework name will be derived from the filename (e.g., `newframework_controls.csv` -> `NEWFRAMEWORK`).
   ```csv
   id,name,description
   CONTROL-1,Control Name,Description...
   ```

2. Add mappings in `data/mappings.csv`:
   ```csv
   NIST800-53,AC-2,NEWFRAMEWORK,CONTROL-1,equivalent
   ```

*(The CLI now dynamically scans and loads all `*_controls.csv` files in the `data/` directory automatically, so no code changes are required to add new frameworks!)*

### Custom Queries

Use the Python API directly:

```python
from mapper.loader import load_controls, load_mappings
from mapper.engine import ControlMapper

controls = load_controls("data/nist80053_controls.csv", "NIST800-53")
mappings = load_mappings("data/mappings.csv")
mapper = ControlMapper(controls, mappings)

# Find all mappings for a control
results = mapper.map_control("NIST800-53", "AC-2")
for mapping, target_control in results:
    print(f"{mapping.target_framework} {mapping.target_id}: {target_control.name}")
```

## Requirements

- Python 3.7+
- Dependencies: pydantic, pandas, tabulate, pyyaml

## Contributing

Contributions welcome! Areas for improvement:
- Additional framework mappings (CIS Controls, PCI-DSS, HIPAA)
- Enhanced relationship types
- Web-based UI
- Export to common formats (Excel, JSON, PDF)
- Integration with GRC platforms

## License

MIT License

## Author

Imane Errayes - [imanologya.substack.com](https://imanologya.substack.com)

---

**Note**: Control mappings are approximations based on publicly available crosswalk documents. Always validate mappings with qualified auditors for your specific compliance requirements.
