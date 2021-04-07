import math



class Node:
    def __init__(self,data):
        self.data = data
        self.left = self.right = None

    def printTree(self, ref = "root ->") -> None:
        
        if self == None:
            return
        
        print(ref, self.data)

        if self.left != None:
            self.left.printTree(ref + " left ->")

        if self.right != None:
            self.right.printTree(ref + " right ->")

class BTree:
    __preorder = 0

    def __init__(self, data = None):
        self.root = Node(data)

    def print_BTree(self) -> None:
        self.root.printTree()        

    def search(self, item) -> str:

        temp = self.root

        result = "root"
        
        if temp == None:
            return "Error: Empty tree"

        while temp != None:
            if temp.data == item:
                return f"Found At: {result}."
            else:
                result += " -> left" if temp.data > item else " -> right"
                temp = temp.left if temp.data > item else temp.right                

        return "Result not found."

    def BuildTree(self, inorder, preorder):
        inord = inorder.copy()
        preord = preorder.copy()
        self.root = self.builder(inord, preord)

    def builder(self, inorder, preorder):

        if len(inorder) <= 0 or len(preorder) <= 0:
            return None

        data = preorder[self.__preorder]
        ridx =  inorder.index(data)
        self.__preorder += 1
        
        left_in = inorder[:ridx]
        right_in = inorder[ridx+1:]

        root = Node(data)

        if len(left_in) > 0:
            root.left = self.builder(left_in, preorder)

        if len(right_in) > 0:
            root.right = self.builder(right_in, preorder)

            
        return root

    def isPrefect(self, root) -> bool: # Not a exact procedure
        '''
        A perfect binary tree is a type of binary tree in which every internal node 
        has exactly two child nodes and all the leaf nodes are at the same level or depth.
        '''
        if root == None:
            return True

        if root.left == None and root.right == None:
            return True

        if root.left != None:
            left = self.isPrefect(root.left)
        else:
            left = False
        
        if root.right != None:
            right = self.isPrefect(root.right)
        else:
            right = False

        return left and right

    def is_Prefect(self, root, d, level) -> bool: # The exact procedure
        '''
        A perfect binary tree is a type of binary tree in which every internal node 
        has exactly two child nodes and all the leaf nodes are at the same level or depth.
        '''
        if root == None:
            return True

        if root.left == None and root.right == None:
            return (d == level + 1)

        if root.left != None or root.right != None:
            return False
            
        return is_Prefect(root.left, d , level + 1) and is_Prefect(root.right, d , level + 1) 

    def Height(self, root) -> int:
        if root == None:
            return 0

        return 1 + max(self.Height(root.left), self.Height(root.right))

    def NodeCount(self, root) -> int:
        if root == None:
            return 0

        return 1 + self.NodeCount(root.left) + self.NodeCount(root.right)


    def is_Prefect_Formula(self) -> bool: # Not a exact procedure
        '''
        A perfect binary tree is a type of binary tree in which every internal node 
        has exactly two child nodes and all the leaf nodes are at the same level or depth.

        A perfect binary tree of height h has 2h + 1 – 1 node.

        node = pow( 2, h + 1) - 1

        '''
        h = self.Height(self.root) - 1

        n = self.NodeCount(self.root)

        return n == pow( 2, h + 1) - 1


    def isFull(self, root):
        if root == None:
            return True

        if root.left == None and root.right == None:
            return True

        if root.left != None and root.right !=None:
            return (self.isFull(root.left) and self.isFull(root.right))

        return False



def main():
    
    # Root Node
    btree = BTree()
    btree.BuildTree([4,5,6,7],[6,4,5,7])
    # # Left Sub Tree
    # btree.root.left = Node(4)
    # btree.root.left.left = Node(3)
    # btree.root.left.right = Node(5)
    # # Right Sub Tree
    # btree.root.right = Node(8)
    # btree.root.right.left = Node(7)
    # btree.root.right.right = Node(9)


    btree.print_BTree()
    print("Height:",btree.Height(btree.root))

    # # Check for Perfect Binary Tree
    # print( 'This is perfect binary tree' if btree.isPrefect(btree.root) else 'This is not a perfect binary tree' )
    # print( 'This is perfect binary tree' if btree.is_Prefect(btree.root, btree.Height(btree.root), 0) else 'This is not a perfect binary tree' )
    # print( 'This is perfect binary tree' if btree.is_Prefect_Formula() else 'This is not a perfect binary tree' )
    # print(btree.search(4))
    # print(btree.search(9))
    # print(btree.search(10))



if __name__ == "__main__": 
    main()
    #print(math.frexp(6))
     