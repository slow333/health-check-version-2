from flask import Flask
from config import Config
from .extensions import db, mail, login_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    
    # 설정 클래스로부터 설정을 로드
    app.config.from_object(config_class)

    # SQLAlchemy 객체를 앱과 연결
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # Admin 패널 초기화 및 화면 등록
    from .admin import init_admin
    init_admin(app, db)

    # 블루프린트나 다른 라우트를 여기서 등록
    with app.app_context():
        from .models.users import Users
        @login_manager.user_loader
        def load_user(user_id):
            return Users.query.get(int(user_id))
        
        # 모든 blueprints를 등록(app/routes/__init__.py)
        from . import routes 
        routes.init_app(app)

        # from . import server_info
        # server_info.init_app(app)


        # 데이터베이스 테이블 생성
        db.create_all()

    return app