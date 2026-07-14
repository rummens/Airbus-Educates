"""Put the portal source dir on sys.path so `from portal import ...` resolves.

test_portal.py used to live next to the portal package; it now lives here under
test/. This is the one-line bridge instead of packaging the portal.
"""
import pathlib
import sys

PORTAL_SRC = pathlib.Path(__file__).resolve().parents[2] / "images" / "dcs-academy-portal"
sys.path.insert(0, str(PORTAL_SRC))
