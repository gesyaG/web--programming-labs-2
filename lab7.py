from flask import Blueprint, redirect, request

lab7 = Blueprint('lab7', __name__)


@lab7.route('/lab7/')
def lab():
    return render_template('lab7/lab7.html')