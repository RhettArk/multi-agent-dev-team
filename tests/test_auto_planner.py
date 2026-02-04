# tests/test_auto_planner.py
"""Tests for auto-planning module."""

import pytest
from utils.auto_planner import (
    analyze_domains,
    synthesize_plan,
    extract_task_title,
    extract_scope_from_responses,
    load_kb_state
)


class TestDomainAnalysis:
    """Tests for domain analysis functionality."""

    def test_analyze_domains_backend_keywords(self):
        """Test domain detection with backend-related keywords."""
        description = "Add a new API endpoint for user authentication"
        domains = analyze_domains(description)

        assert 'backend' in domains
        assert len(domains) >= 1

    def test_analyze_domains_frontend_keywords(self):
        """Test domain detection with frontend-related keywords."""
        description = "Create a new UI component for displaying user profile"
        domains = analyze_domains(description)

        assert 'frontend' in domains
        assert len(domains) >= 1

    def test_analyze_domains_both_keywords(self):
        """Test domain detection when both backend and frontend are mentioned."""
        description = "Add API endpoint and create UI component for chat feature"
        domains = analyze_domains(description)

        assert 'backend' in domains
        assert 'frontend' in domains

    def test_analyze_domains_docker_keywords(self):
        """Test domain detection with docker-related keywords."""
        description = "Update the docker container configuration for deployment"
        domains = analyze_domains(description)

        assert 'backend-deployment' in domains

    def test_analyze_domains_chat_keywords(self):
        """Test domain detection with chat-related keywords."""
        description = "Implement message streaming in the chat interface"
        domains = analyze_domains(description)

        assert 'frontend-chat' in domains

    def test_analyze_domains_matterport_keywords(self):
        """Test domain detection with Matterport 3D keywords."""
        description = "Add mattertag support to the 3D viewer"
        domains = analyze_domains(description)

        assert 'frontend-3d' in domains

    def test_analyze_domains_with_user_hints(self):
        """Test that user hints override automatic detection."""
        description = "Some generic feature description"
        user_hints = {'domains': ['backend', 'frontend-chat']}
        domains = analyze_domains(description, user_hints)

        assert domains == ['backend', 'frontend-chat']

    def test_analyze_domains_default_fallback(self):
        """Test that unclear descriptions default to both backend and frontend."""
        description = "Implement some generic feature"
        domains = analyze_domains(description)

        # Should default to both
        assert 'backend' in domains
        assert 'frontend' in domains

    def test_analyze_domains_case_insensitive(self):
        """Test that domain detection is case-insensitive."""
        description = "Add new API ENDPOINT for DATABASE queries"
        domains = analyze_domains(description)

        assert 'backend' in domains


class TestPlanSynthesis:
    """Tests for plan synthesis functionality."""

    def test_synthesize_plan_basic_structure(self):
        """Test that synthesize_plan creates valid plan structure."""
        feature_description = "Add login endpoint"
        specialist_responses = {
            'backend-architect': 'Design response',
            'fastapi-specialist': 'Implementation response'
        }
        domains = ['backend']

        plan = synthesize_plan(feature_description, specialist_responses, domains)

        # Verify plan structure
        assert 'plan_id' in plan
        assert 'created_at' in plan
        assert 'feature_description' in plan
        assert 'domains_affected' in plan
        assert 'tasks' in plan
        assert 'scope_boundaries' in plan
        assert 'success_criteria' in plan

        # Verify content
        assert plan['feature_description'] == feature_description
        assert plan['domains_affected'] == domains
        assert len(plan['tasks']) == 2

    def test_synthesize_plan_task_ordering(self):
        """Test that tasks follow workflow order."""
        specialist_responses = {
            'fastapi-specialist': 'Response',
            'backend-architect': 'Response',  # Should come before fastapi
            'docker-specialist': 'Response'
        }
        domains = ['backend']

        plan = synthesize_plan("Test feature", specialist_responses, domains)
        task_ids = list(plan['tasks'].keys())

        # Extract specialists in order
        specialists = [plan['tasks'][tid]['specialist'] for tid in task_ids]

        # backend-architect should come before fastapi-specialist
        arch_idx = specialists.index('backend-architect')
        fastapi_idx = specialists.index('fastapi-specialist')
        assert arch_idx < fastapi_idx

    def test_synthesize_plan_dependencies(self):
        """Test that tasks have proper dependencies."""
        specialist_responses = {
            'backend-architect': 'Response',
            'fastapi-specialist': 'Response',
            'docker-specialist': 'Response'
        }
        domains = ['backend']

        plan = synthesize_plan("Test feature", specialist_responses, domains)

        # First task should have no dependencies
        first_task = plan['tasks']['task-1']
        assert first_task['dependencies'] == []

        # Subsequent tasks should depend on previous
        second_task = plan['tasks']['task-2']
        assert second_task['dependencies'] == ['task-1']

        third_task = plan['tasks']['task-3']
        assert third_task['dependencies'] == ['task-2']

    def test_synthesize_plan_task_status(self):
        """Test that all tasks start with pending status."""
        specialist_responses = {
            'backend-architect': 'Response',
            'fastapi-specialist': 'Response'
        }
        domains = ['backend']

        plan = synthesize_plan("Test feature", specialist_responses, domains)

        # All tasks should be pending
        for task in plan['tasks'].values():
            assert task['status'] == 'pending'

    def test_synthesize_plan_scope_boundaries(self):
        """Test that scope boundaries are included."""
        specialist_responses = {
            'backend-architect': 'Design new endpoint'
        }
        domains = ['backend']

        plan = synthesize_plan("Test feature", specialist_responses, domains)

        assert 'what_to_change' in plan['scope_boundaries']
        assert 'what_not_to_change' in plan['scope_boundaries']
        assert isinstance(plan['scope_boundaries']['what_to_change'], list)
        assert isinstance(plan['scope_boundaries']['what_not_to_change'], list)

    def test_synthesize_plan_success_criteria(self):
        """Test that success criteria are defined."""
        specialist_responses = {
            'backend-architect': 'Response'
        }
        domains = ['backend']

        plan = synthesize_plan("Test feature", specialist_responses, domains)

        assert len(plan['success_criteria']) > 0
        assert any('completed' in criterion.lower() for criterion in plan['success_criteria'])


class TestHelperFunctions:
    """Tests for helper functions."""

    def test_extract_task_title_known_specialist(self):
        """Test extracting task title for known specialists."""
        title = extract_task_title('backend-architect', 'Some response')
        assert 'architecture' in title.lower() or 'design' in title.lower()

        title = extract_task_title('fastapi-specialist', 'Some response')
        assert 'endpoint' in title.lower() or 'implement' in title.lower()

    def test_extract_task_title_unknown_specialist(self):
        """Test extracting task title for unknown specialists."""
        specialist = 'unknown-specialist'
        title = extract_task_title(specialist, 'Some response')
        assert specialist in title

    def test_extract_scope_from_responses(self):
        """Test extracting scope boundaries from responses."""
        responses = {
            'backend-architect': 'Add new endpoint, modify schema',
            'fastapi-specialist': 'Implement route handler'
        }

        scope = extract_scope_from_responses(responses, 'change')
        assert isinstance(scope, list)
        assert len(scope) > 0

    def test_load_kb_state_structure(self):
        """Test that KB state is loaded with correct structure."""
        # This test may fail if kb/ directory doesn't exist
        # but should still return valid structure
        try:
            kb_state = load_kb_state()

            assert 'patterns' in kb_state
            assert 'recent_decisions' in kb_state
            assert isinstance(kb_state['patterns'], dict)
            assert isinstance(kb_state['recent_decisions'], list)
        except FileNotFoundError:
            pytest.skip("KB directory not found")


class TestIntegration:
    """Integration tests for auto-planning workflow."""

    def test_full_domain_to_plan_flow(self):
        """Test complete flow from domain analysis to plan synthesis."""
        # Step 1: Analyze domains
        description = "Add authentication API with login UI"
        domains = analyze_domains(description)

        assert 'backend' in domains
        assert 'frontend' in domains

        # Step 2: Mock specialist responses
        specialist_responses = {
            'backend-architect': 'Design auth architecture',
            'fastapi-specialist': 'Implement auth endpoints',
            'ui-ux': 'Design login interface',
            'javascript-specialist': 'Implement login form'
        }

        # Step 3: Synthesize plan
        plan = synthesize_plan(description, specialist_responses, domains)

        # Verify plan is complete and valid
        assert len(plan['tasks']) == 4
        assert plan['domains_affected'] == domains
        assert all(task['status'] == 'pending' for task in plan['tasks'].values())

    def test_multi_domain_specialist_selection(self):
        """Test that different domains trigger different specialist responses."""
        # Backend-only feature
        backend_desc = "Add database migration tool"
        backend_domains = analyze_domains(backend_desc)
        assert 'backend' in backend_domains
        assert 'frontend' not in backend_domains or len(backend_domains) == 2  # default case

        # Frontend-only feature
        frontend_desc = "Create new UI component for user profiles"
        frontend_domains = analyze_domains(frontend_desc)
        assert 'frontend' in frontend_domains

        # Full-stack feature
        fullstack_desc = "Add chat feature with API and UI"
        fullstack_domains = analyze_domains(fullstack_desc)
        assert 'backend' in fullstack_domains
        assert 'frontend' in fullstack_domains


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
