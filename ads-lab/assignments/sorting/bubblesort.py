def bubblesort(arr):
    n =  len(arr)
    for i in range(n-1):
        swapped = False
        for j in range(n-1-i):
            if arr[j]>arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if not swapped:
            break
    for i in range(len(arr)):
        print(arr[i])

arr = [3,4,5,1,9,2,7,0,6]
bubblesort(arr)
