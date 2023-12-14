class Directory:
    def __init__(self, name):
        self.name = name
        self.children = {}

    def add_child(self, child):
        self.children[child.name] = child

    def get_child(self, name):
        return self.children.get(name)

class File:
    def __init__(self, name, content=""):
        self.name = name
        self.content = content

class FileSystem:
    def __init__(self):
        self.root = Directory("/")

    def mkdir(self, path):
        current_dir = self.root
        components = path.split("/")[1:]

        for component in components:
            if component not in current_dir.children:
                new_dir = Directory(component)
                current_dir.add_child(new_dir)
            current_dir = current_dir.get_child(component)

    def cd(self, path):
        if path == "/":
            return self.root

    current_dir = self.root
    components = path.split("/")[1:]

    for component in components:
        if component == "..":
            current_dir = current_dir.parent if current_dir.parent else current_dir
        else:
            next_dir = current_dir.get_child(component)
            if next_dir:
                current_dir = next_dir
            else:
                new_dir = Directory(component)
                current_dir.add_child(new_dir)
                current_dir = new_dir

    return current_dir



    def ls(self, path):
        current_dir = self.cd(path)
        return [item.name for item in current_dir.children.values()]

    def touch(self, path):
        current_dir = self.cd(path[:-len(path.split("/")[-1])])
        new_file = File(path.split("/")[-1])
        current_dir.add_child(new_file)

    def cat(self, path):
        current_dir = self.cd(path[:-len(path.split("/")[-1])])
        file = current_dir.get_child(path.split("/")[-1])
        if file:
            return file.content
        else:
            return "File not found."

    def echo(self, path, content):
        current_dir = self.cd(path[:-len(path.split("/")[-1])])
        file = current_dir.get_child(path.split("/")[-1])
        if file:
            file.content = content
        else:
            new_file = File(path.split("/")[-1], content)
            current_dir.add_child(new_file)

    def mv(self, source, destination):
        source_dir = self.cd(source[:-len(source.split("/")[-1])])
        source_item = source_dir.get_child(source.split("/")[-1])

        destination_dir = self.cd(destination[:-len(destination.split("/")[-1])])
        destination_item = destination_dir.get_child(destination.split("/")[-1])

        if source_item:
            source_dir.children.pop(source_item.name)
            destination_dir.add_child(source_item)

    def cp(self, source, destination):
        source_dir = self.cd(source[:-len(source.split("/")[-1])])
        source_item = source_dir.get_child(source.split("/")[-1])

        destination_dir = self.cd(destination[:-len(destination.split("/")[-1])])

        if source_item:
            if isinstance(source_item, Directory):
                new_dir = Directory(source_item.name)
                destination_dir.add_child(new_dir)
                self._copy_directory(source_item, new_dir)
            elif isinstance(source_item, File):
                new_file = File(source_item.name, source_item.content)
                destination_dir.add_child(new_file)

    def _copy_directory(self, source_dir, destination_dir):
        for child in source_dir.children.values():
            if isinstance(child, Directory):
                new_child = Directory(child.name)
                destination_dir.add_child(new_child)
                self._copy_directory(child, new_child)
            elif isinstance(child, File):
                new_child = File(child.name, child.content)
                destination_dir.add_child(new_child)

    def rm(self, path):
        current_dir = self.cd(path[:-len(path.split("/")[-1])])
        current_dir.children.pop(path.split("/")[-1], None)


# Example usage:
fs = FileSystem()
fs.mkdir("/home")
fs.mkdir("/home/user")
fs.touch("/home/user/file.txt")
fs.echo("/home/user/file.txt", "Hello, this is a test.")
print(fs.cat("/home/user/file.txt"))
fs.cp("/home/user/file.txt", "/home/file_copy.txt")
print(fs.ls("/home"))
fs.mv("/home/user/file.txt", "/home/user/file_moved.txt")
print(fs.ls("/home/user"))
fs.rm("/home/user/file_moved.txt")
print(fs.ls("/home/user"))
