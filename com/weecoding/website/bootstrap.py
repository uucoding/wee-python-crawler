#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

#web 站点启动类

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/hello")
def hello():
    return render_template("lagou/index.html")

if __name__ == '__main__':
    app.run('0.0.0.0','9999',debug=True)