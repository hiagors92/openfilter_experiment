from pytest_bdd import scenarios
from pathlib import Path

FEATURE_DIR = Path(__file__).parent.parent / "features"
if not FEATURE_DIR.exists():
    FEATURE_DIR = Path(__file__).parent.parent.parent / "features"

scenarios(str(FEATURE_DIR / "integration_success.feature"))
scenarios(str(FEATURE_DIR / "ocr_performance.feature"))
scenarios(str(FEATURE_DIR / "performance.feature"))
