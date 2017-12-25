# this file will take the input jack file and will run the program accordingly. this main supports linux enviroment
from Tokenizer import Tokenizer
from ComilationEngine import CompilationEngine
import sys
import os

def main(argv):
    """
    main function to run the program
    :param argv:
    :return:
    """
    file_or_directory_to_process = argv[0]
    file_or_directory_to_process = str(file_or_directory_to_process)
    path =  os.path.normcase(os.path.join(os.path.dirname(__file__), file_or_directory_to_process))

    if os.path.isdir(path) == False : #in case it's not a directory
        name_of_file = os.path.basename(path)
        path = os.path.dirname(path) # getting only the path
        start = name_of_file.replace('.jack', '')
        output_file_full_name = os.path.join(path,str(start) + ".xml") # the file with the final xml code
        input_file_full_name = os.path.join(path,str(name_of_file))
        from_single_jack_file_to_xml(input_file_full_name,output_file_full_name)

    else:
        all_files = os.listdir(path)
        for file in all_files:
            list_of_file = file.split('.')
            size_of_list = len(list_of_file)
            suffix = list_of_file[size_of_list - 1]
            if suffix == 'jack':
                name_of_file = file.replace('.jack', '')
                output_file_full_name = os.path.join(path,str(name_of_file) + ".xml")
                input_file_full_name =  os.path.join(path,str(file))
                from_single_jack_file_to_xml(input_file_full_name, output_file_full_name)


def from_single_jack_file_to_xml(file_name, output_file_name):
    """
    will create xml file from a given vm file
    :param file_name: the name of the file
    :param output_file_name: name of the file to write to(full path)
    """
    tokenizer = Tokenizer(file_name) # creating the tokenizer for the current file
    tokenizer.process_all()
    compilation_engine = CompilationEngine(tokenizer)
    compilation_engine.compileAll(output_file_name)
    return

if __name__ == "__main__":
    if len(sys.argv) < 2:
        main([os.getcwd()])
    else:
        main(sys.argv[1:])