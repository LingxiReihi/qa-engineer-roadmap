class FileError(Exception):
    def __init__(self, file_path):
        self.file_path = file_path
        super().__init__(self)

    def __str__(self) -> str:
        return f"未找到文件: {self.file_path}"
