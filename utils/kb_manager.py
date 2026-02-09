# utils/kb_manager.py
"""Knowledge base initialization and management."""

import json
from pathlib import Path
from typing import List, Optional


def _get_kb_dir() -> Path:
    """Get KB directory relative to the plugin root, not the CWD."""
    # Look for kb/ relative to this file's location (the plugin root)
    plugin_root = Path(__file__).resolve().parent.parent
    return plugin_root / "kb"


def initialize_kb(kb_dir: Optional[Path] = None):
    """Create KB directory structure if it doesn't exist."""
    kb = kb_dir or _get_kb_dir()
    kb.mkdir(exist_ok=True)

    # Create empty pattern files if they don't exist
    patterns = ["backend-patterns.md", "frontend-patterns.md", "api-contracts.md"]
    for pattern in patterns:
        path = kb / pattern
        if not path.exists():
            path.write_text(f"# {pattern.replace('-', ' ').title()}\n\n")

    # Create empty decisions log
    log_path = kb / "decisions.log"
    if not log_path.exists():
        log_path.write_text("# Decision Log\n\n")

    # Create empty dependencies graph
    deps_path = kb / "dependencies.json"
    if not deps_path.exists():
        deps_path.write_text(json.dumps({}, indent=2))


def verify_kb_exists(kb_dir: Optional[Path] = None) -> bool:
    """Check if KB is initialized."""
    kb = kb_dir or _get_kb_dir()
    return kb.exists() and (kb / "decisions.log").exists()


def log_decision(specialist: str, decision: str, rationale: str, affects: List[str], ref: str = "", kb_dir: Optional[Path] = None):
    """Append decision to KB log."""
    from datetime import datetime

    kb = kb_dir or _get_kb_dir()
    log_path = kb / "decisions.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    entry = f"[{timestamp}] [{specialist}] Decision: {decision}\n"
    entry += f"Rationale: {rationale}\n"
    entry += f"Affects: {', '.join(affects)}\n"
    if ref:
        entry += f"Ref: {ref}\n"
    entry += "\n"

    with log_path.open('a') as f:
        f.write(entry)
