import sys
sys.path.append('backend')
import app
app.app.testing = True
client = app.app.test_client()
response = client.get('/api/projetos/test_codigo')
print("Status Code:", response.status_code)
print("Data:", response.get_json())
