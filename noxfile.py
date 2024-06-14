import nox


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
