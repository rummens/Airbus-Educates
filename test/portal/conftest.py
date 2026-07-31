"""Put the portal source dir on sys.path so `from portal import ...` resolves.

test_portal.py used to live next to the portal package; it now lives here under
test/. This is the one-line bridge instead of packaging the portal.
"""
import pathlib
import sys

import pytest

PORTAL_SRC = pathlib.Path(__file__).resolve().parents[2] / "images" / "dcs-academy-portal"
sys.path.insert(0, str(PORTAL_SRC))


@pytest.fixture(autouse=True)
def close_feedback_db():
    """Hand the pooled sqlite connection back after every test.

    The portal keeps one module-global connection; a test that opens one (directly or by
    building the app) and leaves it behind gets it closed by the garbage collector later,
    which reports `ResourceWarning: unclosed database` against whatever unrelated line
    happened to trigger the GC. Closing here keeps the suite's warning output honest.
    The import is inside the fixture so test modules can still set their env before the
    portal package is imported."""
    yield
    from portal import feedback
    feedback.close()
