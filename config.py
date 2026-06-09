class Config:
    SECRET_KEY = 'ifri-mentorlink-secret-key-2026'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mentorlink.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SOCKETIO_ASYNC_MODE = 'eventlet'
    SOCKETIO_CORS_ALLOWED_ORIGINS = '*'
