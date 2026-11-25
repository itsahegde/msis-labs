# bst 

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def insert(node, val):
    if node is None:
        return TreeNode(val)
    else:
        if node.data < val:
            node.right = insert(node.right, val)
        elif node.data > val:
            node.left = insert(node.left, val)
    return node

def inser_it(node, val):
    new_node = TreeNode(val)
    curr = node
    if node is None:
        return new_node
    while True:
        if curr.val > val:
            if curr.left is None:
                curr.left = new_node
            curr = curr.left
        elif curr.val < val:
            if curr.right is None:
                curr.right = new_node
            curr = curr.right
        else:
            return node

def search(node, target):
    if node is None:
        return None
    elif node.data == target:
        return node
    elif node.data < target:
        return search(node.right, target)
    else:
        return search(node.left, target)

def search_it(node, target):
    curr = node
    while curr is not None:
        if curr.val > target:
            curr = curr.left
        elif curr.val < target:
            curr = curr.right
        else:
            return curr
    return None

def minvaluenode(node):
    curr = node
    while curr.left is not None:
        curr = curr.left
    return curr

def delete(node, target):
    if not node:
        return None
    
    if node.data < target:
        node.right = delete(node.right, target)
    elif node.data > target:
        node.left = delete(node.left, target)
    else:
        if not node.left:
            return node.right
        elif not node.right:
            return node.left
        node.data = minvaluenode(node.right).data
        node.right = delete(node.right, node.data)
    
    return node

def inorder(node):
    if not node:
        return
    inorder(node.left)
    print({node.data})
    inorder(node.right)

if __name__ == "__main__":

    root = TreeNode(13)
    node7 = TreeNode(7)
    node15 = TreeNode(15)
    node3 = TreeNode(3)
    node8 = TreeNode(8)
    node14 = TreeNode(14)
    node19 = TreeNode(19)
    node18 = TreeNode(18)
    root.left = node7
    root.right = node15

    node7.left = node3
    node7.right = node8

    node15.left = node14
    node15.right = node19

    node19.left = node18

    inorder(root)

    result = search(root, 14)
    if result:
        print(f"Result found: {result.data}")
    else:
        print("Value not found in bst")

    result = search(root, 99)
    if result:
        print(f"Result found: {result.data}")
    else:
        print("Value not found in bst")

    insert(root, 10)

    print(minvaluenode(root).data)

    delete(root,15)

    inorder(root)