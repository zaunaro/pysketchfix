import ast

import asttokens

from Config.ConfigReader import ConfigReader
from Schemas.TransformationManager import TransformationManager


class Statement(object):
    """
    Here the ast token library is used. You find the library https://github.com/gristlabs/asttokens
    Last Access: 11.09.2020. This is also a library which you need to install into your python interpreter. Here the
    information about code lines is used to generated transformations.
    """

    OPERATORS = ['And', 'Or', 'Mod', 'Eq', 'Sub', 'Mult', 'Not', 'Div', 'Add', 'Not', 'NotEq', 'Lt', 'LtE',
                 'BitAnd', 'GtE', 'Is', 'IsNot', 'In', 'NotIn', 'Pow', 'LShift', 'RShift', 'BitOr', 'BitXor',
                 'FloorDiv', 'Gt']

    @staticmethod
    def find_closer_variables_for_line(line):
        """
        This method is used for finding the closer variables in the given line. This is only used by the Closer
        Variables Finder.

        :param line: The line where the closer variables are searched in.
        :return: an array of closer variables. This could be empty if the line could not be parsed.
        :raise ParsingException: if the line could not be parsed by the ast tokens.
        """
        # Parse the tree with the asttokens library.
        closerVariables = []
        try:
            parsed_line = asttokens.ASTTokens(line, parse=True)
        except SyntaxError:
            return closerVariables
        # Now the children will be parsed.
        last_statement_type = ''
        for node in ast.walk(parsed_line.tree):
            # For every children of the tree get the code and the statement type.
            code = parsed_line.get_text(node)
            statement_type = node.__class__.__name__
            # If the statement type is not a load, store, module or expression (because if you would take them you
            # would have to many duplicates) it is skipped.
            if statement_type != 'Load' and statement_type != 'Store' and statement_type != 'Module' and \
                    statement_type != 'Expr':
                # Here only the variables are taken and no return variables because they are also duplicate in the code.
                if Statement.is_variable(statement_type) and not code.__contains__("return"):
                    # If the last statement type which is set is not call or name then the variable is appended to the
                    # array. This is also here done, because unless there were to many duplicates in the list.
                    if not (last_statement_type == 'Call' and statement_type == 'Name'):
                        closerVariables.append(code)
                last_statement_type = statement_type
        return closerVariables

    @staticmethod
    def parse_line_to_statement(line):
        """
        The line is parsed to a statement with the asttokens library. A tree is generated from them, which should
        determine the root statement. In this case Module and Expr are not needed so they were skipped and the third
        node is taken as root statement. Then for this root statement all children are stored with the ast library.
        After that the constructor of the statement is called the root statement is generated and returned.

        :param line: The line parameter is the line of code which should be parsed.
        :return: the root statement which is created. Could also be none if the ast token can not be parsed.
        :raises: A value error if the root node can not be found.
        """
        # If you want to look at the line which is parsed then you can print the tree of the line to the console.
        # Statement.print_tree(line)
        # Parse the tree with the asttokens library.
        try:
            parsed_line = asttokens.ASTTokens(line, parse=True)
        except SyntaxError:
            return None
        # Now the children will be parsed.
        root_node = None
        children = None
        for root_node in ast.walk(parsed_line.tree):
            # If the root node is no module and no expression then the child could be taken and stored.
            # Because if you take the children of the root node then module and expression would be in it and this
            # only would be duplicates later.
            if root_node.__class__.__name__ != 'Module' and root_node.__class__.__name__ != 'Expr':
                children = ast.iter_child_nodes(root_node)
                break
        # Set the root statement and return it. Here the tree is setup in the constructor.
        if root_node is None:
            raise ValueError('root node is none at line: ' + line)
        else:
            code = parsed_line.get_text(root_node)
            statement_type = root_node.__class__.__name__
            root_statement = Statement(statement_type, code, children, None, parsed_line)
            return root_statement

    @staticmethod
    def print_tree(line):
        """
        Parses the line and prints the whole tree which is parsed with asttokens library. This is only needed for debug
        reasons.

        :param line: The line parameter is the line of code which should be parsed.
        """
        # Parse the tree with the asttokens library.
        parsed_line = None
        try:
            parsed_line = asttokens.ASTTokens(line, parse=True)
        except SyntaxError:
            print("Tree could not be parsed.")
        # Now the children will be parsed.
        for node in ast.walk(parsed_line.tree):
            # For every child the transformation type and the code is printed.
            print('-------Parent-------')
            print('TransformationType:' + node.__class__.__name__)
            print('Code:' + parsed_line.get_text(node))
            # And after that, all children are printed.
            print('-------Children:-------')
            children = ast.iter_child_nodes(node)
            for child in children:
                print('TransformationType:' + child.__class__.__name__)
                print('Code:' + parsed_line.get_text(child))

    @staticmethod
    def set_operator_by_statement_type(statement_type):
        """
        Sets the operator for statements where the child does not determine the operator. This is called by the
        Statement init method and returns the operator of the statement name in the AST Node Library.

        :param statement_type: The operator description of the current statement from the ast node library.
        :return: the real code operator to the name of the statement.
        """
        if statement_type == 'Raise':
            return 'raise'
        elif statement_type == 'Assign':
            return '='
        elif statement_type == 'AugAssign':
            return '='
        elif statement_type == 'Return':
            return 'return'
        elif statement_type == 'UnaryOp':
            return 'not'
        elif statement_type == 'Tuple':
            return ', '
        elif statement_type == 'Index':
            return 'Index'
        elif statement_type == 'Slice':
            return ':'
        else:
            return None

    @staticmethod
    def get_operator_by_node_child(node_child_statement_type, statement_type):
        """
        The ast library defines operators as they are named and give no real code of them. So this method cares about
        setting the operator of the statement as it is in the code.

        :param node_child_statement_type: The operator description of the child from the ast node library.
        :param statement_type: The operator description of the current statement from the ast node library.
        :return: the real code operator to the name of the statement.
        """
        if statement_type == 'BoolOp':
            if node_child_statement_type == 'And':
                return 'and'
            elif node_child_statement_type == 'Or':
                return 'or'
        if statement_type == 'UnaryOp':
            if node_child_statement_type == 'Not':
                return 'not'
        if statement_type == 'AugAssign':
            if node_child_statement_type == 'Sub':
                return '-='
            elif node_child_statement_type == 'Mult':
                return '*='
            elif node_child_statement_type == 'Div':
                return '/='
            elif node_child_statement_type == 'Mod':
                return '%='
            elif node_child_statement_type == 'Add':
                return '+='
            elif node_child_statement_type == 'Pow':
                return '**='
            elif node_child_statement_type == 'LShift':
                return '<<='
            elif node_child_statement_type == 'RShift':
                return '>>='
            elif node_child_statement_type == 'BitOr':
                return '|='
            elif node_child_statement_type == 'BitXor':
                return '^='
            elif node_child_statement_type == 'BitAnd':
                return '&='
            elif node_child_statement_type == 'FloorDiv':
                return '//='
        if statement_type == 'BinOp':
            if node_child_statement_type == 'Sub':
                return '-'
            elif node_child_statement_type == 'Mult':
                return '*'
            elif node_child_statement_type == 'Div':
                return '/'
            elif node_child_statement_type == 'Mod':
                return '%'
            elif node_child_statement_type == 'Add':
                return '+'
            elif node_child_statement_type == 'Pow':
                return '**'
            elif node_child_statement_type == 'LShift':
                return '<<'
            elif node_child_statement_type == 'RShift':
                return '>>'
            elif node_child_statement_type == 'BitOr':
                return '|'
            elif node_child_statement_type == 'BitXor':
                return '^'
            elif node_child_statement_type == 'BitAnd':
                return '&'
            elif node_child_statement_type == 'FloorDiv':
                return '//'
        if statement_type == 'Compare':
            if node_child_statement_type == 'Eq':
                return '=='
            elif node_child_statement_type == 'NotEq':
                return '!='
            elif node_child_statement_type == 'Lt':
                return '<'
            elif node_child_statement_type == 'LtE':
                return '<='
            elif node_child_statement_type == 'Gt':
                return '>'
            elif node_child_statement_type == 'GtE':
                return '>='
            elif node_child_statement_type == 'Is':
                return 'is'
            elif node_child_statement_type == 'IsNot':
                return 'is not'
            elif node_child_statement_type == 'In':
                return 'in'
            elif node_child_statement_type == 'NotIn':
                return 'not in'
        return None

    @staticmethod
    def is_operator_node_child(node_child_statement_type, statement_type):
        """
        The node child operator description is checked for a operation.

        :param node_child_statement_type: The node child operator description.
        :param statement_type: The operator description of the current statement from the ast node library.
        :return: True, if the node child is an operator.
        """
        if Statement.is_variable(statement_type):
            return False
        for operator in Statement.OPERATORS:
            if operator == node_child_statement_type:
                return True
        return False

    def __init__(self, statement_type, code, node_children, parent, parsed_line):
        """
        This creates a statement tree which starts at the root statement. Here for every child a Statement is created
        and appended to the children of his parent and so on. At the end a tree is created where every child has a
        current code, operator, parent, a transformation (which at first is the code itself) and children which
        are also have children. This is all done because the ast tokens library creates statements with no operators
        and to filter the operators, which are needed for transformation later. Many of the tree components are
        deleted or not taken in the tree. Here also is needed that children operators are based with the statement
        type of the parent operator.

        :param statement_type: is the type of code, e.g. a constant, a binary operation, etc
        :param code: which is currently evaluated
        :param node_children: the children of the ast library. These are not statements.
        :param parent: the parent of this statement.
        :param parsed_line: the line which is parsed by the ast library.
        """
        # The statement type which is set by the ast token library. So the type of code defined.
        self.statement_type = statement_type
        # The code of the current statement (this could be a variable, an operator with variables)
        self.code = code
        # The statement parent of the statement.
        self.parent = parent
        # The operator is needed for statements with children. Here the statement operator is for example +, -, ..
        # But also there are statement operators like raise or return. If the statement is a method call then the
        # operator is the name of the method.
        self.operator = None
        # The children of the statement.
        self.children = []
        # The transformation which is applied later (EXP, ARI..)
        self.transformation = code
        # First of all the operator of this transformation is set. This is the only the case at raise, return, assign or
        # unary operators. (Only if the operator is not determined in the children then None is returned.
        self.operator = Statement.set_operator_by_statement_type(statement_type)

        # Now the other children (if a Call statement type) or the children of the node is added as statement
        # children. First of all the operator of some nodes is defined as a node child in the tree. So to get the
        # operator of the operation the children must be at first checked if they are a operator child.
        if node_children is not None:
            for node_child in node_children:
                # Define the statement type and code of the children.
                node_child_statement_type = node_child.__class__.__name__
                node_child_code = parsed_line.get_text(node_child)

                # In this special case, if the statement type is call then, the operator is determined by the first
                # child of the method. It is also important to iterate the node children one ahead, because if this is
                # not done, the method name is seen as parameter of the method.
                if self.operator is None and (statement_type == 'Call' or statement_type == 'Subscript'):
                    method_name = node_child_code
                    if method_name is None:
                        raise ValueError('Method or Subscript has no name. ' + self.statement_type + ' ' + self.code)
                    else:
                        self.operator = method_name
                else:
                    # If the child is a operator node child then set the operator of this statement.
                    if Statement.is_operator_node_child(node_child_statement_type, statement_type):
                        self.operator = Statement.get_operator_by_node_child(node_child_statement_type, statement_type)

                    # If the node child is not Load or Store, because the statement don't need this information, it is
                    # checked if the child has children or is a variable. If it is a variable a Statement with no
                    # children is created. If it has no children a statement with children is created. At the end the
                    # statement child is added in this statement.
                    elif node_child_statement_type != 'Load' and node_child_statement_type != 'Store':
                        node_grand_children = ast.iter_child_nodes(node_child)
                        statement_child = Statement(node_child_statement_type, node_child_code, node_grand_children,
                                                    self, parsed_line)
                        self.children.append(statement_child)
        # At the end (if children are found) the number of children is defined, if there are children and if there is
        # a parent, so if the statement is the root.
        self.has_children = len(self.children) > 0
        self.has_parent = parent is not None

    def to_array(self):
        """
        :return: the array with all parameters (type, code, transformation applied) of the statement and if a statement
        has children the operator, which is applied for the children is appended, as well as the children itself.
        """
        children = []
        if self.has_children:
            for child in self.children:
                children.append(child.to_array())
            return [self.statement_type, self.code, self.transformation, self.operator, children]
        else:
            return [self.statement_type, self.code, self.transformation]

    def change_to_transformation(self, transformation_schemas, line_number, depth, closer_variables):
        """
        In this method transformations like COM, ARI, LOG are done with the created tree of the root statement.
        Here also expression transformations could be done, but only if it is in combination with another transformation
        schema. If it is only EXP transformation then the method: change_to_exp_transformation should be used, because
        is faster. At the end the transformation of the root statement where the method is called is changed so that
        every transformation of its children is taken to the root transformation.

        :param transformation_schemas: the transformation schemas which should be applied.
        :param line_number: The line number where te transformation is done.
        :param closer_variables: The closer variables which are taken for the expression transformations.
        :param depth: The depth how deep the tree of the statement is parsed.
        """
        # This can only be done if the statement has children. This is needed for recursion, because if at the end
        # a variable is called, then the recursion stops. Here statements which are root statement have normally
        # children unless they would not compile either. If the statement has no children then a normal code is taken
        # as transformation.
        if not self.has_children:
            self.build_statement_operator_transformation()
        else:
            if not self.is_two_sided_operation():
                if Statement.is_in_transformations_schemas('EXP', transformation_schemas):
                    self.change_to_exp_transformation(line_number, depth, closer_variables)
            if self.is_two_sided_operation():
                # If it is so, then the children are fetched and the recursion is started until the depth is reached or
                # the children do not have any children anymore. If it is at the end, then the transformations of it
                # are taken.
                left_child = self.children[0]
                right_child = self.children[1]
                if left_child.has_children:
                    if depth > 0:
                        left_child.change_to_transformation(transformation_schemas, line_number, depth - 1,
                                                            closer_variables)
                if right_child.has_children:
                    if depth > 0:
                        right_child.change_to_transformation(transformation_schemas, line_number, depth - 1,
                                                             closer_variables)
                left_transformation = left_child.transformation
                right_transformation = right_child.transformation

                # If in the transformation schemas is an 'EXP' transformation then this had to be done first. So
                # only if the expression transformation is in a combination with the other transformations. But this
                # is only done, if the right or left statement is a variable. A expression transformation is always
                # applied, because it is a combination transformation which must be applied before the COM, ARI and EXP
                # transformations.
                if Statement.is_in_transformations_schemas('EXP', transformation_schemas):
                    if Statement.is_variable(right_child.statement_type):
                        right_transformation = TransformationManager.create_EXP_transformation(line_number, True,
                                                                                               closer_variables)
                    if Statement.is_variable(left_child.statement_type):
                        left_transformation = TransformationManager.create_EXP_transformation(line_number, True,
                                                                                              closer_variables)
                # The next statement type is the COM transformation. Here is also checked if the schema is in the array
                # of transformations and if the statement is a compare statement. Only then the transformation is
                # created by the TransformationManager. Here the left and right transformation is the transformation
                # of its two children.
                if self.statement_type == 'Compare' and Statement.is_in_transformations_schemas('COM',
                                                                                                transformation_schemas):
                    self.transformation = TransformationManager.create_transformation('COM', line_number,
                                                                                      self.has_parent,
                                                                                      left_transformation,
                                                                                      right_transformation)
                # The next statement type is the ARI transformation. Here is also checked if the schema is in the array
                # of transformations and if the statement is a compare statement. Only then the transformation is
                # created by the TransformationManager. Here the left and right transformation is the transformation
                # of its two children.
                elif self.statement_type == 'BinOp' and Statement.is_in_transformations_schemas('ARI',
                                                                                                transformation_schemas):
                    self.transformation = TransformationManager.create_transformation('ARI', line_number,
                                                                                      self.has_parent,
                                                                                      left_transformation,
                                                                                      right_transformation)
                # The next statement type is the COM transformation. Here is also checked if the schema is in the array
                # of transformations and if the statement is a compare statement. Only then the transformation is
                # created by the TransformationManager. Here the left and right transformation is the transformation
                # of its two children.
                elif self.statement_type == 'BoolOp' and Statement.is_in_transformations_schemas('LOG',
                                                                                                 transformation_schemas
                                                                                                 ):
                    self.transformation = TransformationManager.create_transformation('LOG', line_number,
                                                                                      self.has_parent,
                                                                                      left_transformation,
                                                                                      right_transformation)
                # If the statement type is not in the above transformation schemas then a normal code is created. This
                # is needed because it also could be that only the com transformations have to be applied and not any
                # ari transformations. So it is important to create the com transformations with the original code.
                else:
                    self.build_statement_operator_transformation()

    @staticmethod
    def is_in_transformations_schemas(applied_schema, transformation_schemas):
        """
        This method is needed for change to transformation method. Here is checked if the schema is in the array of
        combination which should be done.

        :param applied_schema: The schema which should be applied.
        :param transformation_schemas: The array of transformation schema combinations.
        :return: False, if the combination is not in it, True otherwise.
        """
        for transformation_schema in transformation_schemas:
            if transformation_schema == applied_schema:
                return True
        return False

    def change_to_exp_transformation(self, line_number, depth, closer_variables):
        """
        This method is called by the Line Transformer if there is only the expression transformation which should be
        applied. Here not every transformation must be build as in the change to transformation method. So it is faster
        if you only want to apply expression transformations.

        :param line_number: The line number where te transformation is done.
        :param closer_variables: The closer variables which are taken for the expression transformations.
        :param depth: The depth how deep the tree of the statement is parsed.
        """
        # If the statement has children, then make the expression transformation for them at first. But only for a
        # certain depth of the tree. If the depth is to low, the expression transformation don't reach the code which is
        # very deep in the tree. This is done for performance issues.
        if self.has_children:
            if depth > 0:
                for child in self.children:
                    child.change_to_exp_transformation(line_number, depth - 1, closer_variables)
            # If the statement has children and after the children are all transformed it is checked with transformation
            # is applied by the operator and the statement type. Then the transformation of this statement is set.
            self.build_statement_operator_transformation()
        # If the statement is a variable then the transformation manager is called to get an expression transformation.
        if Statement.is_variable(self.statement_type):
            self.transformation = TransformationManager.create_EXP_transformation(line_number, False, closer_variables)

    def build_statement_operator_transformation(self):
        """
        If no PySketchFix transformation is done, the normal operator transformation is performed. Therefore the
        operator of the current statement is used to build back the original code with the transformations (EXP) applied
        on them in leaves further down in the tree.

        :return: the transformation of this statement where the statement operator is selected with the statement type.
        """
        # If the current statement is a two sided operator, then the operator is connected with the two children's
        # transformations. This is then the new transformation of self.
        if self.is_two_sided_operation():
            left_child = self.children[0]
            right_child = self.children[1]
            self.transformation = '(' + left_child.transformation + ' ' + self.operator + ' ' + \
                                  right_child.transformation + ')'
        # If the current statement type is a one sided slice then only on the right side of the transformation the : is
        # set.
        elif self.is_one_slice():
            left_child = self.children[0]
            self.transformation = self.operator + left_child.transformation
        # If the current statement type is a two sided slice then set the slice between the children.
        elif self.is_two_slice():
            left_child = self.children[0]
            right_child = self.children[0]
            self.transformation = left_child.transformation + ' ' + self.operator + ' ' + right_child.transformation
        # If the current statement is a one sided operator, then the operator is connected with the two children's
        # transformations. This is then the new transformation of self. The difference here is that this operator could
        # also be a assignment.
        elif self.is_one_sided_operation():
            left_child = self.children[0]
            right_child = self.children[1]
            self.transformation = left_child.code + ' ' + self.operator + ' ' + right_child.transformation
        # If the current statement is a single operation, then the operator is connected with the one! children's
        # transformations. This is then the new transformation of self. The difference here is that this operators are
        # only with one child, so e.g. return statements.
        elif self.is_single_operation():
            child = self.children[0]
            self.transformation = self.operator + ' ' + child.transformation
        # If the current statement is a method, then the operator (here method name) is connected with all children's
        # transformations This is then the new transformation of self.
        elif self.is_method():
            comma_separated_children = ''
            for child in self.children:
                comma_separated_children += ', ' + child.transformation
            transformation = self.operator + '(' + comma_separated_children + ')'
            transformation = transformation.replace('(, ', '(')
            self.transformation = transformation
        # If the current statement is a subscript, then the operator is connected with all children's transformations.
        # This is then the new transformation of self.
        elif self.is_subscript():
            transformation = ''
            for child in self.children:
                transformation = self.operator + '[' + child.transformation + ']'
                break
            transformation = transformation.replace('[, ', '[')
            self.transformation = transformation
        # If the current statement is a tuple, then the operator is connected with all children's transformations.
        # This is then the new transformation of self.
        elif self.is_tuple():
            transformation = '{'
            for child in self.children:
                transformation = transformation + self.operator + child.transformation
            transformation = transformation.replace('{, ', '')
            self.transformation = transformation
        # If the current statement is a index, then the operator is connected with all children's transformations.
        # This is then the new transformation of self.
        elif self.is_index():
            for child in self.children:
                self.transformation = child.transformation
                break
        # Check if the current statement is an attribute of an object then call it on the right side with a
        # transformation.
        elif self.is_attribute() and self.code.__contains__("."):
            index_of_point = str(self.code).index(".")
            number_of_points = str(self.code).count(".")
            if index_of_point > 0 and number_of_points == 1:
                left_of_attribute = str(self.code)[:index_of_point]
                self.transformation = left_of_attribute + "." + self.children[0].transformation
            else:
                self.transformation = self.code
        # Here you can code new transformations and buildings of new code generations.
        else:
            if ConfigReader.get_debug_mode():
                print('Transformation to complex. You can add the transformation yourself in the Statement if '
                      'you want:' + str(self.to_array()))
            self.transformation = self.code

    @staticmethod
    def is_variable(statement_type):
        """
        Checks if the statement type is a Name, Num, Constant or List. Then it is a variable.

        :param statement_type: The AST Tokens statement type.
        :return: True, if it is a variable, False otherwise.
        """
        return (statement_type == 'Name' or statement_type == 'Num' or statement_type
                == 'NameConstant' or statement_type == 'List')

    def is_attribute(self):
        """
        :return: True, if the statement type is an attribute operation so a.b
        """
        return self.statement_type == 'Attribute' and len(self.children) == 1

    def is_one_slice(self):
        """
        :return: True, if the statement type is slice and he has only one child: then [:1]
        """
        return self.statement_type == 'Slice' and len(self.children) == 1

    def is_two_slice(self):
        """
        :return: True, if the statement type is slice and he has only one child: then [1:1]
        """
        return self.statement_type == 'Slice' and len(self.children) == 2

    def is_two_sided_operation(self):
        """
        :return: True, if the statement type is a bool operation, a binary operation or a compare operation and the
        statement only has two children. A two sided operation has transformation on the left and right hand side of the
        operator.
        """
        two_sided_operations = ['BoolOp', 'Compare', 'BinOp']
        for two_sided_operation in two_sided_operations:
            if two_sided_operation == self.statement_type:
                return len(self.children) == 2
        return False

    def is_one_sided_operation(self):
        """
        :return: True, if the statement type is a assignment and the aug assign and the statement only has
        two children. A one sided operation has at the left side the normal code and on the right side the
        transformation which was done.
        """
        one_sided_operations = ['Assign', 'AugAssign']
        for one_sided_operation in one_sided_operations:
            if one_sided_operation == self.statement_type:
                return len(self.children) == 2
        return False

    def is_single_operation(self):
        """
        :return: True, if the statement type is a raise, unary operation or return operation and the statement only has
        one child. A single operation has only one child and a operator on the left side.
        """
        single_operations = ['Return', 'Raise', 'UnaryOp']
        for single_operation in single_operations:
            if single_operation == self.statement_type:
                return len(self.children) == 1
        return False

    def is_method(self):
        """
        :return: True, if the statement type is a method call and the call has more or zero children.
        """
        return self.statement_type == 'Call' and len(self.children) >= 0

    def is_subscript(self):
        """
        :return: True, if the statement type is a subscript call and the call has more or zero children.
        """
        return self.statement_type == 'Subscript' and len(self.children) == 1

    def is_index(self):
        """
        :return: True, if the statement type is an index and has a tuple as children (so more then one child).
        """
        return self.statement_type == 'Index' and len(self.children) == 1

    def is_tuple(self):
        """
        :return: True, if the statement type is an index and has one child.
        """
        return self.statement_type == 'Tuple' and len(self.children) > 1
