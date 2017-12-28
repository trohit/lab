# taken from https://gist.github.com/Makistos
def parse_test_file(filename):
    retval = []
    with open(filename) as f:
        lines = f.read().splitlines()

    path, script = os.path.split(os.path.abspath(filename))
    cwd = os.getcwd()
    if cwd != path:
        os.chdir(path)
    for line in lines:
        if line.startswith('/include'):
            retval = retval + parse_test_file(line[9:])
        else:
            retval.append(line)
    if cwd != path:
        os.chdir(cwd)

    return retval
