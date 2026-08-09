import os
import subprocess
import sys
import wave

from trinity_tts.config import PROFILES


def _pythonpath_env():
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    return env


def test_cli_runs_as_package_module(tmp_path):
    output = tmp_path / "package.wav"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "trinity_tts.cli",
            "Hello from package mode",
            "--output",
            str(output),
            "--profile",
            "micro",
        ],
        check=True,
        capture_output=True,
        env=_pythonpath_env(),
        text=True,
    )

    assert "Saved speech" in result.stdout
    assert output.exists()


def test_cli_runs_from_package_directory_with_dotted_filename(tmp_path):
    output = tmp_path / "local-dotted.wav"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "cli.py",
            "Hello from local dotted mode",
            "--output",
            str(output),
            "--profile",
            "micro",
        ],
        cwd="src/trinity_tts",
        check=True,
        capture_output=True,
        text=True,
    )

    assert "Saved speech" in result.stdout
    assert output.exists()


def test_cli_runs_from_package_directory_with_module_name(tmp_path):
    output = tmp_path / "local-module.wav"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "cli",
            "Hello from local module mode",
            "--output",
            str(output),
            "--profile",
            "micro",
        ],
        cwd="src/trinity_tts",
        check=True,
        capture_output=True,
        text=True,
    )

    assert "Saved speech" in result.stdout
    with wave.open(str(output), "rb") as wav_file:
        assert wav_file.getframerate() == PROFILES["micro"].sample_rate


def test_cli_runs_as_script_from_package_directory(tmp_path):
    output = tmp_path / "local-script.wav"

    result = subprocess.run(
        [
            sys.executable,
            "cli.py",
            "Hello from local script mode",
            "--output",
            str(output),
            "--profile",
            "micro",
        ],
        cwd="src/trinity_tts",
        check=True,
        capture_output=True,
        text=True,
    )

    assert "Saved speech" in result.stdout
    assert output.exists()
