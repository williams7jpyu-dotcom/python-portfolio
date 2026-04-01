"""pytest configuration: add src/ to sys.path so tests can import scraper directly."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
