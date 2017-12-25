from Parser import Parser
import Code_Writer
import sys
import os


def main(argv):
    """
    this main method will create a new parser object, and will run the functions in order to: pars the commands,
    and write the commands to the output file
    """
    file_or_directory_to_process = argv[0]
    file_or_directory_to_process = str(file_or_directory_to_process)
    # getting the full path
    path = os.path.normcase(os.path.join(os.path.dirname(__file__), file_or_directory_to_process))
    if os.path.isdir(file_or_directory_to_process) == False:
        input_file_name = os.path.basename(path).replace('.vm', '')
        only_path = os.path.dirname(path)
        output_file_name = os.path.join(only_path, str(input_file_name) + ".asm")
        input_file = open(path) # opening the input file
        output_file = open(output_file_name,'w')
        process_one_file(input_file,output_file)
    else:
        # in case it's not a file, but a directory
        name = os.path.basename(path)
        # getting a list of all the files
        all_files = os.listdir(file_or_directory_to_process)
        with open(os.path.join(path, name + '.asm'),'w') as output_file:
            for file in all_files:
                list_of_file = file.split('.')
                size_of_list = len(list_of_file)
                suffix = list_of_file[size_of_list-1]
                if suffix == 'vm' or suffix == 'VM':
                    file_object = open(os.path.join(file_or_directory_to_process,file)) # the file we wish to read
                    process_one_file(file_object,output_file)


def process_one_file(file_to_process,output_file_object):
    # creating the parser of the argument:
    name = os.path.basename(file_to_process.name).replace('.vm','')
    Code_Writer.set_file_name(name)
    parser = Parser(file_to_process)
    parser.parse_all_commands()  # add all the commands to the table
    # giving the code writer the commands objects to write
    Code_Writer.write_all_commands(parser.program_commands,output_file_object)

if __name__ == "__main__":
    main(sys.argv[1:])