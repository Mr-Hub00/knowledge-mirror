import subprocess
import sys
import os
import pathlib

# Python

def test_manage_py_help_runs():
    # Arrange: get the path to manage.py
    manage_py = pathlib.Path(__file__).parent / "manage.py"
    assert manage_py.exists()

    # Act: run "python manage.py help"
    result = subprocess.run(
        [sys.executable, str(manage_py), "help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=manage_py.parent,
        text=True,
    )

    # Assert: process exits successfully and help text is present
    assert result.returncode == 0
    assert "Type 'manage.py help <subcommand>'" in result.stdout