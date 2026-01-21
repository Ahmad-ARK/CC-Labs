#LL(1) Parser for Decaf Subset

#Author: Ahmad Khalid (2022-CS-31)

#Project: Compiler Construction Lab (CS-471L)

##Overview

This project implements a table-driven LL(1) parser for a subset of the Decaf programming language. It includes a Lexical Analyzer (Scanner), a Symbol Table manager, and a Stack-based Parser.

The parser handles:

    - Variable Declarations: int, double, bool.

    - Assignments: Identifier-based assignment operations.

    - Arithmetic Expressions: Addition (+) and subtraction (-).

##Project Structure

parser.py: The main Python implementation containing the Scanner, Symbol Table, and Parser classes.

lab_report.pdf: Detailed documentation of the grammar transformation and FIRST/FOLLOW sets.

parsing_table.xlsx: The LL(1) parsing table used for the implementation.

##How It Works

    1. Scanner: Converts source code into a stream of tokens and ignores whitespace.

    2. Symbol Table: Stores identifier information (type, scope, line number).

    3. LL(1) Parser: Uses a stack and a pre-computed parsing table to validate the syntax of the token stream. It outputs a step-by-step trace of the parsing process.

##How to Run

Ensure you have Python 3.x installed. Run the parser using the following command:

python parser.py


##Grammar Transformation

    - The original Decaf grammar was transformed to remove Left Recursion and apply Left Factoring.

    - Left-recursive Expr was converted to a right-recursive structure using Expr'.

    - The Program structure was converted to a recursive Decl Program' form.

##Test Cases

    - The script includes built-in test cases:

    - Valid: Variable declarations and assignments.

    - Invalid: Missing semicolons, invalid operators, or malformed syntax.