
LIST_OF_PRE_DEFINED_SYMBOLS = [("R" + str(i + 1), i + 1) for i in range(-1, 15)]+[("SCREEN",16384), ("KBD",24576),
                                ("SP",0), ("LCL",1), ("ARG",2), ("THIS",3), ("THAT",4)]

curr_ram_address = 16  # this is the initial value. curr ram address holds the lase address that was used by the program
assembler_symbolic_table = [] # the table of symbols of the program

"""
this function will set the pre defined hack symbols in the global table
"""
def initialize_symbol_table():
    for i in LIST_OF_PRE_DEFINED_SYMBOLS:
        assembler_symbolic_table.append(i)
    return

"""
this function will parse the file and will add to the table the labels and their values - aka the label string
name and the ROM instruction address it refers to
"""
def first_pass(symbolic_file):
    num_of_instructions = 0
    with open(symbolic_file) as file_to_iterate:
        for line in file_to_iterate:
            temp_clean_line = line.replace(' ', '')
            clean_line = temp_clean_line.replace('\n','')
            if clean_line != '' and clean_line[0] == '(':
                final_line = clean_line.split('//')[0]
                temp_label = final_line.replace('(','')
                label = temp_label.replace(')','')
                assembler_symbolic_table.append((label,num_of_instructions))
            elif clean_line != '' and clean_line[0] != '/':
                num_of_instructions += 1 # raise by 1 for each line who is an instruction
    return

"""
this function will get an instruction and will lookup the value in the table. if it was find - will change the 
instruction object to the non symbolic code, else - will add to the table and then change it
"""
def update_table_and_switch_symbol(a_instruction_object):
    current_symbol = a_instruction_object.get_symbol_string()
    global curr_ram_address
    item = [i for i in assembler_symbolic_table if i[0]==current_symbol]
    if item == []:
        assembler_symbolic_table.append((current_symbol,curr_ram_address))
        a_instruction_object.set_val(curr_ram_address)
        curr_ram_address+=1
    else:
        a_instruction_object.set_val(item[0][1])
    return
