import sys


def except_hook(cls, exception, traceback):
   sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
 print()