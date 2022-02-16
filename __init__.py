from flask import Flask

# application factory


def create_app():
    app = Flask(__name__, template_folder='templates')

    from sec3_app.routes import bp
    app.register_blueprint(bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
