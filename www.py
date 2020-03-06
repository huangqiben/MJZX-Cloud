from application import app
from web.controllers.admin.attend import teacher_info
from web.controllers.user.User import user
from web.controllers.video.Video import video
from web.controllers.index import index

app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(video, url_prefix='/video')
app.register_blueprint(teacher_info, url_prefix='/admin')
app.register_blueprint(index)
