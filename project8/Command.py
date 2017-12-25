
"a class to hold the commands objects. can hol all sort of commands, including future commands"
class Command:
    original_command_line = ''
    command_type = ''
    arg1 = ''
    arg2 = None # its to seperate cases when we don't have a second argument
    segment_point = '' # it's the name of the segment in case of one of the four initial segments

    def __init__(self, original_line, command_type, arg1, arg2):
        self.original_command_line = original_line
        self.command_type = command_type
        self.arg1 = arg1
        self.arg2 = arg2

    def get_command_type(self):
        return self.command_type

    def get_arg_1(self):
        return self.arg1

    def get_arg_2(self):
        return self.arg2

    def set_seg_point(self,segment_point_name):
        self.segment_point = segment_point_name


