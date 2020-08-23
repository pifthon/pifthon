

##############################
# TOKENS
##############################


COMMENT     =   'COMMENT'   # a comment
PASS        =   'PASS'      # pass statement
IMPORT      =   'IMPORT'    # import another file
THREAD      =   'THREAD'    # a thread class
INT         =   'INT'       # integer
FLOAT       =   'FLOAT'     # float
BOOL        =   'BOOL'      # boolean variable
STRING      =   'STRING'    # string or character
ID          =   'ID'        # variable identifier
FDEF        =   'DEF'       # function definition
ENDEF       =   'ENDEF'     # end of function definition
FCALL       =   'FCALL'     # function call
IF          =   'IF'        # if statement
ELSE        =   'ELSE'      # else
ENDIF       =   'ENDIF'     # end of if-block
WHILE       =   'WHILE'     # while statement
EWHILE      =   'EWHILE'    # end of while-block
ASSIGN      =   'ASSIGN'    # assignment
TUPLE       =   'TUPLE'     # denotes a tuple
ETUPLE      =   'ETUPLE'    # denotes end of tuples
ARGS        =   'ARGS'      # function arguments/parameters
EARGS       =   'EARGS'     # denotes end of function arguments/parameters
RETURN      =   'RETURN'    # denote return keyword
DOWNGRADE   =   'DOWNGRADE' # denote the expression downgrade

# List of delimiters
# SPACE       =   ' '         # ' '
# NEWLINE     =   '\n'        # \n
# TAB         =   '\t'        # \t
# COLON       =   ':'         # :
# COMMA       =   ','         # ,
# SRBRACKET   =   ']'         # ]
# SLBRACKET   =   '['         # [
# DOT         =   '.'         # .
SPACE       =   'SPACE'       # ' '
NEWLINE     =   'NEWLINE'     # \n
TAB         =   'TAB'         # \t
COLON       =   'COLON'       # :
COMMA       =   'COMMA'       # ,
SRBRACKET   =   'SRBRACKET'   # ]
SLBRACKET   =   'SLBRACKET'   # [
CLBRACKET   =   'CLBRACKET'   # {
CRBRACKET   =   'CRBRACKET'   # }
DOT         =   'DOT'         # .
EOF         =   'EOF'


# List of operators

# PLUS        =   '+'     # + operator
# MINUS       =   '-'     # - operator
# MUL         =   '*'     # * operator
# DIV         =   '/'     # / operator
# MOD         =   '%'     # % operator    
# LPAREN      =   '('     # ( bracket
# RPAREN      =   ')'     # ) bracket
# EQUAL       =   '='     # = operator
# COMPARE     =   '=='    # == operator
# LEQ         =   '<='    # <= operator
# GEQ         =   '>='    # >= operator
# GTHAN       =   '>'     # > operator
# LTHAN       =   '<'     # < operator
# NEQ         =   '!='    # != operator
# AND         =   'and'   # && operator
# OR          =   'or'    # || operator
# NOT         =   'not'   # ! operator
# XOR         =   'xor'   # ^ operator
PLUS        =   'PLUS'    # + operator
MINUS       =   'MINUS'   # - operator
MUL         =   'MUL'     # * operator
DIV         =   'DIV'     # / operator
MOD         =   'MOD'     # % operator    
LPAREN      =   'LPAREN'     # ( bracket
RPAREN      =   'RPAREN'     # ) bracket
COMPARE     =   'COMPARE'    # == operator
LEQ         =   'LEQ'    # <= operator
GEQ         =   'GEQ'    # >= operator
GTHAN       =   'GTHAN'     # > operator
LTHAN       =   'LTHAN'     # < operator
NEQ         =   'NEQ'    # != operator
AND         =   'AND'   # && operator
OR          =   'OR'    # || operator
NOT         =   'NOT'   # ! operator
XOR         =   'XOR'   # ^ operator
SQUOTE      =   'SQUOTE'    # ' single quote
DQUOTE      =   'DQUOTE'    # ' double quote



# the structure shall verify the syntax of a statement 
# either the statement is an assignment, if-else, while or a function defnition
structure = [
    r'([ \t]*)(def)\s?(\w+)\s?\(((\w+(,\s?)?)+)\)\s?\:',
    r'([ \t]*)(\w+)\s?\(((\w+(,\s?)?)+)\)',
    r'([ \t]*)(.+)\s*\=(.+)',
]


token_expr = [
    (r' +',         SPACE),
    (r'\t+',        TAB),
    (r'#[^\n]+',    COMMENT),
    (r'\n',         NEWLINE),
    (r'True',       BOOL),
    (r'False',      BOOL),
    (r'import\s?(\w+)', IMPORT),
    (r'Thread',     THREAD),
    (r'==',         COMPARE),
    (r'pass',       PASS),
    (r'return',     RETURN),
    (r'\=',         ASSIGN),
    (r'\(',         LPAREN),
    (r'\)',         RPAREN),
    (r'\+',         PLUS),
    (r'\-',         MINUS),
    (r'\*',         MUL),
    (r'\^',         XOR),
    (r'/',          DIV),
    (r'%',          MOD),
    (r'<=',         LEQ),
    (r'>=',         GEQ),
    (r'<',          LTHAN),
    (r'>',          GTHAN),
    (r'!=',         NEQ),
    (r'&',          AND),
    (r'and',        AND),
    (r'\|',         OR),
    (r'or',         OR),
    (r'!',          NOT),
    (r'not',        NOT),
    (r'if',         IF),
    (r'else',       ELSE),
    (r'endif',      ENDIF),
    (r'while',      WHILE),
    (r'ewhile',     EWHILE),
    (r'def',        FDEF),
    (r'endef',      ENDEF),
    (r':',          COLON),
    (r',',          COMMA),
    (r'\.',         DOT),
    (r'\'',         SQUOTE),
    (r'\"',         DQUOTE),
    (r'\[',         SLBRACKET),
    (r'\]',         SRBRACKET),
    (r'\{',         CLBRACKET),
    (r'\}',         CRBRACKET),

    # Regex for float, integer or variable
    # (r'(\'[A-Za-z0-9]+\'|\"[A-Za-z0-9]+\")', STRING),
    (r'[0-9]+[.][0-9]+',         FLOAT),
    (r'[0-9]+',                  INT),
    (r'downgrade',               DOWNGRADE),
    (r'[A-Za-z_][A-Za-z0-9_]*',  ID)

]

