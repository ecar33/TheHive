from flask import render_template

def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template('errors/405.html'), 405

    @app.errorhandler(429)
    def too_many_requests(e):
        return render_template('errors/429.html', error=e), 429

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500