from mindsdb_sql_parser import parse_sql
from mindsdb_sql_parser.ast.mindsdb import *
from mindsdb_sql_parser.ast import *


class TestDropDatasource:
    def test_drop_datasource(self):
        sql = "DROP DATASOURCE IF EXISTS dsname"
        ast = parse_sql(sql)
        expected_ast = DropDatasource(name=Identifier('dsname'), if_exists=True)
        assert str(ast).lower() == sql.lower()
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

    def test_drop_project(self):

        sql = "DROP PROJECT dbname"
        ast = parse_sql(sql)

        expected_ast = DropDatabase(name=Identifier('dbname'), if_exists=False)

        assert str(ast).lower() == str(expected_ast).lower()
        assert ast.to_tree() == expected_ast.to_tree()

