# Classic-EBNF-Parser

Hello, this parser I created is for EBNF syntax (a grammar language). First of all, you need to install **Python**:

```bash
# This depends on your operating system (OS)
sudo apt update && sudo apt upgrade
apt install python```

Once that’s done, you’ll need to create a .py file (e.g., main.py) and run it using `python <your_file>`

In the file, you need to import the Parser class in order to use my parser for classic EBNF.

## Example
```python
parser = Parser()

ebnf = """
expr = term, {EXPR, term};
EXPR = "+" | "-";

term = unary, {TERM, term};
TERM = "*" | "/" | "%";

unary = [EXPR], power;
power = atom, {"**", unary};

atom = number | "(", expr, ")";
number = [{digit}, "."], int | int, ".";

int = digit, {digit};
digit = "0" | "1" | "2" | "3" | "4" | "5" |  "6" | "7" | "8" | "9";
"""
ast = parser.parse(ebnf)
print(ast)
print(f"\n{ast.pretty()}")```