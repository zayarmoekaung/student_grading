from flask import Flask, Blueprint, render_template, request, session,url_for,redirect

controller = Blueprint("controller", __name__)
@controller.route("/", defaults={'path':''})
@controller.route("/dashboard",defaults={'path':''})
@controller.route("/<path:path>")
def main_app(path):
    return render_template('index.html')
