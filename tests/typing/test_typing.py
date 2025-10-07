import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
PROJECT_ROOT = ROOT.parent.parent


def _run_ty(path: Path) -> subprocess.CompletedProcess:
    return subprocess.run(  # noqa: S603
        [  # noqa: S607
            "uv",
            "run",
            "--no-project",
            "ty",
            "check",
            path,
        ],
        check=False,
    )


def test_typing_decls() -> None:
    result = _run_ty(ROOT / "declarations.py")
    assert result.returncode == 0, "Type checking failed for the declarations examples"


def test_module_typing() -> None:
    result = _run_ty(PROJECT_ROOT / "fastapi_backports")
    assert result.returncode == 0, "Type checking failed for the fastapi_backports module"
