import sys
import os.path


def read_file(filename, pathlength):
    try:
        f = open(filename)
        linecounter = 0
        blanklines = 0

        for line in f:
            linecounter += 1
            if line == '\n' or line == '\r\n':
                blanklines += 1
        print("\n", filename[pathlength:])
        print("Lines      : ", linecounter)
        print("Blank lines: ", blanklines)
        if blanklines != 0:
            print("{0}% blank lines \n".format(round(blanklines/linecounter * 100, 2)))

    except IOError as err:
        #print("Error reading the file {0}: {1} \n".format(filename[pathlength:], err))
        print("Error reading the file {0} \n".format(filename[pathlength:]))
        #sys.exit(-1)

    except UnicodeDecodeError as err:
        #print("Error reading the file {0}: {1} \n".format(filename[pathlength:], err))
        print("Error reading the file {0} \n".format(filename[pathlength:]))
        #sys.exit(-1)


def read_dir(dirname):
    pathlength = len(dirname) + 1
    dirs = os.listdir(dirname)
    for d in dirs:
        fullpath = "{0}/{1}".format(dirname, d)
        if os.path.isfile(fullpath):
            read_file(fullpath, pathlength)
        elif os.path.isdir(fullpath):
            read_dir(fullpath)
        else:
            print("{0} is not a file or directory. \n".format(fullpath[pathlength:]))


#----------------------------------------------------------------------


if len(sys.argv) < 2:
    print("Input a file name or directory to read.\n")
    sys.exit(-1)

print("\n", sys.argv[1], "\n")

name = sys.argv[1]

if os.path.isfile(name):
    read_file(name, 0)

elif os.path.isdir(name):
    read_dir(name)

else:
    print("No such file or directory: {0} \n".format(name))
    sys.exit(-1)
