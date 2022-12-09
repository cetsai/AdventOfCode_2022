import re

def readInput(filesystem):
    # directory "dir ([a-z]+)"
    # file "([0-9]+) ([a-z.]+)"
    # command "$ (?:cd|ls) ?([/.a-z]*)"
    cmd = re.compile(r"[$] (?:ls|cd) ?(?P<name>[/.a-z]*)$")
    node = re.compile(r"(?:dir|(?P<size>[0-9]+)) (?P<name>[a-z.]+)$")
    
    cwd = ["/"]

    with open("7/input") as f:
        for line in f:
            if line[0] == "$":
                match = cmd.match(line)
                assert match
                if not match.group("name"):
                    continue
                elif match.group("name") == "..":
                    cwd.pop()
                elif match.group("name") == "/":
                    cwd = ["/"]
                else:
                    cwd.append(match.group("name"))
            else:
                size, name = node.match(line).group("size", "name")
                dir = "/".join(cwd) + "/"
                path = dir + name + ("" if size else "/") # directory names end with /
                filesystem[dir].append(path)
                if not size:
                    filesystem[path] = []
                else:
                    filesystem[path] = int(size)

def sumDirsRec(path, filesystem):
    dir = filesystem[path]
    if not isinstance(dir, list):
        return dir

    sum = 0
    for node in filesystem[path]:
        name = node[node.rfind("/", 0, -1) + 1:]
        name = path + name
        sum += sumDirsRec(name, filesystem)

    filesystem[path] = sum
    return sum

def main():
    filesystem = {"//":[]}
    readInput(filesystem)

    path = "//"
    sumDirsRec(path, filesystem)

    used = filesystem["//"]
    unused = 70000000 - used
    threshold = 30000000 - unused
    candidates = [size for name, size in filesystem.items() if size > threshold and name[-1] == "/"]
    print(min(candidates))

if __name__ == "__main__":
    main()