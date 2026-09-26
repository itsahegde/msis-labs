class DynamicArrayQueue:
    def __init__(self):
        self._capacity = 2
        self._head = 0
        self._size = 0
        self._arr = [None] * self._capacity

    def _resize(self, new_capacity):
        new_arr = [None] * new_capacity
        for i in range(self._size):
            new_arr[i] = self._arr[(self._head + i) % self._capacity]
        self._arr = new_arr
        self._head = 0
        self._capacity = new_capacity

    def is_empty(self):
        return self._size == 0

    def enqueue(self, item):
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        tail = (self._head + self._size) % self._capacity
        self._arr[tail] = item
        self._size += 1
        print(f"Enqueued: {item}")

    def dequeue(self):
        if self.is_empty():
            print("Queue Underflow! Queue is empty.")
            return None
        dequeued = self._arr[self._head]
        self._arr[self._head] = None
        self._head = (self._head + 1) % self._capacity
        self._size -= 1
        if 0 < self._size <= self._capacity // 4:
            self._resize(max(2, self._capacity // 2))
        return dequeued

    def peek(self):
        if self.is_empty():
            print("Queue is empty.")
            return None
        return self._arr[self._head]

    def display(self):
        if self.is_empty():
            print("Queue is empty.")
            return
        elements = [
            str(self._arr[(self._head + i) % self._capacity])
            for i in range(self._size)
        ]
        print("Front -> " + " -> ".join(elements) + " <- Rear")

    def size(self):
        return self._size

    def capacity(self):
        return self._capacity


def main():
    queue = DynamicArrayQueue()
    while True:
        print("\n--- Queue (Circular Dynamic Array) Menu ---")
        print("1. Enqueue")
        print("2. Dequeue")
        print("3. Peek")
        print("4. Display")
        print("5. Size & Capacity")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()
        if choice == "1":
            val = input("Enter value to enqueue: ")
            queue.enqueue(val)
        elif choice == "2":
            val = queue.dequeue()
            if val is not None:
                print(f"Dequeued value: {val}")
        elif choice == "3":
            val = queue.peek()
            if val is not None:
                print(f"Front element: {val}")
        elif choice == "4":
            queue.display()
        elif choice == "5":
            print(f"Current size: {queue.size()} | Capacity: {queue.capacity()}")
        elif choice == "6":
            print("Exiting program.")
            break
        else:
            print("Invalid choice! Please select 1-6.")


if __name__ == "__main__":
    main()