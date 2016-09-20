#! /usr/bin/python
import click
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

import columbo.spiders.user_search
import columbo.spiders.user
import columbo.spiders.repo

configure_logging()
runner = CrawlerRunner()


@click.command()
@click.option(
    '--q',
    type=(str),
    default="location: brno language: python",
    help="Github search query"
)
def solve(q):
    user_search_spider = columbo.spiders.user_search.UserSearchSpider
    user_search_spider.q = q
    user_spider = columbo.spiders.user.UserSpider
    repo_spider = columbo.spiders.repo.RepoSpider
    spiders = [user_search_spider, user_spider, repo_spider]
    run(spiders)


@click.command()
@click.option(
    '--q',
    type=(str),
    default="location:brno language:python",
    help="Github search query"
)
def suspectslist(q):
    user_search_spider = columbo.spiders.user_search.UserSearchSpider
    user_search_spider.q = q
    spiders = [user_search_spider, ]
    run(spiders)


@click.command()
def suspectprofiles():
    user_spider = columbo.spiders.user.UserSpider
    spiders = [user_spider, ]
    run(spiders)


@click.command()
def suspectrepos():
    repo_spider = columbo.spiders.repo.RepoSpider
    spiders = [repo_spider, ]
    run(spiders)


@click.group()
def cli():
    pass


@defer.inlineCallbacks
def crawl(spiders):
    # TODO: ensure reporter started
    for spider in spiders:
        yield runner.crawl(spider)
    reactor.stop()


def run(spiders):
    crawl(spiders)
    reactor.run()


cli.add_command(suspectslist)
cli.add_command(suspectprofiles)
cli.add_command(suspectrepos)
cli.add_command(suspectrepos)

if __name__ == "__main__":
    cli()
