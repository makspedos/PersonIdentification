import os

def clean_temp():
    directory = r'C:\Users\maksp\PycharmProjects\face_recognision\media\faces'
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
