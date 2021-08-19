#! /bin/python3
# -*- coding:utf-8 -*-

from flask import Flask,render_template,request,Response,redirect,url_for
#内网ip

app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello Flask!'


@app.route("/index")
def ind():
    return render_template("area-stack-gradient.html")



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000,debug=True)

