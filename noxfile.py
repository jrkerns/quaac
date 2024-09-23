import shutil

import nox


@nox.session(python=False)
def run_tests(session):
    for py_ver in ('3.8', '3.9', '3.10', '3.11', '3.12'):
        shutil.rmtree('test-env', ignore_errors=True)
        session.run('uv', 'venv', 'test-env', '--python', py_ver)
        session.run('uv', 'sync', '--python', py_ver, env={'UV_PROJECT_ENVIRONMENT': 'test-env'})
        session.run(
            "uv", "run", "pytest", env={'UV_PROJECT_ENVIRONMENT': 'test-env'}
        )
        shutil.rmtree('test-env', ignore_errors=True)


@nox.session(python=False)
def serve_docs(session):
    session.run(
        "sphinx-autobuild",
        "docs",
        "docs/_build",
        '-a',
        "--port",
        "8787",
        "--open-browser",
    )


@nox.session(python=False)
def build_dist(session):
    session.run(
        "hatch",
        "build",
    )


@nox.session(python=False)
def publish_dist(session):
    session.run(
        "twine",
        "upload",
        "dist/*.whl",
        "--skip-existing",
        '--config-file',
        '.pypirc',
    )
