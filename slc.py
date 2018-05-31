import sys
import os.path


class Counters:

    def __init__(self):
        self.totalfiles = 0
        self.totalsize = 0
        self.totallines = 0
        self.totalblanks = 0
        self.totalcomments = 0


class Reader:

    def __init__(self, counters):
        self.counters = counters

    def read_file(self, filename):
        try:
            self.counters.totalsize += os.path.getsize(filename)
            with open(filename) as f:
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
        super().__init__(counters)

    def read_file(self, filename):
        try:
            self.counters.totalsize += os.path.getsize(filename)
            with open(filename) as f:
                self.counters.totalfiles += 1
                flagsingle = False
                flagdouble = False

                for line in f:
                    self.counters.totallines += 1
                    if flagsingle:
                        self.counters.totalcomments += 1
                        if line.find("'''") != -1:
                            flagsingle = False
                            continue
                    if flagdouble:
                        self.counters.totalcomments += 1
                        if line.find('"""') != -1:
                            flagdouble = False
                            continue
                    if line.isspace():
                        self.counters.totalblanks += 1
                    if line.startswith("#"):
                        self.counters.totalcomments += 1

                    if line.find("'''") != -1:
                        flagsingle = True
                        self.counters.totalcomments += 1
                    if line.find('"""') != -1:
                        self.counters.totalcomments += 1
                        flagdouble = True

        except IOError as err:
            pass

        except UnicodeDecodeError as err:
            pass


class JavaReader(Reader):

    def __init__(self, counters):
        super().__init__(counters)

    def read_file(self, filename):
        try:
            self.counters.totalsize += os.path.getsize(filename)
            with open(filename) as f:
                self.counters.totalfiles += 1
                flag = False

                for line in f:
                    self.counters.totallines += 1

                    if flag:
                        self.counters.totalcomments += 1
                        if line.find("*/") != -1:
                            flag = False

                    if line.isspace():
                        self.counters.totalblanks += 1
                    if line.startswith("//"):
                        self.counters.totalcomments += 1

                    if line.find("/*") != -1 or line.find("/**") != -1:
                        flag = True
                        self.counters.totalcomments += 1

        except IOError as err:
            pass

        except UnicodeDecodeError as err:
            pass


class HTMLReader(Reader):

    def __init__(self, counters):
        super().__init__(counters)

    def read_file(self, filename):
        try:
            self.counters.totalsize += os.path.getsize(filename)
            with open(filename) as f:
                self.counters.totalfiles += 1
                flag = False

                for line in f:
                    self.counters.totallines += 1

                    if flag:
                        self.counters.totalcomments += 1
                        if line.startswith("=end"):
                            flag = False

                    if line.isspace():
                        self.counters.totalblanks += 1
                    if line.startswith("#"):
                        self.counters.totalcomments += 1

                    if line.startswith("=begin"):
                        flag = True
                        self.counters.totalcomments += 1

        except IOError as err:
            pass

        except UnicodeDecodeError as err:
            pass


class RubyReader(Reader):

    def __init__(self, counters):
        super().__init__(counters)

    def read_file(self, filename):
        try:
            self.counters.totalsize += os.path.getsize(filename)
            with open(filename) as f:
                self.counters.totalfiles += 1
                flag = False

                for line in f:
                    self.counters.totallines += 1

                    if flag:
                        self.counters.totalcomments += 1
                        if line.find("-->") != -1:
                            flag = False

                    if line.isspace():
                        self.counters.totalblanks += 1

                    if line.find("<!--") != -1:
                        flag = True
                        self.counters.totalcomments += 1

        except IOError as err:
            pass

        except UnicodeDecodeError as err:
            pass

# ----------------------------------------------------------------------

# counters_dict keys are language names (langname)


counters_dict = dict()

reader_map = {
    ".py": {"name": "Python", "reader": PythonReader},
    ".java": {"name": "Java", "reader": JavaReader},
    ".cpp": {"name": "C++", "reader": JavaReader},
    ".c++": {"name": "C++", "reader": JavaReader},
    ".cxx": {"name": "C++", "reader": JavaReader},
    ".c": {"name": "C", "reader": JavaReader},
    ".cs": {"name": "C Shell", "reader": JavaReader},
    ".css": {"name": "CSS", "reader": JavaReader},
    ".html": {"name": "HTML", "reader": HTMLReader},
    ".rb": {"name": "Ruby", "reader": RubyReader},
    "[other]": {"name": "Other", "reader": Reader},
}


def create_reader(filename):
    ext = os.path.splitext(filename)[1]

    if ext in reader_map:
        lang = reader_map[ext]
        reader = lang["reader"]
        langname = lang["name"]
    else:
        lang = reader_map["[other]"]
        reader = lang["reader"]
        langname = lang["name"]

    if langname in counters_dict:
        c = counters_dict[langname]
    else:
        c = Counters()
        counters_dict[langname] = c

    return reader(c)


# def create_reader(filename):
#
#     if filename.endswith(".py"):
#         if "Python" in counters_dict:
#             c = counters_dict["Python"]
#         else:
#             c = Counters()
#             counters_dict["Python"] = c
#         return PythonReader(c)
#
#     elif filename.endswith(".java"):
#         if "Java" in counters_dict:
#             c = counters_dict["Java"]
#         else:
#             c = Counters()
#             counters_dict["Java"] = c
#         return JavaReader(c)
#
#     elif filename.endswith(".cpp"):
#         if "C++" in counters_dict:
#             c = counters_dict["C++"]
#         else:
#             c = Counters()
#             counters_dict["C++"] = c
#         return JavaReader(c)
#
#     elif filename.endswith(".c"):
#         if "C" in counters_dict:
#             c = counters_dict["C"]
#         else:
#             c = Counters()
#             counters_dict["C"] = c
#         return JavaReader(c)
#
#     elif filename.endswith(".cs"):
#         if "C Shell" in counters_dict:
#             c = counters_dict["C Shell"]
#         else:
#             c = Counters()
#             counters_dict["C Shell"] = c
#         return JavaReader(c)
#
#     elif filename.endswith(".css"):
#         if "CSS" in counters_dict:
#             c = counters_dict["CSS"]
#         else:
#             c = Counters()
#             counters_dict["CSS"] = c
#         return JavaReader(c)
#
#     elif filename.endswith(".html") or filename.endswith(".html.erb"):
#         if "HTML" in counters_dict:
#             c = counters_dict["HTML"]
#         else:
#             c = Counters()
#             counters_dict["HTML"] = c
#         return HTMLReader(c)
#
#     elif filename.endswith(".rb"):
#         if "Ruby" in counters_dict:
#             c = counters_dict["Ruby"]
#         else:
#             c = Counters()
#             counters_dict["Ruby"] = c
#         return RubyReader(c)
#
#     else:
#         if "Other" in counters_dict:
#             c = counters_dict["Other"]
#         else:
#             c = Counters()
#             counters_dict["Other"] = c
#         return Reader(c)

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
    size = 0
    files = 0
    lines = 0
    blanks = 0
    comments = 0

    for key in counters_dict:
        print("\n")
        print(key)

        counterobject = counters_dict[key]
        sizeformat = prefix(counterobject.totalsize)

        print("Size              : ", sizeformat[0], sizeformat[1] + "B")
        print("Number of files   : ", counterobject.totalfiles)
        print("Lines             : ", counterobject.totallines)
        print("Empty lines       : ", counterobject.totalblanks)
        print("Comments          : ", counterobject.totalcomments)

        size += counterobject.totalsize
        files += counterobject.totalfiles
        lines += counterobject.totallines
        blanks += counterobject.totalblanks
        comments += counterobject.totalcomments

    print("\n")
    totalsizeformat = prefix(size)
    print("Total size        : ", totalsizeformat[0], totalsizeformat[1] + "B")
    print("Total files       : ", files)
    print("Total lines       : ", lines)
    print("Total empty lines : ", blanks)
    print("Total comments    : ", comments)
    print("\n")


def prefix(n):
    if n >= 1000000:
        return [round(n / (1024*1024), 2), "M"]
    elif n >= 1000:
        return [round(n / 1024, 2), "K"]
    else:
        return [n, ""]

# ----------------------------------------------------------------------


if len(sys.argv) < 2:
    print("Input a file name or directory to read.\n")
    sys.exit(-1)

name = sys.argv[1]

print("\n")
print(name, "\n")

if os.path.isfile(name):
    r = create_reader(name)
    r.read_file(name)
    print_stats()

elif os.path.isdir(name):
    read_dir(name)
    print_stats()

else:
    print("No such file or directory: {0} \n".format(name))
    sys.exit(-1)
