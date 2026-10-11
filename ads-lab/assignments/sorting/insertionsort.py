def sort(arr):

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j>=0 and arr[j]>key:
            arr[j+1] = arr[j]
            j-=1

        arr[j+1] = key

    for i in range(len(arr)):
        print(arr[i])

arr = [3,4,5,1,9,2,7,0,6]
sort(arr)
