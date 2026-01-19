const sysArgs = process.argv.slice(2);
const exprStr = sysArgs.join(" ");

function formatNum(n) {
    return Number.isInteger(n) ? n : parseFloat(n.toFixed(10));
}

function applyOp(op, left, right) {
    let res = 0;
    if (op === '+') res = left + right;
    else if (op === '-') res = left - right;
    else if (op === '*') res = left * right;
    else if (op === '/') res = left / right;
    
    res = formatNum(res);
    console.log(`Applied operator: ${op}`);
    console.log(`Left: ${formatNum(left)} Right: ${formatNum(right)} Result: ${res}`);
    return res;
}

function evaluatePostfix(tokens) {
    let stack = [];
    for (let t of tokens) {
        console.log(`Token: ${t}`);
        if (["()", "[]", "{}"].includes(t)) continue;
        if (!isNaN(t) && t.trim() !== "") {
            stack.push(formatNum(parseFloat(t)));
        } else {
            let r = stack.pop();
            let l = stack.pop();
            stack.push(applyOp(t, l, r));
        }
    }
    return stack[0];
}

function evaluatePrefix(tokens) {
    let stack = [];
    let reversed = [...tokens].reverse();
    for (let t of reversed) {
        console.log(`Token: ${t}`);
        if (["()", "[]", "{}"].includes(t)) continue;
        if (!isNaN(t) && t.trim() !== "") {
            stack.push(formatNum(parseFloat(t)));
        } else {
            let l = stack.pop();
            let r = stack.pop();
            stack.push(applyOp(t, l, r));
        }
    }
    return stack[0];
}

function evaluateInfix(tokens) {
    let ops = [];
    let values = [];
    let prec = {'+': 1, '-': 1, '*': 2, '/': 2};
    let pairs = {')': '(', ']': '[', '}': '{'};
    
    for (let t of tokens) {
        console.log(`Token: ${t}`);
        if (!isNaN(t) && t.trim() !== "") {
            values.push(formatNum(parseFloat(t)));
        } else if ("([{".includes(t)) {
            ops.push(t);
        } else if (")]}".includes(t)) {
            while (ops.length && ops[ops.length - 1] !== pairs[t]) {
                let op = ops.pop();
                let r = values.pop();
                let l = values.pop();
                values.push(applyOp(op, l, r));
            }
            ops.pop();
        } else if ("+-*/".includes(t)) {
            while (ops.length && "+-*/".includes(ops[ops.length - 1]) && prec[ops[ops.length - 1]] >= prec[t]) {
                let op = ops.pop();
                let r = values.pop();
                let l = values.pop();
                values.push(applyOp(op, l, r));
            }
            ops.push(t);
        }
    }
    while (ops.length) {
        let op = ops.pop();
        let r = values.pop();
        let l = values.pop();
        values.push(applyOp(op, l, r));
    }
    return values[0];
}

if (exprStr) {
    console.log(`Expression: ${exprStr}`);
    let rawTokens = exprStr.match(/\d+\.\d+|\d+|\[\]|\{\}|\(\)|[+\-*/()\[\]{}]/g);
    
    let isPostfix = "+-*/".includes(rawTokens[rawTokens.length - 1]);
    let isPrefix = "+-*/".includes(rawTokens[0]);
    
    let finalRes;
    if (isPostfix) {
        finalRes = evaluatePostfix(rawTokens);
    } else if (isPrefix) {
        finalRes = evaluatePrefix(rawTokens);
    } else {
        let processed = [];
        for (let i = 0; i < rawTokens.length; i++) {
            processed.push(rawTokens[i]);
            if (i + 1 < rawTokens.length) {
                let curr = rawTokens[i];
                let nxt = rawTokens[i+1];
                if ((!isNaN(curr) || ")]}".includes(curr)) && ("([{".includes(nxt) || !isNaN(nxt))) {
                    processed.push("*");
                }
            }
        }
        finalRes = evaluateInfix(processed);
    }
    console.log(`Result: ${finalRes}`);
}