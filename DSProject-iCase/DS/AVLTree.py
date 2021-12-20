class Node:
    def __init__(self, data=None):
        self.data = data
        self.left = None
        self.right = None
        self.height = 0

    def __repr__(self):
        return str(self.data)
        # return "[node:" + str(self.data) + ']'


class AVL:
    def __init__(self):
        self.root = None
        self.length = 0

    def insert(self, data):
        if not self.root:
            self.root = Node(data)
            self.length += 1
        else:
            self.root = self._insert(data, self.root)

    def _insert(self, data, node):
        if data < node.data:
            if node.left:
                node.left = self._insert(data, node.left)
                return self._rebalance(node)
            else:
                node.left = Node(data)
                self.length += 1
                return node
        elif data > node.data:
            if node.right:
                node.right = self._insert(data, node.right)
                return self._rebalance(node)
            else:
                node.right = Node(data)
                self.length += 1
                return node

    def _rebalance(self, node):
        bf = self.balance_factor(node)

        # Left heavy tree
        if bf > 1:
            if node.left:
                if self.balance_factor(node.left) > 0:
                    # Left Left case; Perform Right rotate to fix it.
                    return self.rotate_right(node)
                elif self.balance_factor(node.left) < 0:
                    # Left Right case; Perform Left rotate then Right rotate to fix it.
                    node.left = self.rotate_left(node.left)
                    return self.rotate_right(node)

        # Right heavy tree
        if bf < -1:
            if node.right:
                if self.balance_factor(node.right) < 0:
                    # Right Right case; Perform Left ritate to fix it.
                    return self.rotate_left(node)
                elif self.balance_factor(node.right) > 0:
                    # Right Left case; Perform Right rotate then Left rotate to fix it.
                    node.right = self.rotate_right(node.right)
                    return self.rotate_left(node)

        return node            
        
    def rotate_left(self, x):
        # prep
        y = x.right
        T2 = y.left

        # perform
        x.right = T2
        y.left = x
        return y

    def rotate_right(self, x):
        # prep
        y = x.left
        T2 = y.right

        # perform
        x.left = T2
        y.right = x
        return y

    def insert_no_return(self, data):
        if not self.root:
            self.root = Node(data)
            self.length += 1
        else:
            self._insert_no_return(data, self.root)
            self.root = self._rebalance(self.root)

    def _insert_no_return(self, data, node):
        if data < node.data:
            if node.left:
                self._insert_no_return(data, node.left)
                node.left = self._rebalance(node.left)
            else:
                node.left = Node(data)
                self.length += 1

        elif data > node.data:
            if node.right:
                self._insert_no_return(data, node.right)
                node.right = self._rebalance(node.right)
            else:
                node.right = Node(data)
                self.length += 1

    def in_order_traversal(self, node=None):
        elements = []
        if self.root is None:
            return None
        if node is None:
            node = self.root

        if node.left:
            elements += self.in_order_traversal(node.left)

        elements.append(node.data)

        if node.right:
            elements += self.in_order_traversal(node.right)

        return elements

    def _in_order_successor(self, node):
        if node.right:
            # Case I
            succ = node.right
            while succ.left:
                succ = succ.left
            return succ

        if not node.right:
            # Case II
            p = self.root
            while (p is not None):
                if node.data < p.data:
                    # p is greather than the node; might be the successor
                    succ = p
                    p = p.left
                if node.data > p.data:
                    # p is less than the node; should go right for being greather
                    p = p.right

            return succ

    def delete(self, data):
        if self.root is None:
            raise ValueError

        self.root = self._delete(data, self.root)
        self.length -= 1
        self.root = self._rebalance(self.root)

    def _delete(self, data, node):

        if node is None:
            raise ValueError(f"{data} is not contained in the tree")

        if data == node.data:
            # 4 State:
            if not node.left and not node.right:
                # Has no child
                return None

            if node.left and not node.right:
                # Has only left child
                return node.left

            if not node.left and node.right:
                # Has only right child
                return node.right

            if node.left and node.right:
                # Has both child

                # replace the deleted node with the successor
                succ = self._in_order_successor(node)
                node.data = succ.data

                # delete old successor node
                node.right = self._delete(succ.data, node.right)

                return node

        elif data < node.data:
            node.left = self._delete(data, node.left)
            return self._rebalance(node)

        elif data > node.data:
            node.right = self._delete(data, node.right)
            return self._rebalance(node)

        raise ValueError

    def is_empty(self):
        return self.root is None

    def is_not_empty(self):
        return self.root is not None

    def height(self):
        return self._height(self.root)

    def _height(self, node=None):
        if self.root is None:
            return None

        if node is None:
            return 0

        return 1 + max(self._height(node.left), self._height(node.right))

    def balance_factor(self, node):
        if node is None:
            node = self.root

        try:
            hl = self._height(node.left)
        except:
            hl = 0

        try:
            hr = self._height(node.right)
        except:
            hr = 0

        return hl-hr

    def search(self,x,node=None):
        if node is None:
            node = self.root

        if node.data == x:
            return node

        elif x > node.data:
            if node.left is not None:
                return self.search(x,node.left)

        elif x < node.data:
            if node.right is not None:
                return self.search(x,node.right)

        raise KeyError(f'{x} is not in the tree')

    def __len__(self):
        return self.length

    def _printTree(self, node, level=0):
        if node != None:
            self._printTree(node.right, level + 1)
            print('     ' * level, node)
            self._printTree(node.left, level + 1)

    def print_tree(self):
        self._printTree(self.root)

    def __repr__(self) :

        elements = self.in_order_traversal()        

        return '[' + ','.join(str(x) for x in elements) + ']'

    def __iter__(self):
        elements = self.in_order_traversal()
        if elements is None:
            # No elements
            return

        for e in elements:
            yield e