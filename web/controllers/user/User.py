from flask import Blueprint, request, render_template, redirect, jsonify, make_response, Response, url_for

from services.study import StudyServices
from services.user import UserServices
import common.utils.error_code as err

user = Blueprint('user', __name__)


@user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('user/login.html', mess=request.cookies.get('uid'))

    if request.method == 'POST':
        data = request.json
        us = UserServices()
        uid = us.get_login(data['user'], data['pwd'])
        rsp: Response = make_response(err.Success().get_body())
        rsp.content_type = "application/json;charset=UTF-8"
        rsp.set_cookie('uid', str(uid))
        return rsp


@user.route('/register', methods=['GET', 'POST'])
def register():
    us = UserServices()
    if request.method == 'GET':
        return "<h1>注册通道已关闭</h1>"
        # return render_template("user/register.html")

    user_data = request.json
    us = UserServices()
    uid = us.add_user(user_data['name'], user_data['pwd'], user_data['phone'], user_data['group'])
    rsp: Response = make_response(err.Success().get_body())
    rsp.content_type = "application/json;charset=UTF-8"
    rsp.set_cookie('uid', str(uid))
    return rsp


@user.route('/exit')
def delete_cookie():
    rsp: Response = make_response(redirect('/user/login'))
    rsp.delete_cookie('uid')
    return rsp


@user.route('/update', methods=['POST'])
def update_time():
    data = request.json
    uid = request.cookies.get('uid')
    if uid is None:
        raise err.Forbidden('无权限')
    ss = StudyServices()
    ss.add_study_item(uid, data['live'])
    return err.Success()
