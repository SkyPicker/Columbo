import datetime

from twisted.internet import inotify
from twisted.python import filepath
from twisted.internet import reactor

from db import db
from db import Queries

cache = {}


def cont(filename):
    last_execution = cache.get(filename, None)
    if last_execution is None:
        return True
    locked_to = datetime.datetime.now() + datetime.timedelta(seconds=1)
    if last_execution > locked_to:
        return True
    return False


def notify(_, filepath, mask):
    _ = inotify.humanReadableMask(mask)
    filepath = filepath.path
    filename = filepath.split("/")[::-1][0]
    if cont(filename):
        cache[filename] = datetime.datetime.now()
        user_id, repo_id, report_id = filename.split("_")
        user = db.query(Queries.user.select_user_by_id.__query__, id=user_id)[0]
        repo = db.query(Queries.repo.select_repo_by_id.__query__, id=user_id)[0]
        print user.login, repo.id


notifier = inotify.INotify()
notifier.startReading()
notifier.watch(filepath.FilePath("/tmp/repo/.reports/"), callbacks=[notify])
reactor.run()
