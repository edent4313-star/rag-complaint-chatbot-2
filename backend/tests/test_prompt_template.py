"""
Unit tests for PromptEngine in src/prompt_template.py.
No external dependencies — pure logic tests.
"""
import pytest
from src.prompt_template import PromptEngine


class TestPromptEngineFormat:
    """Tests for the classmethod PromptEngine.format()"""

    def test_returns_string(self):
        result = PromptEngine.format(context="ctx", question="q")
        assert isinstance(result, str)

    def test_contains_question(self):
        result = PromptEngine.format(context="some context", question="What is X?")
        assert "What is X?" in result

    def test_contains_context(self):
        result = PromptEngine.format(context="Complaint about fees", question="q")
        assert "Complaint about fees" in result

    def test_contains_system_prompt_keywords(self):
        result = PromptEngine.format(context="ctx", question="q")
        # System prompt must orient the model as a financial analyst
        assert "Financial Complaint Analyst" in result

    def test_answer_marker_present(self):
        result = PromptEngine.format(context="ctx", question="q")
        assert "ANSWER:" in result

    def test_empty_context_still_returns_prompt(self):
        result = PromptEngine.format(context="", question="any question")
        assert "any question" in result
        assert len(result) > 50

    def test_empty_question_still_returns_prompt(self):
        result = PromptEngine.format(context="some context", question="")
        assert "some context" in result


class TestPromptEngineBuildPrompt:
    """Tests for the instance method PromptEngine.build_prompt()"""

    def setup_method(self):
        self.engine = PromptEngine()

    def test_build_prompt_joins_contexts(self):
        contexts = ["ctx one", "ctx two"]
        result = self.engine.build_prompt(question="q", contexts=contexts)
        assert "ctx one" in result
        assert "ctx two" in result

    def test_build_prompt_contains_question(self):
        result = self.engine.build_prompt(
            question="What are mortgage issues?",
            contexts=["ctx"]
        )
        assert "What are mortgage issues?" in result

    def test_build_prompt_equivalent_to_format(self):
        """build_prompt should produce the same output as format()."""
        contexts = ["ctx A", "ctx B"]
        joined = "\n\n".join(contexts)
        via_build = self.engine.build_prompt(question="q", contexts=contexts)
        via_format = PromptEngine.format(context=joined, question="q")
        assert via_build == via_format

    def test_empty_contexts_list(self):
        result = self.engine.build_prompt(question="q", contexts=[])
        assert isinstance(result, str)
