from collections import defaultdict
from .models import Control, Mapping


class UnknownFrameworkError(ValueError):
    """Raised when a query names a framework that appears nowhere in the data."""


class ControlMapper:
    """Main engine for mapping controls across frameworks."""

    def __init__(self, controls, mappings):
        self.controls = controls
        self.mappings = mappings

        self.controls_by_key = {(c.framework, c.id): c for c in controls}
        self.frameworks_with_controls = {c.framework for c in controls}

        # Full set of ids known per framework: defined controls OR referenced
        # by a mapping. Coverage is measured against this, not just the local
        # CSV rows (bug #1).
        self.ids_by_framework = defaultdict(set)
        self.defined_ids_by_framework = defaultdict(set)
        for c in controls:
            self.ids_by_framework[c.framework].add(c.id)
            self.defined_ids_by_framework[c.framework].add(c.id)

        self.index = defaultdict(list)
        for m in mappings:
            self.index[(m.source_framework, m.source_id)].append(m)
            reverse_m = Mapping(
                source_framework=m.target_framework,
                source_id=m.target_id,
                target_framework=m.source_framework,
                target_id=m.source_id,
                relationship=m.relationship,
            )
            self.index[(m.target_framework, m.target_id)].append(reverse_m)
            self.ids_by_framework[m.source_framework].add(m.source_id)
            self.ids_by_framework[m.target_framework].add(m.target_id)

        self.known_frameworks = set(self.ids_by_framework.keys())

    def _require_framework(self, framework: str):
        if framework not in self.known_frameworks:
            raise UnknownFrameworkError(
                f"Unknown framework '{framework}'. "
                f"Known frameworks: {', '.join(sorted(self.known_frameworks))}"
            )

    def map_control(self, source_framework: str, source_id: str):
        """Find all mappings for a specific control."""
        self._require_framework(source_framework)
        key = (source_framework, source_id)
        mappings = self.index.get(key, [])

        results = []
        for m in mappings:
            target_key = (m.target_framework, m.target_id)
            target_control = self.controls_by_key.get(target_key)
            if not target_control:
                target_control = Control(
                    framework=m.target_framework,
                    id=m.target_id,
                    name="Unknown (Control details not loaded)",
                    description="",
                )
            results.append((m, target_control))
        return results

    def map_framework(self, source_framework: str, target_framework: str):
        """Map all controls from one framework to another."""
        self._require_framework(source_framework)
        self._require_framework(target_framework)

        results = []
        for cid in sorted(self.ids_by_framework[source_framework]):
            control = self.controls_by_key.get((source_framework, cid))
            if control is None:
                control = Control(
                    framework=source_framework,
                    id=cid,
                    name="Unknown (Control details not loaded)",
                    description="",
                )
            mapped = [
                (m, tc)
                for (m, tc) in self.map_control(source_framework, cid)
                if m.target_framework == target_framework
            ]
            if mapped:
                results.append((control, mapped))
        return results

    def get_coverage(self, source_framework: str, target_framework: str):
        """Calculate mapping coverage percentage against the full known id set."""
        self._require_framework(source_framework)
        self._require_framework(target_framework)

        source_ids = self.ids_by_framework[source_framework]
        mapped_count = 0
        for cid in source_ids:
            mappings = self.map_control(source_framework, cid)
            if any(m.target_framework == target_framework for m, _ in mappings):
                mapped_count += 1

        total = len(source_ids)
        coverage = (mapped_count / total * 100) if total > 0 else 0
        return {
            "source_framework": source_framework,
            "target_framework": target_framework,
            "total_controls": total,
            "defined_controls": len(self.defined_ids_by_framework[source_framework]),
            "mapped_controls": mapped_count,
            "coverage_percent": round(coverage, 2),
        }
