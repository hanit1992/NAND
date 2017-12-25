import SymbolTable

"""
holds A instruction objects.
"""
class InstructionA:
    symbol_string = ''
    val = 0

    """
    recognize if it's a value or a sumbol and updates the val accordingly. the instruction holds
    the int val at the end, no matter if it was a symbol or not
    """
    def __init__(self, full_a_instruction):
        val = full_a_instruction.replace('@',"")
        if val.isdigit():
            self.val = val
        else:
            self.symbol_string = val
            SymbolTable.update_table_and_switch_symbol(self)

    def get_symbol_string(self):
        return self.symbol_string

    def get_val(self):
        return self.val

    def set_val(self,new_val):
        self.val = new_val