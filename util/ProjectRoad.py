import os


def getRoad():
    return os.path.abspath(os.path.join(os.getcwd(), ".."))

if __name__ == '__main__':
    print(getRoad())


