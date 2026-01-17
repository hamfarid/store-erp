import pytest

from src.utils.sequential_thinking import SequentialThinking


def test_sequential_thinking_pipeline_basic():
    st = SequentialThinking()
    st.add_step("lower", lambda s: s.lower())
    st.add_step("split", lambda s: s.split())
    st.add_step("count", lambda words: len(words))

    assert st.run("Hello Sequential Thinking") == 3


def test_sequential_thinking_empty_returns_none():
    st = SequentialThinking()
    assert st.run("anything") is None
