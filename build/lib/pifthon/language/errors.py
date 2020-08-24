import sys

###############################
# TOKEN POSITION
###############################

''' The Position class enables to uniquely identify the
position of a token using the attributes file name, statement,
row, column and index. 

row: line number in a file or terminal input
column: column number of a character

Initially row, column all are set to 0
'''
# class Position:
#     def __init__(self, file_name, statement, row, column):
#         self.file_name = file_name
#         self.statement = statement
#         self.row = row
#         self.column = column

#     def get_position(self):
#         return Position(self.file_name, self.statement, self.row, self.column)

#     def __repr__(self):
#         return f'File {self.file_name}, line {self.row} column {self.column}'

        


##############################
# ERRORS
##############################

# list of errors
# ICHAR   =   'IllegalCharacter'
# ISYN    =   'InvalidSyntax'
# UVAR    =   'UndefinedVariable'
# IDEN    =   'InvalidIndentation'

# ''' The class Error defines the a number of errors and 
# messages that might occur and eventually be displayed
# to the programmer in the case of practice that do not 
# follow the PyX syntax'''

# class Error:
#     def __init__(self, position, error_name, error_message):
#         self.error_name = error_name
#         self.error_message = error_message
#         self.position = position
#         print(self)
#         sys.exit(1)

#     def __repr__(self):
#         return f'{self.position}\n{self.position.statement}\n{self.error_name}: {self.error_message}'


# class IllegalCharError(Error):
#     def __init__(self, position, error_message):
#         super().__init__(position, ICHAR, error_message)

# class InvalidSyntaxError(Error):
#     def __init__(self, position, error_message):
#         super().__init__(position, ISYN, error_message)

# class VariableNameError(Error):
#     def __init__(self, position, error_message):
#         super().__init__(position, UVAR, error_message)

# class InvalidIndentationError(Error):
#     def __init__(self, position, error_message):
#         super().__init__(position, IDEN, error_message)


# from enum import Enum

# class ErrorCode(Enum):
#     INVALID_TOKEN   = 'Invalid token'
#     UNDEFINED_ID    = 'ID not defined' 
#     DUPLICATE_ID    = 'Duplicate ID found' 

class Error(Exception):
    def __init__(self, token=None, message=None):
        # self.error_code = error_code
        self. token = token
        self.message = f'{self.__class__.__name__}:  {message}'
        print(self.token.position)
        print(self.message)
    # def __init__(self, message):
    #     self.message = f'{self.__class__.__name__}:{message}'
    #     print(self.message)

class InvalidSyntax(Error):
    def __init__(self, token=None, message=None):
        super().__init__(token=token, message=message)
        
class InvalidCharacter(Error):
    def __init__(self, token=None, message=None):
        super().__init__(token=token, message=message)


class UndefinedID(Error):
    def __init__(self, token=None, message=None):
        super().__init__(token=token, message=message)


class DuplicateID(Error):
    def __init__(self, token=None, message=None):
        super().__init__(token=token, message=message)


class InvalidIndentation(Error):
    def __init__(self, token=None, message=None):
        super().__init__(token=token, message=message)


class InvalidFlow(Error):
    def __init__(self, token=None, message=None):
        super().__init__(token=token, message=message)


class InvalidOperation(Error):
    def __init__(self, token=None, message=None):
        super().__init__(token=token, message=message)

class InvalidStatement(Error):
    def __init__(self, token=None, message=None):
        super().__init__(token=token, message=message)





