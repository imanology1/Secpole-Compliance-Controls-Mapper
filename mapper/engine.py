from collections import defaultdict
from .models import Control, Mapping

class ControlMapper:
    """Main engine for mapping controls across frameworks."""
    
    def __init__(self, controls, mappings):
        self.controls = controls
        self.mappings = mappings
        
        # Build lookup indexes
        self.controls_by_key = {
            (c.framework, c.id): c for c in controls
        }
        
        self.index = defaultdict(list)
        for m in mappings:
            # Forward mapping
            self.index[(m.source_framework, m.source_id)].append(m)
            # Bidirectional/Reverse mapping
            reverse_m = Mapping(
                source_framework=m.target_framework,
                source_id=m.target_id,
                target_framework=m.source_framework,
                target_id=m.source_id,
                relationship=m.relationship
            )
            self.index[(m.target_framework, m.target_id)].append(reverse_m)

    def map_control(self, source_framework: str, source_id: str):
        """Find all mappings for a specific control."""
        key = (source_framework, source_id)
        mappings = self.index.get(key, [])
        
        results = []
        for m in mappings:
            target_key = (m.target_framework, m.target_id)
            target_control = self.controls_by_key.get(target_key)
            
            if target_control:
                results.append((m, target_control))
        
        return results

    def map_framework(self, source_framework: str, target_framework: str):
        """Map all controls from one framework to another."""
        results = []
        
        for (fw, cid), control in self.controls_by_key.items():
            if fw != source_framework:
                continue
            
            mapped = [
                (m, tc) for (m, tc) in self.map_control(source_framework, cid)
                if m.target_framework == target_framework
            ]
            
            if mapped:
                results.append((control, mapped))
        
        return results

    def get_coverage(self, source_framework: str, target_framework: str):
        """Calculate mapping coverage percentage."""
        source_controls = [
            c for c in self.controls if c.framework == source_framework
        ]
        
        mapped_count = 0
        for control in source_controls:
            mappings = self.map_control(source_framework, control.id)
            if any(m.target_framework == target_framework for m, _ in mappings):
                mapped_count += 1
        
        total = len(source_controls)
        coverage = (mapped_count / total * 100) if total > 0 else 0
        
        return {
            "source_framework": source_framework,
            "target_framework": target_framework,
            "total_controls": total,
            "mapped_controls": mapped_count,
            "coverage_percent": round(coverage, 2)
        }
