#!/usr/bin/env python
import os
from app import create_app
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app) 
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def runtornado():
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5050)
    IOLoop.instance().start()

if __name__ == '__main__':
    import sys
    if sys.version_info.major < 3:
            reload(sys)
    sys.setdefaultencoding('utf8')
    manager.run()
