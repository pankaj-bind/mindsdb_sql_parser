from mindsdb_sql_parser import parse_sql
from mindsdb_sql_parser.ast import *


class TestDelete:
    def test_delete(self):
        sql = "delete from ds.table1 where field > value"

        ast = parse_sql(sql)
        expected_ast = Delete(
            table=Identifier('ds.table1'),
            where=BinaryOperation(
                op='>',
                args=(
                    Identifier('field'),
                    Identifier('value'),
                )
            ),
        )

        assert str(ast).lower() == sql.lower()
        assert ast.to_tree() == expected_ast.to_tree()

    def test_delete_no_where(self):
        sql = "delete from ds.table1"

        ast = parse_sql(sql)
        expected_ast = Delete(
            table=Identifier('ds.table1'),
            where=None
        )

        assert str(ast).lower() == sql.lower()
        assert ast.to_tree() == expected_ast.to_tree()