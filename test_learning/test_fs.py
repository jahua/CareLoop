class FileSystem:
    def __init__(self):
        self.files = {}
        self.values = {}

    def createPath(self, path: str, value: int) -> bool:
        _path = path[1:].split('/')
        f = self.files
        for p in _path[:-1]:
            try:
                f = f[p]
            except:
                return False
        if _path[-1] not in f:
            f[_path[-1]] = {}
            self.values[path] = value
            return True
        return False

    def get(self, path: str) -> int:
        return self.values.get(path, -1)

fs = FileSystem()
print(fs.createPath("/a", 1)) # True
print(fs.get("/a")) # 1
print(fs.createPath("/a/b", 2)) # True
print(fs.get("/a/b")) # 2
print(fs.createPath("/c/d", 1)) # False
print(fs.get("/c")) # -1
