import sys, os, re
from os import system, name
import getopt, logging, datetime, parse_json
from language import execute





def main(argv):

    try:
        if len(argv) == 0:
            raise ValueError()

        # later try to implement argparse instead of getopt
        options, arguments = getopt.getopt(sys.argv[1:],"hi:j:l:g:",["help","input=","json=","log=","log-level="])


        input_files = None
        json_files = None

        # create a default log file using the timestamp
        # log_file = 'log/pifthon' + str(datetime.datetime.now()).split(' ')[1] + '.log'
        log_file = "logging"
        
        # set default logging level as NOTSET
        logging.basicConfig(filename=log_file, level=logging.DEBUG)

        for option, argument in options:
            if option in ("-h", "--help"):
                print('pifthon.py -i [sourcefile,...] -j [jsonfile,...] -l <logfile> -g <ERROR|INFO|DEBUG>')
                sys.exit()

            elif option in ("-i", "--input"):
                is_input_file = True
                input_files = argument

            elif option in ("-j", "--json"):
                json_files = argument

            elif option in ("-l", "--log"):
                log_file = argument
            elif option in ("-g", "--log-level"):
                levels = {"ERROR":logging.ERROR,
                          "INFO":logging.INFO,
                          "DEBUG":logging.DEBUG}
                logging.basicConfig(filename=log_file, level=levels.get(option, logging.NOTSET))
                
    except (ValueError, getopt.GetoptError):
        print('pifthon.py -h [--help]' )
        sys.exit(2)

    # logging.info(f'Given input files: {input_files}')
    # logging.info(f'Given json files: {json_files}')
    # print('input files: ', input_files)
    # print('json files: ', json_files)
    # print('log file: ' + log_file)

    # check if user has provided the json file since 
    # the json file is mandatory for pifthon interpreter
    if json_files == None:
        print('JSON file not found')
        print('pifthon.py -j [jsonfile,...]')
        sys.exit()
    else:
        user_inputs = parse_json.JSONParser(json_files)


    tokens = []
    temp_tokens = None

    if input_files:
        statement = ''
        with open(input_files, 'r') as file:
            while True:
                text = file.readline()

                statement = statement + text

                if not text:
                    break
        try:
            temp_tokens = execute('<stdin>',statement, tokens, user_inputs)
        except Exception:
            quit()
        else:
            tokens += temp_tokens
            # print(tokens)
            print('The program is flow secure')

    else: 
        try:
            # infinitely take input until programmer interrupts
            while True:
                # store the user input into statement without the newline 
                statement = input('pifthon >> ')
                # text will store each line within a block, i.e., if/else/while/def
                text = statement
                # if the string "text" conatins any block statement
                if text.__contains__('if') or text.__contains__("while") or text.__contains__("def"):

                    # infinitely take user inputs until the block is closed by pressing double "ENTER"
                    while text != '':

                        text = input('       ... ')

                        statement = statement + '\n' + text

                try:
                    temp_tokens = execute('<stdin>',statement, tokens, user_inputs)
                except Exception:
                    temp_tokens = None
                    continue

                if temp_tokens:
                    tokens += temp_tokens
                    # print(tokens)
                    print('The program is flow secure')
        except (KeyboardInterrupt, EOFError):
            sys.exit('\n')
        
    

def clear():
    'The function is to clear the terminal screen'
    # for windows
    if name == 'nt':
        _ = system('cls')
    
    # for mac and linux
    else:
        _ = system('clear')




if __name__ == "__main__":
    main(sys.argv[1:])