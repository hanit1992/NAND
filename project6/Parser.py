from InstructionA import InstructionA
from InstructionC import InstructionC

"""
this function will get a new line to parse, and will return the matched object - c instruction or a instruction.
in addition will also update the number of commands in the text
"""
def parse_text_line(new_line):
    first_char = new_line[0]
    instruction_object_to_return = None
    temp_clean_line = new_line.replace('\n','')

    if first_char == '(' or first_char == ' ' or first_char == "/" or temp_clean_line == '':
        # those are the cases when we ignore the line
        return instruction_object_to_return
    elif first_char == '@':
        clean_line = temp_clean_line.split('//')[0]
        instruction_object_to_return = InstructionA(clean_line)
    else:
        clean_line = temp_clean_line.split('//')[0]
        instruction_object_to_return = InstructionC(clean_line)
    return instruction_object_to_return

