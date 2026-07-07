from pathlib import Path

from django.conf import settings
from django.core.files.storage import FileSystemStorage


def moving_files():
    """Move the uploaded source image into the saved-results media folder."""
    source_path = Path(settings.MEDIA_ROOT) / "faces" / "face_original.png"
    target_dir = Path(settings.MEDIA_ROOT) / "faces_dataset"
    target_dir.mkdir(parents=True, exist_ok=True)

    fs = FileSystemStorage(location=target_dir)
    with source_path.open("rb") as source:
        saved_name = fs.save(source_path.name, source)

    source_path.unlink(missing_ok=True)
    return str(Path("faces_dataset") / saved_name)