from mindsdb_sql_parser.lexer import MindsDBLexer

lexer = MindsDBLexer()


class TestLexer:
    def test_select_basic(self):

        sql = f'SELECT 1'
        tokens = list(lexer.tokenize(sql))

        assert tokens[0].type == 'SELECT'
        assert tokens[0].value == 'SELECT'

        assert tokens[1].type == 'INTEGER'
        assert tokens[1].value == "1"

        sql = f'select 1'
        tokens = list(lexer.tokenize(sql))
        assert tokens[0].type == 'SELECT'
        assert tokens[1].type == 'INTEGER'
        assert tokens[1].value == "1"

        sql = f'select a'
        tokens = list(lexer.tokenize(sql))
        assert tokens[0].type == 'SELECT'
        assert tokens[1].type == 'ID'
        assert tokens[1].value == 'a'

    def test_select_basic_ignored_symbols(self):

        sql = f'SELECT \t\r\n1'
        tokens = list(lexer.tokenize(sql))

        assert tokens[0].type == 'SELECT'
        assert tokens[0].value == 'SELECT'

        assert tokens[1].type == 'INTEGER'
        assert tokens[1].value == "1"

        sql = f'select 1'
        tokens = list(lexer.tokenize(sql))
        assert tokens[0].type == 'SELECT'
        assert tokens[1].type == 'INTEGER'
        assert tokens[1].value == "1"

        sql = f'select a'
        tokens = list(lexer.tokenize(sql))
        assert tokens[0].type == 'SELECT'
        assert tokens[1].type == 'ID'
        assert tokens[1].value == 'a'

    def test_select_identifiers(self):
        sql = 'SELECT abcd123, 123abcd, __whatisthi123s__, idwith$sign, `spaces in id`, multipleparts__whoa, `multiple_parts with brackets` '
        tokens = list(lexer.tokenize(sql))
        assert tokens[0].type == 'SELECT'

        for i, t in enumerate(tokens[1:]):
            if i % 2 != 0:
                assert t.type == 'COMMA'
            else:
                assert t.type == 'ID'

    def test_select_float(self):
        for val in [0.0, 1.000, 0.1, 1.0, 99999.9999]:
            val = str(val)
            sql = f'SELECT {val}'
            tokens = list(lexer.tokenize(sql))

            assert tokens[0].type == 'SELECT'
            assert tokens[0].value == 'SELECT'

            assert tokens[1].type == 'FLOAT'
            assert tokens[1].value == val

    def test_select_strings(self):
        sql = 'SELECT "a", "b", "c"'
        tokens = list(lexer.tokenize(sql))
        assert tokens[0].type == 'SELECT'
        assert tokens[1].type == 'DQUOTE_STRING'
        assert tokens[1].value == '"a"'
        assert tokens[2].type == 'COMMA'
        assert tokens[3].type == 'DQUOTE_STRING'
        assert tokens[3].value == '"b"'
        assert tokens[5].type == 'DQUOTE_STRING'
        assert tokens[5].value == '"c"'

        sql = "SELECT 'a', 'b', 'c'"
        tokens = list(lexer.tokenize(sql))
        assert tokens[0].type == 'SELECT'
        assert tokens[1].type == 'QUOTE_STRING'
        assert tokens[1].value == "'a'"
        assert tokens[2].type == 'COMMA'
        assert tokens[3].type == 'QUOTE_STRING'
        assert tokens[3].value == "'b'"
        assert tokens[5].type == 'QUOTE_STRING'
        assert tokens[5].value == "'c'"

    def test_select_strings_nested(self):
        sql = "SELECT '\"a\"', \"'b'\" "
        tokens = list(lexer.tokenize(sql))
        assert tokens[0].type == 'SELECT'
        assert tokens[1].type == 'QUOTE_STRING'
        assert tokens[1].value == "'\"a\"'"
        assert tokens[2].type == 'COMMA'
        assert tokens[3].type == 'DQUOTE_STRING'
        assert tokens[3].value == '\"\'b\'\"'

    def test_binary_ops(self):
        for op, expected_type in [
            ('+', 'PLUS'),
            ('-', 'MINUS'),
            ('/', 'DIVIDE'),
            ('*', 'STAR'),
            ('%', 'MODULO'),
            ('=', 'EQUALS'),
            ('!=', 'NEQUALS'),
            ('<>', 'NEQUALS'),
            ('>', 'GREATER'),
            ('>=', 'GEQ'),
            ('<', 'LESS'),
            ('<=', 'LEQ'),
            ('>>', 'RIGHT_SHIFT'),
            ('<<', 'LEFT_SHIFT'),
            ('AND', 'AND'),
            ('OR', 'OR'),
            ('IS', 'IS'),
            # ('IS NOT', 'ISNOT'),
            ('LIKE', 'LIKE'),
            ('IN', 'IN'),
        ]:
            sql = f'SELECT 1 {op} 2'
            tokens = list(lexer.tokenize(sql))
            assert tokens[0].type == 'SELECT'
            assert tokens[0].value == 'SELECT'

            assert tokens[1].type == 'INTEGER'
            assert tokens[1].value == "1"

            assert tokens[2].type == expected_type
            assert tokens[2].value == op

            assert tokens[3].type == 'INTEGER'
            assert tokens[3].value == "2"

    def test_binary_ops_not(self):

        sql = f'SELECT 1 IS NOT 2'
        tokens = list(lexer.tokenize(sql))
        assert tokens[0].type == 'SELECT'
        assert tokens[0].value == 'SELECT'

        assert tokens[1].type == 'INTEGER'
        assert tokens[1].value == "1"

        assert tokens[2].type == 'IS_NOT'

        assert tokens[3].type == 'INTEGER'
        assert tokens[3].value == "2"

        #
        sql = f'SELECT 1 NOT IN 2'
        tokens = list(lexer.tokenize(sql))
        assert tokens[0].type == 'SELECT'
        assert tokens[0].value == 'SELECT'

        assert tokens[1].type == 'INTEGER'
        assert tokens[1].value == "1"

        assert tokens[2].type == 'NOT_IN'

        assert tokens[3].type == 'INTEGER'
        assert tokens[3].value == "2"


    def test_select_from(self):
        sql = f'SELECT column AS other_column FROM db.schema.tab'
        tokens = list(lexer.tokenize(sql))

        assert tokens[0].type == 'SELECT'
        assert tokens[0].value == 'SELECT'

        assert tokens[1].type == 'ID'
        assert tokens[1].value == 'column'

        assert tokens[2].type == 'AS'
        assert tokens[2].value == 'AS'

        assert tokens[3].type == 'ID'
        assert tokens[3].value == 'other_column'

        assert tokens[4].type == 'FROM'
        assert tokens[4].value == 'FROM'

        assert tokens[5].type == 'ID'
        assert tokens[5].value == 'db'

        assert tokens[6].type == 'DOT'
        assert tokens[6].value == '.'

        assert tokens[7].type == 'SCHEMA'

        assert tokens[8].type == 'DOT'
        assert tokens[8].value == '.'

        assert tokens[9].type == 'ID'
        assert tokens[9].value == 'tab'

    def test_select_star(self):
        sql = f'SELECT * FROM tab'
        tokens = list(lexer.tokenize(sql))

        assert tokens[0].type == 'SELECT'
        assert tokens[0].value == 'SELECT'

        assert tokens[1].type == 'STAR'
        assert tokens[1].value == '*'

        assert tokens[2].type == 'FROM'
        assert tokens[2].value == 'FROM'

        assert tokens[3].type == 'ID'
        assert tokens[3].value == 'tab'

    def test_select_where(self):
        sql = f'SELECT column FROM tab WHERE column = "something"'
        tokens = list(lexer.tokenize(sql))

        assert tokens[0].type == 'SELECT'
        assert tokens[1].type == 'ID'
        assert tokens[2].type == 'FROM'
        assert tokens[3].type == 'ID'
        assert tokens[4].type == 'WHERE'
        assert tokens[4].value == 'WHERE'
        assert tokens[5].type == 'ID'
        assert tokens[5].value == 'column'
        assert tokens[6].type == 'EQUALS'
        assert tokens[6].value == '='
        assert tokens[7].type == 'DQUOTE_STRING'
        assert tokens[7].value == '"something"'

    def test_select_group_by(self):
        sql = f'SELECT column, sum(column2) FROM tab GROUP BY column'
        tokens = list(lexer.tokenize(sql))

        assert tokens[0].type == 'SELECT'
        assert tokens[1].type == 'ID'
        assert tokens[2].type == 'COMMA'
        assert tokens[3].type == 'ID'
        assert tokens[4].type == 'LPAREN'
        assert tokens[5].type == 'ID'
        assert tokens[6].type == 'RPAREN'
        assert tokens[7].type == 'FROM'
        assert tokens[8].type == 'ID'
        assert tokens[9].type == 'GROUP_BY'
        assert tokens[9].value == 'GROUP BY'
        assert tokens[10].type == 'ID'
        assert tokens[10].value == 'column'

    def test_select_order_by(self):
        for order_dir in ['ASC', 'DESC']:
            sql = f'SELECT column, sum(column2) FROM tab ORDER BY column {order_dir}'
            tokens = list(lexer.tokenize(sql))

            assert tokens[0].type == 'SELECT'
            assert tokens[1].type == 'ID'
            assert tokens[2].type == 'COMMA'
            assert tokens[3].type == 'ID'
            assert tokens[4].type == 'LPAREN'
            assert tokens[5].type == 'ID'
            assert tokens[6].type == 'RPAREN'
            assert tokens[7].type == 'FROM'
            assert tokens[8].type == 'ID'
            assert tokens[9].type == 'ORDER_BY'
            assert tokens[9].value == 'ORDER BY'
            assert tokens[10].type == 'ID'
            assert tokens[10].value == 'column'
            assert tokens[11].type == order_dir
            assert tokens[11].value == order_dir

    def test_as_ones(self):
        sql = "SELECT *, (SELECT 1) AS ones FROM t1"
        tokens = list(lexer.tokenize(sql))

        assert tokens[0].type == 'SELECT'
        assert tokens[1].type == 'STAR'
        assert tokens[2].type == 'COMMA'
        assert tokens[3].type == 'LPAREN'
        assert tokens[4].type == 'SELECT'
        assert tokens[5].type == 'INTEGER'
        assert tokens[6].type == 'RPAREN'
        assert tokens[7].type == 'AS'
        assert tokens[8].type == 'ID'
        assert tokens[9].type == 'FROM'
        assert tokens[10].type == 'ID'

        sql = "SELECT *, (SELECT 1) AS ones FROM t1".lower()
        tokens = list(lexer.tokenize(sql))

        assert tokens[0].type == 'SELECT'
        assert tokens[1].type == 'STAR'
        assert tokens[2].type == 'COMMA'
        assert tokens[3].type == 'LPAREN'
        assert tokens[4].type == 'SELECT'
        assert tokens[5].type == 'INTEGER'
        assert tokens[6].type == 'RPAREN'
        assert tokens[7].type == 'AS'
        assert tokens[8].type == 'ID'
        assert tokens[9].type == 'FROM'
        assert tokens[10].type == 'ID'

    def test_select_parameter(self):
        sql = f'SELECT ?'
        tokens = list(lexer.tokenize(sql))

        assert tokens[0].type == 'SELECT'
        assert tokens[0].value == 'SELECT'

        assert tokens[1].type == 'PARAMETER'
        assert tokens[1].value == '?'

    def test_show_character_set(self):
        sql = "show character set where charset = 'utf8mb4'"
        tokens = list(lexer.tokenize(sql))

        assert tokens[0].type == 'SHOW'
        assert tokens[1].type == 'CHARACTER'
        assert tokens[2].type == 'SET'
        assert tokens[3].type == 'WHERE'
        assert tokens[4].type == 'CHARSET'
        assert tokens[4].value == 'charset'
        assert tokens[5].value == '='
        assert tokens[6].type == 'QUOTE_STRING'
        assert tokens[6].value == "'utf8mb4'"

