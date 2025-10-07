import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
PROJECT_ROOT = ROOT.parent.parent


def test_typing_decls() -> None:
    result = subprocess.run(  # noqa: S603
        [  # noqa: S607
            "uv",
            "run",
            "ty",
            "check",
            ROOT / "declarations.py",
        ],
        check=False,
    )

    assert result.returncode == 0, "Type checking failed for the declarations examples"


def test_module_typing() -> None:
    result = subprocess.run(  # noqa: S603
        [  # noqa: S607
            "uv",
            "run",
            "ty",
            "check",
            PROJECT_ROOT / "fastapi_backports",
        ],
        check=False,
    )

    assert result.returncode == 0, "Type checking failed for the fastapi_backports module"
