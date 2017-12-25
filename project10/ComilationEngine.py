import xml.etree.cElementTree as ET
import Tokenizer

class CompilationEngine:
    """
    this class will hold a compilation engine for each jack file we want to compile, and create an xml
    """

    tokenizer_of_engine = ''
    current_token = ''
    current_token_index = 0
    class_xml_output_file = ''
    class_token = ET.Element("class")
    output_file_name = ''

    def __init__(self, tokenizer_object):
        self.tokenizer_of_engine = tokenizer_object
        self.current_token = self.tokenizer_of_engine.tokensTable[0] # putting in the table the first
        self.class_token.clear() # reseting the tree
        self.current_token_index = 0

    def compileClass(self,output_file_name):
        """
        takes the tokenizer's output and compile the class in the file.
        :return: if something is wrong - throw exception
        """
        self.output_file_name = output_file_name
        # 'class' component
        self.printKeyWordAndAdvance(self.class_token)

        # className component
        self.printIdentifierAndAdvance(self.class_token)

        # { symbol
        self.printSymbolAndAdvance(self.class_token)

        # checking for multiple class var declaration
        for i in range(self.current_token_index,len(self.tokenizer_of_engine.tokensTable)):
            # will run on maximum the remaining tokens. the idea is to keep calling the var declaration method
            # until it's not legal, and only than to check the functions (the order is agreed in advance)
            if self.compileClassVarDec(self.class_token):
                # if it's true, will continue. if not - will break
                continue
            else:
                break

        # checking for multiple sub routine declarations
        for i in range(self.current_token_index, len(self.tokenizer_of_engine.tokensTable)):
            if self.compileSubRoutineDec(self.class_token):
                continue
            else:
                break

        # } symbol
        self.printSymbolAndAdvance(self.class_token)
        # the function above returns after updating the relevant output name file with the xml content.
        return

    def printKeyWordAndAdvance(self,root):
        """
        will add son to the given root of a keyword token
        :param root: this is the root of this specific node. we are passing a tree element object
        :return: True if successful, False otherwise
        """
        keyword = ET.SubElement(root, "keyword")
        keyword.text = ' ' + self.current_token.getValue() + ' '  # prints the current token, which is a class
        self.current_token_index += 1
        if self.current_token_index == len(self.tokenizer_of_engine.tokensTable):
            return False
        self.current_token = self.tokenizer_of_engine.tokensTable[
            self.current_token_index]  # advancing the current token
        return True

    def printIdentifierAndAdvance(self,root):
        """
        this function will start to return and stop the recurssion
        :param root: father of the identifier in the tree
        :return:
        """
        identifier = ET.SubElement(root, "identifier")
        identifier.text = ' ' + self.current_token.getValue() + ' '  # prints the current token, which is a class
        self.current_token_index += 1
        if self.current_token_index == len(self.tokenizer_of_engine.tokensTable):
            CompilationEngine.terminateProgram(self.output_file_name,self.class_token)
            return
        self.current_token = self.tokenizer_of_engine.tokensTable[
            self.current_token_index]  # advancing the current token
        return

    def printSymbolAndAdvance(self,root):
        """
        a function to add to xml a symbol
        :param root: father to add the xml symbol to
        :return:
        """
        symbol = ET.SubElement(root, "symbol")
        symbol.text = ' ' + self.current_token.getValue() + ' '  # prints the current token, which is a class
        self.current_token_index += 1
        if self.current_token_index >= len(self.tokenizer_of_engine.tokensTable):
            CompilationEngine.terminateProgram(self.output_file_name, self.class_token)
            return
        self.current_token = self.tokenizer_of_engine.tokensTable[
            self.current_token_index]  # advancing the current token
        return

    def printIntConstantAndAdvance(self,root):
        """
        a function to add to xml a intConstant
        :param root:
        :return:
        """
        integerConstant = ET.SubElement(root, "integerConstant")
        integerConstant.text = ' ' + self.current_token.getValue() + ' '  # prints the current token, which is a class
        self.current_token_index += 1
        if self.current_token_index == len(self.tokenizer_of_engine.tokensTable):
            return False
        self.current_token = self.tokenizer_of_engine.tokensTable[
            self.current_token_index]  # advancing the current token
        return True

    def printStringConstantAndAdvance(self,root):
        """

        :param root:
        :return:
        """
        #TODO i made here some changes
        stringConstant = ET.SubElement(root, "stringConstant")
        if self.current_token.getValue() != "":
            # in case it's not empty
            stringConstant.text = ' ' + self.current_token.getValue() + ' ' # prints the current token, which is a class
        else:
            stringConstant.text = self.current_token.getValue()
        self.current_token_index += 1
        if self.current_token_index == len(self.tokenizer_of_engine.tokensTable):
            return False
        self.current_token = self.tokenizer_of_engine.tokensTable[
            self.current_token_index]  # advancing the current token
        return True


    def compileClassVarDec(self,root):
        """
        a function to compile class variable declaration
        should advance the end!
        :return: True if it was successfull, False otherwise
        """
        # checking if there are 'static' or 'field' keywords
        if self.current_token.getValue() != 'static' and self.current_token.getValue() != 'field':
            return False # we don't want to throw exception or to advance it, because there is a chance it's not var dec
        else:
            # only here we want to create the tree
            classVarDec = ET.SubElement(root, "classVarDec")  # first, initializing the sub tree class var
            self.printKeyWordAndAdvance(classVarDec)

        # type object
        if self.current_token.getType() == Tokenizer.IDENTIFIER:
            self.printIdentifierAndAdvance(classVarDec)
        else:
            self.printKeyWordAndAdvance(classVarDec)

        # first var name = which is an identifier
        self.printIdentifierAndAdvance(classVarDec)

        # checking for the other var names - not mandatory
        for i in range(self.current_token_index,len(self.tokenizer_of_engine.tokensTable)):
            if self.current_token.getValue() != ',':
                break
            else:
                self.printSymbolAndAdvance(classVarDec)
                self.printIdentifierAndAdvance(classVarDec)
                continue

        # the ';' symbol
        self.printSymbolAndAdvance(classVarDec)
        return True # i added another declaration

    def compileSubRoutineDec(self,root):
        """
        should advance the end!
        a function to compile subroutine declaration
        :return: True if it was successfull, False otherwise
        """

        # checking for the requested initial keywords
        if self.current_token.getValue() not in ['constructor','function','method']:
            return False # it's false and not exception, because it doesn't have to be from the first place
        else:
            subroutineDec = ET.SubElement(root,"subroutineDec")
            self.printKeyWordAndAdvance(subroutineDec)

        # checking if it's a type or void next
        if self.current_token.getType() == Tokenizer.IDENTIFIER:
            self.printIdentifierAndAdvance(subroutineDec)
        else:
            self.printKeyWordAndAdvance(subroutineDec)

        # subroutine name = identifier
        self.printIdentifierAndAdvance(subroutineDec)

        # '('
        self.printSymbolAndAdvance(subroutineDec)

        # parameter list
        self.compileParameterList(subroutineDec)

        # ')'
        self.printSymbolAndAdvance(subroutineDec)

        # a legal body
        self.compileSubRoutineBody(subroutineDec)
        return True # means that it was good

    def compileParameterList(self,root):
        """
        should advance the current token
        a function to compile parameter list
        :param root: father of the created list token
        :return: True if there was a success, false otherwise
        """
        # we would like the following operations to appear one or zero times
        parameterList = ET.SubElement(root, "parameterList")  # first, initializing the sub tree parameter list
        if not self.isItATypeToken(): # if we don't have a token next, it's empty
            parameterList.text = '\n'
            return # in the case where there is nothing here, it's ok. still not an exception
        else:
            # in case we do have something here
            if self.current_token.getType() == Tokenizer.IDENTIFIER:
                self.printIdentifierAndAdvance(parameterList)
            else:
                self.printKeyWordAndAdvance(parameterList)

        # a following name
        self.printIdentifierAndAdvance(parameterList)

        # check for more - optional
        for i in range(self.current_token_index, len(self.tokenizer_of_engine.tokensTable)):
            if self.current_token.getValue() != ',':
                return True # we want to get out of the function
            else:
                # if there is a comma
                self.printSymbolAndAdvance(parameterList)

                # printing the type or class var
            if self.current_token.getType() == Tokenizer.IDENTIFIER:
                self.printIdentifierAndAdvance(parameterList)
            else:
                self.printKeyWordAndAdvance(parameterList)

            # a following name
            self.printIdentifierAndAdvance(parameterList)
        return True # after the loop - we can return

    def compileSubRoutineBody(self, root):
        """
        should advance the current token
        :param root:
        :return: True if there was a success, false otherwise
        """
        subroutineBody = ET.SubElement(root, "subroutineBody")

        # a '{' symbol
        self.printSymbolAndAdvance(subroutineBody)

        # check for varDeck
        for i in range(self.current_token_index, len(self.tokenizer_of_engine.tokensTable)):
            if self.compileVarDec(subroutineBody):
                continue
            else:
                break

        # check for statements
        self.compileStatements(subroutineBody)

        # a '}' symbol
        self.printSymbolAndAdvance(subroutineBody)
        return True

    def compileTerm(self,root):
        """
        this method will not advance if there wasn't a term
        :param root: father of created term
        :return: false if there is not a term, and true is there was
        """

        # we need to figure out what to print
        if self.current_token.getType() == Tokenizer.INT_CONST:
            term = ET.SubElement(root, "term")
            self.printIntConstantAndAdvance(term)
            return True
        if self.current_token.getType() == Tokenizer.STRING_CONST:
            term = ET.SubElement(root, "term")
            self.printStringConstantAndAdvance(term)
            return True
        if self.current_token.getValue() in ['true','false','null','this']:
            term = ET.SubElement(root, "term")
            self.printKeyWordAndAdvance(term)
            return True
        if self.current_token.getType() == Tokenizer.IDENTIFIER:
            term = ET.SubElement(root, "term")
            # two options. first print the common
            # lets look at the next value:
            next_token = self.tokenizer_of_engine.tokensTable[self.current_token_index+1]
            if next_token.getValue() == '[':
                # it's a list element
                self.printIdentifierAndAdvance(term)
                # the '['
                self.printSymbolAndAdvance(term)
                # the expression
                self.compileExpression(term)
                # the ']'
                self.printSymbolAndAdvance(term)
                return True
            if next_token.getValue() == '(' or next_token.getValue() == '.':
                # it's a subroutine call
                self.compileSubRoutineCallWithNoSubTree(term)
                return True
            else:
                # if not, it's a simple var name
                self.printIdentifierAndAdvance(term)
                return True
        if self.current_token.getValue() == '(':
            term = ET.SubElement(root, "term")
            # '('
            self.printSymbolAndAdvance(term)
            # expression
            self.compileExpression(term)
            # ')'
            self.printSymbolAndAdvance(term)
            return True
        if self.current_token.getValue() in ['-','~']:
            term = ET.SubElement(root, "term")
            # print symbol
            self.printSymbolAndAdvance(term)
            # term
            self.compileTerm(term) #recurssion
            return True
        return False # if nothing was found, there is no term


    def isItATypeToken(self):
        if self.current_token.getValue() not in ['int','char','boolean'] and\
                        self.current_token.getType() != Tokenizer.IDENTIFIER:
            return False
        return True


    def compileStatements(self,root):
        """
        a function to compile a statement
        :param root: father of the created statement
        :return:
        """
        statements = ET.SubElement(root, "statements")  # first, initializing the sub tree parameter list

        # getting zero or more statements
        index_when_entering_function = self.current_token_index
        for i in range(self.current_token_index, len(self.tokenizer_of_engine.tokensTable)):
            if self.current_token.getValue() not in ['let', 'if','while','do','return']:
                if i == index_when_entering_function:
                    statements.text = '\n'
                return # no statements, no advance
            else:
                if self.current_token.getValue() == 'let':
                    self.compileLetStatement(statements)
                elif self.current_token.getValue() == 'if':
                    self.compileIfStatement(statements)
                elif self.current_token.getValue() == 'while':
                    self.compileWhileStatement(statements)
                elif self.current_token.getValue() == 'do':
                    self.compileDoStatement(statements)
                elif self.current_token.getValue() == 'return':
                    self.compileReturnStatement(statements)

    def compileIfStatement(self,root):
        """
        a function to compile if statement
        :param root: father of the created statement
        :return:
        """
        ifStatement = ET.SubElement(root,"ifStatement")

        # check for 'if'
        self.printKeyWordAndAdvance(ifStatement)

        # check for '('
        self.printSymbolAndAdvance(ifStatement)

        # check for expression
        self.compileExpression(ifStatement)

        # check for ')'
        self.printSymbolAndAdvance(ifStatement)

        # check for '{'
        self.printSymbolAndAdvance(ifStatement)

        # check for statements
        self.compileStatements(ifStatement)

        # check for '}'
        self.printSymbolAndAdvance(ifStatement)

        # check for optional part
        if self.current_token.getValue() != 'else':
            return True # no else so we finished
        else:
            self.printKeyWordAndAdvance(ifStatement)

        # check for '{'
        self.printSymbolAndAdvance(ifStatement)

        # check for statements
        self.compileStatements(ifStatement)

        # check for '}'
        self.printSymbolAndAdvance(ifStatement)
        return True

    def compileLetStatement(self,root):
        """
        a function to compile let statement
        :param root: father of created statement
        :return:
        """
        letStatement = ET.SubElement(root,"letStatement")

        # check for 'let'
        self.printKeyWordAndAdvance(letStatement)

        # check for var name
        self.printIdentifierAndAdvance(letStatement)

        # optional part - check for '['
        if self.current_token.getValue() == '[':
            self.printSymbolAndAdvance(letStatement)

            # check for expression
            self.compileExpression(letStatement)

            # check for ']'
            if self.current_token.getValue() == ']':
                self.printSymbolAndAdvance(letStatement)

        # print '='
        self.printSymbolAndAdvance(letStatement)

        # check for expression
        self.compileExpression(letStatement)

        # check for ';'
        self.printSymbolAndAdvance(letStatement)
        return True

    def compileWhileStatement(self,root):
        """
        a function to compile while statement
        :param root: father of created statement
        :return:
        """
        whileStatement = ET.SubElement(root,"whileStatement")

        # check for 'while'
        self.printKeyWordAndAdvance(whileStatement)

        # check for '('
        self.printSymbolAndAdvance(whileStatement)

        # check for expression
        self.compileExpression(whileStatement)

        # check for ')'
        self.printSymbolAndAdvance(whileStatement)

        # check for '{'
        self.printSymbolAndAdvance(whileStatement)

        # check for statements
        self.compileStatements(whileStatement)

        # check for '}'
        self.printSymbolAndAdvance(whileStatement)
        return True

    def compileDoStatement(self,root):
        """
        a function to compile do statement
        :param root: father of created statment
        :return:
        """
        doStatement = ET.SubElement(root,"doStatement")

        # check for 'do'
        self.printKeyWordAndAdvance(doStatement)

        # check for subroutine call
        self.compileSubRoutineCallWithNoSubTree(doStatement)

        # check for ';'
        self.printSymbolAndAdvance(doStatement)
        return

    def compileSubRoutineCallWithNoSubTree(self,root):
        """
        a function to compile subroutine call
        :param root: father of the created call
        :return:
        """
        # checking for name = identifier
        self.printIdentifierAndAdvance(root)

        # checking for two options:
        # 1. a direct function call
        if self.current_token.getValue() == '(':
            # we are in the first optional case
            self.printSymbolAndAdvance(root)
            # check for expression list
            self.compileExpressionList(root)

            # ')'
            self.printSymbolAndAdvance(root)
            return True  # if we reached here, first case was successfull

        # checking the other option
        if self.current_token.getValue() == '.':
            self.printSymbolAndAdvance(root)

        # printing name = identifier
        self.printIdentifierAndAdvance(root)

        # checking for '('
        self.printSymbolAndAdvance(root)

        # check for expression list
        self.compileExpressionList(root)

        # checking for ')'
        self.printSymbolAndAdvance(root)
        return True

    def compileExpressionList(self,root):
        """
        a function to compile expression list
        :param root: father of the created list
        :return:
        """
        expressionList = ET.SubElement(root, "expressionList")
        if not self.compileExpression(expressionList):
            expressionList.text = '\n' # putting something default in the empty case
            return False # in this case we have nothing

        # in case we do, check for 0 or more times
        for i in range(self.current_token_index, len(self.tokenizer_of_engine.tokensTable)):
            if self.current_token.getValue() != ',':
                return True # the list is finished

            # printing ','
            self.printSymbolAndAdvance(expressionList)

            # printing expression
            self.compileExpression(expressionList)
            continue
        return True

    def compileReturnStatement(self,root):
        """
        a function to compile return statement
        :param root: father of the created statement
        :return:
        """
        returnStatement = ET.SubElement(root,"returnStatement")

        # 'return'
        self.printKeyWordAndAdvance(returnStatement)

        # check for optional expression
        if self.current_token.getValue() == ';':
            # in case it's a non expression option
            self.printSymbolAndAdvance(returnStatement)
            return True

        else:
            # check for expression
            self.compileExpression(returnStatement)

            # check for ';'
            self.printSymbolAndAdvance(returnStatement)
            return True

    def compileVarDec(self,root):
        """
        a function to compile variable declaration
        :param root: father of the created var dec
        :return: true for success, false otherwise
        """

        # 'var'
        if self.current_token.getValue() != 'var':
            return False # there is a case when we don't want to go on
        else:
            varDec = ET.SubElement(root, "varDec")  # first, initializing the sub tree parameter list
            self.printKeyWordAndAdvance(varDec)

        # type
        if self.current_token.getType() == Tokenizer.IDENTIFIER:
            self.printIdentifierAndAdvance(varDec)
        else:
            self.printKeyWordAndAdvance(varDec)

        # var name = identifier
        self.printIdentifierAndAdvance(varDec)

        # check for more
        for i in range(self.current_token_index, len(self.tokenizer_of_engine.tokensTable)):
            if self.current_token.getValue() != ',':
                break
            else:
                self.printSymbolAndAdvance(varDec)

                # print name = identifier
                self.printIdentifierAndAdvance(varDec)

        # check for ';' symbol
        self.printSymbolAndAdvance(varDec)
        return True

    def compileExpression(self,root):
        """
        a function to compile expression
        :param root: father of the created expression
        :return:
        """
        expression = ET.SubElement(root, "expression")

        # first, term
        if not self.compileTerm(expression):
            root.remove(expression)
            return False # we don't have an expression , will not advance if it's false


        # 0 or more times , op + term
        for i in range(self.current_token_index,len(self.tokenizer_of_engine.tokensTable)):
            if self.current_token.getValue() not in ['+','-','*','/','&','|','<','>','=']:
                break
            else:
                # printing the symbol
                self.printSymbolAndAdvance(expression)

                # printing the term
                self.compileTerm(expression)
                continue
        return True # finished


    # def isItATerm(self):
    #     return

    def compileAll(self, output_file):
        """
        :return:
        """
        self.compileClass(output_file)
        return

    @staticmethod
    def printingTheTreeNicely(elem, level=0):
        """
        will organize the tree so it will look like an ordered xml tree
        :param elem:
        :param level: level to create
        :return:
        """
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                CompilationEngine.printingTheTreeNicely(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i


    def terminateProgram(output_file_name, main_token):
        """
        this function will write the created tree - to an actuall xml file, in the given name - which
        is a full path directory
        :param main_token: this is the root of the tree
        :return:
        """
        # at the end, we will write all the class to the xml file
        CompilationEngine.printingTheTreeNicely(main_token)
        class_xml_output_file = ET.ElementTree(main_token)  # this is the xml root
        class_xml_output_file.write(output_file_name,short_empty_elements=False)
        return



