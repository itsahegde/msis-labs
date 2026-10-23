def sort(arr, low, high):
    if low<high:
        mid = (low + high)//2
        sort(arr, low, mid)
        sort(arr, mid+1, high)

        merge(arr, low, mid, high)
    return arr

def merge(arr, low, mid, high):
    left, right = arr[low:mid+1], arr[mid+1:high+1]
    i, j, k = 0, 0, low

    while i<len(left) and j<len(right):
        if left[i]<=right[j]:
            arr[k] = left[i]
            i+=1
        elif left[i]>right[j]:
            arr[k] = right[j]
            j+=1
        k+=1

    while i<len(left):
        arr[k] = left[i]
        i+=1
        k+=1
    while j<len(right):
        arr[k] = right[j]
        j+=1
        k+=1  

arr = [3,4,5,1,9,2,7,0,6]
sort(arr, 0, len(arr)-1)
for i in range(len(arr)):
    print(arr[i])
