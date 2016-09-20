# -*- coding: utf-8 -*-
import json

import scrapy

from db import db
from db import Queries
import columbo.items


BASE_URL = "https://api.github.com/users/{login}"


class UserSpider(scrapy.Spider):
    name = "user"
    start_urls = (
        'http://www.api.github.com/',
    )

    def start_requests(self):
        users = db.query(Queries.user.select_all_users.__query__)
        for user in users:
            url = BASE_URL.format(login=user.login)
            yield self.make_requests_from_url(url)

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        yield columbo.items.GithubUserDetailItem(json_response)
