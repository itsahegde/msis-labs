class Node:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None

class DoubleLL:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    def append(self, val):
        node = Node(val)
        if not self.head:
            self.head = self.tail = node
            self.size+=1
            return
        self.tail.next = node
        node.prev = self.tail
        self.tail = node
        self.size+=1
        return
    def delete(self, val):
        if self.head is None:
            print("List is empty!! ")
            return 
        
        if self.head.val == val:
            print(f"Head node with value {self.head.val} deleted!! ")
            self.head = self.head.next
            self.size-=1

            if self.head is None:
                self.head = None

            return
        curr = self.head

        while curr.next is not None and curr.next.val != val:
            curr = curr.next

        if curr.next is None:
            print(f"Node with value {val} not found!! ")
            return 

        if curr.prev is not None:
            curr.prev.next = curr.next
        else:
            self.head = curr.next

        if curr.next is not None:
            curr.next.prev = curr.prev
        else:
            self.tail = curr.prev

        self.size-=1
        print(f"Node with value {curr.next.val} deleted")

    def appendAtHead(self, val):
        node = Node(val)
        if self.head is None:
            self.head , self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node

        self.size+=1
        print(f"Node of val: {node.val} added at head.")

    def getSize(self):
        print("Size of Linkedlist: ", self.size)
    def getHeadNode(self):
        if self.head is None:
            print("List is empty")
            return
        print("Head Node val: ", self.head.val)
    def getTailNode(self):
        if self.tail is None:
            print("List is empty")
            return
        print("Tail Node val: ", self.tail.val)
    def display(self):
        curr = self.head
        if not self.head:
            print("Empty List, cannot print anything!! ")
            return
        while curr.next!=None:
            print(curr.val +" ->")
            curr = curr.next
        print(curr.val)
        print(" End of LinkedList. ")

def main():
    ll = DoubleLL()
    while True:
        print("\n---- Doubly Linked List Menu ----")
        print("1. Append Node")
        print("2. Append Node at Head")
        print("3. Delete Node")
        print("4. Get Size")
        print("5. Display")
        print("6. Get Head")
        print("7. Get Tail")
        print("8. Exit")

        choice = input("Enter a number between 1 and 5: ").strip()
        if choice == "1":
            val = input("Enter a value to append: ")
            ll.append(val)
        elif choice == "2":
            val = input("Enter a value to append at head: ")
            ll.appendAtHead(val)
        elif choice == "3":
            val = input("Enter value of node to be deleted: ")
            ll.delete(val)
        elif choice == "4":
            ll.getSize()
        elif choice == "5":
            ll.display()
        elif choice == "6":
            ll.getHeadNode()
        elif choice == "7":
            ll.getTailNode()
        elif choice == "8":
            break
        else:
            print("Invalid choice, please select again! ")

if __name__ == "__main__":
    main()

    

        

        