import app
from config import get_config

if __name__ == '__main__':
    app = app.create_app(get_config())
    app.run(host='0.0.0.0', port=8000)
