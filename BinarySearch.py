import sys


def fillList():
    newList = []
    oldList = input("Введите числа через пробел: ")
    oldList = oldList.split()
    for el in oldList:
        newList.append(int(el))
    newList.sort()
    return newList


def binarySearch(ourList):
    val = int(input("Введите искомый элемент: "))
    first = 0
    last = len(ourList)-1
    index = -1
    while (first <= last) and (index == -1):
        mid = (first + last) // 2
        if ourList[mid] == val:
            index = mid
        else:
            if val < ourList[mid]:
                last = mid - 1
            else:
                first = mid + 1
    return index


def except_hook(cls, exception, traceback):
   sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    list1 = fillList()
    print("Список: ", list1)
    result = binarySearch(list1)
    if result != -1:
        print("Индекс элемента:", str(result))
    else:
        print("Индекс элемента не найден.")
