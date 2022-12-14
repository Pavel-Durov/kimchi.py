from src.kimchi_ast.ast import (
    BlockStatement,
    Boolean,
    CallExpression,
    ExpressionStatement,
    FunctionLiteral,
    Identifier,
    IfExpression,
    InfixExpression,
    IntegerLiteral,
    LetStatement,
    AssignStatement,
    PrefixExpression,
    Program,
    ReturnStatement,
    ArrayLiteral,
    StringLiteral,
    IndexExpression,
    HashLiteral,
    WhileExpression
)

from src.kimchi_tk import Tk


class Parser:
    LOWEST = 0
    EQUALS = 1  # ==
    LESSGREATER = 2  # > or <
    SUM = 3  # +
    PRODUCT = 4  # *
    PREFIX = 5  # -X or !X
    CALL = 6  # myFunction(X)
    INDEX = 8  # [0]

    precedences = {
        Tk.EQ: EQUALS,
        Tk.ASSIGN: EQUALS,
        Tk.NOT_EQ: EQUALS,
        Tk.LT: LESSGREATER,
        Tk.GT: LESSGREATER,
        Tk.PLUS: SUM,
        Tk.MINUS: SUM,
        Tk.SLASH: PRODUCT,
        Tk.ASTERISK: PRODUCT,
        Tk.LPAREN: CALL,
        Tk.LBRACKET: INDEX,
    }

    def __init__(self, lexer):
        self.l = lexer
        self.cur_token = None
        self.peek_token = None
        self.errors = []

        self.next_token()
        self.next_token()

    def parse_infix_token_exist(self, tk, left):
        if tk == Tk.PLUS:
            return True
        elif tk == Tk.MINUS:
            return True
        elif tk == Tk.SLASH:
            return True
        elif tk == Tk.ASTERISK:
            return True
        elif tk == Tk.EQ:
            return True
        elif tk == Tk.NOT_EQ:
            return True
        elif tk == Tk.LT:
            return True
        elif tk == Tk.GT:
            return True
        elif tk == Tk.LPAREN:
            return True
        elif tk == Tk.LBRACKET:
            return True
        return False

    def parse_infix_token(self, tk, left):
        if tk == Tk.PLUS:
            return self.parse_infix_expression(left)
        elif tk == Tk.MINUS:
            return self.parse_infix_expression(left)
        elif tk == Tk.SLASH:
            return self.parse_infix_expression(left)
        elif tk == Tk.ASTERISK:
            return self.parse_infix_expression(left)
        elif tk == Tk.EQ:
            return self.parse_infix_expression(left)
        elif tk == Tk.NOT_EQ:
            return self.parse_infix_expression(left)
        elif tk == Tk.LT:
            return self.parse_infix_expression(left)
        elif tk == Tk.GT:
            return self.parse_infix_expression(left)
        elif tk == Tk.LPAREN:
            return self.parse_call_expression(left)
        elif tk == Tk.LBRACKET:
            return self.parse_index_expression(left)
        return None

    def parse_hash_literal(self):
        pairs = {}
        while not self.peek_token_is(Tk.RBRACE):
            self.next_token()
            key = self.parse_expression(self.LOWEST)
            if not self.expect_peek(Tk.COLON):
                return None
            self.next_token()
            value = self.parse_expression(self.LOWEST)
            pairs[key] = value
            if not self.peek_token_is(Tk.RBRACE) and not self.expect_peek(Tk.COMMA):
                return None
        if not self.expect_peek(Tk.RBRACE):
            return None
        return HashLiteral(self.cur_token, pairs)

    def parse_index_expression(self, left):
        self.next_token()
        index = self.parse_expression(self.LOWEST)
        exp = IndexExpression(self.cur_token, left, index)

        if not self.expect_peek(Tk.RBRACKET):
            return None
        return exp

    def parse_array_literal(self):
        return ArrayLiteral(self.cur_token, self.parse_expression_list(Tk.RBRACKET))

    def parse_expression_list(self, end):
        expressions = []
        if self.peek_token_is(end):
            self.next_token()
            return expressions

        self.next_token()

        expressions.append(self.parse_expression(self.LOWEST))

        while self.peek_token_is(Tk.COMMA):
            self.next_token()
            self.next_token()
            expressions.append(self.parse_expression(self.LOWEST))

        if not self.expect_peek(Tk.RBRACKET):
            return None

        return expressions

    def parse_string_literal(self):
        return StringLiteral(self.cur_token, self.cur_token.literal)

    def parse_call_expression(self, func):
        exp = CallExpression(self.cur_token, func, None)
        exp.arguments = self.parse_call_arguments()
        return exp

    def parse_call_arguments(self):
        args = []
        if self.peek_token_is(Tk.RPAREN):
            self.next_token()
            return []
        self.next_token()
        args.append(self.parse_expression(self.LOWEST))

        while self.peek_token_is(Tk.COMMA):
            self.next_token()
            self.next_token()
            args.append(self.parse_expression(self.LOWEST))

        if not self.expect_peek(Tk.RPAREN):
            return None

        return args

    def parse_function_literal(self):
        lit = FunctionLiteral(token=self.cur_token)
        if not self.expect_peek(Tk.LPAREN):
            return None
        lit.parameters = self.parse_function_parameters()
        if not self.expect_peek(Tk.LBRACE):
            return None
        lit.body = self.parse_block_statement()
        return lit

    def parse_function_parameters(self):
        identifiers = []
        if self.peek_token_is(Tk.RPAREN):
            self.next_token()
            return []

        self.next_token()
        ident = Identifier(self.cur_token, self.cur_token.literal)
        identifiers.append(ident)

        while self.peek_token_is(Tk.COMMA):
            self.next_token()
            self.next_token()
            ident = Identifier(self.cur_token, self.cur_token.literal)
            identifiers.append(ident)

        if not self.expect_peek(Tk.RPAREN):
            return None

        return identifiers

    def parse_while_expression(self):
        exp = WhileExpression(token=self.cur_token)
        if self.expect_peek(Tk.LPAREN) == False:
            return None
        self.next_token()
        exp.condition = self.parse_expression(self.LOWEST)
        if self.expect_peek(Tk.RPAREN) == False:
            return None
        if self.expect_peek(Tk.LBRACE) == False:
            return None
        exp.body = self.parse_block_statement()
        return exp

    def parse_if_expression(self):
        exp = IfExpression(token=self.cur_token)
        if self.expect_peek(Tk.LPAREN) == False:
            return None
        self.next_token()
        exp.condition = self.parse_expression(self.LOWEST)
        if self.expect_peek(Tk.RPAREN) == False:
            return None
        if self.expect_peek(Tk.LBRACE) == False:
            return None
        exp.consequence = self.parse_block_statement()

        if self.cur_token_is(Tk.ELSE):
            if self.expect_peek(Tk.LBRACE) is False:
                return None
            exp.alternative = self.parse_block_statement()
            # TODO: this might be needed as it diverges from the book
            self.next_token()
        return exp

    def parse_block_statement(self):
        block = BlockStatement(token=self.cur_token)
        self.next_token()
        while (
                self.cur_token_is(Tk.RBRACE) == False and self.cur_token_is(Tk.EOF) == False
        ):
            stmt = self.parse_statement()
            block.statements.append(stmt)
            self.next_token()
        self.next_token()
        return block

    def parse_grouped_expression(self):
        self.next_token()
        exp = self.parse_expression(self.LOWEST)
        if self.expect_peek(Tk.RPAREN) == False:
            return None
        return exp

    def parse_boolean(self):
        return Boolean(self.cur_token, self.cur_token_is(Tk.TRUE))

    def parse_identifier(self):
        return Identifier(self.cur_token, self.cur_token.literal)

    def peek_error(self, token_type):
        msg = "expected next token to be %s, got %s instead" % (
            token_type, self.peek_token.type
        )
        self.errors.append(msg)

    def next_token(self):
        self.cur_token = self.peek_token
        self.peek_token = self.l.next_token()

    def parse_program(self):
        prog = Program()
        while self.cur_token.type != Tk.EOF:
            stmt = self.parse_statement()
            if stmt is not None:
                prog.statements.append(stmt)
            self.next_token()
        return prog

    def parse_infix_expression(self, left):
        exp = InfixExpression(
            token=self.cur_token,
            operator=self.cur_token.literal,
            left=left
        )
        precedence = self.cur_precedence()
        self.next_token()
        exp.right = self.parse_expression(precedence)
        return exp

    def parse_prefix_expression(self):
        exp = PrefixExpression(token=self.cur_token, operator=self.cur_token.literal)
        self.next_token()
        exp.right = self.parse_expression(self.PREFIX)
        return exp

    def parse_assign_statment(self):
        name = Identifier(self.cur_token, self.cur_token.literal)

        if not self.expect_peek(Tk.ASSIGN):
            return None
        stmt = AssignStatement(token=self.cur_token, identifier=name, value_exp=None)
        self.next_token()
        stmt.value = self.parse_expression(self.LOWEST)
        while not self.cur_token_is(Tk.SEMICOLON):
            self.next_token()
        return stmt

    def parse_let_statement(self):
        stmt = LetStatement(token=self.cur_token, identifier=None, value_exp=None)
        if not self.expect_peek(Tk.IDENT):
            return None

        stmt.name = Identifier(self.cur_token, self.cur_token.literal)
        if not self.expect_peek(Tk.ASSIGN):
            return None
        self.next_token()

        stmt.value = self.parse_expression(self.LOWEST)

        while not self.cur_token_is(Tk.SEMICOLON):
            self.next_token()
        return stmt

    def parse_return_statement(self):
        stmt = ReturnStatement(token=self.cur_token, return_value=None)
        self.next_token()
        stmt.return_value = self.parse_expression(self.LOWEST)
        while not self.cur_token_is(Tk.SEMICOLON):
            self.next_token()
        return stmt

    def on_prefix_parse_fn_error(self, token_type):
        self.errors.append("no prefix parse function for %s found" % (token_type))

    def peek_precedence(self):
        if self.peek_token.type in self.precedences:
            return self.precedences[self.peek_token.type]
        return self.LOWEST

    def cur_precedence(self):
        if self.cur_token.type in self.precedences:
            return self.precedences[self.cur_token.type]
        return self.LOWEST

    def parse_integer_literal(self):
        value = 0
        try:
            value = int(self.cur_token.literal)
        except ValueError:
            self.errors.append(
                "could not parse %s as integer" % (self.cur_token.literal)
            )
            return None
        return IntegerLiteral(self.cur_token, value)

    def parse_expression_statement(self):
        exp = self.parse_expression(self.LOWEST)
        stms = ExpressionStatement(token=self.cur_token, expression=exp)
        if self.peek_token_is(Tk.SEMICOLON):
            self.next_token()
        return stms

    def parse_statement(self):
        if self.cur_token.type == Tk.LET:
            return self.parse_let_statement()
        elif self.cur_token.type == Tk.RETURN:
            return self.parse_return_statement()
        elif self.cur_token.type == Tk.IDENT and self.peek_token_is(Tk.ASSIGN):
            return self.parse_assign_statment()
        else:
            return self.parse_expression_statement()

    def cur_token_is(self, token_type):
        return self.cur_token.type == token_type

    def peek_token_is(self, token_type):
        return self.peek_token.type == token_type

    def expect_peek(self, token_type):
        if self.peek_token_is(token_type):
            self.next_token()
            return True
        else:
            self.peek_error(token_type)
            return False

    def parse_expression(self, precedence):
        tk = self.cur_token.type
        left_exp = None
        if tk == Tk.IDENT:
            left_exp = self.parse_identifier()
        elif tk == Tk.INT:
            left_exp = self.parse_integer_literal()
        elif tk == Tk.BANG or tk == Tk.MINUS:
            left_exp = self.parse_prefix_expression()
        elif tk == Tk.TRUE or tk == Tk.FALSE:
            left_exp = self.parse_boolean()
        elif tk == Tk.LPAREN:
            left_exp = self.parse_grouped_expression()
        elif tk == Tk.IF:
            left_exp = self.parse_if_expression()
        elif tk == Tk.WHILE:
            left_exp = self.parse_while_expression()
        elif tk == Tk.FUNCTION:
            left_exp = self.parse_function_literal()
        elif tk == Tk.STRING:
            left_exp = self.parse_string_literal()
        elif tk == Tk.LBRACKET:
            left_exp = self.parse_array_literal()
        elif tk == Tk.LBRACE:
            left_exp = self.parse_hash_literal()
        else:
            self.on_prefix_parse_fn_error(self.cur_token.type)

        while (self.peek_token_is(Tk.SEMICOLON) == False and precedence < self.peek_precedence()):
            tk = self.peek_token.type
            self.next_token()
            if tk == Tk.PLUS:
                left_exp = self.parse_infix_expression(left_exp)
            elif tk == Tk.MINUS:
                left_exp = self.parse_infix_expression(left_exp)
            elif tk == Tk.SLASH:
                left_exp = self.parse_infix_expression(left_exp)
            elif tk == Tk.ASTERISK:
                left_exp = self.parse_infix_expression(left_exp)
            elif tk == Tk.EQ:
                left_exp = self.parse_infix_expression(left_exp)
            elif tk == Tk.NOT_EQ:
                left_exp = self.parse_infix_expression(left_exp)
            elif tk == Tk.LT:
                left_exp = self.parse_infix_expression(left_exp)
            elif tk == Tk.GT:
                left_exp = self.parse_infix_expression(left_exp)
            elif tk == Tk.LPAREN:
                left_exp = self.parse_call_expression(left_exp)
            elif tk == Tk.LBRACKET:
                left_exp = self.parse_index_expression(left_exp)
            elif tk == Tk.ASSIGN:
                left_exp = self.parse_infix_expression(left_exp)
            else:
                return left_exp

        return left_exp
