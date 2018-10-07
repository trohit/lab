#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
import os
import sys
import subprocess
import commands
import urllib
import re
import subprocess
import datetime

app = flask.Flask(__name__)

def _get_list_from_lines(res):
    lines = re.split('\n', res)
    return lines

def is_file_exists(f):
    return os.access(f, os.R_OK)

@app.route("/logs/<string:logfile>")
def showlog(logfile):
    abs_logfile = logpath + logfile
    print("Logs:" + abs_logfile)
    return flask.send_from_directory(logpath, logfile, mimetype='text/plain', cache_timeout=5)

@app.route("/deploy")
def deploy():
    #start
    TODAY= datetime.datetime.now().strftime("%m-%d-%Y_%H%M%S")
    a = flask.request.args.get('a')
    user_agent = flask.request.headers.get('User-Agent')
    ip_addr = flask.request.environ['REMOTE_ADDR']
    print(user_agent)
    print(ip_addr)
    print(flask.request.headers.getlist('accept'))
    return flask.render_template('page.html', **locals()), 201

@app.route("/show/<path:file>")
def showfile(file):
    print("cat " + file)
    process = subprocess.Popen(['cat', ' ', file], stdout = subprocess.PIPE)
    out, err = process.communicate()
    print(out)
    return(out)


@app.route("/")
def main():
    return flask.render_template('index.html', **locals()), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)
