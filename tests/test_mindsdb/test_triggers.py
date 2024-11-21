from mindsdb_sql_parser import parse_sql
from mindsdb_sql_parser.ast.mindsdb import *
from mindsdb_sql_parser.ast import *


class TestTriggers:
    def test_create_trigger(self):
        sql = '''
            create trigger proj2.tname on db1.tbl1 
             (
                 retrain p1
            ) 
        '''
        ast = parse_sql(sql)
        expected_ast = CreateTrigger(
            name=Identifier('proj2.tname'),
            table=Identifier('db1.tbl1'),
            query_str="retrain p1",
        )
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

    def test_create_trigger_cols(self):
        sql = '''
            create trigger proj2.tname on db1.tbl1 
            columns aaa
             (
                 retrain p1
            ) 
        '''
        ast = parse_sql(sql)
        expected_ast = CreateTrigger(
            name=Identifier('proj2.tname'),
            table=Identifier('db1.tbl1'),
            columns=[Identifier('aaa')],
            query_str="retrain p1",
        )
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

        # 2 columns
        sql = '''
            create trigger proj2.tname on db1.tbl1 
            columns aaa, bbb
             (
                 retrain p1
            ) 
        '''
        ast = parse_sql(sql)
        expected_ast = CreateTrigger(
            name=Identifier('proj2.tname'),
            table=Identifier('db1.tbl1'),
            columns=[Identifier('aaa'), Identifier('bbb')],
            query_str="retrain p1",
        )
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

    def test_drop_trigger(self):
        sql = '''
            drop trigger proj1.tname
        '''
        ast = parse_sql(sql)
        expected_ast = DropTrigger(
            name=Identifier('proj1.tname'),
        )
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()
