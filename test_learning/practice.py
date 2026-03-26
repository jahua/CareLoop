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
            except KeyError:  # Catch only KeyError instead of all exceptions
                return False
        if _path[-1] not in f:
            f[_path[-1]] = {}
            self.values[path] = value
            return True
        return False

    def get(self, path: str) -> int:
        return self.values.get(path, -1)


# Testing the implementation
if __name__ == "__main__":
    obj = FileSystem()
    print("create /a:", obj.createPath("/a", 1))       # True
    print("get /a:", obj.get("/a"))                    # 1
    print("create /a/b:", obj.createPath("/a/b", 2))   # True
    print("get /a/b:", obj.get("/a/b"))                # 2
    print("create /c/d:", obj.createPath("/c/d", 1))   # False (parent /c doesn't exist)
    print("get /c:", obj.get("/c"))                    # -1