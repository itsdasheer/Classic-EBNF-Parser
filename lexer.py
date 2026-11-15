# Hi
# By ItsDasheer
# This is a EBNF Lexer
# You can read the code
# But you can't modify the code (well, you shouldn't, but that's up to you)

# Thanks you for read!

from re import compile
from dataclasses import dataclass
from sys import exit

def err(string, line, column, size=1):
    lines = string.splitlines()
    lineerr = lines[line-1]
    l = len(f"{line} | ")
    e = (" " * l) + (" " * (column-1)) + ("^"*size)
    return f"{line} | {lineerr}\n{e}"
    

@dataclass
class Token:
    type: str
    value: str
    line:int=1
    column:int=1
    def __repr__(self):
        return f"Token(type={self.type!r}, value={self.value!r})" # it is just a small change in the representation
    
    def pretty(self, idt=0):
        return f"{'  '*idt}{self.value}" # The ONLY reason this class has a "pretty" function is that I’ll be using the raw version of this class in the Parser, and I need to make them compatible :p

class Lexer: # Main class
    def __init__(self):
        self.toks = {
            "WS": r"\s+", # Ignore
            "COMENTARY": r"\(\*[\s\S]*?\*\)", # Ignore
            
            "SEMICOLON": r";", # ex = ...;
            "EXCEPT": r"-", # ex - except
            "LPAREN": r"\(", # Group
            "RPAREN": r"\)", # (...)
            "LBRAK": r"\[", # Optional Group
            "RBRAK": r"\]", # [...]
            "LBRACE": r"\{", # Zero or More Group
            "RBRACE": r"\}", # {...}
            "OR": r"\|", # first | second
            
            "COMMA": r",", # first, second
            "ASSIGN": r"=", # ex = ...
            "_STRL": r"'([^'\\\n]|\\.)*'", # 'Hi!'
            "_STRR": r'"([^"\\\n]|\\.)*"', # "Hi!"
            
            "RULE": r"[a-z_][a-z0-9_]*", # expr
            "TERM": r"[A-Z_][A-Z0-9_]*", # EXAMPLE
            
            # Example:
            
            # expr = term, {"+", term};
            # term = atom, {"*", atom};
            # atom = number | ( "(", expr, ")" );
            # number = [MINUS | PLUS], ([{digit}, "."], int)|(int, ".") (* /[+-]?(\d*\.)?\d+|\d+\./ *);
            # MINUS = "-";
            # PLUS = "+";
            # int = digit, {digit};
            # digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9";
            
            "MM": r"." # MisMatch
        }
        self.IGNORE = {"WS", "COMENTARY"}
        self.STRING = {"_STRL", "_STRR"}
        self.RE = compile("|".join(f"(?P<{t}>{r})" for t, r in self.toks.items()))
   
    def tokenize(self, text):
        tmp = []
        if not text:
            print("An empty text cannot be processed.")
            exit(1)
        
        line = 1
        column = 1
        for m in self.RE.finditer(text):
            type = m.lastgroup
            match = m.group()
            line = text.count("\n", 0, m.start())+1
            column = m.start() - text.rfind("\n", 0, m.start())
            
            if type in self.IGNORE:
                continue
            elif type in self.STRING:
                type = "STRING"
            elif type == "MM":
                print(err(text, line, column))
                print(f"Invalid token: {match!r} (U+{hex(ord(match))[2:].zfill(4)})")
                exit(1)
            tmp.append(Token(type, match, line, column))
        tmp.append(Token("EOF", " ", line, column))
        return tmp

if __name__ == "__main__":
    lexer = Lexer()
    # Test
    text = """
expr = term, {"+", term} ;
    @ (* Comentary *)
    """
    print(lexer.tokenize(text))