import logging
from pathlib import Path

from django.conf import settings


logger = logging.getLogger(__name__)


def clean_temp():
    """Remove temporary face-analysis files before a new upload."""
    directory = Path(settings.MEDIA_ROOT) / "faces"
    directory.mkdir(parents=True, exist_ok=True)
    for file_path in directory.iterdir():
        try:
            if file_path.is_file():
                file_path.unlink()
        except OSError as exc:
            logger.warning("Could not delete temporary file %s: %s", file_path, exc)