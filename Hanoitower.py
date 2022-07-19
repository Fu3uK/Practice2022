import sys


def tower_of_hanoi(numbers, start, end):
    if numbers == 1:
        print(f"Переложить диск 1 со стержня-{start} на стержень-{end}")
    else:
        tower_of_hanoi(numbers - 1, start, 6 - start - end)
        print(f"Переложить диск {numbers} со стержня-{start} на стержень-{end}")
        tower_of_hanoi(numbers - 1, 6 - start - end, end)


def except_hook(cls, exception, traceback):
   sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    numbers = int(input("Введите количество дисков: "))
    tower_of_hanoi(numbers, 1, 2)