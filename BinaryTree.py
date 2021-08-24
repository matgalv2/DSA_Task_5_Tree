import queue


class Node:

    def __init__(self, value: int):
        self.value: int = value
        self.parent: Node = None
        self.leftChild: Node = None
        self.rightChild: Node = None

    def setParent(self, parentNode):
        self.parent = parentNode

    def setChild(self, child):
        if child.value < self.value:
            self.leftChild = child
        else:
            self.rightChild = child

    def getLeftChild(self):
        return self.leftChild

    def getRightChild(self):
        return self.rightChild

    @staticmethod
    def inorder(node):
        if node is not None:
            node.inorder(node.leftChild)
            print(node)
            node.inorder(node.rightChild)

    def __str__(self):
        left = '_'
        right = '_'
        if self.leftChild is not None:
            left = self.leftChild.value
        if self.rightChild is not None:
            right = self.rightChild.value

        return str(self.value) + '[' + str(left) + ',' + str(right) + ']'

    # def __delete__(self, instance):
    #     del self.value


class BinarySearchTree(object):

    # def __init__(self):
    #     self.root = Node(0)

    def __init__(self, initialValue: int):
        self.root = Node(initialValue)

    def __str__(self):
        self.root.inorder(self.root)

    def getRoot(self) -> Node:
        return self.root

    def add(self, value: int):

        def addRec(value: int, node: Node, parent: Node or None):
            if node is not None:
                if value > node.value:
                    addRec(value, node.rightChild, node)
                else:
                    addRec(value, node.leftChild, node)
            else:
                node = Node(value)
                node.setParent(parent)
                parent.setChild(node)

        addRec(value, self.root, None)

    def height(self) -> int:
        def heightRec(node: Node) -> int:
            if node is None:
                return -1
            left = heightRec(node.leftChild)
            right = heightRec(node.rightChild)

            # return 1 + max(heightRec(node.leftChild), heightRec(node.rightChild))
            return 1 + max(left, right)

        return heightRec(self.root)

    def inorderDFS(self, function):
        def inorderRec(node):
            if node is not None:
                inorderRec(node.leftChild)
                function(node)
                inorderRec(node.rightChild)

        inorderRec(self.root)

    def pointRoot(self, node):
        if node == self.root:
            print(str(node) + '-> root')
        else:
            print(node)

    def find(self, value: int) -> Node:

        nodesQue = queue.Queue()
        nodesQue.put(self.root)

        while not (nodesQue.empty()):
            tmp: Node = nodesQue.get()
            if tmp is not None:
                if tmp.value == value:
                    return tmp

                nodesQue.put(tmp.leftChild)
                nodesQue.put(tmp.rightChild)

    def minValueSubtree(self, node):
        if node.leftChild is None:
            return node
        return self.minValueSubtree(node.leftChild)

    def successor(self, value) -> Node or None:
        node = self.find(value)
        if node.rightChild is not None:
            return self.minValueSubtree(node.rightChild)

        elif node.rightChild is None:
            while node is not None:
                '''We don't have to divide statement into 2 "ifs" because python supports lazy evaluation.'''
                if node.parent is not None and node.parent.leftChild == node:
                    return node.parent
                node = node.parent
        else:
            return None

    def deleteNode(self, value):
        node: Node = self.find(value)

        # 1st case (0 children)
        if node.leftChild is None and node.rightChild is None:
            if node.parent is not None:
                if node.parent.leftChild == node:
                    node.parent.leftChild = None
                else:
                    node.parent.rightChild = None

        # 2nd case (1 child)
        elif node.leftChild is None or node.rightChild is None:

            if node.leftChild is not None:
                node.parent.leftChild = node.leftChild
                node.leftChild.parent = node.parent

            else:
                node.parent.rightChild = node.rightChild
                node.rightChild.parent = node.parent

        # 3rd case (2 children)
        else:
            successor = self.successor(value)

            # Checking if a node isn't the root of the tree.
            if node.parent is not None:
                successor.parent = node.parent

                if node.parent.leftChild == node:
                    node.parent.leftChild = successor
                    successor.leftChild = node.leftChild

                else:
                    node.parent.rightChild = successor
                    successor.rightChild = node.rightChild

            else:

                if successor.parent.leftChild == successor:
                    successor.parent.leftChild = successor.leftChild
                else:
                    successor.parent.rightChild = successor.rightChild

                successor.leftChild = node.leftChild
                node.leftChild.parent = successor

                successor.rightChild = node.rightChild
                node.rightChild.parent = successor

                successor.parent = None
                self.root = successor


BST = BinarySearchTree(4)

# BST.getRoot().__delete__(k.getRoot())

BST.add(5)
BST.add(6)
BST.add(2)
BST.add(3)
BST.add(1)
BST.deleteNode(4)

# BST.inorderDFS(print)
BST.inorderDFS(BST.pointRoot)
