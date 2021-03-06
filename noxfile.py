"""Nox sessions."""
import tempfile
from typing import Any

import nox
from nox.sessions import Session

package = "python_project"
locations = "src", "tests", "noxfile.py", "docs/conf.py"
nox.options.sessions = "lint", "doc8", "mypy", "pytype", "safety", "tests"


def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages constrained by Poetry's lock file."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python=["3.8", "3.7"])
def tests(session: Session) -> None:
    """Run the test suite."""
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(
        session, "coverage[toml]", "pytest", "pytest-cov", "pytest-mock"
    )
    session.run("pytest", *args)


# TODO: Add more flake8 plugins
@nox.session(python=["3.8", "3.7"])
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    # Would typically just install flake8 and extensions, but isort
    # needs to see which packages are installed
    session.run("poetry", "install", "--no-dev", external=True)
    # Manually add non dev packages which are imported, like pytest
    install_with_constraints(
        session,
        "darglint",
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-isort",
        "flake8-rst-docstrings",
        "pandas-vet",
        "pep8-naming",
        "pytest",
        "pytest-mock",
    )
    session.run("flake8", *args)


@nox.session(python=["3.8", "3.7"])
def doc8(session: Session) -> None:
    """Lint rst files using doc8."""
    args = session.posargs or ["docs"]
    install_with_constraints(session, "doc8", "pygments")
    session.run("doc8", *args)


@nox.session(python="3.8")
def sort(session: Session) -> None:
    """Sort imports with isort."""
    args = session.posargs or locations
    # isort needs to see all installed packages that are imported
    session.run("poetry", "install", "--no-dev", external=True)
    # Manually add any non dev packages which are imported, like pytest
    install_with_constraints(session, "pytest", "pytest-mock", "toml")
    session.run("isort", "-rc", *args)


@nox.session(python="3.8")
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python="3.8")
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        install_with_constraints(session, "safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


@nox.session(python=["3.8", "3.7"])
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations
    install_with_constraints(session, "mypy")
    session.run("mypy", *args)


# TODO: Update pytype
# As of now (2-11-2020), pytype does not yet support 3.8
# https://github.com/google/pytype/issues/440
@nox.session(python=["3.7"])
def pytype(session: Session) -> None:
    """Type-check using pytype."""
    args = session.posargs or ["--disable=import-error", *locations]
    install_with_constraints(session, "pytype")
    session.run("pytype", *args)


@nox.session(python=["3.8", "3.7"])
def typeguard(session: Session) -> None:
    """Runtime type checking using Typeguard."""
    args = session.posargs or ["-m", "not e2e"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "pytest", "pytest-mock", "typeguard")
    session.run("pytest", f"--typeguard-packages={package}", *args)


@nox.session(python=["3.8", "3.7"])
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "xdoctest", "pygments")
    session.run("python", "-m", "xdoctest", package, *args)


@nox.session(python="3.8")
def docs(session: Session) -> None:
    """Build the documentation."""
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "sphinx", "sphinx-autodoc-typehints")
    session.run("sphinx-build", "docs", "docs/_build")


@nox.session(python="3.8")
def coverage(session: Session) -> None:
    """Upload coverage data."""
    install_with_constraints(session, "coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
