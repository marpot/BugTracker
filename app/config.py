class Config:
    # Flask Configuration
    SECRET_KEY = 'your_secret_key_here'
    DEBUG = True  # Set to False in production
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///your_database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail Configuration (if you plan to use email functionality)
    # MAIL_SERVER = 'smtp.example.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USE_SSL = False
    # MAIL_USERNAME = 'your_username'
    # MAIL_PASSWORD = 'your_password'

    # Custom Application Configuration
    # Add any other custom configuration options here
