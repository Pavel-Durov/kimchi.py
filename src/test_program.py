import src.kimchi_ioc as ioc
import src.kimchi_object as obj
from src.kimchi_evaluator.evaluator import Evaluator
from src.kimchi_lexer import Lexer
from src.kimchi_parser import Parser


def test_return_literal_value():
    source = """
        let b = 9;
        b;
    """
    evaluated = eval_test(source)
    assert isinstance(evaluated, obj.Integer)
    self_like_eval = eval_test(source, True)
    assert evaluated.value == self_like_eval.value == 9


def test_while_program():
    source = """
        let a = 0;
        
        while (a < 5){
           let a = a + 1;
        };
        let b = 0;
        while (b < 5){
           let b = b + a;
        };
        b;
    """
    evaluated = eval_test(source)
    assert isinstance(evaluated, obj.Integer)
    self_like_eval = eval_test(source, True)
    assert evaluated.value == self_like_eval.value == 5


def test_function_calls():
    source = """
    let fibonacci = fn(x) { 
      if (x < 2) {
        return x;
      }
      return fibonacci(x-1) + fibonacci(x-2);
    }; 
    
    let getOne = fn(){
      return 1;
    };
    getOne() + fibonacci(7);
    """
    evaluated = eval_test(source)
    assert isinstance(evaluated, obj.Integer)
    self_like_eval = eval_test(source, True)
    assert evaluated.value == self_like_eval.value == 14


def test_closure():
    input = """
    let add = fn(x) {
      fn(y) { x + y };
    };
    let addTwo = add(2);
    addTwo(3);
    """
    evaluated = eval_test(input)
    assert evaluated.value == 5


def eval_test(str, self_like=False):
    lexer = Lexer(str)
    parser = Parser(lexer)
    program = parser.parse_program()

    if self_like:
        e = Evaluator(ioc.IOC(self_like=True))
        return e.eval(program, e.create_env(None))
    e = Evaluator(ioc.IOC(self_like=False))
    return e.eval(program, e.create_env(None))
