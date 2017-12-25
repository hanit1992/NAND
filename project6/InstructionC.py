"""
this class holds a c instruction object. it holds the different fields of the instruction and allows us to
easily change and translate the different parts to binary
"""
class InstructionC:
    jump_string = ''
    dest_string = ''
    comp_string = ''

    """
    using the parse function, will initialize a new c instruction object with the slitted parts,
     not in binary
    """
    def __init__(self,full_c_instruction):
        dest, jump, comp = self.parse_instruction(full_c_instruction)
        self.jump_string = jump
        self.comp_string = comp
        self.dest_string = dest

    """
    splits the instruction,and returning all the parts. if a part is not there, will be None
    """
    def parse_instruction(self, full_c_instruction):
        clean_full_instruction = full_c_instruction.replace(" ","") #this will replace all the whitespace
                                                                    #  with empty string, to get rid of them
        dest = None
        jump = None
        comp = None
        right_hand = None
        if clean_full_instruction.find('=') != -1:
            dest, right_hand = clean_full_instruction.split('=')
            if right_hand.find(';') != -1:
                comp,jump = right_hand.split(';')
            else: # right hand has no ;
                comp = right_hand
        else:
            # if there isn't a '=', there has to be ';' by the assumption of the language
            comp,jump = clean_full_instruction.split(';')

        return dest,jump,comp

    def get_jump_string(self):
        return self.jump_string

    def get_dest_string(self):
        return self.dest_string

    def get_comp_string(self):
        return self.comp_string