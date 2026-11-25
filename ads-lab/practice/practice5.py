# seperate chaining hash table

size = 10
table = [[] for i in range(size)]

def insert(key):
    index = (key)%size
    if key in table[index]:
        print("Key already present in table")
        return
    table[index].append(key)

def search(key):
    index = (key)%size
    if key in table[index]:
        print("Key found at index", index)
        return
    print("Key not found")

def delete(key):
    index = (key)%size
    if key in table[index]:
        print("Deleted key")
        table[index].remove(key)
        return
    print("Key not found")
    