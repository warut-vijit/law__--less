#!/usr/bin/python
import time
from daemon import runner
class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/foo.pid'
        self.pidfile_timeout = 5
    def run(self):
        while True:
	    import app
            time.sleep(10)

app1 = App()
daemon_runner = runner.DaemonRunner(app1)
daemon_runner.do_action()
