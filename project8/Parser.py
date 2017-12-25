from Command import Command
from enum import Enum

ARITHMETIC_COMMANDS = ['add','sub','neg','gt','eq','lt','and','or','not']

"an enum to all the commands. can be easily extanded"
class Commands(Enum):
    C_ARITHMETIC = 'C_ARITHMETIC'
    C_POP = 'C_POP'
    C_PUSH = 'C_PUSH'
    C_LABEL = 'C_LABEL'
    C_GOTO = 'C_GOTO'
    C_IF = 'C_IF'
    C_FUNCTION = 'C_FUNCTION'
    C_RETURN = 'C_RETURN'
    C_CALL = 'C_CALL'

"a class of a parser object. will hold an array of parsed command created from the input file lines"
class Parser:
    file_to_parse = None
    current_line = ''
    program_commands = []

    """creates a new parser by the name of the file it reads"""
    def __init__(self, file):
        self.program_commands.clear()  # clearing the table of the commands to write, from previous vm file
        self.file_to_parse = file  # replacing the input file object to read from
        self.current_line = ''  # initializing the current line

    """takes a command line and returns a const string of the command type"""
    def command_type(self):
        name = self.current_line.split(' ')[0]
        if name == 'push':
            return Commands.C_PUSH
        elif name == 'pop':
            return Commands.C_POP
        elif name in ARITHMETIC_COMMANDS:
            return Commands.C_ARITHMETIC
        elif name == 'label':
            return Commands.C_LABEL
        elif name == 'goto':
            return Commands.C_GOTO
        elif name == 'if-goto':
            return Commands.C_IF
        elif name == 'call':
            return Commands.C_CALL
        elif name == 'function':
            return Commands.C_FUNCTION
        elif name == 'return':
            return Commands.C_RETURN

    """takes a command line and returns the string of first argument.
    this could be either the memory segment name to manipulate, or the arithmetic command name"""
    def arg1(self,command_type):
        if command_type == Commands.C_RETURN:
            # there are no arguments if it's return
            return
        if command_type == Commands.C_ARITHMETIC:
            # only one argument if it's arithmetic, and the argument is the command itself
            return self.current_line.split(' ')[0]
        elif command_type == Commands.C_POP or command_type == Commands.C_PUSH or command_type == Commands.C_FUNCTION\
                or command_type == Commands.C_CALL:
            # if there are 2 arguments
            first, second, third = self.current_line.split(' ')
            return second
        elif command_type == Commands.C_IF or command_type == Commands.C_GOTO or command_type == Commands.C_LABEL:
            # if there is only one argument
            first, second = self.current_line.split(' ')
            return second
        return


    """in case of some commands, will return an int which is the parameter of the second argument"""
    def arg2(self,command_type):
        if command_type == Commands.C_POP or command_type == Commands.C_PUSH or command_type == Commands.C_FUNCTION\
                or command_type == Commands.C_CALL:
            first, second, third = self.current_line.split(' ')
            return int(third) # if there is one, it's always int
        else:
            return None

    "will work on the 'current_line' field of the parser, and will add to the list of commands the command created" \
    "from it"
    def parse_command(self):
        command_name = self.command_type()
        command_first_arg = self.arg1(command_name)
        command_second_arg = self.arg2(command_name)
        new_command = Command(self.current_line, command_name, command_first_arg, command_second_arg)
        self.program_commands.append(new_command)

    """will add to the commands the first call, only when the first vm file is parsed"""
    def parse_first_call(self):
        # first, parsing call sys.init command
        first = 'call Sys.init 0'
        self.current_line = first
        self.parse_command()

    """will create from the current line a command object, add to the commands table and advanced to the next in case 
    we have more commends to execute"""
    def parse_all_commands(self):
        for line in self.file_to_parse:
            line = line.strip()  # getting rid of all the white space in the side
            line = ' '.join(line.split())  # split by all kinds of white space and joining with a single white space
            if line != '' and line[0] != '/' and line != '\n': # skipping on the empty lines
                # first cleanning non empty lines from notes
                temp_line = line.split('//')[0]
                final_line = temp_line.split('\n')[0]
                the_line = final_line.strip()
                self.current_line = the_line
                self.parse_command()