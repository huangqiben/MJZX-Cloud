import datetime

from flask import Blueprint, render_template, jsonify, request
import common.utils.error_code as err
from services.study import StudyServices

teacher_info = Blueprint('tea_info', __name__)


def get_week():
    today = ['', '', '', '', '', '', '']
    index = datetime.datetime.now().weekday()
    today[index] = '(今天)'
    return today


@teacher_info.route('/teacher-info')
def teacher():
    result = StudyServices().get_week_info(class_id=7)
    for i, v in zip(range(len(result)), result):
        v['编号'] = i + 1
        study_time = v['周一'] if v['周一'] is not None else 0 + v['周二'] if v['周二'] is not None else 0 + v['周三'] if v['周三'] is not None else 0 + v['周四'] if v['周四'] is not None else 0 + v['周五'] if v['周五'] is not None else 0
        v['考勤'] = '合格' if study_time > 20 * 500 else '-'
        v['周一'] = '-' if v['周一'] is None or v['周一'] == 0 else v['周一']
        v['周二'] = '-' if v['周二'] is None or v['周二'] == 0 else v['周二']
        v['周三'] = '-' if v['周三'] is None or v['周三'] == 0 else v['周三']
        v['周四'] = '-' if v['周四'] is None or v['周四'] == 0 else v['周四']
        v['周五'] = '-' if v['周五'] is None or v['周五'] == 0 else v['周五']

    return render_template('admin/teacherinfo.html', teacher_list=result, today=get_week())


@teacher_info.route('/student-info')
def student():
    class_map = {
        1: '701班',
        2: '702班',
        3: '801班',
        4: '802班',
        5: '901班',
        6: '902班'
    }
    class_id = request.args.get('classId')
    if class_id is None:
        raise err.ParameterException('未指定查询班级')
    result = StudyServices().get_week_info(class_id=class_id)
    for i, v in zip(range(len(result)), result):
        v['编号'] = i + 1
        v['班级'] = class_map[int(class_id)]
        study_time = v['周一'] if v['周一'] is not None else 0 + v['周二'] if v['周二'] is not None else 0 + v['周三'] if v['周三'] is not None else 0 + v['周四'] if v['周四'] is not None else 0 + v['周五'] if v['周五'] is not None else 0
        v['考勤'] = '合格' if study_time > 20 * 500 else '-'
        v['周一'] = '-' if v['周一'] is None or v['周一'] == 0 else v['周一']
        v['周二'] = '-' if v['周二'] is None or v['周二'] == 0 else v['周二']
        v['周三'] = '-' if v['周三'] is None or v['周三'] == 0 else v['周三']
        v['周四'] = '-' if v['周四'] is None or v['周四'] == 0 else v['周四']
        v['周五'] = '-' if v['周五'] is None or v['周五'] == 0 else v['周五']

    return render_template('admin/studentinfo.html', students_list=result, today=get_week())
