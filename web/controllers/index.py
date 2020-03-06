from flask import render_template, request, Blueprint, redirect
from services.user import UserServices

index = Blueprint('blue', __name__)


@index.route('/')
def get_index():
    uid = request.cookies.get('uid')
    if uid is None:
        return redirect('/user/login', 302)
    us = UserServices()
    result = us.get_user_info(uid)
    total_time = us.get_user_time(uid)
    return render_template('index/index.html', username=result['user_name'], total_time=round(total_time/60, 1))
