from Parser import Parser
import Code_Writer
import sys
import os


def main(argv):
    """
    this main method will create a new parser object, and will run the functions in order to: pars the commands," \
    and write the commands to the output file
    :param argv:
    :return:
    """
    file_or_directory_to_process = argv[0]
    file_or_directory_to_process = str(file_or_directory_to_process)
    # getting the full path
    path = os.path.normcase(os.path.join(os.path.dirname(__file__), file_or_directory_to_process))
    if os.path.isdir(file_or_directory_to_process) == False:
        input_file_name = os.path.basename(path).replace('.vm', '')
        only_path = os.path.dirname(path)
        output_file_name = os.path.join(only_path, str(input_file_name) + ".asm")
        object_file = open(path)
        output_object_file = open(output_file_name,'w')
        process_one_file(object_file, True,output_object_file)
    else:
        name = os.path.basename(path)
        all_files = os.listdir(file_or_directory_to_process)
        is_first = True
        with open(os.path.join(path, name + '.asm'), 'w') as output_file:
            for file in all_files:
                list_of_file = file.split('.')
                size_of_list = len(list_of_file)
                suffix = list_of_file[size_of_list-1]
                if suffix == 'vm' or suffix == 'VM':
                    file_object = open(os.path.join(file_or_directory_to_process,file))
                    process_one_file(file_object, is_first,output_file)
                    is_first = False # after the first time, not the first file anymore

def process_one_file(file_to_process,is_first_file, output_file_object):
    """
    this function will process one vm file into an xml file
    :param file_to_process: the input file object
    :param is_first_file: boolean if it's the first
    :param output_file_object: the output file object to write to
    :return:
    """
    name = os.path.basename(file_to_process.name).replace('.vm', '')
    Code_Writer.set_file_name(name)
    parser = Parser(file_to_process)
    if is_first_file:
        parser.parse_first_call()  # as part of booting of the program, first call sys_init
    parser.parse_all_commands()  # add all the other commands
    if is_first_file:
        Code_Writer.write_init(output_file_object)

    Code_Writer.write_all_commands(parser.program_commands,output_file_object)

if __name__ == "__main__":
    if len(sys.argv)<2:
        main([os.getcwd()])
    else:
        main(sys.argv[1:])