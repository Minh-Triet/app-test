import ma
from app import create_app

app = create_app()

if __name__ == '__main__':
    ma.ma.init_app(app)
    app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)
