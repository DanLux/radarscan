# Generic BBST Node structure
class Node:
    def __init__(self, value, relation_function):
        self.value = value
        self.left_son = None
        self.right_son = None
        self.parent = None
        self.height = 1
        self.total_order_relation = relation_function

    def is_right_child(self):
        return self.parent.right_son == self

    def is_left_child(self):
        return self.parent.left_son == self

    def update_height(self):
        left_height = 0 if self.left_son is None else self.left_son.height
        right_height = 0 if self.right_son is None else self.right_son.height
        self.height = 1 + max(left_height, right_height)

    def get_balance(self):
        left_height = 0 if self.left_son is None else self.left_son.height
        right_height = 0 if self.right_son is None else self.right_son.height
        return left_height - right_height

    def lesser_than(self, node):
        return self.total_order_relation(self, node) == -1

    def greater_than(self, node):
        return self.total_order_relation(self, node) == 1

    def equal(self, node):
        return not(self.greater_than(node) or self.lesser_than(node))

# Generic BBST structure
class BalancedBinarySearchTree:
    def __init__(self, function):
        self.root = None
        self.comparison_function = function

    def contains(self, value):
        node = self.__get(self.__create_node(value), self.root)
        if node is None: return False
        else: return True

    def __create_node(self, value):
        return Node(value, self.comparison_function)

    def __get(self, node, root):
        if root is None: return None

        if node.lesser_than(root):
            return self.__get(node, root.left_son)
        elif node.greater_than(root):
            return self.__get(node, root.right_son)
        else:
            return root

    def insert(self, value):
        new_node = self.__create_node(value)
        if self.root is None:
            self.root = new_node
            self.root.parent = self.root
        else: self.__insert(self.root, new_node)

    def remove(self, value):
        node = self.__get(self.__create_node(value), self.root)
        if not(node.left_son is None or node.right_son is None):
            successor = BalancedBinarySearchTree.__min_node(node.right_son)
            node.value = successor.value
            node = successor

        if node.left_son and (not node.right_son):
            if self.root == node:
                node.left_son.parent = node.left_son
                self.root = node.left_son
            else:
                node.left_son.parent = node.parent
                if node.is_left_child():
                    node.parent.left_son = node.left_son
                else:
                    node.parent.right_son = node.left_son
                self.__balance_tree_after_deletion(node.parent)

        elif node.right_son and (not node.left_son):
            if self.root == node:
                node.right_son.parent = node.right_son
                self.root = node.right_son
            else:
                node.right_son.parent = node.parent
                if node.is_right_child():
                    node.parent.right_son = node.right_son
                else:
                    node.parent.left_son = node.right_son
                self.__balance_tree_after_deletion(node.parent)

        else:
            if self.root == node:
                self.root = None
            else:
                if node.is_left_child():
                    node.parent.left_son = None
                else:
                    node.parent.right_son = None
                self.__balance_tree_after_deletion(node.parent)

    def min(self):
        min_node = BalancedBinarySearchTree.__min_node(self.root)
        return None if min_node is None else min_node.value

    @staticmethod
    def __min_node(root):
        if root is None or root.left_son is None:
            return root
        else:
            return BalancedBinarySearchTree.__min_node(root.left_son)

    def __insert(self, node, new_node):
        if new_node.lesser_than(node):
            if node.left_son:
                self.__insert(node.left_son, new_node)
            else:
                node.left_son = new_node
                node.left_son.parent = node
                self.__balance_tree_after_insertion(node)
        else:
            if node.right_son:
                self.__insert(node.right_son, new_node)
            else:
                node.right_son = new_node
                node.right_son.parent = node
                self.__balance_tree_after_insertion(node)

    def __balance_tree_after_insertion(self, node):
        node.update_height()
        if node.get_balance() == 1 or node.get_balance() == -1:
            if self.root != node:
                self.__balance_tree_after_insertion(node.parent)
        elif node.get_balance() == 2:
            if node.left_son.get_balance() == 1:
                self.__rotate_right(node)
            else: self.__rotate_left_right(node)
        elif node.get_balance() == -2:
            if node.right_son.get_balance() == -1:
                self.__rotate_left(node)
            else: self.__rotate_right_left(node)

    def __balance_tree_after_deletion(self, node):
        node.update_height()
        parent = node.parent

        if node.get_balance() == 2:
            if node.left_son.get_balance() == -1:
                self.__rotate_left_right(node)
            else: self.__rotate_right(node)
        if node.get_balance() == -2:
            if node.right_son.get_balance() == 1:
                self.__rotate_right_left(node)
            else: self.__rotate_left(node)

        if parent != node:
            self.__balance_tree_after_deletion(parent)

    def __rotate_right(self, node):
        son = node.left_son
        node.left_son = son.right_son
        if son.right_son:
            son.right_son.parent = node
        if self.root == node:
            son.parent = son
            self.root = son
        else:
            son.parent = node.parent
            if node.is_right_child():
                node.parent.right_son = son
            else: node.parent.left_son = son
        son.right_son = node
        node.parent = son
        node.update_height()
        son.update_height()

    def __rotate_left(self, node):
        son = node.right_son
        node.right_son = son.left_son
        if son.left_son:
            son.left_son.parent = node
        if self.root == node:
            son.parent = son
            self.root = son
        else:
            son.parent = node.parent
            if node.is_left_child():
                node.parent.left_son = son
            else: node.parent.right_son = son
        son.left_son = node
        node.parent = son
        node.update_height()
        son.update_height()

    def __rotate_left_right(self, node):
        son = node.left_son
        grandson = son.right_son
        son.right_son = grandson.left_son
        if grandson.left_son:
            grandson.left_son.parent = son
        node.left_son = grandson.right_son
        if grandson.right_son:
            grandson.right_son.parent = node

        son.update_height()
        node.update_height()

        grandson.left_son = son
        son.parent = grandson
        if self.root == node:
            grandson.parent = grandson
            self.root = grandson
        else:
            grandson.parent = node.parent
            if node.is_left_child():
                node.parent.left_son = grandson
            else: node.parent.right_son = grandson
        grandson.right_son = node
        node.parent = grandson
        grandson.update_height()

    def __rotate_right_left(self, node):
        son = node.right_son
        grandson = son.left_son
        son.left_son = grandson.right_son
        if grandson.right_son:
            grandson.right_son.parent = son
        node.right_son = grandson.left_son
        if grandson.left_son:
            grandson.left_son.parent = node

        son.update_height()
        node.update_height()

        grandson.right_son = son
        son.parent = grandson
        if self.root == node:
            grandson.parent = grandson
            self.root = grandson
        else:
            grandson.parent = node.parent
            if node.is_right_child():
                node.parent.right_son = grandson
            else: node.parent.left_son = grandson
        grandson.left_son = node
        node.parent = grandson
        grandson.update_height()


    def print_tree(self):
        print
        self.__print_tree_rec(0, self.root)
        print

    def __print_tree_rec(self, tabs, node):
        for i in range(0, tabs):
            print " ",
        if not node is None:
            print str(node.value) + '(' + str(node.parent.value) + '/' + str(node.get_balance()) + ')'
            self.__print_tree_rec(tabs + 3, node.right_son)
            self.__print_tree_rec(tabs + 3, node.left_son)
        else: print 'Nil'


######################################################################
# Simple tree structure test

def node_comparison_function_test(self, node):
    if self.value < node.value: return -1
    elif self.value > node.value: return 1
    else: return 0


def test_avl_tree():
    tree = BalancedBinarySearchTree(node_comparison_function_test)
    while True:
        v = raw_input()
        if tree.contains(v):
            tree.remove(v)
        else: tree.insert(v)
        tree.print_tree()
######################################################################
