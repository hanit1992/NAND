from Parser import Commands
import os

"this is a list of the segments who has a lot in common comare to the other memory segments"
FIRST_TYPE_SEGMENTS = ['local','argument','this','that','temp']

"this command pops the last value of the stack, stores it in the address that D holds, and stores it in D"
POP_TO_D_ADDRESS = '@R13' + '\n' + \
                'M=D' + '\n' + \
                '@SP' + '\n' + \
                'M=M-1' + '\n' + \
                'A=M' + '\n' + \
                'D=M' + '\n' + \
                '@R13' + '\n' + \
                'A=M' + '\n' + \
                'M=D' + '\n'

"this command pops the last value of the stack and only stored it in D register"
POP_TO_D_REGISTER = '@SP' + '\n' + \
                    'M=M-1' + '\n' + \
                    'A=M' + '\n' + \
                    'D=M' + '\n'

"this command pushes to the stack the value that its address is in D register"
PUSH_FROM_D_ADDRESS = 'A=D' + '\n' + \
               'D=M' +'\n' \
                '@SP' + '\n' + \
                'A=M' + '\n' + \
                'M=D' + '\n' + \
                '@SP' +'\n' + \
                'M=M+1' + '\n'

"this command pushes to the stack the value stored in D"
PUSH_FROM_D_VALUE = '@SP' + '\n' + \
                  'A=M' + '\n' + \
                  'M=D' + '\n' + \
                  '@SP' +'\n' + \
                  'M=M+1' + '\n'

SUB_ARITHMETIC = '@SP' + '\n' + \
           'AM=M-1' + '\n' + \
           'D=M' + '\n' + \
           '@SP' + '\n' + \
           'M=M-1' + '\n' + \
           'A=M' + '\n' + \
           'D=M-D' + '\n' + \
           'M=D' + '\n' + \
            '@SP' + '\n' + \
            'M=M+1' + '\n'

output_file = None # global variable
boolean_counter = 0 # this is a counter for the commands of the boolean operations. this is in order to create different
                    # rom spots so that each jump that is used in the operation will be local
number_of_calls_for_current_function_counter = 0
current_file_name = '' # the name of the current vm file who is translated to assembly and being written to the output
                       # file. the main reason for this is the names of the function calls and returns, who are
                       # involving the file name as part of the program convention
current_function_name = '' # initial name
output_asm_name = ''


def set_file_name(current_vm_file_name):
    """
    this function will set the current vm file name that is being translated to the relevant global variable
    :param current_vm_file_name: the vm file that is being translated
    """
    global current_file_name
    current_file_name = current_vm_file_name


def write_all_commands(commands_list,output_file_object):
    """
    receives a list of commands objects and writes the equivelent hack command to the file in the order of the
    list
    :param commands_list:
    :param output_file_object:
    :return:
    """
    global output_file
    global output_asm_name
    output_file = output_file_object
    output_asm_name = os.path.basename(output_file_object.name).replace('.vm','')
    for command in commands_list:
        # first for each command, write the original command in the vm code
        text_to_write = '//' + command.original_command_line + '\n'
        output_file.write(text_to_write)
        if command.get_command_type() == Commands.C_ARITHMETIC:
            write_aritmetic(command)
        elif command.get_command_type() == Commands.C_POP or command.get_command_type() == Commands.C_PUSH:
            write_push_pop(command)
        elif command.get_command_type() == Commands.C_LABEL:
            write_label(command)
        elif command.get_command_type() == Commands.C_GOTO:
            write_goto(command)
        elif command.get_command_type() == Commands.C_IF:
            write_if(command)
        elif command.get_command_type() == Commands.C_CALL:
            write_call(command)
        elif command.get_command_type() == Commands.C_FUNCTION:
            write_function(command)
        elif command.get_command_type() == Commands.C_RETURN:
            write_return()
        output_file.write('\n')
    return


def write_aritmetic(arithmetic_command):
    """
    this function will be called for each arithmetic command, will map it's kind and will write the hack " \
    command accordingly
    :param arithmetic_command: the command to translate to asm
    """
    name = arithmetic_command.get_arg_1()
    if name == 'add':
        write_add_aritmetic()
    elif name == 'sub':
        write_sub_aritmetic()
    elif name == 'neg':
        write_neg_aritmetic()
    elif name == 'eq':
        write_eq_arithmetic()
    elif name == 'gt':
        write_gt_arithmetic()
    elif name == 'lt':
        write_lt_arithmetic()
    elif name == 'and':
        write_and_arithmetic()
    elif name == 'or':
        write_or_arithmetic()
    elif name == 'not':
        write_not_arithmetic()


def write_add_aritmetic():
    text = '@SP' + '\n' + \
           'AM=M-1' + '\n' + \
           'D=M' + '\n' + \
           '@SP' + '\n' + \
           'M=M-1' + '\n'+ \
           'A=M' + '\n' + \
           'D=D+M' + '\n' + \
           'M=D' + '\n' + \
           '@SP' + '\n' + \
           'M=M+1' + '\n'
    output_file.write(text)


def write_sub_aritmetic():
    """
    for the command 'sub'
    """
    text = SUB_ARITHMETIC
    output_file.write(text)


def write_neg_aritmetic():
    """
    for the command 'neg'
    """
    text = POP_TO_D_REGISTER + \
        'D=-D' + '\n' + \
           PUSH_FROM_D_VALUE
    output_file.write(text)


def write_eq_arithmetic():
    """
    for the command 'eq'
    """
    global boolean_counter
    boolean_counter += 1
    text = POP_TO_D_REGISTER + \
           '@R13' + '\n' + \
           'M=D' + '\n' + \
           POP_TO_D_REGISTER +\
           '@R14' + '\n' +\
           'M=D' + '\n' +\
           '@R13' + '\n' +\
           'D=M' + '\n' + \
           '@SEC_IS_POSITIVE.' +str(boolean_counter) + '\n' + \
           'D;JGT' + '\n'+\
           '@R14' + '\n' + \
            'D=M' + '\n' + \
           '@DIFFERENT.'+ str(boolean_counter)+ '\n' +\
           'D;JGT' + '\n' +\
           '@REGULAR.' + str(boolean_counter) + '\n' +\
           '0;JMP' + '\n' +\
           '(SEC_IS_POSITIVE.'+str(boolean_counter) + ')' + '\n' +\
           '@R14' + '\n' + \
            'D=M' + '\n' +\
           '@DIFFERENT.'+str(boolean_counter) + '\n' +\
           'D;JLT' + '\n' +\
           '@REGULAR.'+str(boolean_counter) + '\n' +\
           '0;JMP' + '\n' +\
           '(DIFFERENT.'+str(boolean_counter)+')'+ '\n' +\
           'D=0' +'\n' + PUSH_FROM_D_VALUE  +\
           '@OUT_eq.' +str(boolean_counter) + '\n' +\
           '0;JMP'+ '\n' +\
           '(REGULAR.' +str(boolean_counter) + ')' + '\n' +\
           '@R14' + '\n' +\
           'D=M' + '\n' +\
           '@R13' + '\n' +\
           'D=D-M' + '\n' + \
           '@EQUAL.'+str(boolean_counter) + '\n' + \
           'D;JEQ' + '\n' + \
           'D=0' + '\n' + \
           PUSH_FROM_D_VALUE + \
            '@OUT_eq.'+str(boolean_counter) + '\n' + \
            '0;JMP' + '\n' +\
           '('+'EQUAL.'+str(boolean_counter)+')' + '\n' + \
           'D=-1' + '\n' +\
           PUSH_FROM_D_VALUE +\
           '('+'OUT_eq.'+str(boolean_counter)+')' + '\n'
    output_file.write(text)


def write_gt_arithmetic():
    """
    for the command 'gt'
    """
    global boolean_counter
    boolean_counter += 1
    text = POP_TO_D_REGISTER + \
           '@R13' + '\n' + \
           'M=D' + '\n' + \
           POP_TO_D_REGISTER + \
           '@R14' + '\n' + \
           'M=D' + '\n' + \
           '@R13' + '\n' + \
           'D=M' + '\n' + \
           '@SEC_IS_POSITIVE.' + str(boolean_counter) + '\n' + \
           'D;JGT' + '\n' + \
           '@R14' + '\n' + \
           'D=M' + '\n' + \
           '@SEC_IS_NEG_FIRST_POS.' + str(boolean_counter) + '\n' + \
           'D;JGT' + '\n' + \
           '@REGULAR.' + str(boolean_counter) + '\n' + \
           '0;JMP' + '\n' + \
           '(SEC_IS_POSITIVE.' + str(boolean_counter) + ')' + '\n' + \
           '@R14' + '\n' + \
           'D=M' + '\n' + \
           '@SEC_IS_POS_FIRST_NEG.' + str(boolean_counter) + '\n' + \
           'D;JLT' + '\n' +\
           '@REGULAR.' + str(boolean_counter) + '\n' +\
           '0;JMP' + '\n' +\
           '(SEC_IS_NEG_FIRST_POS.' + str(boolean_counter) + ')' + '\n'+ \
           'D=-1' + '\n' +\
           PUSH_FROM_D_VALUE +\
           '@OUT_gt.' + str(boolean_counter) + '\n' +\
           '0;JMP' + '\n' +\
           '(SEC_IS_POS_FIRST_NEG.' + str(boolean_counter) + ')' + '\n' +\
           'D=0' + '\n' +\
           PUSH_FROM_D_VALUE + \
           '@OUT_gt.' + str(boolean_counter) + '\n' +\
           '0;JMP' + '\n' \
           '(REGULAR.' + str(boolean_counter) + ')' + '\n' +\
           '@R14' + '\n' + \
           'D=M' + '\n' + \
           '@R13' + '\n' + \
           'D=D-M' + '\n' + \
           '@TRUE.' + str(boolean_counter) + '\n' + \
           'D;JGT' + '\n' + \
           'D=0' + '\n' + \
           PUSH_FROM_D_VALUE + \
           '@OUT_gt.' + str(boolean_counter) + '\n' + \
           '0;JMP' + '\n' + \
           '(' + 'TRUE.' + str(boolean_counter) + ')' + '\n' + \
           'D=-1' + '\n' + \
           PUSH_FROM_D_VALUE + \
           '(' + 'OUT_gt.' + str(boolean_counter) + ')' + '\n'
    output_file.write(text)


def write_lt_arithmetic():
    """
    for the command 'lt'
    """
    global boolean_counter
    boolean_counter += 1
    text = POP_TO_D_REGISTER + \
           '@R13' + '\n' + \
           'M=D' + '\n' + \
           POP_TO_D_REGISTER + \
           '@R14' + '\n' + \
           'M=D' + '\n' + \
           '@R13' + '\n' + \
           'D=M' + '\n' + \
           '@SEC_IS_POSITIVE.' + str(boolean_counter) + '\n' + \
           'D;JGT' + '\n' + \
           '@R14' + '\n' + \
           'D=M' + '\n' + \
           '@SEC_IS_NEG_FIRST_POS.' + str(boolean_counter) + '\n' + \
           'D;JGT' + '\n' + \
           '@REGULAR.' + str(boolean_counter) + '\n' + \
           '0;JMP' + '\n' + \
           '(SEC_IS_POSITIVE.' + str(boolean_counter) + ')' + '\n' + \
           '@R14' + '\n' + \
           'D=M' + '\n' + \
           '@SEC_IS_POS_FIRST_NEG.' + str(boolean_counter) + '\n' + \
           'D;JLT' + '\n' + \
           '@REGULAR.' + str(boolean_counter) + '\n' + \
           '0;JMP' + '\n' + \
           '(SEC_IS_NEG_FIRST_POS.' + str(boolean_counter) + ')' + '\n' + \
           'D=0' + '\n' + \
           PUSH_FROM_D_VALUE + \
           '@OUT_lt.' + str(boolean_counter) + '\n' + \
           '0;JMP' + '\n' + \
           '(SEC_IS_POS_FIRST_NEG.' + str(boolean_counter) + ')' + '\n' + \
           'D=-1' + '\n' + \
           PUSH_FROM_D_VALUE + \
           '@OUT_lt.' + str(boolean_counter) + '\n' + \
           '0;JMP' + '\n' \
           '(REGULAR.' + str(boolean_counter) + ')' + '\n' + \
           '@R14' + '\n' + \
           'D=M' + '\n' + \
           '@R13' + '\n' + \
           'D=D-M' + '\n' + \
           '@TRUE.' + str(boolean_counter) + '\n' + \
           'D;JLT' + '\n' + \
           'D=0' + '\n' + \
           PUSH_FROM_D_VALUE + \
           '@OUT_lt.' + str(boolean_counter) + '\n' + \
           '0;JMP' + '\n' + \
           '(' + 'TRUE.' + str(boolean_counter) + ')' + '\n' + \
           'D=-1' + '\n' + \
           PUSH_FROM_D_VALUE + \
           '(' + 'OUT_lt.' + str(boolean_counter) + ')' + '\n'
    output_file.write(text)


def write_and_arithmetic():
    """
    for the command 'and'
    """
    text = POP_TO_D_REGISTER + \
        '@R13' + '\n' + \
        'M=D' + '\n' + \
           POP_TO_D_REGISTER + \
        '@R13' + '\n' + \
        'D=D&M' + '\n' + \
           PUSH_FROM_D_VALUE
    output_file.write(text)


def write_or_arithmetic():
    """
    for the command 'or'
    """
    text = POP_TO_D_REGISTER + \
           '@R13' + '\n' + \
           'M=D' + '\n' + \
           POP_TO_D_REGISTER + \
           '@R13' + '\n' + \
           'D=D|M' + '\n' + \
           PUSH_FROM_D_VALUE
    output_file.write(text)


def write_not_arithmetic():
    """
    for the command 'not'
    """
    text = POP_TO_D_REGISTER + \
           'D=!D' + '\n' + \
           PUSH_FROM_D_VALUE
    output_file.write(text)


def write_push_pop(push_pop_command):
    """
    will write the push or pop command according to the segment
    :param push_pop_command: the vm command object to write
    """
    segment_point = ''  # this is the name of the ram variable who refers to the segment base address
    if push_pop_command.get_arg_1() == 'local':
        segment_point = 'LCL'
    elif push_pop_command.get_arg_1() == 'argument':
        segment_point = 'ARG'
    elif push_pop_command.get_arg_1() == 'this':
        segment_point = 'THIS'
    elif push_pop_command.get_arg_1() == 'that':
        segment_point = 'THAT'
    push_pop_command.set_seg_point(segment_point)
    # writing push or pop kind of commands, according to the type
    command_name = push_pop_command.get_command_type()
    if command_name == Commands.C_PUSH:
        write_push(push_pop_command)
    elif command_name == Commands.C_POP:
        write_pop(push_pop_command)


def write_push(command):
    """
    mapping to the specific push command
    :param command: the push command
    """
    segment = command.get_arg_1()
    if segment in FIRST_TYPE_SEGMENTS :
        write_push_for_simple_segment(command)
    elif segment == 'constant':
        write_push_for_const_segment(command)
    elif segment == 'static':
        write_push_for_static_segment(command)
    elif segment == 'pointer':
        write_push_for_pointer_segment(command)


def write_pop(command):
    """
    mapping to the specific pop command
    :param command: the pop command
    """
    segment = command.get_arg_1()
    if segment in FIRST_TYPE_SEGMENTS:
        write_pop_for_simple_segment(command)
    elif segment == 'static':
        write_pop_for_static_segment(command)
    elif segment == 'pointer':
        write_pop_for_pointer_segment(command)


def write_label(command):
    text = '(' + current_function_name + '$' + command.get_arg_1() + ')' + '\n'
    output_file.write(text)


def write_goto(command):
    text = '@' + current_function_name + '$' + command.get_arg_1() + '\n' + \
           '0;JMP' + '\n'
    output_file.write(text)


def write_if(command):
    text = POP_TO_D_REGISTER + \
           '@' + current_function_name + '$' + command.get_arg_1() + '\n' + \
           'D;JNE' + '\n' # equality to 0 is true by all the boolean operations
    output_file.write(text)


def write_function(command):
    global current_function_name
    current_function_name = command.get_arg_1()  # setting the current function who is being executed
    global number_of_calls_for_current_function_counter
    number_of_calls_for_current_function_counter = 0
    text = '(' + current_function_name + ')' + '\n' + \
           'D=0' + '\n'
    for i in range(command.get_arg_2()):
        # repeating as function of the number of local variables
        text += PUSH_FROM_D_VALUE
    output_file.write(text)


def write_call(command):
    global number_of_calls_for_current_function_counter
    number_of_calls_for_current_function_counter +=1
    num_of_called_function_arguments = command.get_arg_2()
    return_address_name = current_function_name + '$' + 'ret.' + str(number_of_calls_for_current_function_counter)
    text = '@' + return_address_name + '\n' + \
           'D=A' + '\n' + \
           PUSH_FROM_D_VALUE + \
           '@LCL' + '\n' + \
           'D=M' + '\n' + \
           PUSH_FROM_D_VALUE + \
           '@ARG' + '\n' + \
           'D=M' + '\n' + \
           PUSH_FROM_D_VALUE + \
           '@THIS' + '\n' + \
           'D=M' + '\n' + \
           PUSH_FROM_D_VALUE + \
           '@THAT' + '\n' + \
           'D=M' + '\n' + \
           PUSH_FROM_D_VALUE # pushing to the stack the current function state to remember
    text += '@SP' + '\n' + \
            'D=M' + '\n' + \
            PUSH_FROM_D_VALUE + \
            '@R5' + '\n' + \
            'D=A' + '\n' + \
            PUSH_FROM_D_VALUE + \
            SUB_ARITHMETIC + \
            '@' + str(num_of_called_function_arguments) + '\n' + \
            'D=A' + '\n' + \
            PUSH_FROM_D_VALUE + \
            SUB_ARITHMETIC + \
            POP_TO_D_REGISTER + \
            '@ARG' + '\n' + \
            'M=D' + '\n' # calculating the called function argument address and setting arg
    text += '@SP' + '\n' + \
            'D=M' + '\n' + \
            '@LCL' + '\n' + \
            'M=D' + '\n' + \
            '@' + command.get_arg_1() + '\n' + \
            '0;JMP' + '\n' + \
            '(' + return_address_name + ')' + '\n' # final line is the label to return to after the calling is over
    output_file.write(text)


def write_return():
    # before going back, should restore all the reserved values, and then erazing the stack of the called function
    text = '@LCL' + '\n' + \
           'D=M' + '\n' + \
           '@R14' + '\n' + \
           'M=D' + '\n' + \
           PUSH_FROM_D_VALUE + \
           '@R5' + '\n' + \
           'D=A' + '\n' + \
           PUSH_FROM_D_VALUE + \
           SUB_ARITHMETIC + \
           POP_TO_D_REGISTER + \
           'A=D' + '\n' + \
           'D=M' + '\n' + \
           '@R15' + '\n' + \
           'M=D' + '\n' + \
           POP_TO_D_REGISTER + \
           '@ARG' + '\n' + \
           'A=M' + '\n' + \
           'M=D' + '\n' + \
           '@ARG' + '\n' + \
           'D=M' + '\n' + \
           '@SP' + '\n' + \
           'M=D+1' + '\n' # setting the end frame and the return address as temp variables. last line will put the stack
                          # pointer in the first argument location
    # creating a loop in order to set all the segments
    text_parameters = ['@R1', '@THAT', '@R2' , '@THIS',  '@R3', '@ARG', '@R4', '@LCL']
    i = 0
    while i < 8:
        text += '@LCL' + '\n' + \
                'D=M' + '\n' + \
                text_parameters[i] + '\n' + \
                'D=A' + '\n' + \
                '@R14' + '\n'+\
                'M=D' + '\n'+\
                '@LCL' + '\n' + \
                'D=M' + '\n' + \
                '@R14' + '\n' + \
                'M=D-M' + '\n' + \
                '@R14' + '\n' + \
                'A=M' + '\n' +\
                'D=M' + '\n' +\
                text_parameters[i + 1] + '\n' + \
                'M=D' + '\n'
        i += 2
    text += '@R15'+ '\n' + \
            'A=M' + '\n' + \
            '0;JMP' + '\n' # jumping to the return address, after clearing the stack and restoring
    output_file.write(text)


def write_push_for_simple_segment(command):
    """
    for the command 'push segment i', while segment is one of the list above
    :param command
    """
    i = command.get_arg_2()  # second argument is an int describing the place on the segment we would like to pop to
    if command.get_arg_1() != "temp": # in case it's not temp, the address will be set by the segment
        text_to_write = '@' + str(i) + '\n' + \
                     'D=A' + '\n' + \
                     '@' + command.segment_point + '\n' + \
                     'D=M+D' + '\n'
    else: # in case it's temp, the address will be constant
        text_to_write = '@' + str(i) + '\n' + \
                     'D=A' + '\n' + \
                     '@R5' + '\n' + \
                     'D=A+D' + '\n'
    text_to_write += PUSH_FROM_D_ADDRESS
    output_file.write(text_to_write)


def write_pop_for_simple_segment(command):
    """
    for the command 'pop segment i', while segment is one of the list above
    :param command
    :return:
    """
    i = command.get_arg_2() # second argument is an int describing the place on the segment we wold like to pop to

    if command.get_arg_1() != "temp": # in case it's not temp, the address will be set by the segment
        text_to_write = '@' + str(i) + '\n' + \
                     'D=A' + '\n' + \
                     '@' + command.segment_point + '\n' + \
                     'D=M+D' + '\n'
    else: # in case it's temp, the address will be constant
        text_to_write = '@' + str(i) + '\n' + \
                     'D=A' + '\n' + \
                     '@R5' + '\n' + \
                     'D=A+D' + '\n'

    text_to_write += POP_TO_D_ADDRESS
    output_file.write(text_to_write)


def write_push_for_const_segment(command):
    """
    for the command 'push constant i'
    :param command
    """
    i = command.get_arg_2()  # second argument is an int describing the place on the segment we wold like to pop to
    text_to_write = '@' + str(i) + '\n' + \
                     'D=A' + '\n' + \
                    '@SP' + '\n' + \
                    'A=M' + '\n' + \
                    'M=D' + '\n'\
                    '@SP' +'\n' + \
                    'M=M+1' + '\n'
    output_file.write(text_to_write)


def write_pop_for_static_segment(command):
    i = command.get_arg_2()
    # current_file = current_function_name.split('.')[0]
    text_to_write = POP_TO_D_REGISTER + \
                    '@' + current_file_name + '.' + str(i) + '\n' + \
                    'M=D' + '\n'
    output_file.write(text_to_write)


def write_push_for_static_segment(command):
    """
    for the command 'push static i'
    :param command:
    """
    i = command.get_arg_2()
    # current_file = current_function_name.split('.')[0]
    text_to_write = '@' + current_file_name + '.' + str(i) + '\n' + \
                    'D=M' + '\n' + \
                    PUSH_FROM_D_VALUE
    output_file.write(text_to_write)


def write_push_for_pointer_segment(command):
    """
    for the command 'push pointer i'
    :param command:
    """
    i = command.get_arg_2()
    D_register_value = ''
    if i == 0:
        D_register_value = '@THIS' + '\n'
    elif i==1:
        D_register_value = '@THAT' + '\n'
    text_to_write = D_register_value + 'D=M' +'\n' + PUSH_FROM_D_VALUE
    output_file.write(text_to_write)


def write_pop_for_pointer_segment(command):
    """
    for the command 'pop pointer i'
    :param command:
    """
    i = command.get_arg_2()
    D_register_value = ''
    if i == 0:
        D_register_value = '@THIS' + '\n'
    elif i == 1:
        D_register_value = '@THAT' + '\n'
    text_to_write = D_register_value + 'D=A' + '\n' + POP_TO_D_ADDRESS
    output_file.write(text_to_write)