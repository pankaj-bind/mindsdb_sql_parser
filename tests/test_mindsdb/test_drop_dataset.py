import pytest

from mindsdb_parser import parse_sql, ParsingException
from mindsdb_parser.ast.mindsdb import *
from mindsdb_parser.ast import *


class TestDropDataset:
    def test_drop_dataset(self):
        sql = "DROP DATASET IF EXISTS dsname"
        ast = parse_sql(sql)
        expected_ast = DropDataset(name=Identifier('dsname'), if_exists=True)
        assert str(ast).lower() == sql.lower()
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()
