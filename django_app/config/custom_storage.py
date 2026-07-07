from django.core.files.storage import FileSystemStorage


class CustomFileSystemStorage(FileSystemStorage):
    """Storage backend that overwrites temporary uploads with stable names."""

    def get_available_name(self, name, max_length=None):
        """Reuse the requested filename instead of appending a unique suffix."""
        return name