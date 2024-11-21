from mindsdb_sql_parser import parse_sql
from mindsdb_sql_parser.ast import *


class TestDescribe:
    def test_describe(self):
        sql = "DESCRIBE my_identifier"
        ast = parse_sql(sql)
        expected_ast = Describe(value=Identifier('my_identifier'))

        assert str(ast).lower() == sql.lower()
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()


class TestDescribeMindsdb:
    def test_describe_predictor(self):
        sql = "DESCRIBE PREDICTOR my_identifier"
        ast = parse_sql(sql)
        expected_ast = Describe(type='PREDICTOR', value=Identifier('my_identifier'))

        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

        sql = "DESCRIBE MODEL my_identifier"
        ast = parse_sql(sql)

        expected_ast = Describe(type='MODEL', value=Identifier('my_identifier'))
        assert str(ast) == str(expected_ast)
        assert ast.to_tree() == expected_ast.to_tree()

        # describe attr
        sql = "DESCRIBE MODEL pred.attr"
        ast = parse_sql(sql)

        expected_ast = Describe(type='MODEL', value=Identifier(parts=['pred', 'attr']))

        assert str(ast) == str(expected_ast)

        # version
        sql = "DESCRIBE MODEL pred.11"
        ast = parse_sql(sql)

        expected_ast = Describe(type='MODEL', value=Identifier(parts=['pred', '11']))

        assert str(ast) == str(expected_ast)

        # version and attr
        sql = "DESCRIBE MODEL pred.11.attr"
        ast = parse_sql(sql)

        expected_ast = Describe(type='MODEL', value=Identifier(parts=['pred', '11', 'attr']))

        assert str(ast) == str(expected_ast)

        # other objects
        for obj in (
                "AGENT", "JOB", "SKILL", "CHATBOT", "TRIGGER", "VIEW",
                "KNOWLEDGE_BASE", "KNOWLEDGE BASE", "PREDICTOR", "MODEL",
                'database', 'project', 'handler', 'ml_engine'):

            sql = f"DESCRIBE {obj} aaa"
            ast = parse_sql(sql)

            obj = obj.replace(' ', '_')
            expected_ast = Describe(type=obj, value=Identifier(parts=['aaa']))

            assert str(ast) == str(expected_ast)
