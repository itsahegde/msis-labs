class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedListQueue:
    def __init__(self):
        self.front = None
        self.rear = None
        self._size = 0

    def is_empty(self):
        return self.front is None

    def enqueue(self, item):
        new_node = Node(item)
        if self.is_empty():
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self._size += 1
        print(f"Enqueued: {item}")

    def dequeue(self):
        if self.is_empty():
            print("Queue Underflow! Queue is empty.")
            return None
        dequeued = self.front.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self._size -= 1
        return dequeued

    def peek(self):
        if self.is_empty():
            print("Queue is empty.")
            return None
        return self.front.data

    def display(self):
        if self.is_empty():
            print("Queue is empty.")
            return
        curr = self.front
        elements = []
        while curr:
            elements.append(str(curr.data))
            curr = curr.next
        print("Front -> " + " -> ".join(elements) + " <- Rear")

    def size(self):
        return self._size


def main():
    queue = LinkedListQueue()
    while True:
        print("\n--- Queue (Linked List) Menu ---")
        print("1. Enqueue")
        print("2. Dequeue")
        print("3. Peek")
        print("4. Display")
        print("5. Size")
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
            print(f"Current size: {queue.size()}")
        elif choice == "6":
            print("Exiting program.")
            break
        else:
            print("Invalid choice! Please select 1-6.")


if __name__ == "__main__":
    main()