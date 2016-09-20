import records
import anosql


db = records.Database('sqlite:///test.db')
class Queries(object):
    schema = anosql.load_queries("postgresql", "db/sql/schema.sql")
    user = anosql.load_queries("postgresql", "db/sql/user.sql")
    repo = anosql.load_queries("postgresql", "db/sql/repo.sql")

for query in Queries.schema.available_queries:
    db.query(Queries.schema.__dict__[query].__query__)
