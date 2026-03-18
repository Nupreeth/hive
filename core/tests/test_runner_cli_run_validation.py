import argparse

from framework.runner.cli import cmd_run
from framework.runner.preload_validation import PreloadValidationError


def _args() -> argparse.Namespace:
    return argparse.Namespace(
        agent_path="exports/bad_agent",
        input=None,
        input_file=None,
        output=None,
        quiet=True,
        verbose=False,
        model=None,
        resume_session=None,
        checkpoint=None,
    )


def test_cmd_run_returns_error_for_preload_validation(monkeypatch, capsys):
    monkeypatch.setattr("framework.observability.configure_logging", lambda level: None)

    class _Runner:
        @staticmethod
        def load(agent_path, model=None):
            raise PreloadValidationError(["entry node is missing"])

    monkeypatch.setattr("framework.runner.AgentRunner", _Runner)

    result = cmd_run(_args())

    captured = capsys.readouterr()
    assert result == 1
    assert "Pre-load validation failed:" in captured.err
    assert "entry node is missing" in captured.err


def test_cmd_run_returns_error_for_invalid_agent_definition(monkeypatch, capsys):
    monkeypatch.setattr("framework.observability.configure_logging", lambda level: None)

    class _Runner:
        @staticmethod
        def load(agent_path, model=None):
            raise ValueError("Agent is missing nodes")

    monkeypatch.setattr("framework.runner.AgentRunner", _Runner)

    result = cmd_run(_args())

    captured = capsys.readouterr()
    assert result == 1
    assert "Error: Agent is missing nodes" in captured.err
