# utils/auto_planner.py
"""Auto-planning module for coordinator."""

from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
from specialist_consultation import consult_all_relevant_specialists


async def auto_plan_feature(
    feature_description: str,
    user_hints: Optional[Dict] = None
) -> Dict:
    """
    Auto-generate implementation plan by consulting specialists.

    Args:
        feature_description: User's feature request
        user_hints: Optional hints like domains_affected, constraints

    Returns:
        Plan dict with tasks, dependencies, and scope boundaries
    """
    # Step 1: Analyze feature to determine domains affected
    domains = analyze_domains(feature_description, user_hints)

    # Step 2: Load KB state
    kb_state = load_kb_state()

    # Step 3: Consult specialists
    specialist_responses = await consult_all_relevant_specialists(
        feature_description,
        domains,
        kb_state
    )

    # Step 4: Synthesize plan from specialist input
    plan = synthesize_plan(
        feature_description,
        specialist_responses,
        domains
    )

    return plan


def analyze_domains(feature_description: str, user_hints: Optional[Dict] = None) -> List[str]:
    """
    Analyze feature description to determine affected domains.

    Uses keyword matching and user hints.
    """
    hints = user_hints or {}
    if hints and 'domains' in hints:
        return hints['domains']

    domains = []

    # Keyword-based domain detection
    backend_keywords = ['api', 'endpoint', 'database', 'backend', 'server', 'agent', 'tool']
    frontend_keywords = ['ui', 'component', 'frontend', 'client', 'interface']
    docker_keywords = ['container', 'docker', 'deploy']
    chat_keywords = ['chat', 'message', 'conversation']
    matterport_keywords = ['3d', 'matterport', 'viewer', 'mattertag']

    desc_lower = feature_description.lower()

    if any(kw in desc_lower for kw in backend_keywords):
        domains.append('backend')
    if any(kw in desc_lower for kw in frontend_keywords):
        domains.append('frontend')
    if any(kw in desc_lower for kw in docker_keywords):
        domains.append('backend-deployment')
    if any(kw in desc_lower for kw in chat_keywords):
        domains.append('frontend-chat')
    if any(kw in desc_lower for kw in matterport_keywords):
        domains.append('frontend-3d')

    # Default to both if unclear
    if not domains:
        domains = ['backend', 'frontend']

    return domains


def load_kb_state() -> Dict:
    """Load current KB state (patterns, recent decisions)."""
    kb_dir = Path('kb')
    state = {
        'patterns': {},
        'recent_decisions': []
    }

    # Load pattern files
    pattern_files = [
        'backend-patterns.md',
        'frontend-patterns.md',
        'api-contracts.md',
        'openai-agents.md',
        'matterport-integration.md',
        'docker-patterns.md'
    ]

    for pattern_file in pattern_files:
        path = kb_dir / pattern_file
        if path.exists():
            state['patterns'][pattern_file] = path.read_text()

    # Load recent decisions (last 10)
    decisions_path = kb_dir / 'decisions.log'
    if decisions_path.exists():
        lines = decisions_path.read_text().split('\n')
        # Parse last 10 decision entries
        state['recent_decisions'] = lines[-50:]  # ~10 decisions (5 lines each)

    return state


def synthesize_plan(
    feature_description: str,
    specialist_responses: Dict[str, str],
    domains: List[str]
) -> Dict:
    """
    Synthesize plan from specialist consultation responses.

    Returns plan with:
    - Task breakdown
    - Dependencies
    - Scope boundaries
    - Success criteria
    """
    tasks = []
    task_id = 1

    # Order specialists by typical workflow
    workflow_order = [
        'code-reviewer',  # Pre-planning cleanup
        'backend-architect',
        'backend-design',
        'openai-agents-sdk',
        'fastapi-specialist',
        'docker-specialist',
        'ui-ux',
        'javascript-specialist',
        'matterport-sdk',
        'chat-specialist',
        'code-quality-frontend'
    ]

    previous_task_id = None

    for specialist in workflow_order:
        if specialist not in specialist_responses:
            continue

        _response = specialist_responses[specialist]

        # Extract task from specialist response
        # (In real implementation, parse response to extract task details)
        task_title = extract_task_title(specialist, _response)

        task = {
            'id': f'task-{task_id}',
            'title': task_title,
            'specialist': specialist,
            'status': 'pending',
            'dependencies': [previous_task_id] if previous_task_id else []
        }

        tasks.append(task)
        previous_task_id = f'task-{task_id}'
        task_id += 1

    plan = {
        'plan_id': f'auto-plan-{hash(feature_description) % 10000}',
        'created_at': datetime.now().isoformat(),
        'feature_description': feature_description,
        'domains_affected': domains,
        'tasks': {task['id']: task for task in tasks},
        'scope_boundaries': {
            'what_to_change': extract_scope_from_responses(specialist_responses, 'change'),
            'what_not_to_change': extract_scope_from_responses(specialist_responses, 'preserve')
        },
        'success_criteria': [
            'All tasks completed successfully',
            'KB updated with new patterns',
            'No breaking changes to existing functionality'
        ]
    }

    return plan


def extract_task_title(specialist: str, _response: str) -> str:
    """Extract task title from specialist response."""
    # Placeholder - in real implementation, parse response
    titles = {
        'code-reviewer': 'Pre-planning cleanup: remove dead code',
        'backend-architect': 'Design architecture',
        'backend-design': 'Design API schemas',
        'fastapi-specialist': 'Implement endpoints',
        'openai-agents-sdk': 'Create agents and tools',
        'docker-specialist': 'Update container config',
        'ui-ux': 'Design and implement UI',
        'javascript-specialist': 'Implement JavaScript logic',
        'matterport-sdk': 'Integrate Matterport SDK',
        'chat-specialist': 'Implement chat features',
        'code-quality-frontend': 'Review and optimize frontend'
    }
    return titles.get(specialist, f'{specialist} task')


def extract_scope_from_responses(_responses: Dict[str, str], scope_type: str) -> List[str]:
    """Extract scope boundaries from specialist responses."""
    # Placeholder - in real implementation, parse responses for scope mentions
    return [
        f'Items to {scope_type} based on specialist input',
        '(Extracted from consultation responses)'
    ]
