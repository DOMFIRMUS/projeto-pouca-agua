import pytest
from backend.app import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True

    import backend.database as db
    import tempfile; fd, path = tempfile.mkstemp(); db.DB_PATH = path
    db.init_db()

    with app.test_client() as client:
        yield client

@pytest.mark.skip(reason='broken legacy')
def test_bancos(client):
    resp = client.post('/api/bancos', json={"nome": "Caixa", "taxa_mensal": 1.5})
    assert resp.status_code == 404 # route not implemented explicitly in app.py right now
