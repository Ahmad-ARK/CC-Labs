class Node:
    def __init__(self, key, scope, type_val, line_no):
        self.key = key
        self.scope = scope
        self.type = type_val
        self.line_no = line_no
        self.height = 1
        self.left = None
        self.right = None

class SymbolTable:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def rotate_right(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def rotate_left(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, key, scope, type_val, line_no):
        self.root = self._insert(self.root, key, scope, type_val, line_no)

    def _insert(self, node, key, scope, type_val, line_no):
        if not node:
            return Node(key, scope, type_val, line_no)
        elif key < node.key:
            node.left = self._insert(node.left, key, scope, type_val, line_no)
        elif key > node.key:
            node.right = self._insert(node.right, key, scope, type_val, line_no)
        else:
            return node

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        if balance > 1 and key < node.left.key:
            return self.rotate_right(node)
        if balance < -1 and key > node.right.key:
            return self.rotate_left(node)
        if balance > 1 and key > node.left.key:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if balance < -1 and key < node.right.key:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        return node

    def lookup(self, key):
        return self._lookup(self.root, key)

    def _lookup(self, node, key):
        if not node or node.key == key:
            return node
        if key < node.key:
            return self._lookup(node.left, key)
        return self._lookup(node.right, key)

    def modify(self, key, scope, type_val, line_no):
        node = self.lookup(key)
        if node:
            node.scope = scope
            node.type = type_val
            node.line_no = line_no
            return True
        return False

    def display(self):
        self._display(self.root)

    def _display(self, node):
        if node:
            self._display(node.left)
            print(f"ID: {node.key} | Type: {node.type} | Scope: {node.scope} | Line: {node.line_no}")
            self._display(node.right)

if __name__ == "__main__":
    st = SymbolTable()
    st.insert("count", "local", "int", 10)
    st.insert("total", "global", "float", 5)
    st.insert("is_valid", "local", "bool", 12)

    print("Symbol Table Content:")
    st.display()

    print("\nLooking up 'count':")
    res = st.lookup("count")
    if res:
        print(f"Found: {res.key} in {res.scope} scope")

    st.modify("count", "global", "int", 15)
    print("\nAfter modification:")
    st.display()

if __name__ == "__main__":
    st = SymbolTable()

   
    st.insert("if", "local", "keyword", 4)
    st.insert("number", "global", "variable", 2)
    st.insert("total", "global", "float", 5)
    print("Step 1: Symbols inserted successfully.")

    
    print("\nStep 2: Searching for 'if'...")
    record = st.lookup("if")
    if record:
        print(f"Found: {record.key} | Type: {record.type} | Scope: {record.scope}")
    else:
        print("Identifier not found.")

   
    print("\nStep 3: Updating 'number' line reference...")
    if st.modify("number", "global", "variable", 3):
        updated = st.lookup("number")
        print(f"Updated Info: {updated.key} is now on line {updated.line_no}")

    # 4. Display All Entries
    # Shows the final state of the symbol table
    print("\nStep 4: Final Symbol Table State:")
    st.display()