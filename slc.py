import sys
import os.path


class Counters:

    def __init__(self):
        self.totalfiles = 0
        self.totallines = 0
        self.totalblanks = 0
        self.totalcomments = 0


class Reader:

    def __init__(self, counters):
        self.counters = counters

    def read_file(self, filename):
        try:
            f = open(filename)
            self.counters.totalfiles += 1

            for line in f:
                self.counters.totallines += 1
                if line.isspace():
                    self.counters.totalblanks += 1

        except IOError as err:
            pass

        except UnicodeDecodeError as err:
            pass


class PythonReader(Reader):

    def __init__(self, counters):
        super(PythonReader, self).__init__(counters)

    def read_file(self, filename):
        try:
            f = open(filename)
            self.counters.totalfiles += 1
            flagsingle = False
            flagdouble = False

            for line in f:
                self.counters.totallines += 1

                if flagsingle:
                    self.counters.totalcomments += 1
                    if line.find("'''") < 0:
                        flagsingle = False
                if flagdouble:
                    self.counters.totalcomments += 1
                    if line.find('"""') < 0:
                        flagdouble = False

                if line.isspace():
                    self.counters.totalblanks += 1
                if line.startswith("#"):
                    self.counters.totalcomments += 1

                if line.find("'''") > 0:
                    flagsingle = True
                    self.counters.totalcomments += 1
                if line.find('"""') > 0:
                    self.counters.totalcomments += 1
                    flagdouble = True

        except IOError as err:
            pass

        except UnicodeDecodeError as err:
            pass


class JavaReader(Reader):

    def __init__(self, counters):
        super(JavaReader, self).__init__(counters)

    def read_file(self, filename):
        try:
            f = open(filename)
            self.counters.totalfiles += 1
            flag = False

            for line in f:
                self.counters.totallines += 1
                if flag:
                    self.counters.totalcomments += 1
                    if line.find("*/") < 0:
                        flag = False
                if line.isspace():
                    self.counters.totalblanks += 1
                if line.startswith("//"):
                    self.counters.totalcomments += 1
                if line.find("/*") > 0 or line.find("/**") > 0:
                    flag = True
                    self.counters.totalcomments += 1

        except IOError as err:
            pass

        except UnicodeDecodeError as err:
            pass

# ----------------------------------------------------------------------


counters_dict = dict()


def create_reader(filename):

    if filename.endswith(".py"):
        if "Python" in counters_dict:
            c = counters_dict["Python"]
        else:
            c = Counters()
            counters_dict["Python"] = c
        return PythonReader(c)

    elif filename.endswith(".java"):
        if "Java" in counters_dict:
            c = counters_dict["Java"]
        else:
            c = Counters()
            counters_dict["Java"] = c
        return JavaReader(c)

    elif filename.endswith(".cpp"):
        if "C++" in counters_dict:
            c = counters_dict["C++"]
        else:
            c = Counters()
            counters_dict["C++"] = c
        return JavaReader(c)

    elif filename.endswith(".c"):
        if "C" in counters_dict:
            c = counters_dict["C"]
        else:
            c = Counters()
            counters_dict["C"] = c
        return JavaReader(c)

    elif filename.endswith(".cs"):
        if "C Shell" in counters_dict:
            c = counters_dict["C Shell"]
        else:
            c = Counters()
            counters_dict["C Shell"] = c
        return JavaReader(c)

    else:
        if "Other" in counters_dict:
            c = counters_dict["Other"]
        else:
            c = Counters()
            counters_dict["Other"] = c
        return Reader(c)

# ----------------------------------------------------------------------


def read_dir(dirname):
    dirs = os.listdir(dirname)
    for d in dirs:
        fullpath = "{0}/{1}".format(dirname, d)
        if os.path.isfile(fullpath):
            r = create_reader(fullpath)
            r.read_file(fullpath)
        else:
            read_dir(fullpath)

# ----------------------------------------------------------------------


def print_stats():
    files = 0
    lines = 0
    blanks = 0
    comments = 0
    for key in counters_dict:
        print("\n")
        print(key)
        counterobject = counters_dict[key]
        print("Number of files : ", counterobject.totalfiles)
        print("Lines           : ", counterobject.totallines)
        print("Empty lines     : ", counterobject.totalblanks)
        print("Comments        : ", counterobject.totalcomments)
        files += counterobject.totalfiles
        lines += counterobject.totallines
        blanks += counterobject.totalblanks
        comments += counterobject.totalcomments
    print("\n")
    print("Total files       : ", files)
    print("Total lines       : ", lines)
    print("Total empty lines : ", blanks)
    print("Total comments    : ", comments)
    print("\n")

# ----------------------------------------------------------------------


if len(sys.argv) < 2:
    print("Input a file name or directory to read.\n")
    sys.exit(-1)

name = sys.argv[1]

print("\n")
print(name, "\n")

# if os.path.isfile(name):
#     reader = create_reader(name)
#     reader.read_file(name)
#     print_stats()

if os.path.isdir(name) or os.path.isfile(name):
    read_dir(name)
    print_stats()

else:
    print("No such file or directory: {0} \n".format(name))
    sys.exit(-1)


