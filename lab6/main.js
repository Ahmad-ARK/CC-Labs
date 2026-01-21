// 2022-CS-31

class Node {
  constructor(key, scope, typeVal, lineNo) {
    this.key = key;
    this.scope = scope;
    this.type = typeVal;
    this.lineNo = lineNo;
    this.height = 1;
    this.left = null;
    this.right = null;
  }
}

class SymbolTable {
  constructor() {
    this.root = null;
  }

  getHeight(node) {
    return node ? node.height : 0;
  }

  getBalance(node) {
    return node ? this.getHeight(node.left) - this.getHeight(node.right) : 0;
  }

  rotateRight(y) {
    let x = y.left;
    let T2 = x.right;
    x.right = y;
    y.left = T2;
    y.height = Math.max(this.getHeight(y.left), this.getHeight(y.right)) + 1;
    x.height = Math.max(this.getHeight(x.left), this.getHeight(x.right)) + 1;
    return x;
  }

  rotateLeft(x) {
    let y = x.right;
    let T2 = y.left;
    y.left = x;
    x.right = T2;
    x.height = Math.max(this.getHeight(x.left), this.getHeight(x.right)) + 1;
    y.height = Math.max(this.getHeight(y.left), this.getHeight(y.right)) + 1;
    return y;
  }

  insert(key, scope, typeVal, lineNo) {
    this.root = this._insert(this.root, key, scope, typeVal, lineNo);
  }

  _insert(node, key, scope, typeVal, lineNo) {
    if (!node) return new Node(key, scope, typeVal, lineNo);

    if (key < node.key) {
      node.left = this._insert(node.left, key, scope, typeVal, lineNo);
    } else if (key > node.key) {
      node.right = this._insert(node.right, key, scope, typeVal, lineNo);
    } else {
      return node;
    }

    node.height = 1 + Math.max(this.getHeight(node.left), this.getHeight(node.right));
    let balance = this.getBalance(node);

    if (balance > 1 && key < node.left.key) return this.rotateRight(node);
    if (balance < -1 && key > node.right.key) return this.rotateLeft(node);
    if (balance > 1 && key > node.left.key) {
      node.left = this.rotateLeft(node.left);
      return this.rotateRight(node);
    }
    if (balance < -1 && key < node.right.key) {
      node.right = this.rotateRight(node.right);
      return this.rotateLeft(node);
    }
    return node;
  }

  lookup(key) {
    return this._lookup(this.root, key);
  }

  _lookup(node, key) {
    if (!node || node.key === key) return node;
    if (key < node.key) return this._lookup(node.left, key);
    return this._lookup(node.right, key);
  }

  modify(key, scope, typeVal, lineNo) {
    let node = this.lookup(key);
    if (node) {
      node.scope = scope;
      node.type = typeVal;
      node.lineNo = lineNo;
      return true;
    }
    return false;
  }

  display() {
    const results = [];
    this._inOrder(this.root, results);
    console.table(results);
  }

  _inOrder(node, results) {
    if (node) {
      this._inOrder(node.left, results);
      results.push({
        Identifier: node.key,
        Type: node.type,
        Scope: node.scope,
        Line: node.lineNo
      });
      this._inOrder(node.right, results);
    }
  }
}

const st = new SymbolTable();
st.insert("if", "local", "keyword", 4);
st.insert("number", "global", "variable", 2);
st.insert("total", "global", "float", 5);

console.log("Initial Symbol Table:");
st.display();

console.log("\nSearching for 'number'...");
console.log(st.lookup("number") ? "Found" : "Not Found");

st.modify("number", "global", "int", 10);
console.log("\nAfter Modification:");
st.display();