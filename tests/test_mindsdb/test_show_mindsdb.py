from mindsdb_sql_parser import parse_sql
from mindsdb_sql_parser.ast import *


class TestShowMindsdb:
    def test_show_keyword(self):
        for keyword in ['STREAMS',
                        'PREDICTORS',
                        'INTEGRATIONS',
                        'DATASOURCES',
                        'PUBLICATIONS',
                        'DATASETS',
                        'ALL']:
            sql = f"SHOW {keyword}"
            ast = parse_sql(sql)
            expected_ast = Show(category=keyword)

            assert str(ast).lower() == sql.lower()
            assert str(ast) == str(expected_ast)
            assert ast.to_tree() == expected_ast.to_tree()

    def test_show_tables_arg(self):
        for keyword in ['VIEWS', 'TABLES']:
            sql = f"SHOW {keyword} from integration_name"
            ast = parse_sql(sql)
            expected_ast = Show(category=keyword, from_table=Identifier('integration_name'))

            assert str(ast).lower() == sql.lower()
            assert str(ast) == str(expected_ast)
            assert ast.to_tree() == expected_ast.to_tree()

