import json
import collections
from rwfm import Label



class JSONParser:
    def __init__(self, file):
        self.json_file = file
        data = json.load(open(self.json_file))
        # self.source_file = self.getFilename(data)
        self.subject = self.getSubjectName(data)
        # print(f'Executing subject: {self.subject}')

        self.subject_label = self.getSubjectLabel(data)
        # print(f'Subject label: {self.subject_label}')

        self.globals = self.getGlobals(data)

        # print(f'Global variables: {self.globals}')
        # methods = {'name':label}
        self.methods = self.getMethods(data)
        self.threads = self.getThreads(data)
        # a possible extension
        # self.parallel = None

    def getOwner(self, data):
        '''Parse the owner field from the JSON Object'''
        return data["owner"]

    def getReaders(self, data):
        '''Parse the readers field from the JSON Object'''
        readers = set()
        for reader in data["readers"]:
            for key in reader:
                readers.add(reader[key])
        return readers

    def getWriters(self, data):
        '''Parse the writers field from the JSON Object'''
        writers = set()
        for writer in data["writers"]:
            for key in writer:
                writers.add(writer[key])
        return writers
    
    def getFilename(self, data):
        '''Method returns a list containing name of the source files'''
        return data["configurations"]["file_name"]

    
    def getSubjectName(self, data):
        return data["configurations"]["subject"]


    def getSubjectLabel(self, data):
        try:
            owner = self.getOwner(data["configurations"]["label"])
            readers = self.getReaders(data["configurations"]["label"])
            writers = self.getWriters(data["configurations"]["label"])
            
            label = Label(owner,readers,writers)

        except KeyError:
            return None
        else:
            return label
        
        
    def getGlobals(self, data):
        '''
        Method returns a dictionary having global variables as key that is mapped to respective static label 
        '''
        globals_= dict()
        try:
            for global_ in data["configurations"]["global_vars"]:
                id_ = global_["id"]
                owner = self.getOwner(global_["label"])
                readers = self.getReaders(global_["label"])
                writers = self.getWriters(global_["label"])

                label = Label(owner,readers,writers)
                globals_[id_] = label
        except KeyError:
            return None
        else:
            return globals_


    def getMethods(self, data):
        methods = dict()

        try:
            for method in data["configurations"]["method_label"]:
                name = method["name"]
                owner = self.getOwner(method["label"])
                readers = self.getReaders(method["label"])
                writers = self.getWriters(method["label"])

                label = Label(owner,readers,writers)
                methods[name] = label
        except KeyError:
            return None
        else:
            return methods


    def getThreads(self, data):
        threads = []

        try:
            for thread in data["configurations"]["threads"]:
                subject = thread["subject"]
                name = thread["name"]
                threads.append((subject, name))
        except KeyError:
            return None
        else:
            return threads









# def print_globals(globals):
#     str=''
#     if globals:
#         for key in globals.keys():
#             str = str + key + ' : ' + globals[key].to_string() + '\n'
#         return str
#     else:
#         return 'Not Given'

