import sys
from language.tokens import *
from rwfm import Label
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

class Interpreter(NodeVisitor):
    def __init__(self, user_inputs):
        # a dictionary to store the variables along with their values and labels
        self.GLOBAL_SCOPE = dict()
        # store the defined list of variables of a block inside the stack
        # this helps to track the scope of the variables defined inside a block
        # self.VARIABLE_STACK = []
        self.user_inputs = user_inputs
        self.clearance = user_inputs.subject_label
        self.pc = Label(self.clearance.owner,{'*'},{})
        self.terminate = True
        self.mainthread = True

    def visit_BinaryOp(self, node):

        error = None

        if isinstance(node.right, Number) or isinstance(node.right, Variable):
            if node.right.label <= self.clearance:
                self.pc = self.pc + node.right.label
            else:
                error = 'Invalid Flow'
        
        if isinstance(node.left, Number) or isinstance(node.left, Variable):
            if node.left.label <= self.clearance:
                self.pc = self.pc + node.left.label
            else:
                error = 'Invalid Flow'

        if error:
            print(error)
            sys.exit(1)


        if node.operator.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.operator.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.operator.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.operator.type == DIV:
            return self.visit(node.left) / self.visit(node.right)
        elif node.operator.type == AND:
            return self.visit(node.left) and self.visit(node.right)
        elif node.operator.type == OR:
            return self.visit(node.left) or self.visit(node.right)
        elif node.operator.type == XOR:
            return self.visit(node.left) ^ self.visit(node.right)
        elif node.operator.type == COMPARE:
            return self.visit(node.left) == self.visit(node.right)
        elif node.operator.type == LEQ:
            return self.visit(node.left) <= self.visit(node.right)
        elif node.operator.type == GEQ:
            return self.visit(node.left) >= self.visit(node.right)
        elif node.operator.type == LTHAN:
            return self.visit(node.left) < self.visit(node.right)
        elif node.operator.type == GTHAN:
            return self.visit(node.left) > self.visit(node.right)
        elif node.operator.type == NEQ:
            return self.visit(node.left) != self.visit(node.right)
        else:
            raise Exception(f'Invalid operation: {node.operator.type}')


    def visit_UnaryOp(self, node):
        operator = node.operator.type
        if operator == PLUS:
            return +self.visit(node.expr)
        elif operator == MINUS:
            return -self.visit(node.expr)
        elif operator == NOT:
            return not self.visit(node.expr)

    def visit_Number(self, node):
        return node.value


    def visit_Boolean(self, node):
        return node.value


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
            except:
                print(f'Function \'{node.right.name}\' does not return any value')
                sys.exit()
            else:
                value = returned[0]
                label = returned[1]
            # check if the returned label can flow to the function clearance
            if label <= self.clearance:
                self.pc = self.pc + label
        else:
            value = self.visit(node.right)

        # store the label of the target variable
        target_label = node.left.label

        # if the target variable is tagged as global by the user
        if var_id in self.user_inputs.globals:

            # check if LUB of pc and subject label can flow to target label
            if (self.pc + self.clearance) <= target_label:
                # if yes then update the value of the target variable
                self.GLOBAL_SCOPE[var_id] = (value, target_label)
            else:
                # if no raise an error
                print('Invalid Flow')
                sys.exit(1)
        # target variable is a local, therefore update the value and label
        else:
            # if the variable already exist in GLOBAL_SCOPE dictionary
            if var_id in self.GLOBAL_SCOPE:
                self.GLOBAL_SCOPE[var_id] = (value, self.GLOBAL_SCOPE[var_id][1] + self.pc)
            else:
                self.GLOBAL_SCOPE[var_id] = (value, self.pc)



    def visit_IfElse(self, node):
        # evaluate the value of the condition -- True or False
        condition = self.visit(node.condition)

        # Henceforth the idea is to execute seperately the two branches 
        # and join the different labels of a variable generated by the
        # executions of two branches. Similarly join the pc label 
        # produced by two branches. Once this is done the final labels 
        # are again stored in the current instance of the interpreter 
        # and execute any one branches depending on the predicate to 
        # generate the values for the variables.

        # create a temporary instance of the Interpreter to execute 
        # If/Else part seperately
        temp = Interpreter(self.user_inputs)

        # initialize the temp instance with the current GLOBAL_SCOPE and pc label
        temp.GLOBAL_SCOPE = dict(self.GLOBAL_SCOPE)
        temp.pc = self.pc

        # follow the natural execution of the branch based on the predicate value
        # thus obtain the values for the variables
        if condition == True:
            # natural execution if condition is True
            self.visit(node.left)
            # if Else part is given execute it seperately
            if node.right: temp.visit(node.right)
        # if else part is given
        elif node.right:
            # natural execution if condition is False
            self.visit(node.right)
            # execute the If part seperately
            temp.visit(node.left)
        # if else part is not given
        else:
            # if the condition is False and there is no Else part 
            # then execute the If part seperately
            temp.visit(node.left)

        # iterate the variables in GLOBAL_SCOPE of temp
        for var in temp.GLOBAL_SCOPE:
            # if the variable exist in the GLOBAL_SCOPE of current instance self
            if var in self.GLOBAL_SCOPE:
                # if the labels of a variable in temp and self are different
                if temp.GLOBAL_SCOPE[var][1] != self.GLOBAL_SCOPE[var][1]:
                    # the final label of the variable is the join of the label from temp and self
                    self.GLOBAL_SCOPE[var] = (self.GLOBAL_SCOPE[var][0], self.GLOBAL_SCOPE[var][1] + temp.GLOBAL_SCOPE[var][1])
            # else add the variable into the GLOBAL_SCOPE of the current instance 
            # with the label from temp and value None
            else:
                self.GLOBAL_SCOPE[var] = (None, temp.GLOBAL_SCOPE[var][1])

        # finally join the generated pc labels after executing 
        # two branches and store it into the current instance
        if temp.pc != self.pc:
            self.pc = self.pc + temp.pc



    def visit_While(self, node):
        # evaluate the value of the condition -- True or False
        # condition = self.visit(node.condition)
        
        # create a temporary instance of the Interpreter 
        temp_1 = Interpreter(self.user_inputs)

        # initialize the temp instance with the current GLOBAL_SCOPE and pc label
        temp_1.GLOBAL_SCOPE = dict(self.GLOBAL_SCOPE)
        temp_1.pc = self.pc

        if self.visit(node.condition):
            self.visit(node.body)
            self.terminate = self.loop(node)

        # create a temporary instance of the Interpreter 
        temp_2 = Interpreter(self.user_inputs)

        # initialize the temp instance with the current GLOBAL_SCOPE and pc label
        temp_2.GLOBAL_SCOPE = dict(self.GLOBAL_SCOPE)
        temp_2.pc = self.pc

        while not temp_2.isequal(temp_1):
            temp_1.GLOBAL_SCOPE = dict(temp_2.GLOBAL_SCOPE)
            temp_1.pc = temp_2.pc
            temp_2.visit(node.condition)
            temp_2.visit(node.body)

        for var in temp_2.GLOBAL_SCOPE:
            self.GLOBAL_SCOPE[var] = (self.GLOBAL_SCOPE[var][0], temp_2.GLOBAL_SCOPE[var][1])

    

    def isequal(self, other):
        ''' check if GLOBAL_SCOPE of two instances of Interpreter are equal'''
        for var in self.GLOBAL_SCOPE:
            if var in other.GLOBAL_SCOPE:
                if self.GLOBAL_SCOPE[var][1] != other.GLOBAL_SCOPE[var][1] \
                    or self.pc != other.pc:
                    return False
            else:
                return False

        return True



    def loop(self, node):
        try:
            if self.visit(node.condition):
                self.visit(node.body)
                return self.loop(node)
            else:
                # the loop terminates, hence return True
                return True
        except RecursionError:
            # loop does not terminate, hence return False
            return False


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
                temp = Interpreter(self.user_inputs)
                # if the function is given a clearance label then assign the same 
                # for the new instance of the interpreter; default clearance label 
                # is the subject label
                if func_name in temp.user_inputs.methods:
                    temp.clearance = temp.user_inputs.methods[func_name]
                # obtain the function parameters list from the dictionary FUNCTIONS
                parameters = FUNCTIONS[func_name].parameters
                # initialize the index position as zero
                index = 0
                # iterate the parameters list
                for param in parameters:
                    argument = node.arguments[index]
                    arg_value = None
                    arg_label = None
                    # if argument is a variable
                    if isinstance(argument, Variable):
                        # check if the variable is defined earlier
                        if argument.value in self.GLOBAL_SCOPE:
                            arg_value = self.GLOBAL_SCOPE[argument.value][0]
                            arg_label = self.GLOBAL_SCOPE[argument.value][1]
                        else:
                            print(f'Variable {argument.value} not defined')
                            sys.exit()
                    # if argument is a number
                    if isinstance(argument, Number):
                        arg_value = self.visit(argument)
                        arg_label = Label(self.clearance.owner, {'*'}, {})
                    # argument is an expression
                    else:
                        arg_value = self.visit(argument)
                        arg_label = self.pc

                    # store the value and label of each argument as local variable
                    # into the GLOBAL_SCOPE of the new instance of the Interpreter
                    temp.GLOBAL_SCOPE[param.value] = (arg_value, Label(temp.clearance.owner, arg_label.readers, arg_label.writers))

                    # increment the index to obtain next argument
                    index += 1
                
                # execute the body of the function
                temp.visit(FUNCTIONS[func_name].body)
                # obtain the termination status of the function
                self.terminate = temp.terminate
            else:
                print('Invalid number of function arguments')
                sys.exit()
        else:
            print(f'Function \'{func_name}\' is not defined')
            sys.exit()


    def visit_ThreadCall(self, node):
        # create a temporary instance of the interpreter
        temp = Interpreter(self.user_inputs)
        # set the mainthread as false
        temp.mainthread = False
        # import the python Thread module
        from threading import Thread


    def visit_Return(self, node):
    
        value = self.visit(node.expr)

        # check if the return parameter is a variable 
        if isinstance(node.expr, Variable):
            # check if the variable is a global variable:
            if node.expr.value in self.user_inputs.globals:
                # check if the pc label can flow to the variable
                if self.pc <= self.user_inputs.globals[node.expr.value]:
                    label = self.user_inputs.globals[node.expr.value]
                else:
                    print('Invalid Flow')
                    sys.exit()
            # if the variable is a local variable the label of returned 
            # variable shall be join of variable label and pc label
            else:
                label = self.GLOBAL_SCOPE[node.expr.value][1] + self.pc
        # if return parameter is an expression
        else:
            # if the return parameter is an expression (may or maynot comprise 
            # global variable) then return the pc label
            label = self.pc

        CALL_STACK.append((value, label))

            


    def visit_Variable(self, node):
        var_id = node.value
        value = self.GLOBAL_SCOPE.get(var_id)[0]
        if value is None:
            raise NameError(repr(var_id))
        else:
            label = self.GLOBAL_SCOPE.get(var_id)[1]
            if label <= self.clearance:
                self.pc = self.pc + label
                return value
            else:
                # if no raise an error
                print('Invalid Flow')
                sys.exit(1)


    def interpret(self, tree):
        return self.visit(tree)
