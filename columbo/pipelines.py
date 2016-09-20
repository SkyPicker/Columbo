# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import subprocess
import os

import sqlalchemy.exc
import sqlparse

from db import db
from db import Queries

HANDLEREPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'handlerepo.sh'))


def get_fields(query):
    """ Helper function to parse out available fields, so they
    don't have to be hardcoded.

    Uses sqlparse to tokenize statement. It gets the "Parenthesis"
    token (the only one in our simple create statements) and
    parses the fields out of it.

    Args:
        query(str): Create table statement.
    Returns:
        list of strings: fields parsed from statement
    """
    sql = sqlparse.parse(query)
    statement = sql[0]

    # Filters out first Parenthesis token (the only one we are interested in)
    raw_fields = filter(lambda x: isinstance(x, sqlparse.sql.Parenthesis), statement.tokens)[0]

    # Make it string again and get rid of the parenthesis, so we get just part
    # of the statement looking like this:
    # id PRIMARY KEY, created_date timestamp, updated_date timestamp..
    fields = str(raw_fields).replace(")", "").replace("(", "")

    # By splitting the string, stripping the whitespace etc. we're done
    return [field.strip().split(" ")[0] for field in fields.split(",")]


def get_params(item, fields, exclude=None):
    """ Helper function to prepare dict of named params to
    be passed to query method

    Args:
        item (obj): scrapy.Item instance
        fields (list[str]): list of fields
    Kwargs:
        exclude (list[str]): list of fields to exclude
    Returns:
        dict with named params
    """
    if exclude is not None:
        fields = [field for field in fields if field not in exclude]
    return {field: item.get(field, None) for field in fields}


class PersistencePipeline(object):
    """ TODO: open & close cursor """

    def __process_item(self, item, create_statement, insert_statement, update_statement):
        fields = get_fields(create_statement)
        params = get_params(item, fields, exclude=["first_seen"])
        try:
            db.query(insert_statement, **params)
        except sqlalchemy.exc.IntegrityError:
            db.query(update_statement, **params)

    def __handle_repo(self, repo):
        user_id = str(repo["owner"]["id"])
        user_login = repo["owner"]["login"]
        repo_name = repo["name"]
        repo_id = str(repo["id"])
        git_url = repo["git_url"]
        # TODO: defer
        subprocess.Popen([HANDLEREPO, user_id, user_login, repo_name, repo_id, git_url])

    def __process_repo(self, item):
        print "x"*1000
        create_table_repo = Queries.schema.create_table_repo.__query__
        insert_repo = Queries.repo.insert_repo.__query__
        update_repo = Queries.repo.update_repo.__query__
        self.__process_item(item, create_table_repo, insert_repo, update_repo)
        self.__handle_repo(item)

    def __process_user(self, item):
        create_table_user = Queries.schema.create_table_user.__query__
        insert_user = Queries.user.insert_user.__query__
        update_user = Queries.user.update_user.__query__
        self.__process_item(item, create_table_user, insert_user, update_user)

    def process_item(self, item, spider):
        actions = {
            "user_search": self.__process_user,
            "user": self.__process_user,
            "repo": self.__process_repo,
        }
        print "x"*1000
        name = spider.crawler.spidercls.name
        action = actions.get(name, None)
        if action is not None:
            action(item)
