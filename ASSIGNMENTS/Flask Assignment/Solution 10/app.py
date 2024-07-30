from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "Welcome to the Home Page!"

    @app.route('/cause_500')
    def cause_500():
        # This route is intentionally set up to cause a 500 error
        return 1 / 0

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
