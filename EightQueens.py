import sys


<<<<<<< Updated upstream
def EightQueens():
    n = 8
    x = []
    y = []
    for i in range(n):
        new_x, new_y = [int(s) for s in input().split()]
        x.append(new_x)
        y.append(new_y)
    correct = True
    for i in range(n):
        for j in range(i + 1, n):
            if x[i] == x[j] or y[i] == y[j] or abs(x[i] - x[j]) == abs(y[i] - y[j]):
                correct = False
    if correct:
        return 1
    else:
        return -1
=======

>>>>>>> Stashed changes


def except_hook(cls, exception, traceback):
   sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
<<<<<<< Updated upstream
    print("Введите числа от 1 до 8")
    result = EightQueens()
    if result == 1:
        print("Ферзи не бьют друг друга.")
    else:
        print("Ферзи бьют друг друга.")
=======
    print()
>>>>>>> Stashed changes
