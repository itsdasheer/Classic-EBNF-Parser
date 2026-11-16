import lexer
import tree
from sys import exit

class Parser: # Main class
    def __init__(self):
        self.lexer = lexer.Lexer()
        self.toks = []
        self.pos = 0
        self.prev = ''
    
    def _prepare(self, text):
        self.prev = text
        self.toks = self.lexer.tokenize(text)
        self.pos = 0
    
    def current(self):
        return self.toks[self.pos]
    
    def consume(self, *exp):
       c = self.current()
       self.pos += 1
       if exp == ():
           return c
       
       if c.type in exp:
           return c
       
       print(lexer.err(self.prev, c.line, c.column, len(c.value)))
       print(f"UnexpectedToken: One of: \n\n* {'\n* '.join(exp)}\n\nwas expected, but found {c.type!r}")
       exit(1)
   
   
    # Or, Except
    def _process_bin(self):
        left = self._process_tree(d=True)
        while self.current().value in "|-":
            op = self.consume()
            right = self._process_tree(d=True)
            left = tree.BinaryOp(left, op, right)
        return left
    
    # Group
    def _group(self, mode):
        if mode == tree.Default():
            self.consume("LPAREN")
            v = self._process_bin()
            self.consume("RPAREN")
            return tree.BinaryOp(mode, "group", v)
        if mode == tree.Optional():
            self.consume("LBRAK")
            v = self._process_bin()
            self.consume("RBRAK")
            return tree.BinaryOp(mode, "group", v)
        if mode == tree.Star():
            self.consume("LBRACE")
            v = self._process_bin()
            self.consume("RBRACE")
            return tree.BinaryOp(mode, "group", v)
    
    
    # Tree
    def _process_node(self, d=False):
        if self.current().type == "EOF":
            c = self.current()
            print(lexer.err(self.prev, c.line, c.column))
            print("UnexpectedEOF")
            exit(1)
            
        if not d:
            c = self.consume("RULE", "TERM")
            if c.type == "RULE":
                op = "new_rule"
                left = tree.Rule(c.value)
                self.consume("ASSIGN")
                right = self._process_bin()
                self.consume("SEMICOLON")
                return tree.BinaryOp(left, op, right)
            elif c.type == "TERM":
                op = "new_terminal"
                left = tree.Terminal(c.value)
                self.consume("ASSIGN")
                right = self._process_bin()
                self.consume("SEMICOLON")
                return tree.BinaryOp(left, op, right)
        
        c = self.consume()
        if c.type == "RULE":
            return tree.Rule(c.value)
        
        if c.type == "TERM":
            return tree.Terminal(c.value)
        
        if c.type == "STRING":
            return tree.String(c.value[1:-1])
        
        # Group
        if c.type == "LPAREN":
            self.pos -= 1
            return self._group(tree.Default())
        
        elif c.type == "LBRAK":
            self.pos -= 1
            return self._group(tree.Optional())
        
        elif c.type == "LBRACE":
            self.pos -= 1
            return self._group(tree.Star())
        
            
        print(lexer.err(self.prev, c.line, c.column, len(c.value)))
        
        if c.value in "}])":
            print("SyntaxError: You should not close a group that has no content")
            exit(1)
        print(f"SyntaxError: {c.value!r}")
        exit(1)
            
    def _process_tree(self, d=False):
        t = [self._process_node(d)]
        while self.current().value == ",":
            self.consume("COMMA")
            t.append(self._process_node(d))
        return tree.Tree(t)
     
    def parse(self, text):
        self._prepare(text)
        t = []
        while self.current().type != "EOF":
            t.append(self._process_tree().children[0])
        self.consume("EOF")
        return tree.Tree(t)


def main():
    import time
    
    text = """
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
    parser = Parser()
    
    s = time.time()
    parser.parse(text)
    e = time.time()
    print((e - s) * 1000)
    
if __name__ == "__main__":
    main()