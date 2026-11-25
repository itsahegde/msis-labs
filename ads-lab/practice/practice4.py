size = 10
arr = [None] * size


def insert(key):
    index = key % size
    start = index

    while arr[index] is not None and arr[index] != "DEL":
        if arr[index] == key:
            print("Key already present in table")
            return
        index = (index + 1) % size
        if index == start:
            print("Table full")
            return

    arr[index] = key
    print("Element inserted into table")


def search(key):
    index = key % size
    start = index

    while arr[index] is not None:
        if arr[index] == key:
            print("Key found at index:", index)
            return True, index
        index = (index + 1) % size
        if index == start:
            break

    print("Element not in table")
    return False, -1


def delete(key):
    found, ind = search(key)
    if found:
        arr[ind] = "DEL"
        print("Element deleted")
    else:
        print("Key not found")