import argparse
import json
import csv
import sys
from tabulate import tabulate
from mapper.loader import load_controls, load_mappings
from mapper.engine import ControlMapper, UnknownFrameworkError
from mapper.frameworks import discover_control_files

def build_mapper():
    """Load all controls and mappings, return mapper instance."""
    controls = []

    # Dynamically load controls from all *_controls.csv files in data/.
    # Framework naming is centralized in mapper.frameworks (single source of truth).
    for file_path, framework in discover_control_files("data"):
        try:
            controls += load_controls(file_path, framework)
        except Exception as e:
            print(f"Warning: Failed to load controls from {file_path}: {e}")

    try:
        mappings = load_mappings("data/mappings.csv")
    except FileNotFoundError:
        print("Error: Mappings file not found")
        mappings = []

    return ControlMapper(controls, mappings)

def cmd_map_control(args):
    """Map a single control to other frameworks."""
    mapper = build_mapper()
    mappings = mapper.map_control(args.framework, args.control_id)

    if not mappings:
        print(f"No mappings found for {args.framework} {args.control_id}")
        return

    rows = []
    for mapping, target in mappings:
        rows.append([
            f"{mapping.source_framework} {mapping.source_id}",
            f"{mapping.target_framework} {mapping.target_id}",
            target.name,
            mapping.relationship,
        ])

    headers = ["Source", "Target", "Target Name", "Relationship"]
    if args.format == "json":
        json_data = [dict(zip(headers, row)) for row in rows]
        print(json.dumps(json_data, indent=2))
    elif args.format == "csv":
        writer = csv.writer(sys.stdout)
        writer.writerow(headers)
        writer.writerows(rows)
    else:
        print(tabulate(
            rows,
            headers=headers,
            tablefmt="github"
        ))

def cmd_map_framework(args):
    """Map entire framework to another framework."""
    mapper = build_mapper()
    results = mapper.map_framework(args.source_framework, args.target_framework)

    if not results:
        print(f"No mappings found between {args.source_framework} and {args.target_framework}")
        return

    rows = []
    for control, mappings in results:
        for mapping, target in mappings:
            rows.append([
                f"{control.framework} {control.id}",
                control.name,
                f"{target.framework} {target.id}",
                target.name,
                mapping.relationship,
            ])

    headers = ["Source", "Source Name", "Target", "Target Name", "Rel"]
    if args.format == "json":
        json_data = [dict(zip(headers, row)) for row in rows]
        print(json.dumps(json_data, indent=2))
    elif args.format == "csv":
        writer = csv.writer(sys.stdout)
        writer.writerow(headers)
        writer.writerows(rows)
    else:
        print(tabulate(
            rows,
            headers=headers,
            tablefmt="github",
        ))

def cmd_coverage(args):
    """Show mapping coverage statistics."""
    mapper = build_mapper()
    coverage = mapper.get_coverage(args.source_framework, args.target_framework)
    
    if args.format == "json":
        print(json.dumps(coverage, indent=2))
    elif args.format == "csv":
        writer = csv.writer(sys.stdout)
        writer.writerow(coverage.keys())
        writer.writerow(coverage.values())
    else:
        print(f"\n=== Mapping Coverage ===")
        print(f"Source Framework: {coverage['source_framework']}")
        print(f"Target Framework: {coverage['target_framework']}")
        print(f"Total Known Controls: {coverage['total_controls']}")
        print(f"  (of which locally defined: {coverage['defined_controls']})")
        print(f"Mapped Controls: {coverage['mapped_controls']}")
        print(f"Coverage: {coverage['coverage_percent']}%\n")

def main():
    parser = argparse.ArgumentParser(
        description="NIST 800-53 Control Mapper - Map security controls across frameworks"
    )
    sub = parser.add_subparsers()

    # Map single control
    p1 = sub.add_parser("map-control", help="Map a single control")
    p1.add_argument("--framework", required=True, help="Source framework (e.g., NIST800-53)")
    p1.add_argument("--control-id", required=True, help="Control ID (e.g., AC-2)")
    p1.add_argument("--format", choices=["table", "json", "csv"], default="table", help="Output format")
    p1.set_defaults(func=cmd_map_control)

    # Map entire framework
    p2 = sub.add_parser("map-framework", help="Map an entire framework to another")
    p2.add_argument("--source-framework", required=True, help="Source framework")
    p2.add_argument("--target-framework", required=True, help="Target framework")
    p2.add_argument("--format", choices=["table", "json", "csv"], default="table", help="Output format")
    p2.set_defaults(func=cmd_map_framework)

    # Coverage statistics
    p3 = sub.add_parser("coverage", help="Show mapping coverage statistics")
    p3.add_argument("--source-framework", required=True, help="Source framework")
    p3.add_argument("--target-framework", required=True, help="Target framework")
    p3.add_argument("--format", choices=["table", "json", "csv"], default="table", help="Output format")
    p3.set_defaults(func=cmd_coverage)

    args = parser.parse_args()

    if hasattr(args, "func"):
        try:
            args.func(args)
        except UnknownFrameworkError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
