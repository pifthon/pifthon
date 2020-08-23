import sys 
import re
from language.tokens import *
# from language.tokens import token_expr
from language.errors import *


#######################
# POSITION
#######################

''' class Position is required for reporting errors '''
class Position(object):
    def __init__(self, file_name, statement=None, line_no=None, column_no=None):
        self.file_name = file_name
        self.statement = statement
        self.line_no = line_no
        self.column_no = column_no
    

    def __repr__(self):
        message = self.statement + '\n'
        for _ in range(self.column_no):
            message = message + ' '
        message = message + '^'
        return message


######################
# TOKEN
######################


class Token(object):
    def __init__(self, type_, value=None, position=None, length=None):
        self.type = type_
        self.value = value
        self.position = position
        self.length = length


    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}:{self.length}'
        else: return f'{self.type}:{self.length}'


############################
# BLOCKS
############################

BLOCK_STACK = []

# TAB_LENGTH shall be set whenever a TAB or SPACE is encountered after a NEWLINE 
# and reset to zero on NEWLINE, the default value is zero
TAB_LENGTH = 0 


class Block(object):

    def __init__(self, block_name, tab_length=None, present=False):
        self.block_type = block_name
        self.tab_length = tab_length
        self.body = present




############################
# SYNTAX CHECKER
############################



class Node(object):
    pass


class BinaryOp(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class UnaryOp(Node):
    def __init__(self, operator, expr):
        self.token = self.operator = operator
        self.expr = expr


class Number(Node):
    def __init__(self, token):
        self.token = token
        

class Boolean(Node):
    def __init__(self, token):
        self.token = token


class String(Node):
    def __init__(self, token):
        self.token = token


class Set(Node):
    def __init__(self, elements):
        self.elements = elements

class Compound(Node):
    def __init__(self):
        self.children = []

class Assign(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.token = self.operator = operator
        self.right = right

class Variable(Node):
    # class represents a variable
    def __init__(self, token):
        self.token = token


class NoOperation(Node):
    # this node represents a no operation statement
    pass


class IfElse(Node):
    def __init__(self, condition, left, right):
        self.left = left
        self.condition = condition
        self.right = right


# class If(Node):
#     def __init__(self, condition, body):
#         self.condition = condition
#         self.body = body


# class Else(Node):
#     def __init__(self, body):
#         self.body = body


class While(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class MethodDef(Node):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body



class MethodCall(Node):
    def __init__(self, name, arguments, token):
        self.name = name
        self.arguments = arguments # a list of AST nodes
        self.token = token


class ThreadCall(Node):
    def __init__(self, method_call):
        self.method_call = method_call


class Return(Node):
    def __init__(self, expr):
        self.expr = expr


class Downgrade(Node):
    def __init__(self, token, variable, readers):
        self.token = token
        self.variable = variable
        self.readers = readers
        


# class Indent(Node):
#     def __init__(self, token, length):
#         self.token = token
#         self.length = length
        




class SyntaxTree:

    def __init__(self, file_name, tokens):
        self.file_name = file_name
        # initialize tokens with the set of temp_tokens
        self.tokens = tokens
        # initialize the index as zero
        self.index = 0
        # initialize the error with False, if found any error set to True
        self.error = False



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


    def _error(self):
        self.error = True
        global BLOCK_STACK
        BLOCK_STACK = []
        raise Exception('exit')



    def _set(self):

        self.match((CLBRACKET))
        
        elements = set()

        def add_elements():
            if self.tokens[self.index].type in (INT, FLOAT):
                elements.add(Number(self.tokens[self.index]))
                self.match() # for INT or FLOAT

            elif self.tokens[self.index].type == SQUOTE:
                self.match() # for SQUOTE
                if self.tokens[self.index].type in (INT,FLOAT,ID):
                    elements.add(String(self.tokens[self.index]))
                    self.match() # for INT/FLOAT/ID
                    self.match((SQUOTE))
            elif self.tokens[self.index].type == DQUOTE:
                self.match() # for DQUOTE
                if self.tokens[self.index].type in (INT,FLOAT,ID):
                    elements.add(String(self.tokens[self.index]))
                    self.match() # for INT/FLOAT/ID
                    self.match((DQUOTE))
            # elif self.tokens[self.index].type == STRING:
            #     elements.add(String(self.tokens[self.index]))
            #     self.match()
            else:
                try:    
                    # raise an error for illegal character
                    raise InvalidCharacter(self.tokens[self.index],'Unknown element found')
                except InvalidCharacter:
                    self._error()

        add_elements()

        while self.tokens[self.index].type == COMMA:
            self.match() # for COMMA
            add_elements()

        self.match((CRBRACKET))

        return Set(elements)

        
        

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
            return Number(token)
        elif token.type == FLOAT:
            self.match()
            return Number(token)
        elif token.type == BOOL:
            self.match()
            return Boolean(token)
        elif token.type in (SQUOTE, DQUOTE):
            if self.tokens[self.index].type == SQUOTE:
                self.match() # for SQUOTE
                if self.tokens[self.index].type in (INT,FLOAT,ID):
                    token = self.tokens[self.index]
                    self.match() # for INT/FLOAT/ID
                    self.match((SQUOTE))
            elif self.tokens[self.index].type == DQUOTE:
                self.match() # for DQUOTE
                if self.tokens[self.index].type in (INT,FLOAT,ID):
                    token = self.tokens[self.index]
                    self.match() # for INT/FLOAT/ID
                    self.match((DQUOTE))
            return String(token)
        elif token.type == LPAREN:
            node = self.expr()
            return node
        elif token.type == CLBRACKET:
            node = self._set()
            return node
        elif token.type == DOWNGRADE:
            self.match()
            node = self.downgrade()
            return node
        elif token.type == ID:
            node = self.variable()
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
        rparen_required = False

        if self.tokens[self.index].type == LPAREN:
            self.match()
            rparen_required = True

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

        if rparen_required:
            self.match(RPAREN)

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
        self.match() # for PASS
        return NoOperation()


    def variable(self):
        # variable :: ID
        node = Variable(self.tokens[self.index])
        self.match((ID))
        return node


    def assignment(self):
        # assignment :: variable ASSIGN expr 
        token = self.tokens[self.index]

        left = self.variable()
        token = self.tokens[self.index]
        self.match((ASSIGN))
        right = None
        # check if the right hand side is a method call
        if self.tokens[self.index].type == ID and self.tokens[self.index+1].type == LPAREN:
            right = self.method_call()
        # elif self.tokens[self.index].type == THREAD:
        #     right = self.thread_call()
        else:
            right = self.expr()
        node = Assign(left, token, right)
        return node




    def _else(self):
        # Add an else block into the BLOCK STACK
        BLOCK_STACK.append(Block(self.tokens[self.index].type, TAB_LENGTH))
        return None

        # body = self.compund_statement()

        


    def if_else(self):
        # if-else :: if condition compound_statement else compound_statement
        BLOCK_STACK.append(Block(self.tokens[self.index].type, TAB_LENGTH))
        self.match((IF))
        condition = self.condition()
        self.match((COLON))
        self.match((NEWLINE))

        if_node = else_node = None

        while self.tokens[self.index].type != ENDIF:
            if_node = self.compund_statement()
            if self.tokens[self.index].type == ELSE:
                self.match((ELSE))
                self.match((COLON))
                self.match((NEWLINE))
                else_node = self.compund_statement()

        self.match((ENDIF))

        return IfElse(condition, if_node , else_node)

    




    def loop(self):
        # while :: while condition compound_statement

        # Add a WHILE block into the BLOCK STACK
        BLOCK_STACK.append(Block(self.tokens[self.index].type, TAB_LENGTH))

        self.match() # for WHILE
        condition = self.condition()
        self.match((COLON)) # for COLON
        self.match((NEWLINE)) # for NEWLINE

        body = None

        while self.tokens[self.index].type != EWHILE:
            body = self.compund_statement()

        self.match((EWHILE)) # for EWHILE

        return While(condition, body)


    def method_def(self):
        # Function definition cannot be nested
        if not len(BLOCK_STACK) == 0:
            # raise error
            try:    
                # raise an error for illegal character
                raise InvalidSyntax(self.tokens[self.index],'Nested function definition is not permitted')
            except InvalidSyntax:
                self._error()

        # Add a FDEF block into the BLOCK STACK
        BLOCK_STACK.append(Block(self.tokens[self.index].type, TAB_LENGTH))

        self.match((FDEF)) # for FDEF
        name = self.tokens[self.index].value
        self.match((ID)) # for ID
        self.match((LPAREN)) # for LPAREN

        parameters = []

        if self.tokens[self.index].type != RPAREN:
            node = self.expr()
            parameters.append(node)

        while self.tokens[self.index].type == COMMA:
            self.match() # for COMMA
            parameters.append(self.expr())

        self.match((RPAREN)) # for RPAREN
        self.match((COLON)) # for COLON
        self.match((NEWLINE)) # for NEWLINE

        body = None
        while self.tokens[self.index].type != ENDEF:
            body = self.compund_statement()

        self.match((ENDEF)) # for ENDEF
        return MethodDef(name, parameters, body)


    def method_call(self):
        # method_call :: ID LPAREN (expr (COMMA expr)*)? RPAREN  
        token = self.tokens[self.index]
        method_name = token.value
        self.match((ID)) # for ID
        self.match((LPAREN)) # for LPAREN

        arguments = []

        if self.tokens[self.index].type != RPAREN:
            node = self.expr()
            arguments.append(node)

        while self.tokens[self.index].type == COMMA:
            self.match() # for COMMA
            node = self.expr()
            arguments.append(node)
        
        self.match((RPAREN)) # for RPAREN

        return MethodCall(method_name, arguments, token)



    def downgrade(self):
        # method_call :: ID LPAREN (expr (COMMA expr)*)? RPAREN  
        token = self.tokens[self.index]
        self.match((LPAREN)) # for LPAREN
        variable = Variable(self.tokens[self.index])
        self.match((ID)) # check for ID

        self.match((COMMA)) # check if the second parameter is seperated by COMMA

        readers = self._set()

        self.match((RPAREN)) # check if the downgrade is closed by ')'

        return Downgrade(token, variable, readers)


    def thread_call(self):
        # thread_call :: ID ASSIGN THREAD (ID, [(expr (COMMA expr)*)?])
        # self.match(THREAD)
        # self.match(LPAREN)
        # token = self.tokens[self.index]
        # name = self.tokens[self.index]
        # self.match(ID)
        # self.match(COMMA)
        # self.match(SLBRACKET)
        # arguments = []
        # if self.tokens[self.index].type != SLBRACKET:
        #     node = self.expr()
        #     arguments.append(node)

        # while self.tokens[self.index].type == COMMA:
        #     self.match(COMMA)
        #     node = self.expr()
        #     arguments.append(node)

        # self.match(SRBRACKET)
        # self.match(RPAREN)
        # return ThreadCall(MethodCall(name,arguments,token))
        pass



    def return_statement(self):
        self.match() # for RETURN
        return Return(self.expr())
        


    def indentation(self):
        
        # length = self.tokens[self.index].length
        global TAB_LENGTH
        # if current token is a TAB then set the tab length to the global TAB_LENGTH variable 
        # otherwise store the default value zero
        if self.tokens[self.index].type == TAB:
            # store the length of the initial TAB token
            TAB_LENGTH = self.tokens[self.index].length
        else:
            TAB_LENGTH = 0

        if self.check_indentation(): 
            # store the index before adding the closing tokens
            temp_index = self.index

            # perform the inclusion of closing tokens based on the indentation
            self.manage_indentation()

            # resote the index position
            self.index = temp_index


        else:
            # raise error
            try:    
                # raise an error for illegal character
                raise InvalidIndentation(self.tokens[self.index],'Indentation is not proper')
            except InvalidIndentation:
                self._error()
    

        # if the index is poiting to TAB or SPACE remove the token
        if self.tokens[self.index].type == TAB:
            self.tokens.pop(self.index)

        # in case the last TAB token is poped then reset the index to the last token
        if self.index >= len(self.tokens):
            self.index = len(self.tokens)-1
        



        
    def statement(self):
        # statement :: assignment | compound_statement | skip | if condition statement else statement
        #              | method_call

        # if the current token is a NEWLINE or ENDEF or ENDIF or EWHILE return None
        if self.tokens[self.index].type in (ENDIF, ENDEF, EWHILE, NEWLINE):
            return None
        # if the current token is a TAB and not followed by an empty statement
        elif self.tokens[self.index].type != TAB or self.tokens[self.index+1].type != NEWLINE:
            self.indentation()

        # otherwise advance the index by removing the token from the list
        else:
            self.tokens.pop(self.index)



        if self.tokens[self.index].type == ID:
            if self.tokens[self.index+1].type == LPAREN:
                return self.method_call()
            else:
                return self.assignment()          
        elif self.tokens[self.index].type == PASS:
            return self.skip()
        elif self.tokens[self.index].type == RETURN:
            return self.return_statement()
        elif self.tokens[self.index].type == (INT or FLOAT or BOOL):
            return self.expr()
        elif self.tokens[self.index].type in IF:
            return self.if_else()
        elif self.tokens[self.index].type in ELSE:
            return self._else()
        elif self.tokens[self.index].type == WHILE:
            return self.loop()
        elif self.tokens[self.index].type == FDEF:
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

        
        # check the indentation a final time at the end of the program
        if self.index == len(self.tokens)-1:
            self.indentation()

        return root
    


    def program(self):
        # create the parse tree for a program 
        # that consists of compound statements
        node = self.compund_statement()
        return node


    def check(self):
        self.program()
        return self.tokens



    def check_indentation(self):
        ''' Check if given indentation is correct and return True or False accordingly'''
        # if Block  stack is empty then return True
        if len(BLOCK_STACK) == 0:
            return True
        # otherwise check indentation when the body is present and not
        else:
            if TAB_LENGTH <= BLOCK_STACK[-1].tab_length:
                # check if body of the last block is present or not
                return True if BLOCK_STACK[-1].body == True else False
            else:
                # set the body of the last block True
                BLOCK_STACK[-1].body = True
                return True




    def manage_indentation(self):
        ''' Close blocks in block stack according to indentation, 
        handle special blocks such as else carefully, 
        return new list of tokens added with closing tokens'''
        
        #if block stack is empty then return list of tokens and index
        if len(BLOCK_STACK) == 0:
            # when block stack is empty then next token cannot be an else block 
            if self.index < len(self.tokens)-1 and self.tokens[self.index+1].type == ELSE:
                # raise error
                try:    
                    # raise an error for illegal character
                    raise InvalidSyntax(self.tokens[self.index],'There is no IF block')
                except InvalidSyntax:
                    self._error()

        # if block stack is not empty and tab_length is more than tab_length 
        # of previous block then return list of tokens and index
        elif len(BLOCK_STACK) > 0 and TAB_LENGTH > BLOCK_STACK[-1].tab_length:
            try:
                # the next token cannot be an ELSE, 
                # because there should be an IF with equal tab length
                if self.tokens[self.index+1].type == ELSE:
                    # raise error
                    # raise an error for illegal character
                    raise InvalidIndentation(self.tokens[self.index],'No IF block found with equal indentation')

            except InvalidIndentation:
                    self._error()

        # if tab length is less than previous block's tab length
        elif len(BLOCK_STACK) > 0 and TAB_LENGTH < BLOCK_STACK[-1].tab_length:
            # closing_block = close_block()
            closing_type, value = self.close_block()

            self.add_closing_tokens(closing_type, value)

            # call the function recursively to compute the next closing 
            # block until the block stack become empty of tab length 
            # becomes more than the previous block's tab length
            self.manage_indentation()

        # if tab length is equal to previous block's tab length
        elif len(BLOCK_STACK) > 0 and TAB_LENGTH == BLOCK_STACK[-1].tab_length:

            # if the current token (in case there is no tab in front of ELSE) or the next token is else
            if self.index < len(self.tokens)-1 and (self.tokens[self.index].type == ELSE or self.tokens[self.index+1].type == ELSE):
                # check if previous block is if and has equal tab length
                if not (BLOCK_STACK[-1].block_type == IF):
                    # raise error
                    try:    
                        # raise an error for illegal character
                        raise InvalidIndentation(self.tokens[self.index],'No IF block found with equal indentation')
                    except InvalidIndentation:
                        self._error()


                # pop the last IF block from the BLOCK STACK 
                # but do not add the closing token ENDIF
                self.close_block()

            else:

                # closing_block = close_block()
                closing_type, value = self.close_block()

                self.add_closing_tokens(closing_type, value)

                # call the function recursively to compute the next closing 
                # block until the block stack become empty of tab length 
                # becomes more than the previous block's tab length
                self.manage_indentation()
        
        
            

    def add_closing_tokens(self, type_, value):
        # create position similar to the current token
        # initialize the position object using line no and col no.
        position = Position(self.file_name, self.tokens[self.index].position.statement, self.tokens[self.index].position.line_no, self.tokens[self.index].position.column_no)
            
        # create a token object with closing block
        closing_token = Token(type_, value, position, len(value))

        # create another token object with NEWLINE type
        newline_token = Token(NEWLINE,'NEWLINE', position, 1)

        # add the token into the list of tokens at the current index
        self.tokens.insert(self.index, closing_token)

        # proceed to next token to adjust the index due to insertion
        self.index += 1

        # add the token into the list of tokens at the current index
        self.tokens.insert(self.index, newline_token)

        # proceed to next token to adjust the index due to insertion
        self.index += 1





    def close_block(self):
        ''' Close the blocks based on the tab size at the starting of the
        string, returning a list of tags for the closing blocks'''

        closing_block = ''

        if BLOCK_STACK[-1].block_type == 'IF':
            closing_block = ENDIF
            value = 'ENDIF'
        elif BLOCK_STACK[-1].block_type == 'ELSE':
            closing_block = ENDIF
            value = 'ENDIF'
        elif BLOCK_STACK[-1].block_type == 'WHILE':
            closing_block = EWHILE
            value = 'EWHILE'
        elif BLOCK_STACK[-1].block_type == 'DEF':
            closing_block = ENDEF
            value = 'ENDEF'

        BLOCK_STACK.pop()

        return closing_block, value

    





##############################
# LEXER
##############################

''' The Lexer class is responsible for tokenizing the input
statements from the console or a source file'''

class Lexer:

    def __init__(self, file_name, program, tokens):
        self.file_name = file_name
        self.lines = program.split('\n')
        self.tokens = tokens

        
    
    def create_tokens(self):
        # create an empty list of tokens named temp_tokens
        temp_tokens = []

        # if self.tokens is empty initialize with line no 1
        if self.tokens == []:
            line_no = 0
        else:
            # initialize line no with line no. of the last added token position + 1
            line_no = self.tokens[-1].position.line_no

        # for each line in self.lines
        for line in self.lines:

            # first increase line no by 1 
            line_no += 1

            # initialize the column to 0
            column = 0

            # while column is less than the length of the line
            while column < len(line):

                # initialize the result as None
                result = None

                # initialize the position object using line no and col no.
                position = Position(self.file_name, line, line_no, column)

                # for each expr in token_expr
                for expr in token_expr:

                    # intialize pattern and type from the expr
                    pattern, type_ = expr

                    # update the result on finding a matched pattern
                    result = re.match(pattern, line[column:])

                    # if result is not None
                    if result:

                        # calculate length of the matched pattern and initialize into length
                        length = result.end()

                        # # initialize the position object using line no and col no.
                        # position = Position(self.file_name, line, line_no, column)

                        # initialize a token object
                        token = Token(type_,result.group(0), position, length)

                        # insert the token into temp_tokens list
                        temp_tokens.append(token)

                        # advance the column number by the length
                        column += length

                        # break the loop
                        break

                # if the result is None means no matching pattern is found
                if result == None:
                    try:
                        # create a token filled with None type 
                        token = Token(None,None,position,None)
                        # raise an error for illegal character
                        raise InvalidCharacter(token,'Invalid character found')
                    except InvalidCharacter:
                        return None
            
            # initialize the position object using line no and col no.
            position = Position(self.file_name, line, line_no, column)

            # initialize a token object
            token = Token(NEWLINE,'NEWLINE', position, 1)

            # insert the token into temp_tokens list
            temp_tokens.append(token)

            # advance the column number by the length
            column += 1

        # remove the unnecessary tokens from the list temp_tokens
        temp_tokens = self.optimize_tokens(temp_tokens)

        syntax = SyntaxTree(self.file_name, temp_tokens)

        temp_tokens = syntax.check()

        # If there is any error then return None
        if syntax.error:
            return True, None
        else:
            # return the list of tokens
            return False, temp_tokens




    def optimize_tokens(self, tokens):
        ''' This module optimizes the list of tokens by removing irrelevent tokens such as SPACE, TAB, COMMENT, EOF and return the reduced list of tokens'''
        index = 0

        # keep the TAB given at initial position index zero
        if tokens[index].type == TAB:
            index = index + 1

        while index < len(tokens):
            
            if index < len(tokens) and tokens[index].type == NEWLINE:
                index = index + 1
                # if there is a TAB after a NEWLINE then keep the token
                if index < len(tokens) and tokens[index].type == TAB:
                    index = index + 1
                    
                continue

            if index < len(tokens) and tokens[index].type in (SPACE, TAB, COMMENT, EOF):
                tokens.pop(index)
                continue

            index = index + 1

        return tokens


    
