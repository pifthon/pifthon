import sys
# import rwfm.subjects, rwfm.objects
#####################
# FLOW ERRORS
#####################

# List of flow errors
# IFLOW   =   'Error:: IllegalFlow'
# IDOWN   =   'Error:: InvalidDowngrade'

# ''' The class Error contains the list of flow errors
# that might occur during an information flow transition'''

# class FlowError:
#     def __init__(self, error_name, error_message, self, other):
#         self.error_name = error_name
#         self.error_message = error_message
#         self.self = self
#         self.other = other

#     def __repr__(self):
#         return f'{self.error_name}:{self.error_message} from{self.self} to {self.other}'


# class InvalidFlowError(FlowError):
#     def __init__(self, error_message, self, other):
#         super().__init__(IFLOW, error_message, self, other)

# class InvalidDowngradeError(FlowError):
#     def __init__(self, error_message, self, other):
#         super().__init__(IDOWN, error_message, self, other)
#####################
# LABEL
#####################

''' Class label represents a security label
and has three components: owner, readers and writers
'''

class Label:
    def __init__(self, owner, readers, writers):
        self.owner = owner
        self.readers = readers
        self.writers = writers

    def __repr__(self):
        if self.readers == {'*'}:
            return f'({self.owner},{{*}},{self.writers})'
        else:
            return f'({self.owner},{self.readers},{self.writers})'

    def __eq__(self, other):
        return self.owner == other.owner and self.readers == other.readers and self.writers == other.writers



    def get_label(self):
        return Label(self.owner, self.readers, self.writers)



    def __add__(self, other):
        # join operation between self and label which 
        # represents a flow from label to self

        if self.readers == {'*'} and other.readers == {'*'}:
            new_label = Label(self.owner, {'*'}, set(self.writers) | set(other.writers))
        
        elif self.readers != {'*'} and other.readers == {'*'}:
            new_label = Label(self.owner, self.readers, set(self.writers) | set(other.writers))

        elif self.readers == {'*'} and other.readers != {'*'}:
            new_label = Label(self.owner, other.readers, set(self.writers) | set(other.writers))

        elif set(self.readers) & set(other.readers) == {}:
            print('Error in joining')
            sys.exit(1)

        else:
            new_label = Label(self.owner, set(self.readers) & set(other.readers), set(self.writers) | set(other.writers))

        return new_label



    def __mul__(self, label):
        pass


    def __le__(self, other):
        # less than equal operator verifies
        #  the can-flow-to relationship
        # error = InvalidFlowError('information cannot flow',self,other)
        if self.readers == {'*'} or set(self.readers).issuperset(other.readers):

            if other.writers == {'*'} or set(other.writers).issuperset(self.writers):
                return True
            else:
                return False
        else:
            return False


def downgrade(subject, object_label, readers):
    '''Return (downgraded label, None) if downgrading is successful otherwise (None, error message)'''
    # check if subject and owner of the object label is same
    if subject == object_label.owner:
        # Check if the set principals is a subset of writers set 
        # of object_label
        # or If owner is the sole writer  of object_label
        if not (set(readers).issubset(set(object_label.writers)) \
            or object_label.writers == set(subject) \
                or readers == object_label.writers):
            return None, f'New readers set {readers} is not a subset of the writers set {object_label.writers}'
    # otherwise throw error
    else:
        return None, f'Owner of the object label, i.e., \'{object_label.owner}\' is not same as the executing subject, i.e., \'{subject}\''

    # new label after downgrading
    new_label = Label(subject, object_label.readers | readers, object_label.writers)

    return new_label, None

################################
# FLOW OPERATIONS
################################


# def downgrade(subject, object_, principals):
#     # new label after downgrading
#     new_label = Label(object_.label.owner, object_.label.readers | principals, object_.label.writers)

#     if subject.label.owner == object_.label.owner:
        # If the set principals is a subset of writers set 
        # of object_label
        # or If owner is the sole writer  of object_label
        # then return 
    #     if set(principals).issubset(set(object_.label.writers)) \
    #         or object_.label.writers == subject.label.owner \
    #             or principals == object_.label.writers:
                
    #             return new_label, None
    #     else:
    #         return None, InvalidDowngradeError('New readers are not in the current writers, unable to downgrade', object_.label, new_label)
    # else:
    #     return None, InvalidDowngradeError('Executing subject is not allowed to downgrade', object_.label, new_label)
