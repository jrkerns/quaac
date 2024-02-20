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
