# -*- coding: utf-8 -*-
import json

import scrapy

from db import db
from db import Queries
import columbo.items


class RepoSpider(scrapy.Spider):
    name = "repo"
    allowed_domains = ["api.github.com"]
    start_urls = (
        'http://www.api.github.com/',
    )

    def start_requests(self):
        users = db.query(Queries.user.select_public_repos.__query__)
        for user in users:
            url = user.repos_url
            yield self.make_requests_from_url(url)

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        for item in json_response:
            owner_id = item["owner"]["id"]
            owner_login = item["owner"]["login"]
            del item["owner"]
            item["owner"] = owner_id
            item["owner_login"] = owner_login
            yield columbo.items.GithubRepoDetailItem(item)
