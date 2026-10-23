from collections import deque


class Node:
    def __init__(self, val):
        self.left = None
        self.right = None
        self.val = val
class BST:
    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, val):
        node = Node(val)

        if self.root is None:
            self.root = node
            self.size+=1
            print("Node inserted at Root with value: ", self.node.val)
            return

        curr = self.root

        while True:
            if curr.val> val:
                if curr.left is None:
                    curr.left = node
                    self.size+=1
                    print("Node inserted with value: ", node.val)
                    return
                curr = curr.left
            elif curr.val<val:
                if curr.right is None:
                    curr.right = node
                    self.size+=1
                    print("Node inserted with value: ", node.val)
                    return
                curr = curr.right
            else:
                print("Cannot insert duplicate node with value: ", node.val)
                return

    def search(self, val):
        curr = self.root

        while curr is not None:
            if curr.val == val:
                print(f"Node with value {val} found. ")
                return True
            elif curr.val > val:
                curr = curr.left
            else:
                curr = curr.right

        print(f"Node with value {val} not found. ")
        return False

    def findMin(self, node):
        while node.left is not None:
            node = node.left
        return node

    def delete(self, val):
        self.root, deleted = self._delete(self.root, val)

        if deleted:
            self.size-=1
            print(f"Node with value {val} deleted. ")
        else:
            print(f"Node with value {val} not found. ")

    def _delete(self, node, val):
        if node is None:
            return None, False
        if val<node.val:
            node.left, deleted = self._delete(node.left, val)
        elif val>node.val:
            node.right, deleted = self._delete(node.right, val)

        else:
            if node.left is None and node.right is None:
                return None, True
            if node.right is None:
                return node.left
            if node.left is None:
                return node.right
            
            successor = self.findMin(node.right)
            node.val = successor.val
            node.right, _ = self._delete(node.right, successor.val)
            return node, True

        return node, deleted

    def preorder(self, node):
        if node is None:
            return
        print(node.val, end=' ')
        self.preorder(node.left)
        self.preorder(node.right)

    def inorder(self, node):
        if node is None:
            return
        self.inorder(node.left)
        print(node.val, end=' ')
        self.inorder(node.right)

    def postorder(self, node):
        if node is None:
            return
        self.postorder(node.left)
        self.postorder(node.right)
        print(node.val, end=' ')

    def levelOrder(self, node):
        if self.root is None:
            print("Tree is empty!! ")
            return 

        que = deque([self.root])

        while que:

            curr = que.popleft()
            print(curr.val, end=" ")

            if curr.left:
                que.append(curr.left)
            if curr.right:
                que.append(curr.right)

    def getMin(self, node):
        if self.root is None:
            print("Tree is empty !! ")
            return

        print("Minimum value: ", self.findMin(self.root).val)

    def getMax(self, node):
        if self.root is None:
            print("Tree is empty !! ")
            return

        curr = self.root

        while curr.right is not None:
            curr = curr.right

        print("Maximum Value: ", curr.val)

    def getSize(self):
        if self.root is None:
            print("Empty tree!! ")
            return
        print("Size of tree: ", self.size)

    def getRoot(self):
        if self.root is None:
            print("Empty Tree !! ")
            return
        print("Root of tree: ", self.root.val)

    def display(self):
        if self.root is None:
            print("Empty Tree !! ")
            return

        que = deque([self.root])
        while que:

            curr = que.popleft()
            leftval = curr.left.val if curr.left else None
            rightval = curr.right.val if curr.right else None

            print(
                f"Node value: {curr.val} "
                f"Left = {leftval}"
                f"Right = {rightval}"
            )

            if curr.left:
                que.append(curr.left)
            if curr.right:
                que.append(curr.right)

def main():
    bst = BST()

    while True:
        print("\n---- Binary Search Tree Menu ----")
        print("1. Insert Node")
        print("2. Delete Node")
        print("3. Search Node")
        print("4. Preorder Traversal")
        print("5. Inorder Traversal")
        print("6. Postorder Traversal")
        print("7. Level-order Traversal")
        print("8. Get Minimum")
        print("9. Get Maximum")
        print("10. Get Size")
        print("11. Get Root")
        print("12. Display Tree")
        print("13. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            val = int(input("Enter value to insert: "))
            bst.insert(val)

        elif choice == "2":
            val = int(input("Enter value to delete: "))
            bst.delete(val)

        elif choice == "3":
            val = int(input("Enter value to search: "))
            bst.search(val)

        elif choice == "4":
            print("Preorder:", end=" ")
            bst.preorder(bst.root)
            print()

        elif choice == "5":
            print("Inorder:", end=" ")
            bst.inorder(bst.root)
            print()

        elif choice == "6":
            print("Postorder:", end=" ")
            bst.postorder(bst.root)
            print()

        elif choice == "7":
            print("Level-order:", end=" ")
            bst.levelorder()
            print()

        elif choice == "8":
            bst.getMin()

        elif choice == "9":
            bst.getMax()

        elif choice == "10":
            bst.getSize()

        elif choice == "11":
            bst.getRoot()

        elif choice == "12":
            bst.display()

        elif choice == "13":
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()


