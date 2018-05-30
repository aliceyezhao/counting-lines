import sys
import os.path


class Reader:
    instantiated = 0
    totallines = 0
    totalblanks = 0

    def __init__(self):
        Reader.instantiated += 1

    def read_file(self, filename):
        try:
            f = open(filename)
            linecounter = 0
            blanklines = 0

            for line in f:
                linecounter += 1
                if line.isspace():
                    blanklines += 1
            Reader.totallines += linecounter
            Reader.totalblanks += blanklines
            return [linecounter, blanklines]

        except IOError as err:
            pass

        except UnicodeDecodeError as err:
            pass


class PythonReader(Reader):
    instantiated = 0
    totallines = 0
    totalblanks = 0
    totalcomments = 0

    def __init__(self):
        PythonReader.instantiated += 1

    def read_file(self, filename):
        try:
            f = open(filename)
            linecounter = 0
            blanklines = 0
            comments = 0

            for line in f:
                linecounter += 1
                if line.isspace():
                    blanklines += 1
                if line.startswith("#"):
                    comments += 1

            PythonReader.totallines += linecounter
            PythonReader.totalblanks += blanklines
            PythonReader.totalcomments += comments
            return [linecounter, blanklines, comments]

        except IOError as err:
            pass

        except UnicodeDecodeError as err:
            pass


class JavaReader(Reader):
    instantiated = 0
    totallines = 0
    totalblanks = 0
    totalcomments = 0

    def __init__(self):
        JavaReader.instantiated += 1

    def read_file(self, filename):
        try:
            f = open(filename)
            linecounter = 0
            blanklines = 0
            comments = 0
            flag = False

            for line in f:
                print(flag, linecounter)
                linecounter += 1
                if flag:
                    print("a") #4
                    comments += 1
                    flag = not line.endswith("*/")
                if line.isspace():
                    print("b") #10
                    blanklines += 1
                if line.startswith("//"):
                    print("c") #5
                    comments += 1
                if line.startswith("/*") or line.startswith("/**"):
                    print("d") #1
                    flag = True
                    comments += 1

            JavaReader.totallines += linecounter
            JavaReader.totalblanks += blanklines
            JavaReader.totalcomments += comments
            return [linecounter, blanklines, comments]

        except IOError as err:
            pass

        except UnicodeDecodeError as err:
            pass

# ----------------------------------------------------------------------


def create_reader(filename):
    if filename.endswith(".java"):
        return JavaReader()
    elif filename.endswith(".py"):
        return PythonReader()
    else:
        return Reader()

# ----------------------------------------------------------------------


def read_dir(dirname):
    dirs = os.listdir(dirname)
    for d in dirs:
        fullpath = "{0}/{1}".format(dirname, d)
        if os.path.isfile(fullpath):
            reader = create_reader(fullpath)
            arr = reader.read_file(fullpath)
            #print_stats(arr)
        else:
            read_dir(fullpath)

# ----------------------------------------------------------------------


def print_stats(arr):
    print("Lines       : ", arr[0])
    print("Empty lines : ", arr[1])
    try:
        print("Comments    : ", arr[2])
    except IndexError as err:
        pass

# ----------------------------------------------------------------------


if len(sys.argv) < 2:
    print("Input a file name or directory to read.\n")
    sys.exit(-1)

name = sys.argv[1]

print("\n")
print(name, "\n")

if os.path.isfile(name):
    reader = create_reader(name)
    arr = reader.read_file(name)
    print_stats(arr)

elif os.path.isdir(name):
    read_dir(name)

    print("{0} Python files".format(PythonReader.instantiated))
    print_stats([PythonReader.totallines, PythonReader.totalblanks, PythonReader.totalcomments])
    print("\n")

    print("{0} Java files".format(JavaReader.instantiated))
    print_stats([JavaReader.totallines, JavaReader.totalblanks, JavaReader.totalcomments])
    print("\n")

    print("{0} other files".format(Reader.instantiated))
    print_stats([Reader.totallines, Reader.totalblanks])
    print("\n")

    print("{0} TOTAL files".format(Reader.instantiated + JavaReader.instantiated + PythonReader.instantiated))
    print_stats([PythonReader.totallines + JavaReader.totallines + Reader.totallines,
                 PythonReader.totalblanks + JavaReader.totalblanks + Reader.totalblanks,
                 PythonReader.totalcomments + JavaReader.totalcomments])
    print("\n")

else:
    print("No such file or directory: {0} \n".format(name))
    sys.exit(-1)


