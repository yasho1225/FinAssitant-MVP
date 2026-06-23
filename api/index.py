import sys
from pathlib import Path

# Ensure project root is on the path for `app` imports
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mangum import Mangum  # noqa: E402
from app.main import app  # noqa: E402

# Vercel serverless entrypoint
handler = Mangum(app, lifespan="off")
