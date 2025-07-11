class ORMQueryBuilder:

    QUERY_JSON: dict[any, any]

    QUERY_STRING: str = ""

    OPERATORS = {
        "is": "=",
        "contains": "__icontains=",
        "contains_list": "in",
        "greater than or equal to": "__gte=",
        "lesser that or equal to": "__lte=",
        "exists": "__isnull=False",
        "not exists": "__isnull=True",
        "in range": "__range=",
    }

    DATABASE_LOGICAL_OPERATORS = {
        "and": " & ",
        "or": " | "
    }

    def __init__(self, query_json: dict[any, any] = None):
        if query_json:
            self.QUERY_JSON = query_json

        self.build_orm_query_string()
        


    def build_orm_query_string(self) -> str:
        blocks = []
        database_logic = self.DATABASE_LOGICAL_OPERATORS.get(self.QUERY_JSON.get("type", "&"))

        for i, query in enumerate(self.QUERY_JSON.get('queries')):

            statements = []
            database_logic_inner = self.DATABASE_LOGICAL_OPERATORS.get(query.get("type", "&"))

            for j, statement in enumerate(query.get("statements", [])):

                attr = statement.get("attr").lower().lstrip().rstrip().replace("/", "__").replace(" ", "_")

                operator = self.OPERATORS.get(statement.get('operator'))

                value = statement.get("value")
                if not operator:
                    continue

                full_statement = f"Q({attr}{operator}{value})" if j == 0 else f"{database_logic_inner} Q({attr}{operator}{value})"
                statements.append(full_statement)

            full_block = ''.join(statements)
            full_block = f"Q({full_block})"

            if i > 0:
                full_block = f"{database_logic} {full_block}"

            blocks.append(full_block)

        _filter =  ''.join(blocks)
        model_name = self.QUERY_JSON.get("target", "candidate").lstrip().rstrip()
        statement = f"{model_name.title()}.objects.filter(Q({_filter})).distinct().order_by(\"pk\")"
        
        self.QUERY_STRING = statement