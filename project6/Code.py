from InstructionA import InstructionA

addition = '' # this is the string of the initial addition in the c instruction

# this is the dictionary that contains all the binary coding of the comp part of the instruction
comp_dict = {'0':'0101010', '1':'0111111', '-1':'0111010', 'D':'0001100', 'A':'0110000', '!D':'0001101', '!A':'0110001',
             '-D':'0001111', '-A':'0110011', 'D+1':'0011111', 'A+1':'0110111', 'D-1':'0001110', 'A-1':'0110010',
             'D+A':'0000010', 'D-A':'0010011', 'A-D':'0000111','D&A':'0000000','D|A':'0010101', 'M':'1110000',
             '!M':'1110001','-M':'1110011','M+1':'1110111','M-1':'1110010','D+M':'1000010','D-M':'1010011',
             'M-D':'1000111','D&M':'1000000','D|M':'1010101', 'D<<':'0110000', 'A<<':'0100000', 'M<<':'1100000',
             'D>>':'0010000', 'A>>':'0000000', 'M>>':'1000000' }
"""
this function will take an instruction without any symbols, and will translate it to binary form.
will return the 16 bit binary string
"""
def translate_instruction_to_binary(symbol_less_instruction):
    """
    will map the instruction between the c instruction or the a instruction
    :param symbol_less_instruction: this is the instruction asm code to interpret
    :return:
    """
    if isinstance(symbol_less_instruction,InstructionA):
        op_code = '0'
        binary_string_to_return = format(int(symbol_less_instruction.get_val()),'b')
        zeros_addition = '0'*(15 -(binary_string_to_return.__len__()))
        return op_code + str(zeros_addition) + binary_string_to_return

    else: # it's a c instruction
        binary_string_to_return = translate_c_instruction(symbol_less_instruction)
        return binary_string_to_return


def translate_c_instruction(c_instruction):
    """
    this function will the a c instruction and will translate it to the binary form
    :param c_instruction: the instruction object to translate
    :return: the string of the instruction
    """
    op_code = '1'
    dest_binary = get_dest_binary(c_instruction.get_dest_string())
    comp_binary = get_comp_binary(c_instruction.get_comp_string())
    jump_binary = get_jump_binary(c_instruction.get_jump_string())

    return op_code + addition + comp_binary + dest_binary + jump_binary

def get_jump_binary(jump_part):
    """
    will calculate the jump binary code
    :param jump_part: the asm jump part of the instruction
    :return: the binary string of the jump part
    """
    binary_to_return = ''
    if jump_part == None:
        binary_to_return = '000'
    elif jump_part == 'JMP':
        binary_to_return = '111'
    elif jump_part == 'JGT':
        binary_to_return = '001'
    elif jump_part == 'JEQ':
        binary_to_return = '010'
    elif jump_part == 'JGE':
        binary_to_return = '011'
    elif jump_part == 'JLT':
        binary_to_return = '100'
    elif jump_part == 'JNE':
        binary_to_return = '101'
    elif jump_part == 'JLE':
        binary_to_return = '110'
    return binary_to_return


def get_dest_binary(dest_part):
    """
    getting the dect binary of the given dest part of the instruction
    :param dest_part: the asm part of the destination
    :return: the binary string of the instruction
    """
    left = '0'
    middle = '0'
    right = '0'
    if dest_part == None:
        return left + middle + right
    if dest_part.find('A')!=-1:
        left = '1'
    if dest_part.find('M')!=-1:
        right = '1'
    if dest_part.find('D')!=-1:
        middle = '1'
    return left + middle + right


def get_comp_binary(comp_part):
    """
    getting the comp part of the binary instruction
    :param comp_part: the asm part
    :return: the binary string of the comp instruction part
    """
    if comp_part == None:
        return comp_part
    if comp_part.find('<<') != -1 or comp_part.find('>>') != -1:
        # this is the shift case
        global addition
        addition = '01'

    else:
        # other cases
        addition = '11'

    return comp_dict[comp_part]