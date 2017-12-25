import Parser
import SymbolTable
import Code
import sys
import os

def main(argv):
    """
    main function of the program. will take the directory and read all the asm files, and translate it to hack
    :param argv: command line argument - the directory to translate
    """
    file_or_directory_to_process = argv[0]
    file_or_directory_to_process = str(file_or_directory_to_process)
    path =  os.path.normcase(os.path.join(os.path.dirname(__file__), file_or_directory_to_process)) # getting the full
                                                                                                    #  path

    if os.path.isdir(path) == False : # in case it's not a directory
        input_file_name = os.path.basename(path).replace('.asm','')
        only_path = os.path.dirname(path)
        output_file_name = os.path.join(only_path,str(input_file_name) + ".hack")
        SymbolTable.initialize_symbol_table()
        SymbolTable.first_pass(file_or_directory_to_process)
        final_parse_for_asm_file(path,output_file_name)
    else:
        # in case it's a directory, we want to loop all the asm files
        all_files = os.listdir(path)
        for file in all_files:
            list_of_file = file.split('.')
            size_of_list = len(list_of_file)
            suffix = list_of_file[size_of_list - 1]
            if suffix == 'asm':
                name_of_file = file.replace('.asm', '')
                output_file_name = os.path.join(path,str(name_of_file) + ".hack")
                SymbolTable.initialize_symbol_table()
                SymbolTable.first_pass(os.path.join(path,file))
                final_parse_for_asm_file(os.path.join(path,file),output_file_name)

def final_parse_for_asm_file(file_name, output_file_name):
    """
    this function will parse all the relevant lines and will write their hinary code to the output file
    :param file_name: the full path of the file to read
    :param output_file_name: the full path of the output file
    """
    with open(output_file_name,'w') as output_file, open(file_name,'r') as file_to_iterate:
        for line in file_to_iterate:
            clean_line = line.replace(' ', '')
            instruction = Parser.parse_text_line(clean_line)
            if instruction != None: # in case it's not none, there is an instruction to translate
                binary_instruction = Code.translate_instruction_to_binary(instruction)
                output_file.write(binary_instruction + '\n')

if __name__ == "__main__":
    main(sys.argv[1:])