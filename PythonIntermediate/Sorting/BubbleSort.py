def bubble_sort(arr):
    n = len(arr)

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def recursive_bubble_sort(listt):
    for i, num in enumerate(listt):
        try:
            if listt[i + 1] < num:
                listt[i] = listt[i + 1]
                listt[i + 1] = num
                bubble_sort(listt)
        except IndexError:
            pass
    return listt


A = [3, 12, 5, 81, 2, 17, 5]
print(bubble_sort(A))
print(recursive_bubble_sort(A))
