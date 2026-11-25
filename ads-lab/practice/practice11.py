# bubble sort

def bubble(arr):
    for i in range(len(arr)-1):
        for j in range(len(arr)-1-i):
            if arr[j]>arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

arr = [9, 8, 7, 6]
bubble(arr)
print(arr)

