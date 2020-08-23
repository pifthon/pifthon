import sys, re
from language.structure import *
from language.lexer import Lexer
from language.pyx_parser import Parser
# from language.interpreter import Interpreter
from monitor.analyzer import Analyzer


# ############################
# # BLOCKS
# ############################

# block_stack = []


# class Block(object):
#     def __init__(self, tab_length=None, body=False):
#         self.tab_length = tab_length
#         self.body = body

#     def __call__(self, key, tab_length):
#         # blocks = {'if':'If', 'while':'While', 'def':'Def'}
#         # _class_name = blocks.get(key)
#         if key == 'if':
#             return If(tab_length)
#         elif key == 'else':
#             return Else(tab_length)
#         elif key == 'while':
#             return While(tab_length)
#         elif key == 'def':
#             return Def(tab_length)


# class If(Block):
#     def __init__(self, tab_length=None, body=False):
#         super().__init__(tab_length=tab_length, body=body)


# class Else(Block):
#     def __init__(self, tab_length=None, body=False):
#         super().__init__(tab_length=tab_length, body=body)
        

# class While(Block):
#     def __init__(self, tab_length=None, body=False):
#         super().__init__(tab_length=tab_length, body=body)

# class Def(Block):
#     def __init__(self, tab_length=None, body=False):
#         super().__init__(tab_length=tab_length, body=body)


# ############################
# # CHECK SYNTAX & INDENTATION
# ############################

# def check_syntax(line):
#     # if line is an empty string then return true
#     if line == '' or line == '\n': return True
#     result = None
 
#     # check if line is adhering the language syntax
#     for syn in syntax:
#         result = re.match(syn, line)
#         if result: break
    
#     return True if result else False




# def close_blocks():
#     ''' Close the blocks based on the tab size at the starting of the
#     string, returning a list of tags for the closing blocks'''
    
#     if isinstance(block_stack[-1], If):
#         return 'endif'
#     elif isinstance(block_stack[-1], Else):
#         return 'endif'
#     elif isinstance(block_stack[-1], While):
#         return 'ewhile'
#     elif isinstance(block_stack[-1], Def):
#         return 'endef'
#     else:
#         return None



# def create_blocks(key, tab_length):
#     ''' Check if the indentation are properly placed, if yes then
#     populate the block stack and returns the list of closing block tags'''
#     block = Block()

#     if block_stack == [] and key:
#         block_stack.append(block(key, tab_length))
#         return None

#     elif block_stack != [] and tab_length > block_stack[-1].tab_length:
#         block_stack[-1].body = True
#         if key: block_stack.append(block(key, tab_length))
#         return None

#     elif block_stack != [] and tab_length < block_stack[-1].tab_length:
#         closing_block = close_blocks() 
#         block_stack.pop()
#         return closing_block + '\n' + create_blocks(key, tab_length)

#     elif block_stack != [] and tab_length == block_stack[-1].tab_length:
#         if key == 'else':
#             # before inserting an else-block ensure the previous block is an if-block
#             assert isinstance(block_stack[-1], If), 'Invalid Syntx'
#             block_stack.pop()
#             block_stack.append(block(key, tab_length))
#             return ''

#         closing_block = close_blocks() 
#         block_stack.pop()
#         if key: block_stack.append(block(key, tab_length))
#         return closing_block

#     else:
#         print('Invalid Syntax')
#         sys.exit(0)



# def check_indentation(line):

#     # 
#     if line == '' and block_stack != []:
#         assert block_stack[-1].body, 'Expected an indented block'
        
#     # if the line is a comment then return None
#     if re.match('#[^\n]', line):
#         return None

#     # obtain the starting tab length
#     tab_length = re.match('^[\t]*', line).end() 

#     # check if the given indentation is correct after declaring a if/while/def block
#     if block_stack != [] and block_stack[-1].body == False:
#         assert tab_length == block_stack[-1].tab_length + 1, 'Invalid indentation: expected an indented block'

#     result = re.search(KEYWORDS, line)

#     # if line is a block statement i.e., if/while/else/def
#     if result:
#         block = create_blocks(result.group(0), tab_length)
#     # if line is not a block statement
#     else:
#         # if block stack is not empty
#         if block_stack != []:
#             # if line is not empty and tab_length is equal to 
#             # the tab length of last block ensure there is 
#             # at least one more block present in the stack
#             # if line != '' and tab_length == block_stack[-1].tab_length:
#             #     assert len(block_stack) > 1, 'Invalid indentation: expected an indented block'
#             # obtain the list of closing blocks
#             block = create_blocks(None, tab_length)
#         # if block stack is empty then return block as None
#         else:
#             block = None

#     return block


        





############################
# EXECUTE LEXER
############################

def execute(file_name, text, tokens, user_inputs):
    ''' execute the parser and then interpreter'''
    lexer = Lexer(file_name, text, tokens)
    error, temp_tokens = lexer.create_tokens()
    if not error:
        tokens = tokens + temp_tokens 
        tree = Parser(tokens, user_inputs).parse()
        analyzer = Analyzer(user_inputs)
        value = analyzer.analyze(tree)
    # interpreter = Interpreter(user_inputs)
    # interpreter.interpret(tree)
    # print(interpreter.GLOBAL_SCOPE, f'pc={interpreter.pc}, terminate={interpreter.terminate}')
        if value:
            tokens = None
        else:
            print(analyzer.GLOBAL_SCOPE, 'pc=', analyzer.pc)

    return tokens
    



