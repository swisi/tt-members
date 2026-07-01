import os
import sys
from pathlib import Path

import pytest


@pytest.fixture()
def app():
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    os.environ.setdefault('SECRET_KEY', 'test-secret')
    os.environ.setdefault('SQLALCHEMY_DATABASE_URI', 'sqlite:///:memory:')
    os.environ.setdefault('INTERNAL_API_SECRET', 'test-internal-secret')
    os.environ.setdefault('AUTO_CREATE_DB', 'true')

    from app import create_app

    app = create_app()
    app.config.update(TESTING=True)
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
