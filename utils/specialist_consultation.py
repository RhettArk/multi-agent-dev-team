# utils/specialist_consultation.py
"""Utilities for coordinator to consult specialists during planning."""

from typing import Dict, List
import json


async def consult_specialist(specialist_name: str, question: str, context: Dict) -> str:
    """
    Consult a specialist for their input during planning phase.

    Args:
        specialist_name: Name of specialist to consult (e.g., 'backend-architect')
        question: Question to ask the specialist
        context: Context dict with relevant info (feature description, current KB state, etc.)

    Returns:
        Specialist's response as string
    """
    # In actual implementation, this would invoke the specialist via Task tool
    # For now, placeholder that constructs consultation prompt

    _prompt = f"""
You are being consulted during the planning phase.

Context:
{json.dumps(context, indent=2)}

Question from coordinator:
{question}

Provide your expert input for planning this feature. Focus on:
- What tasks are needed in your domain
- Dependencies on other domains
- Potential challenges or risks
- Estimated complexity

Keep response concise (2-3 paragraphs).
"""

    # TODO: Invoke specialist via Task tool with prompt
    # For now, return placeholder
    return f"[Consultation response from {specialist_name}]"


async def consult_all_relevant_specialists(
    feature_description: str,
    domains_affected: List[str],
    kb_state: Dict
) -> Dict[str, str]:
    """
    Consult all relevant specialists for a feature.

    Args:
        feature_description: User's feature request
        domains_affected: List of domains (e.g., ['backend', 'frontend'])
        kb_state: Current KB state (patterns, recent decisions)

    Returns:
        Dict mapping specialist name to their consultation response
    """
    domain_specialist_map = {
        'backend': ['backend-architect', 'backend-design'],
        'backend-api': ['fastapi-specialist', 'backend-design'],
        'backend-agents': ['openai-agents-sdk'],
        'backend-deployment': ['docker-specialist'],
        'frontend': ['ui-ux', 'javascript-specialist'],
        'frontend-3d': ['matterport-sdk'],
        'frontend-chat': ['chat-specialist']
    }

    specialists_to_consult = set()
    for domain in domains_affected:
        specialists_to_consult.update(domain_specialist_map.get(domain, []))

    # Always consult code reviewer for cleanup assessment
    specialists_to_consult.add('code-reviewer')

    context = {
        'feature_description': feature_description,
        'kb_state': kb_state
    }

    responses = {}
    for specialist in specialists_to_consult:
        question = get_consultation_question(specialist, feature_description)
        response = await consult_specialist(specialist, question, context)
        responses[specialist] = response

    return responses


def get_consultation_question(specialist: str, feature_description: str) -> str:
    """Generate domain-specific consultation question."""
    questions = {
        'backend-architect': f"What's the high-level architecture approach for: {feature_description}?",
        'fastapi-specialist': f"What endpoints/routes are needed for: {feature_description}?",
        'backend-design': f"What API schemas and data models are needed for: {feature_description}?",
        'openai-agents-sdk': f"What agents or tools are needed for: {feature_description}?",
        'docker-specialist': f"Any container config changes needed for: {feature_description}?",
        'ui-ux': f"What UI components and designs are needed for: {feature_description}?",
        'javascript-specialist': f"What JavaScript modules are needed for: {feature_description}?",
        'matterport-sdk': f"Any Matterport SDK integration needed for: {feature_description}?",
        'chat-specialist': f"Any chat/messaging features needed for: {feature_description}?",
        'code-reviewer': f"Any existing code that should be refactored before implementing: {feature_description}?",
        'code-quality-frontend': f"Any frontend code quality concerns for: {feature_description}?"
    }
    return questions.get(specialist, f"Your input for: {feature_description}?")
