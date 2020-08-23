import sys
from language.tokens import *
from rwfm import Label, downgrade
from language.pyx_parser import *

############################
# INTERPRETER
############################

# a list to store the function call stack
# the list shall contain tuples (func_name, value, label)
CALL_STACK = []
# a dictionary to store the funcation name as key and 
# respective AST node and function label as value
# FUNCTIONS[name] = (parameters, body)
FUNCTIONS = dict()
# a dictionary to store the threads as a mapping of an id to thread object
# THREADS[id] = object
THREADS = dict()

class NodeVisitor:
    def visit(self, node):
        # dynamically create the name of the function
        _func_name = 'visit_' + type(node).__name__

        # match the function name and execute the method 
        # otherwise execute generic_visit()
        visitor = getattr(self, _func_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

class Analyzer(NodeVisitor):
    def __init__(self, user_inputs):
        # a dictionary to store the local variables along with their labels
        self.GLOBAL_SCOPE = dict()
        # store the defined list of variables of a block inside the stack
        # this helps to track the scope of the variables defined inside a block
        # self.VARIABLE_STACK = []
        self.user_inputs = user_inputs
        self.clearance = user_inputs.subject_label
        self.pc = Label(self.clearance.owner,{'*'},{})
        self.terminate = True
        self.mainthread = True
        self.error = False

    
    def _error(self):
        self.error = True
        global CALL_STACK
        CALL_STACK = []
        global FUNCTIONS
        FUNCTIONS = dict()
        global THREADS
        THREADS = dict()
        raise Exception('exit')


    def visit_BinaryOp(self, node):

        try:    

            # if isinstance(node.right, Number) or isinstance(node.right, Variable):
            #     if node.right.label <= self.clearance:
            #         self.pc = self.pc + node.right.label
            #     else:
            #         # raise an error for invalid flow
            #         raise InvalidFlow(node.right.token,f'{node.right.token.value} {node.right.label} cannot flow to subject clearance {self.clearance}')
        
            #     if isinstance(node.left, Number) or isinstance(node.left, Variable):
            #         if node.left.label <= self.clearance:
            #             self.pc = self.pc + node.left.label
            #     else:
            #         # raise an error for invalid flow
            #         raise InvalidFlow(node.left.token,f'{node.left.token.value}({node.left.label}) cannot flow to subject clearance {self.clearance}')


            if node.operator.type in (PLUS, MINUS, MUL, DIV, AND, OR, XOR, COMPARE, LEQ, GEQ, LTHAN, GTHAN, NEQ):
                # return self.visit(node.left) + self.visit(node.right)
                self.visit(node.left)
                self.visit(node.right)
            else:
                # raise an error for invalid operation
                raise InvalidOperation(node.operator,f'\'{node.operator.value}\' is an invalid operation')

        except (InvalidFlow, InvalidOperation):
            self._error()



    def visit_UnaryOp(self, node):
        operator = node.operator.type
        try:
            if operator in (PLUS,MINUS,NOT):
                self.visit(node.expr)
            else:
                # raise an error for invalid operation
                raise InvalidOperation(node.operator,f'\'{node.operator.value}\' is an invalid operation')
        except InvalidOperation:
            self._error()



    def visit_Number(self, node):
        # return node.value
        pass


    def visit_Boolean(self, node):
        # return node.value
        pass


    def visit_Compound(self, node):
        for child in node.children:
            if child: self.visit(child)



    def visit_NoOperation(self, node):
        pass


    def visit_Assign(self, node):
        var_id = node.left.value

        # compute the value of the right hand side
        if isinstance(node.right, MethodCall):
            self.visit(node.right)
            try:
                returned = CALL_STACK.pop()
            except IndexError:
                try:
                    raise InvalidOperation(node.right.token,f'Function \'{node.right.name}\' does not return any value')
                except InvalidOperation:
                    self._error()
            else:
                # value = returned[0]
                label = returned
            # check if the returned label can flow to the function clearance
            if label <= self.clearance:
                self.pc = self.pc + label
            else:
                try:
                    # raise an error for invalid flow
                    raise InvalidFlow(node.right.token,f'The returned label {label} cannot flow to subject clearance {self.clearance}')

                except InvalidFlow:
                    self._error()

        else:
            self.visit(node.right)

        
        # if the target variable is tagged as global by the user
        if var_id in self.user_inputs.globals:

            # check if LUB of pc and subject label can flow to target label
            if self.pc <= node.left.label:
                # if yes then update the value of the target variable
                self.GLOBAL_SCOPE[var_id] = node.left.label
            else:
                # if no raise an error
                try:
                    # raise an error for invalid flow
                    raise InvalidFlow(node.left.token,f'PC label {self.pc} cannot flow to the label of global variable \'{var_id}\' {node.left.label}')

                except InvalidFlow:
                    self._error()
        # target variable is a local, therefore update the value and label
        else:
            # if the variable already exist in GLOBAL_SCOPE dictionary
            if var_id in self.GLOBAL_SCOPE:
                self.GLOBAL_SCOPE[var_id] = self.GLOBAL_SCOPE[var_id] + self.pc
            else:
                self.GLOBAL_SCOPE[var_id] = self.pc



    def visit_IfElse(self, node):
        # evaluate the value of the condition -- True or False
        # condition = self.visit(node.condition)
        self.visit(node.condition)

        # Henceforth the idea is to execute seperately the two branches 
        # and join the different labels of a variable generated by the
        # executions of two branches. Similarly join the pc label 
        # produced by two branches. Once this is done the final labels 
        # are again stored in the current instance of the interpreter 
        # and execute any one branches depending on the predicate to 
        # generate the values for the variables.

        # create a temporary instance of the Analyzer to execute 
        # If/Else part seperately
        temp = Analyzer(self.user_inputs)

        # initialize the temp instance with the current GLOBAL_SCOPE and pc label
        temp.GLOBAL_SCOPE = dict(self.GLOBAL_SCOPE)
        temp.pc = Label(self.pc.owner,self.pc.readers,self.pc.writers)

        # execute the left branch
        self.visit(node.left)

        # execute the right branch if not None
        if node.right: temp.visit(node.right)

        # iterate the variables in GLOBAL_SCOPE of temp
        for var in temp.GLOBAL_SCOPE:
            # if the variable exist in the GLOBAL_SCOPE of current instance self
            if var in self.GLOBAL_SCOPE:
                # if the labels of a variable in temp and self are different
                if temp.GLOBAL_SCOPE[var] != self.GLOBAL_SCOPE[var]:
                    # the final label of the variable is the join of the label from temp and self
                    self.GLOBAL_SCOPE[var] = self.GLOBAL_SCOPE[var] + temp.GLOBAL_SCOPE[var]
            # else add the variable into the GLOBAL_SCOPE of the current instance 
            # with the label from temp and value None
            else:
                self.GLOBAL_SCOPE[var] = temp.GLOBAL_SCOPE[var]

        # finally join the generated pc labels after executing 
        # two branches and store it into the current instance
        if temp.pc != self.pc:
            self.pc = self.pc + temp.pc



    def visit_While(self, node):

        # create a temporary instance of the Interpreter 
        temp = Analyzer(self.user_inputs)

        # execute the condition and loop body
        self.visit(node.condition)
        self.visit(node.body)

        while not self.isequal(temp):
            temp.GLOBAL_SCOPE = dict(self.GLOBAL_SCOPE)
            temp.pc = Label(self.pc.owner, self.pc.readers, self.pc.writers)
            self.visit(node.condition)
            self.visit(node.body)

    

    def isequal(self, other):
        ''' check if GLOBAL_SCOPE of two instances of Interpreter are equal'''
        for var in self.GLOBAL_SCOPE:
            if var in other.GLOBAL_SCOPE:
                if self.GLOBAL_SCOPE[var] != other.GLOBAL_SCOPE[var] \
                    or self.pc != other.pc:
                    return False
            else:
                return False

        return True



    # def loop(self, node):
    #     try:
    #         if self.visit(node.condition):
    #             self.visit(node.body)
    #             return self.loop(node)
    #         else:
    #             # the loop terminates, hence return True
    #             return True
    #     except RecursionError:
    #         # loop does not terminate, hence return False
    #         return False


    def visit_MethodDef(self, node):
        # store the function parameters and body in the dictionary
        FUNCTIONS[node.name] = node




    def visit_MethodCall(self, node):
        # obtain the function name
        func_name = node.name
        # check if the function is already defined or not
        if func_name in FUNCTIONS:
            # if the function is defined check if the size of function
            # arguments matches with the size of function parameters
            if len(node.arguments) == len(FUNCTIONS[func_name].parameters):
                # create an instance of Interpreter to execute the function body
                temp = Analyzer(self.user_inputs)
                # if the function is given a clearance label then assign the same 
                # for the new instance of the interpreter; default clearance label 
                # is the subject label
                if func_name in temp.user_inputs.methods:
                    temp.clearance = temp.user_inputs.methods[func_name]
                    temp.pc = Label(temp.clearance.owner,{'*'},{})
                # obtain the function parameters list from the dictionary FUNCTIONS
                parameters = FUNCTIONS[func_name].parameters
                # initialize the index position as zero
                index = 0
                # iterate the parameters list
                for param in parameters:
                    argument = node.arguments[index]
                    # arg_value = None
                    arg_label = None
                    # if argument is a variable
                    if isinstance(argument, Variable):
                        # check if the variable is defined earlier
                        if argument.value in self.GLOBAL_SCOPE:
                            arg_label = self.GLOBAL_SCOPE[argument.value]
                        else:
                            # if no raise an error
                            try:
                                # raise an error for not defined argument
                                raise UndefinedID(argument,f'Variable \'{argument.value}\' not defined')

                            except UndefinedID:
                                self._error()
    
                    # if argument is a number
                    if isinstance(argument, Number):
                        # arg_value = self.visit(argument)
                        arg_label = Label(self.clearance.owner, {'*'}, {})
                    # argument is an expression
                    else:
                        self.visit(argument)
                        arg_label = self.pc

                    # store the value and label of each argument as local variable
                    # into the GLOBAL_SCOPE of the new instance of the Interpreter
                    temp.GLOBAL_SCOPE[param.value] = Label(temp.clearance.owner, arg_label.readers, arg_label.writers)

                    # increment the index to obtain next argument
                    index += 1
                
                # execute the body of the function
                temp.visit(FUNCTIONS[func_name].body)
                # obtain the termination status of the function
                self.terminate = temp.terminate
            else:
                try:
                    # raise an error for not defined argument
                    raise InvalidStatement(node.token,f'Number of arguments does not match with the declared parameters')

                except InvalidStatement:
                    self._error()
        else:
            try:
                # raise an error for not defined argument
                raise UndefinedID(node.token,f'Function \'{func_name}\' is not defined')

            except UndefinedID:
                    self._error()
           


    def visit_ThreadCall(self, node):
        # create a temporary instance of the interpreter
        temp = Analyzer(self.user_inputs)
        # set the mainthread as false
        temp.mainthread = False
        # import the python Thread module
        from threading import Thread



    def visit_Return(self, node):
    
        # label variable that will be returned
        label = None

        # # create a temporary analyzer object
        # temp = Analyzer(self.user_inputs)

        # # set the clearance label same as the current clearance label
        # temp.clearance = self.clearance

        # # visit the expression
        # temp.visit(node.expr)

        # if not self.pc <= temp.pc:
        #     try:
        #         raise InvalidFlow(node.token, f'PC label {self.pc} cannot flow to the label of the expression {temp.pc}') 
        #     except InvalidFlow:
        #         self._error()


        # currently return parameter does not support an expression but variable and downgrade
        # S:: return x | return downgrade
        # if the return parameter is a Variable, then we need to consider two cases further
        if isinstance(node.expr, Variable):
            self.visit(node.expr)
            # check if the variable is a global variable:
            if node.expr.value in self.user_inputs.globals:
                # check if the pc label can flow to the variable
                if self.pc <= self.user_inputs.globals[node.expr.value]:
                    label = self.user_inputs.globals[node.expr.value]
                else:
                    try:
                        # raise an error for invalid flow
                        raise InvalidFlow(node.expr,f'Label of PC {self.pc} cannot flow to the label of global variable \'{node.expr.value}\' {self.user_inputs.globals[node.expr.value]}')

                    except InvalidFlow:
                        self._error()
            # if the variable is a local variable the label of returned 
            # variable shall be join of variable label and pc label
            else:
                label = self.pc
        # if return parameter is a downgrade
        elif isinstance(node.expr, Downgrade):
            # get the variable id
            var_id = node.expr.variable.value
            # get the variable label first
            variable_label = None
            # if the downgraded variable is global then check if pc can flow to the label
            # then only perform the downgrading
            if var_id in self.user_inputs.globals:

                variable_label = node.expr.variable.label
                # check if pc can flow to the label of the global variable
                if self.pc <= variable_label:
                    # set the from label same as variable label
                    node.expr.from_label = variable_label
                    # perform the downgrading
                    self.visit(node.expr)
                else:
                    try:
                        # raise an error for invalid flow
                        raise InvalidFlow(node.token,f'Label of PC {self.pc} cannot flow to the label of global variable \'{var_id}\' {variable_label}')

                    except InvalidFlow:
                        self._error()
            # if the downgraded variable is a local then first join the variable label with pc label
            else:
                if var_id in self.GLOBAL_SCOPE:
                    variable_label = self.GLOBAL_SCOPE[var_id] + self.pc
                else:
                    try:
                        # raise an error for invalid flow
                        raise UndefinedID(node.token,f'The variable \'{var_id}\' is not defined')

                    except UndefinedID:
                        self._error()

                # change the from label for the local variable
                node.expr.from_label = variable_label
                # perform the downgrading
                self.visit(node.expr)
            
            # set the returned label to the newly downgraded label
            label = node.expr.new_label

        # append the label into the call stack
        CALL_STACK.append(label)

            


    def visit_Variable(self, node):
        var_id = node.value

        label = None

        # if the variable is a global
        if var_id in self.user_inputs.globals:
            label = node.label
        # if the label is local
        else:
            if var_id in self.GLOBAL_SCOPE:
                label = self.GLOBAL_SCOPE[var_id]
            else:
                try:
                    raise UndefinedID(node.token, f'Variable \'{var_id}\' is not defined')
                except UndefinedID:
                    self._error()

        if label <= self.clearance:
            self.pc = self.pc + label
        else:
            try:
                # raise an error for invalid flow
                raise InvalidFlow(node.token,f'Label of the variable \'{var_id}\' {label} cannot flow to subject clearance {self.clearance}')

            except InvalidFlow:
                self._error()




    def visit_Downgrade(self, node):
        readers = set()

        for reader in node.readers.elements:
            readers.add(reader.value)


        # only perform the downgrade and show the error message, set the new label on successful downgrading
        if node.from_label:
            downgraded_label, error_message = downgrade(self.clearance.owner, node.from_label, readers)
            
            if downgraded_label:
                node.new_label = downgraded_label
            else:
                try:
                    # raise an error for invalid flow
                    raise InvalidOperation(node.token, error_message)

                except InvalidOperation:
                    self._error()
        # if from label is None throw error as invalid operation
        else:
            try:
                # raise an error for invalid flow
                raise InvalidOperation(node.token, 'Not a proper use of downgrading')

            except InvalidOperation:
                self._error()




    def analyze(self, tree):
        self.visit(tree)
        return True if self.error == True else False
