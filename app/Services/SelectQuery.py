class SelectQuery:

    def __init__(self, table):
        self.pagination = {}
        self.order = ""
        self.columns = []
        self.whereClause = []
        self.table = table

    def select(self, columns):
        self.columns = columns
        return self

    def orderBy(self, column, order):
        self.order = f"{column} {order}"
        return self

    def where(self, column, operator, value):
        self.whereClause.append(f"{column} {operator} {value}")
        return self

    def forPage(self, first, page):
        self.pagination = {"first": first, "page": page}
        return self

    def construct(self):
        sql = f"""
            SELECT {', '.join(self.columns if len(self.columns) > 0 else ["*"])}
            FROM {self.table} """
        if len(self.whereClause) > 0:
            sql += f"""WHERE {" AND ".join(self.whereClause)} """
        if len(self.order) > 0:
            sql += f"""ORDER BY {self.order} """
        if self.pagination:
            sql += f"""LIMIT {self.pagination["first"]} OFFSET {(self.pagination["page"] -  1) * self.pagination["first"]} """

        return sql