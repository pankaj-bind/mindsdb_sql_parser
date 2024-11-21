import pytest

from mindsdb_parser import parse_sql
from mindsdb_parser.ast import *



class TestUse:
    def test_use(self):
        sql = "USE my_integration"
        ast = parse_sql(sql)
        expected_ast = Use(value=Identifier('my_integration'))

        assert str(ast).lower() == sql.lower()
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

