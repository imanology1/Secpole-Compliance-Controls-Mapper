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
        print(f"Coverage: {coverage['coverage_percent']}%")
        print(f"Weighted Coverage: {coverage['weighted_coverage_percent']}% "
              f"(equivalent=1.0, partial=0.5, related=0.25)\n")

def cmd_gap(args):
    """List source controls with no mapping to the target framework."""
    mapper = build_mapper()
    gaps = mapper.get_gaps(args.source_framework, args.target_framework)
    if not gaps:
        print(f"No gaps: every {args.source_framework} control maps to {args.target_framework}")
        return
    rows = [[g["id"], g["name"]] for g in gaps]
    headers = ["Unmapped Control", "Name"]
    if args.format == "json":
        print(json.dumps(gaps, indent=2))
    elif args.format == "csv":
        writer = csv.writer(sys.stdout); writer.writerow(headers); writer.writerows(rows)
    else:
        print(f"\n{len(gaps)} {args.source_framework} controls with NO mapping to "
              f"{args.target_framework}:\n")
        print(tabulate(rows, headers=headers, tablefmt="github"))

def cmd_trace(args):
    """Find a multi-hop path from a control to a target framework."""
    mapper = build_mapper()
    path = mapper.find_path(args.framework, args.control_id,
                            args.target_framework, max_hops=args.max_hops)
    if not path:
        print(f"No path from {args.framework} {args.control_id} to "
              f"{args.target_framework} within {args.max_hops} hops")
        return
    chain = f"{path[0].source_framework} {path[0].source_id}"
    for m in path:
        chain += f"  --[{m.relationship}]-->  {m.target_framework} {m.target_id}"
    print(f"\n{chain}\n({len(path)} hop{'s' if len(path)!=1 else ''})\n")

def cmd_map_transitive(args):
    """Map a control to a target framework, walking intermediate frameworks."""
    mapper = build_mapper()
    results = mapper.map_control_transitive(
        args.framework, args.control_id, args.target_framework, max_hops=args.max_hops)
    if not results:
        print(f"No transitive mappings from {args.framework} {args.control_id} "
              f"to {args.target_framework} within {args.max_hops} hops")
        return
    rows = [[f"{r['target'].framework} {r['target'].id}", r['target'].name,
             r['hops'], r['confidence']] for r in results]
    headers = ["Target", "Target Name", "Hops", "Confidence"]
    if args.format == "json":
        out = [{"target_framework": r['target'].framework, "target_id": r['target'].id,
                "target_name": r['target'].name, "hops": r['hops'],
                "confidence": r['confidence']} for r in results]
        print(json.dumps(out, indent=2))
    elif args.format == "csv":
        writer = csv.writer(sys.stdout); writer.writerow(headers); writer.writerows(rows)
    else:
        print(tabulate(rows, headers=headers, tablefmt="github"))

def cmd_report(args):
    """Generate a formatted Excel coverage report across framework pairs."""
    from mapper.report import build_report
    mapper = build_mapper()
    frameworks = [f.strip() for f in args.frameworks.split(",") if f.strip()]
    out_path = build_report(mapper, frameworks, args.output)
    print(f"Report written to {out_path}")

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

    # Gap analysis
    p4 = sub.add_parser("gap", help="List source controls with no mapping to target")
    p4.add_argument("--source-framework", required=True)
    p4.add_argument("--target-framework", required=True)
    p4.add_argument("--format", choices=["table", "json", "csv"], default="table")
    p4.set_defaults(func=cmd_gap)

    # Trace a multi-hop path
    p5 = sub.add_parser("trace", help="Find a multi-hop path between a control and a framework")
    p5.add_argument("--framework", required=True)
    p5.add_argument("--control-id", required=True)
    p5.add_argument("--target-framework", required=True)
    p5.add_argument("--max-hops", type=int, default=3)
    p5.set_defaults(func=cmd_trace)

    # Transitive mapping
    p6 = sub.add_parser("map-transitive", help="Map a control across intermediate frameworks")
    p6.add_argument("--framework", required=True)
    p6.add_argument("--control-id", required=True)
    p6.add_argument("--target-framework", required=True)
    p6.add_argument("--max-hops", type=int, default=3)
    p6.add_argument("--format", choices=["table", "json", "csv"], default="table")
    p6.set_defaults(func=cmd_map_transitive)

    # Excel report
    p7 = sub.add_parser("report", help="Generate an Excel coverage report")
    p7.add_argument("--frameworks", required=True,
                    help="Comma-separated frameworks to cross-compare (e.g. NIST800-53,SOC2,ISO27001)")
    p7.add_argument("--output", default="secpol_report.xlsx", help="Output .xlsx path")
    p7.set_defaults(func=cmd_report)

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
