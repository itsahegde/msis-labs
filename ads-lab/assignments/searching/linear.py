def linearsearch(arr, x):
    for i in range(len(arr)):
        if arr[i] == x:
            return i
    return -1

arr = [3,4,5,1,9,2,7,0,6]
print(linearsearch(arr, 9))