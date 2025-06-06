from mindsdb_sql_parser.ast.mindsdb.knowledge_base import *
from mindsdb_sql_parser import parse_sql, Variable
from mindsdb_sql_parser.ast.mindsdb.knowledge_base import (
    CreateKnowledgeBase,
    DropKnowledgeBase,
)
from mindsdb_sql_parser.ast import (
    Select,
    Identifier,
    Join,
    Show,
    BinaryOperation,
    Constant,
    Star,
    Delete,
    Insert,
    OrderBy,
)
from mindsdb_sql_parser.utils import to_single_line 

class TestKB:

    def test_create_knowledge_base(self):
        # create without select
        sql = """
            CREATE KNOWLEDGE_BASE my_knowledge_base
            USING
                MODEL=mindsdb.my_embedding_model,
                STORAGE = my_vector_database.some_table
        """
        ast = parse_sql(sql)
        expected_ast = CreateKnowledgeBase(
            name=Identifier("my_knowledge_base"),
            if_not_exists=False,
            model=Identifier(parts=["mindsdb", "my_embedding_model"]),
            storage=Identifier(parts=["my_vector_database", "some_table"]),
            from_select=None,
            params={},
        )
        assert to_single_line(str(ast)) == to_single_line(str(expected_ast)) 
        assert ast == expected_ast

        # using the alias KNOWLEDGE BASE without underscore shall also work
        sql = """
            CREATE KNOWLEDGE BASE my_knowledge_base
            USING
                MODEL=mindsdb.my_embedding_model,
                STORAGE = my_vector_database.some_table
        """
        ast = parse_sql(sql)
        assert ast == expected_ast

        # the order of MODEL and STORAGE should not matter
        sql = """
            CREATE KNOWLEDGE_BASE my_knowledge_base
            USING
                STORAGE = my_vector_database.some_table,
                MODEL = mindsdb.my_embedding_model
        """
        ast = parse_sql(sql)
        assert ast == expected_ast

        # create from a query
        sql = """
            CREATE KNOWLEDGE_BASE my_knowledge_base
            FROM (
                SELECT id, content, embeddings, metadata
                FROM my_table
                JOIN my_embedding_model
            )
            USING
                MODEL = mindsdb.my_embedding_model,
                STORAGE = my_vector_database.some_table
        """
        ast = parse_sql(sql)
        expected_ast = CreateKnowledgeBase(
            name=Identifier("my_knowledge_base"),
            if_not_exists=False,
            model=Identifier(parts=["mindsdb", "my_embedding_model"]),
            storage=Identifier(parts=["my_vector_database", "some_table"]),
            from_select=Select(
                targets=[
                    Identifier("id"),
                    Identifier("content"),
                    Identifier("embeddings"),
                    Identifier("metadata"),
                ],
                from_table=Join(
                    left=Identifier("my_table"),
                    right=Identifier("my_embedding_model"),
                    join_type="JOIN",
                ),
            ),
            params={},
        )

        assert ast == expected_ast

        # create without MODEL
        sql = """
            CREATE KNOWLEDGE_BASE my_knowledge_base
            USING
                STORAGE = my_vector_database.some_table
        """

        expected_ast = CreateKnowledgeBase(
            name=Identifier("my_knowledge_base"),
            if_not_exists=False,
            model=None,
            storage=Identifier(parts=["my_vector_database", "some_table"]),
            from_select=None,
            params={},
        )

        ast = parse_sql(sql)

        assert ast == expected_ast

        # create without STORAGE
        sql = """
            CREATE KNOWLEDGE_BASE my_knowledge_base
            USING
                MODEL = mindsdb.my_embedding_model
        """

        expected_ast = CreateKnowledgeBase(
            name=Identifier("my_knowledge_base"),
            if_not_exists=False,
            model=Identifier(parts=["mindsdb", "my_embedding_model"]),
            from_select=None,
            params={},
        )

        ast = parse_sql(sql)

        assert ast == expected_ast

        # create if not exists
        sql = """
            CREATE KNOWLEDGE_BASE IF NOT EXISTS my_knowledge_base
            USING
                MODEL = mindsdb.my_embedding_model,
                STORAGE = my_vector_database.some_table
        """
        ast = parse_sql(sql)
        expected_ast = CreateKnowledgeBase(
            name=Identifier("my_knowledge_base"),
            if_not_exists=True,
            model=Identifier(parts=["mindsdb", "my_embedding_model"]),
            storage=Identifier(parts=["my_vector_database", "some_table"]),
            from_select=None,
            params={},
        )
        assert ast == expected_ast

        # create without USING ie no storage or model

        sql = """
            CREATE KNOWLEDGE_BASE my_knowledge_base;
        """
        ast = parse_sql(sql)
        expected_ast = CreateKnowledgeBase(
            name=Identifier("my_knowledge_base"),
            if_not_exists=False,
            model=None,
            storage=None,
            from_select=None,
            params={},
        )
        assert ast == expected_ast

        # create with params
        sql = """
            CREATE KNOWLEDGE_BASE my_knowledge_base
            USING
                MODEL = mindsdb.my_embedding_model,
                STORAGE = my_vector_database.some_table,
                some_param = 'some value',
                other_param = {'key': @var1}
        """
        ast = parse_sql(sql)
        expected_ast = CreateKnowledgeBase(
            name=Identifier("my_knowledge_base"),
            if_not_exists=False,
            model=Identifier(parts=["mindsdb", "my_embedding_model"]),
            storage=Identifier(parts=["my_vector_database", "some_table"]),
            from_select=None,
            params={"some_param": "some value", "other_param": {'key': Variable('var1')}},
        )
        assert ast == expected_ast

    def test_drop_knowledge_base(self):
        # drop if exists
        sql = """
            DROP KNOWLEDGE_BASE IF EXISTS my_knowledge_base
        """
        ast = parse_sql(sql)
        expected_ast = DropKnowledgeBase(
            name=Identifier("my_knowledge_base"), if_exists=True
        )
        assert ast == expected_ast

        # drop without if exists
        sql = """
            DROP KNOWLEDGE_BASE my_knowledge_base
        """
        ast = parse_sql(sql)

        expected_ast = DropKnowledgeBase(
            name=Identifier("my_knowledge_base"), if_exists=False
        )
        assert ast == expected_ast


    def test_show_knowledge_base(self):
        sql = """
            SHOW KNOWLEDGE_BASES
        """
        ast = parse_sql(sql)
        expected_ast = Show(
            category="KNOWLEDGE_BASES",
        )
        assert ast == expected_ast

        # without underscore shall also work
        sql = """
            SHOW KNOWLEDGE BASES
        """
        ast = parse_sql(sql)
        expected_ast = Show(
            category="KNOWLEDGE BASES",
        )
        assert ast == expected_ast

    def test_select_from_knowledge_base(self):
        # this is no different from a regular select
        sql = """
            SELECT * FROM my_knowledge_base
            WHERE
                query = 'some text in natural query'
                AND
                metadata.some_column = 'some value'
            ORDER BY
                distances DESC
            LIMIT 10
        """
        ast = parse_sql(sql)

        expected_ast = Select(
            targets=[Star()],
            from_table=Identifier("my_knowledge_base"),
            where=BinaryOperation(
                op="AND",
                args=[
                    BinaryOperation(
                        op="=",
                        args=[Identifier("query"), Constant("some text in natural query")],
                    ),
                    BinaryOperation(
                        op="=",
                        args=[Identifier("metadata.some_column"), Constant("some value")],
                    ),
                ],
            ),
            order_by=[OrderBy(field=Identifier("distances"), direction="DESC")],
            limit=Constant(10),
        )
        assert ast == expected_ast


    def test_delete_from_knowledge_base(self):
        # this is no different from a regular delete
        sql = """
            DELETE FROM my_knowledge_base
            WHERE
                id = 'some id'
                AND
                metadata.some_column = 'some value'
        """
        ast = parse_sql(sql)
        expected_ast = Delete(
            table=Identifier("my_knowledge_base"),
            where=BinaryOperation(
                op="AND",
                args=[
                    BinaryOperation(op="=", args=[Identifier("id"), Constant("some id")]),
                    BinaryOperation(
                        op="=",
                        args=[Identifier("metadata.some_column"), Constant("some value")],
                    ),
                ],
            ),
        )
        assert ast == expected_ast

    def test_insert_into_knowledge_base(self):
        # this is no different from a regular insert
        sql = """
            INSERT INTO my_knowledge_base (
                id, content, embeddings, metadata
            )
            VALUES (
                'some id',
                'some text',
                '[1,2,3,4,5]',
                '{"some_column": "some value"}'
            ),
            (
                'some other id',
                'some other text',
                '[1,2,3,4,5]',
                '{"some_column": "some value"}'
            )
        """
        ast = parse_sql(sql)
        expected_ast = Insert(
            table=Identifier("my_knowledge_base"),
            columns=[
                Identifier("id"),
                Identifier("content"),
                Identifier("embeddings"),
                Identifier("metadata"),
            ],
            values=[
                [
                    Constant("some id"),
                    Constant("some text"),
                    Constant("[1,2,3,4,5]"),
                    Constant('{"some_column": "some value"}'),
                ],
                [
                    Constant("some other id"),
                    Constant("some other text"),
                    Constant("[1,2,3,4,5]"),
                    Constant('{"some_column": "some value"}'),
                ],
            ],
        )
        assert ast == expected_ast

        # insert from a select
        sql = """
            INSERT INTO my_knowledge_base (
                id, content, embeddings, metadata
            )
            SELECT id, content, embeddings, metadata
            FROM my_table
            WHERE
                metadata.some_column = 'some value'
        """
        ast = parse_sql(sql)
        expected_ast = Insert(
            table=Identifier("my_knowledge_base"),
            columns=[
                Identifier("id"),
                Identifier("content"),
                Identifier("embeddings"),
                Identifier("metadata"),
            ],
            from_select=Select(
                targets=[
                    Identifier("id"),
                    Identifier("content"),
                    Identifier("embeddings"),
                    Identifier("metadata"),
                ],
                from_table=Identifier("my_table"),
                where=BinaryOperation(
                    op="=",
                    args=[Identifier("metadata.some_column"), Constant("some value")],
                ),
            ),
        )
        assert ast == expected_ast

    def test_evaluate_knowledge_base(self):
        sql = """
            EVALUATE KNOWLEDGE_BASE my_knowledge_base
            USING
                TEST_TABLE = my_database.some_table_1,
                SAVE_TO = my_database.some_table_2,
                LLM = {
                    "provider": "openai",
                    "model": "gpt-3.5-turbo",
                    "api_key": "my_api_key"
                },
                GENERATE_DATA = {
                    "from_sql": "SELECT content FROM my_database.some_table",
                    "count": 100
                }
        """
        ast = parse_sql(sql)
        expected_ast = EvaluateKnowledgeBase(
            name=Identifier("my_knowledge_base"),
            params={
                "test_table": Identifier(parts=["my_database", "some_table_1"]),
                "save_to": Identifier(parts=["my_database", "some_table_2"]),
                "llm": {
                    "provider": "openai",
                    "model": "gpt-3.5-turbo",
                    "api_key": "my_api_key"
                },
                "generate_data": {
                    "from_sql": "SELECT content FROM my_database.some_table",
                    "count": 100
                }
            }
        )
        assert ast == expected_ast
