import os
from django.core.files.storage import FileSystemStorage


def moving_files():
    old_dir = r'C:\Users\maksp\PycharmProjects\face_recognision\media\faces\face_original.png'
    new_dir = r'C:\Users\maksp\PycharmProjects\face_recognision\media\faces_dataset'
    fs = FileSystemStorage(location=new_dir)
    filename = os.path.basename(old_dir)
    file_save = fs.save(filename, open(old_dir, 'rb'))
    file_save_path = os.path.join(new_dir, file_save)
    os.remove(old_dir)
    return file_save_path