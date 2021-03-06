# [Pifthon](https://github.com/pifthon/pifthon) (Python Information Flow Analyzer)

Pifthon is a flow analyzer that keeps track of all the information flows taking place in a given python program and identify a program point that is vulnerable to an information leak with respect to the given security labels of global variables (variables those interact with outside entities).

>[Pifthon Version 0.1](https://github.com/pifthon/pifthon) 

First, the analyzer reads security labels of global variables of a given program from a JSON file. Then it auto-generates final labels for all the local variables. In the presence of a potential information leak, the analyzer throws an error message with sufficient feedback.

## Local Setup Instructions

+ Clone the project from the source:

```
git clone https://github.com/pifthon/pifthon
```


## Running the tool:


+ Move into the tests directory

```
cd tests
```

+ Run sample case/Add your own python program
```
gedit test.py
```

+ save this code (if you added your program)


+ Open the input.json file

```
gedit input.json
```

+ Modify this JSON to suit your need and don't forget to save the file. You may need to change the labels of the entities involved in your program. Identify the labels as


+ Move out of this directory

```
cd ..
```

+ Run the analyzer in two ways:

 1. Script mode: provide the complete source file as input
```
python pifthon/pifthon.py -j tests/input.json -i tests/test.py
```
 2. Interactive mode: provide immediate feedback for each command line
```
python pifthon/pifthon.py -j tests/input.json
```
