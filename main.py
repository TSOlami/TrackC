from webapp import create_app
from flask import Flask

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
    