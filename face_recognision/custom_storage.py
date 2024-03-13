from django.core.files.storage import FileSystemStorage

class CustomFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        return name

    # def __init__(self, location=None, base_url=None):
    #     location = 'C:/Users/maksp/PycharmProjects/face_recognision/media/faces/'
    #     super().__init__(location, base_url)