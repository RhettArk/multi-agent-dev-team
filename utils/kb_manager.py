# utils/kb_manager.py
"""Knowledge base initialization and management."""

import os
import json
from pathlib import Path
from typing import List

KB_DIR = Path("kb")

def initialize_kb():
    """Create KB directory structure if it doesn't exist."""
    KB_DIR.mkdir(exist_ok=True)

    # Create empty pattern files if they don't exist
    patterns = ["backend-patterns.md", "frontend-patterns.md", "api-contracts.md"]
    for pattern in patterns:
        path = KB_DIR / pattern
        if not path.exists():
            path.write_text(f"# {pattern.replace('-', ' ').title()}\n\n")

    # Create empty decisions log
    log_path = KB_DIR / "decisions.log"
    if not log_path.exists():
        log_path.write_text("# Decision Log\n\n")

    # Create empty dependencies graph
    deps_path = KB_DIR / "dependencies.json"
    if not deps_path.exists():
        deps_path.write_text(json.dumps({}, indent=2))


def verify_kb_exists() -> bool:
    """Check if KB is initialized."""
    return KB_DIR.exists() and (KB_DIR / "decisions.log").exists()


def log_decision(specialist: str, decision: str, rationale: str, affects: List[str], ref: str = ""):
    """Append decision to KB log."""
    from datetime import datetime

    log_path = KB_DIR / "decisions.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    entry = f"[{timestamp}] [{specialist}] Decision: {decision}\n"
    entry += f"Rationale: {rationale}\n"
    entry += f"Affects: {', '.join(affects)}\n"
    if ref:
        entry += f"Ref: {ref}\n"
    entry += "\n"

    with log_path.open('a') as f:
        f.write(entry)
