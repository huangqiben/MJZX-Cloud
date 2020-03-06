from flask import request, Blueprint, render_template, redirect

from services.user import UserServices
from services.video import VideoServices

video = Blueprint('video', __name__)


@video.route('/play')
def video_play():
    uid = request.cookies.get('uid')
    if uid is None:
        return redirect('/user/login', 302)
    video_id = request.args.get('video_id')
    us = UserServices()
    vd = VideoServices()
    u_result = us.get_user_info(uid)
    total_time = us.get_user_time(uid)
    vd = vd.get_video_info(video_id)
    return render_template('video/play.html', username=u_result['user_name'], total_time=round(total_time / 60, 1),
                           vd=vd)


@video.route('/list')
def video_list():
    uid = request.cookies.get('uid')
    if uid is None:
        return redirect('/user/login', 302)
    subject_id = request.args.get('sub')
    us = UserServices()
    u_result = us.get_user_info(uid)
    total_time = us.get_user_time(uid)
    vd = VideoServices()
    v_result = vd.get_video_list(subject_id)

    return render_template('video/list.html', course=v_result, username=u_result['user_name'],
                           total_time=round(total_time / 60, 1))


@video.route('live')
def video_live():
    uid = request.cookies.get('uid')
    live = request.args.get("live")
    if uid is None:
        return redirect('/user/login', 302)
    return render_template("video/live.html", live=live, grade=str(int(request.args.get("live"))))
