# -*- coding: utf-8 -*-
import json

import scrapy

import columbo.items

BASE_URL = "https://api.github.com/search/users?q={q}&page={page}"


class UserSearchSpider(scrapy.Spider):
    """ Spider responsible for downloading all users
    """
    q = "language:python location:brno"
    name = "user_search"
    page = 1

    def __genurl(self, page):
        """ Returns paginated url

        Attrs:
            page(int) -
        Returns:
            str - paginated url
        """
        return BASE_URL.format(q=self.q, page=page)

    def start_requests(self):
        url = self.__genurl(self.page)
        yield self.make_requests_from_url(url)

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        items = json_response["items"]

        # If items list was not empty (ie we there are still
        # results available), request next page
        if items:
            self.page += 1
            url = self.__genurl(self.page)
            yield self.make_requests_from_url(url)

        # Serialize github user as scrapy.Item so it can
        # go to the processing pipeline
        for item in items:
            yield columbo.items.GithubUserItem(**item)
