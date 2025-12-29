import os
class ResumeManager:
    def __init__(self, upload_dir="data/resumes"):
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)

    def save_resume(self, file):
        file_path = os.path.join(self.upload_dir, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        return file_path

    def list_resumes(self):
        return os.listdir(self.upload_dir)

    def delete_resume(self, filename):
        file_path = os.path.join(self.upload_dir, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
