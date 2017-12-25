STRING_CONST = "stringConstant"

class Token:
    """
    this class will represent a token
    """

    type = ''
    value = ''
    str = '' # string representation of the token

    def __init__(self,type,value):
        self.type = type
        self.value = value

        string_value = value
        if self.getType() == STRING_CONST:
            string_value = self.getValue().replace('"','')
        self.value = string_value
        self.str = "<"+self.type+">" + ' ' + string_value + ' ' + '</' + self.type + ">"


    def getValue(self):
        return self.value

    def getType(self):
        return self.type

    def getStr(self):
        return self.str
