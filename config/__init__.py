class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@localhost"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
