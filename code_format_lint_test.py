import subprocess

import pytest


@pytest.mark.black
def test_black_formatting():
    # Run the black command as a subprocess
    # todo- add as pre-commit hook ? github action?
    result = subprocess.run(
        ["black", "--check", "."],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Check if the black command succeeded (exit code 0)
    assert result.returncode == 0, (
        "Black formatting check failed (please run 'black .' command)"
        f":\n{result.stdout}\n{result.stderr}"
    )


@pytest.mark.flake8
def test_flake8_linting():
    # Run the flake8 command as a subprocess
    # todo- add as pre-commit hook ? github action?
    result = subprocess.run(
        ["flake8", "--format=pylint"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Check if the black command succeeded (exit code 0)
    assert (
        result.returncode == 0
    ), "flake8 is complaining.':\n{result.stdout}\n{result.stderr}"


@pytest.mark.isort
def test_isort():
    # Run the flake8 command as a subprocess
    # todo- add as pre-commit hook ? github action?
    result = subprocess.run(
        ["isort", "--check", "."],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Check if the black command succeeded (exit code 0)
    assert (
        result.returncode == 0
    ), "isort is complaining.':\n{result.stdout}\n{result.stderr}"
