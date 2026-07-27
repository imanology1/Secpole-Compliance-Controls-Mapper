from collections import defaultdict, deque
from .models import Control, Mapping


# Relationship strength, used for weighted coverage and for choosing the
# strongest edge when several connect the same two controls.
RELATIONSHIP_WEIGHT = {
    "equivalent": 1.0,
    "partial": 0.5,
    "related": 0.25,
}
DEFAULT_WEIGHT = 0.25


def relationship_weight(rel: str) -> float:
    return RELATIONSHIP_WEIGHT.get((rel or "").lower(), DEFAULT_WEIGHT)


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

        # Weighted coverage: each mapped control contributes the strength of its
        # STRONGEST edge to the target, so a control reachable only via a
        # "related" mapping counts as 0.25, not a full 1.0.
        weighted_sum = 0.0
        for cid in source_ids:
            best = 0.0
            for m, _ in self.map_control(source_framework, cid):
                if m.target_framework == target_framework:
                    best = max(best, relationship_weight(m.relationship))
            weighted_sum += best
        weighted = (weighted_sum / total * 100) if total > 0 else 0

        return {
            "source_framework": source_framework,
            "target_framework": target_framework,
            "total_controls": total,
            "defined_controls": len(self.defined_ids_by_framework[source_framework]),
            "mapped_controls": mapped_count,
            "coverage_percent": round(coverage, 2),
            "weighted_coverage_percent": round(weighted, 2),
        }

    def get_gaps(self, source_framework: str, target_framework: str):
        """Return the source controls that have NO mapping to the target.

        The inverse of coverage: coverage says "how much is covered", gaps says
        exactly WHICH controls are not — the actual audit deliverable.
        """
        self._require_framework(source_framework)
        self._require_framework(target_framework)

        gaps = []
        for cid in sorted(self.ids_by_framework[source_framework]):
            has_mapping = any(
                m.target_framework == target_framework
                for m, _ in self.map_control(source_framework, cid)
            )
            if not has_mapping:
                control = self.controls_by_key.get((source_framework, cid))
                name = control.name if control else "Unknown (Control details not loaded)"
                gaps.append({"framework": source_framework, "id": cid, "name": name})
        return gaps

    def find_path(self, source_framework, source_id, target_framework, max_hops=3):
        """Find the shortest chain of mappings connecting a source control to a
        target framework, walking through intermediate frameworks (e.g. via SCF).

        Returns a list of Mapping hops (source -> ... -> target), or None if no
        path within max_hops. Breadth-first, so the first path found is shortest.
        Cycle-safe via a visited set on (framework, id) nodes.
        """
        self._require_framework(source_framework)
        self._require_framework(target_framework)

        start = (source_framework, source_id)
        if source_framework == target_framework:
            return []

        # queue holds (node, path_of_mappings)
        queue = deque([(start, [])])
        visited = {start}

        while queue:
            (fw, cid), path = queue.popleft()
            if len(path) >= max_hops:
                continue
            for m in self.index.get((fw, cid), []):
                nxt = (m.target_framework, m.target_id)
                new_path = path + [m]
                if m.target_framework == target_framework:
                    return new_path
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append((nxt, new_path))
        return None

    def map_control_transitive(self, source_framework, source_id, target_framework,
                               max_hops=3):
        """All target-framework controls reachable from a source control within
        max_hops, each with the shortest path and an aggregate confidence
        (product of edge weights along the path). Direct (1-hop) results are
        included with their full weight.
        """
        self._require_framework(source_framework)
        self._require_framework(target_framework)

        start = (source_framework, source_id)
        # best_path[node] = (path, confidence) — keep the shortest, then strongest
        best = {}
        queue = deque([(start, [], 1.0)])
        visited_depth = {start: 0}

        while queue:
            (fw, cid), path, conf = queue.popleft()
            if len(path) >= max_hops:
                continue
            for m in self.index.get((fw, cid), []):
                nxt = (m.target_framework, m.target_id)
                new_conf = conf * relationship_weight(m.relationship)
                new_path = path + [m]
                depth = len(new_path)

                if m.target_framework == target_framework:
                    prev = best.get(nxt)
                    if prev is None or depth < prev[0] or (
                        depth == prev[0] and new_conf > prev[1]
                    ):
                        best[nxt] = (depth, new_conf, new_path)

                # continue exploring if we haven't reached this node at a
                # shallower or equal depth already
                if visited_depth.get(nxt, 99) > depth:
                    visited_depth[nxt] = depth
                    queue.append((nxt, new_path, new_conf))

        results = []
        for (tfw, tid), (depth, conf, path) in best.items():
            tc = self.controls_by_key.get((tfw, tid)) or Control(
                framework=tfw, id=tid,
                name="Unknown (Control details not loaded)", description="",
            )
            results.append({
                "target": tc,
                "hops": depth,
                "confidence": round(conf, 4),
                "path": path,
            })
        # strongest, shortest first
        results.sort(key=lambda r: (r["hops"], -r["confidence"]))
        return results
