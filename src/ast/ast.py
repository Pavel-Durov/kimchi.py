
from src.token import Token

class Node():
  def __init__(self):
    pass

  def token_literal():
    pass


class Statement(Node):
  def token_literal():
    pass


class Expression(Node):
  def token_literal():
    pass

  def expression_node():
    pass


class Program(Node):
  def __init__(self):
    self.statements = []


  def token_literal(self):
    if len(self.statements) > 0:
      return self.statements[0].token_literal()
    return ""


### Let statement

class LetStatement(Node):
    def __init__(self, token, identifier, value_exp):
        self.token = token # Token.LET
        self.name = identifier # Identifier
        self.value = value_exp # Expression

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        out = self.token_literal() + " " + self.name.value + " = "
        if self.value != None:
            out += str(self.value)
        out += ";"
        return out

    def statement_node(self):
        pass

## Identifier

class Identifier(Expression):
    def __init__(self, token, value):
       self.token = token
       self.value = value

    def expression_node(self):
        pass

    def token_literal(self):
        return self.token.literal

class AST():
  def __init__(self):
    pass