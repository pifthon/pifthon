import sys
from language.tokens import *
from language.errors import *
# from language.errors import InvalidSyntaxError
from rwfm import Label

###############################
# AST
###############################

class AST(object):
    pass

class BinaryOp(AST):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class UnaryOp(AST):
    def __init__(self, operator, expr):
        self.token = self.operator = operator
        self.expr = expr


class Number(AST):
    def __init__(self, token, label):
        self.token = token
        if self.token.type == INT:
            self.value = int(token.value)
        elif self.token.type == FLOAT:
            self.value = float(token.value)
        self.label = label

class Boolean(AST):
    def __init__(self, token, label):
        self.token = token
        self.value = True if token.value == 'True' else False
        self.label = label


class String(AST):
    def __init__(self, token, label):
        self.token = token
        self.value = token.value
        self.label = label


class Set(AST):
    def __init__(self, token, elements, label=None):
        self.token = token
        self.elements = elements
        self.label = label



class Compound(AST):
    def __init__(self):
        self.children = []

class Assign(AST):
    def __init__(self, left, operator, right):
        self.left = left
        self.token = self.operator = operator
        self.right = right

class Variable(AST):
    # class represents a variable
    def __init__(self, token, label=None):
        self.token = token
        self.value = token.value
        self.label = label

class NoOperation(AST):
    # this node represents a no operation statement
    pass


class IfElse(AST):
    def __init__(self, condition, left, right):
        self.left = left
        self.condition = condition
        self.right = right


class While(AST):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class MethodDef(AST):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body



class MethodCall(AST):
    def __init__(self, name, arguments, token):
        self.name = name
        self.arguments = arguments # a list of AST nodes
        self.token = token


class ThreadCall(AST):
    def __init__(self, method_call):
        self.method_call = method_call


class Return(AST):
    def __init__(self, token, expr):
        self.token = token
        self.expr = expr


class Downgrade(AST):
    def __init__(self, token, variable, readers):
        self.token = token
        self.variable = variable
        self.readers = readers
        self.from_label = None
        self.new_label = None



############################
# PARSER
############################

'''
============ Complete Grammer of PyX ===================

program :: compound_statement

compound_statement :: statement_list

statement_list :: statement | statement NEWLINE statement_list

statement :: assignment | compound_statement | skip | if-else | while | method_call | return expr
            | thread_call

assignment :: variable ASSIGN expr | variable ASSIGN method_call

if-else :: if condition compound_statement else compound_statement

while :: while condition compound_statement

method_call :: ID LPAREN (expr (COMMA expr)*)? RPAREN    

thread_call :: ID ASSIGN THREAD (ID, [(expr (COMMA expr)*)?])

expr :: term ((PLUS | MINUS) term )*

term :: factor ((MUL | DIV) factor)*

factor :: INT | FLOAT | LPAREN expr RPAREN | variable | downgrade

variable :: ID

'''

class Parser:

    def __init__(self, tokens, user_inputs):
        self.tokens = tokens
        # json object conatining user inputs
        self.user_inputs = user_inputs
        # set the index to 0
        self.index = 0
        self.error = False


    def _error(self):
        self.error = True
        raise Exception('exit')


    def match(self, type_= None):
        if type_:
            if self.tokens[self.index].type in type_:
                if self.index < len(self.tokens)-1: self.index += 1
            else:
                try:    
                    # raise an error for illegal character
                    raise InvalidSyntax(self.tokens[self.index],'Invalid syntax found')
                except InvalidSyntax:
                        self._error()
        else:
            if self.index < len(self.tokens)-1: self.index += 1




    def _set(self):

        token = self.tokens[self.index]

        self.match() # for CLBRACKET
        
        elements = set()

        def add_elements():
            # if self.tokens[self.index].type in (INT, FLOAT):
            #     elements.add(Number(self.tokens[self.index],Label(self.user_inputs.subject,{'*'}, {})))
                
            
            # if self.tokens[self.index].type == STRING:
            #     elements.add(String(self.tokens[self.index],Label(self.user_inputs.subject,{'*'}, {})))

            # self.match()

            if self.tokens[self.index].type in (INT, FLOAT):
                elements.add(Number(self.tokens[self.index],Label(self.user_inputs.subject,{'*'}, {})))
                self.match() # for INT or FLOAT

            elif self.tokens[self.index].type == SQUOTE:
                self.match() # for SQUOTE
                if self.tokens[self.index].type in (INT,FLOAT,ID):
                    elements.add(String(self.tokens[self.index], Label(self.user_inputs.subject,{'*'}, {})))
                    self.match()
                    self.match((SQUOTE))
            elif self.tokens[self.index].type == DQUOTE:
                self.match() # for DQUOTE
                if self.tokens[self.index].type in (INT,FLOAT,ID):
                    elements.add(String(self.tokens[self.index], Label(self.user_inputs.subject,{'*'}, {})))
                    self.match()
                    self.match((DQUOTE))
            # elif self.tokens[self.index].type == STRING:
            #     elements.add(String(self.tokens[self.index]))
            #     self.match()
            

        add_elements()

        while self.tokens[self.index].type == COMMA:
            self.match() # for COMMA
            add_elements()

        self.match() # for CRBRACKET

        return Set(token,elements,Label(self.user_inputs.subject,{'*'}, {}))


    def factor(self):
        token = self.tokens[self.index]

        if token.type == PLUS:
            self.match()
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.match()
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == NOT:
            self.match()
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == INT:
            self.match()
            return Number(token, Label(self.user_inputs.subject,{'*'}, {}))
        elif token.type == FLOAT:
            self.match()
            return Number(token, Label(self.user_inputs.subject,{'*'}, {}))
        elif token.type == BOOL:
            self.match()
            return Boolean(token, Label(self.user_inputs.subject,{'*'}, {}))
        elif token.type in (SQUOTE, DQUOTE):
            if self.tokens[self.index].type == SQUOTE:
                self.match() # for SQUOTE
                if self.tokens[self.index].type in (INT,FLOAT,ID):
                    token = self.tokens[self.index]
                    self.match() # for INT/FLOAT/ID
                    self.match() # for SQUOTE
            elif self.tokens[self.index].type == DQUOTE:
                self.match() # for DQUOTE
                if self.tokens[self.index].type in (INT,FLOAT,ID):
                    token = self.tokens[self.index]
                    self.match() # for INT/FLOAT/ID
                    self.match() # for DQUOTE
            return String(token, Label(self.user_inputs.subject,{'*'}, {}))
        elif token.type == LPAREN:
            self.match()
            node = self.expr()
            self.match()
            return node
        elif token.type == CLBRACKET:
            node = self._set()
            return node
        elif token.type == DOWNGRADE:
            node = self.downgrade()
            return node
        elif token.type == ID:
            if token.value in self.user_inputs.globals:
                label = self.user_inputs.globals[token.value]
            else:
                label = Label(self.user_inputs.subject,{'*'}, {})
            node = self.variable(label)
            self.match() # for ID
            return node


    def term(self):
        # term: factor ((MUL|DIV) factor)*
        node = self.factor()

        while self.index < len(self.tokens) and self.tokens[self.index].type in (MUL, DIV, MOD):
            token = self.tokens[self.index]
            if token.type == MUL:
                self.match()
            elif token.type == DIV:
                self.match()
            elif token.type == MOD:
                self.match()
            
            node = BinaryOp(node, token, self.factor())

        return node


    def expr(self):
        # Arithmatic expression parser/interpreter
        # expr :: term ((PLUS | MINUS) term )*
        # term :: factor ((MUL | DIV) factor)*
        # factor :: INT | FLOAT | LPAREN expr RPAREN

        node = self.term()

        while self.index < len(self.tokens) and self.tokens[self.index].type in (PLUS, MINUS, AND, OR, XOR) \
            and self.tokens[self.index].type != COLON:
            token = self.tokens[self.index]
            if token.type == PLUS:
                self.match()
            elif token.type == MINUS:
                self.match()
            elif token.type == AND:
                self.match()
            elif token.type == OR:
                self.match()
            elif token.type == XOR:
                self.match()

            node = BinaryOp(node, token, self.term())

        return node



    def condition(self):
        # condition :: expr (COMPARE | LEQ | GEQ | GTHAN | LTHAN | NEQ ) expr :
        node = self.expr()

        token = self.tokens[self.index]
        if token.type == COLON:
            return node
        elif token.type == COMPARE:
            self.match()
        elif token.type == LEQ:
            self.match()
        elif token.type == GEQ:
            self.match()
        elif token.type == GTHAN:
            self.match()
        elif token.type == LTHAN:
            self.match()
        elif token.type == NEQ:
            self.match()

        return BinaryOp(node, token, self.expr())

        

    def skip(self):
        return NoOperation()


    def variable(self, label):
        # variable :: ID
        node = Variable(self.tokens[self.index], label)
        return node


    def assignment(self):
        # assignment :: variable ASSIGN expr 
        token = self.tokens[self.index]
        if token.value in self.user_inputs.globals:
            label = self.user_inputs.globals[token.value]
        else:
            label = None
        left = self.variable(label)

        self.match() # for ID
        token = self.tokens[self.index]      
        self.match() # for ASSIGN

        right = None
        # check if the right hand side is a method call
        if self.tokens[self.index].type == ID and self.tokens[self.index+1].type == LPAREN:
            right = self.method_call()
        elif self.tokens[self.index].type == THREAD:
            right = self.thread_call()
        else:
            right = self.expr()
        node = Assign(left, token, right)
        return node



    def if_else(self):
        # if-else :: if condition compound_statement else compound_statement
        condition = self.condition()
        self.match() # for COLON
        self.match() # for NEWLINE

        if_node = else_node = None

        while self.tokens[self.index].type != ENDIF:
            if_node = self.compund_statement()
            if self.tokens[self.index].type == ELSE:
                self.match() # for ELSE
                self.match() # for COLON
                self.match() # NEWLINE
                else_node = self.compund_statement()

        self.match() # ENDIF

        return IfElse(condition, if_node , else_node)


    def loop(self):
        # while :: while condition compound_statement
        condition = self.condition()
        self.match() # for COLON
        self.match() # for NEWLINE

        body = None

        while self.tokens[self.index].type != EWHILE:
            body = self.compund_statement()

        self.match() # for EWHILE

        return While(condition, body)


    def method_def(self):
        name = self.tokens[self.index].value
        self.match() # for ID
        self.match() # for LPAREN

        parameters = []

        if self.tokens[self.index].type != RPAREN:
            node = self.expr()
            parameters.append(node)

        while self.tokens[self.index].type == COMMA:
            self.match() # for COMMA
            parameters.append(self.expr())

        self.match() # for RPAREN
        self.match() # for COLON
        self.match() # for NEWLINE

        body = None
        while self.tokens[self.index].type != ENDEF:
            body = self.compund_statement()

        self.match() # for ENDEF
        return MethodDef(name, parameters, body)


    def method_call(self):
        # method_call :: ID LPAREN (expr (COMMA expr)*)? RPAREN  
        token = self.tokens[self.index]
        method_name = token.value
        self.match() # for ID
        self.match() # for LAPREN

        arguments = []

        if self.tokens[self.index].type != RPAREN:
            node = self.expr()
            arguments.append(node)

        while self.tokens[self.index].type == COMMA:
            self.match() # for COMMA
            node = self.expr()
            arguments.append(node)
        
        self.match() # for RPAREN

        return MethodCall(method_name, arguments, token)


    def downgrade(self):
        # method_call :: ID LPAREN (expr (COMMA expr)*)? RPAREN  
        token = self.tokens[self.index]
        self.match() # for "downgrade" keyword
        self.match() # for LPAREN
        if self.tokens[self.index].value in self.user_inputs.globals:
            label = self.user_inputs.globals[self.tokens[self.index].value]
        else:
            label = Label(self.user_inputs.subject,{'*'}, {})

        variable = self.variable(label)
        self.match() # for ID

        self.match() # for COMMA

        readers = self._set()

        self.match() # check if the downgrade is closed by ')'

        return Downgrade(token, variable, readers)


    def thread_call(self):
        # thread_call :: ID ASSIGN THREAD (ID, [(expr (COMMA expr)*)?])
        self.match(THREAD)
        self.match(LPAREN)
        token = self.tokens[self.index]
        name = self.tokens[self.index]
        self.match(ID)
        self.match(COMMA)
        self.match(SLBRACKET)
        arguments = []
        if self.tokens[self.index].type != SLBRACKET:
            node = self.expr()
            arguments.append(node)

        while self.tokens[self.index].type == COMMA:
            self.match(COMMA)
            node = self.expr()
            arguments.append(node)

        self.match(SRBRACKET)
        self.match(RPAREN)
        return ThreadCall(MethodCall(name,arguments,token))



    def return_statement(self):
        token = self.tokens[self.index]
        self.match() # for RETURN
        return Return(token, self.expr())
        

        
    def statement(self):
        # statement :: assignment | compound_statement | skip | if condition statement else statement
        #              | method_call

        if self.tokens[self.index].type == ID:
            if self.tokens[self.index+1].type == LPAREN:
                return self.method_call()
            else:
                return self.assignment()          
        elif self.tokens[self.index].type == PASS:
            self.match() # for PASS
            return self.skip()
        elif self.tokens[self.index].type == RETURN:
            return self.return_statement()
        elif self.tokens[self.index].type == (INT or FLOAT or BOOL):
            return self.expr()
        elif self.tokens[self.index].type == IF:
            self.match() # for IF
            return self.if_else()
        elif self.tokens[self.index].type == WHILE:
            self.match() # for WHILE
            return self.loop()
        elif self.tokens[self.index].type == FDEF:
            self.match() # for FDEF
            return self.method_def()
        else:
            return None
        #     node = self.compund_statement()



        

    def statement_list(self):
        # statement_list :: statement | statement NEWLINE statement_list
        node = self.statement()

        results = [node]

        while self.index < len(self.tokens)-1 and self.tokens[self.index].type == NEWLINE:
            self.match() # for NEWLINE
            results.append(self.statement())

        return results




    def compund_statement(self):
        # create parse tree for a compound statement
        nodes = self.statement_list()
        root = Compound()

        for node in nodes:
            root.children.append(node)

        return root
    


    def program(self):
        # create the parse tree for a program 
        # that consists of compound statements
        node = self.compund_statement()
        return node



    def parse(self):
        return self.program()
