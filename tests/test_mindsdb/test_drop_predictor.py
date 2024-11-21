from mindsdb_sql_parser import parse_sql
from mindsdb_sql_parser.ast.mindsdb import *
from mindsdb_sql_parser.ast import *
from mindsdb_sql_parser.lexer import MindsDBLexer

class TestDropPredictor:
    def test_drop_predictor_lexer(self):
        sql = "DROP PREDICTOR mindsdb.pred"
        tokens = list(MindsDBLexer().tokenize(sql))
        assert tokens[0].type == 'DROP'
        assert tokens[1].type == 'PREDICTOR'
        assert tokens[2].type == 'ID'
        assert tokens[2].value == 'mindsdb'
        assert tokens[3].type == 'DOT'
        assert tokens[4].type == 'ID'
        assert tokens[4].value == 'pred'

    def test_drop_predictor_ok(self):
        sql = "DROP PREDICTOR mindsdb.pred"
        ast = parse_sql(sql)
        expected_ast = DropPredictor(name=Identifier('mindsdb.pred'))
        assert str(ast).lower() == sql.lower()
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

    def test_drop_model(self):
        sql = "DROP model mindsdb.pred"
        ast = parse_sql(sql)
        expected_ast = DropPredictor(name=Identifier('mindsdb.pred'))
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

    def test_drop_predictor_if_exists(self):
        sql = "DROP PREDICTOR IF EXISTS mindsdb.pred"
        ast = parse_sql(sql)
        expected_ast = DropPredictor(
            name=Identifier('mindsdb.pred'),
            if_exists=True)
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()
