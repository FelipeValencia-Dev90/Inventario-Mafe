from flask import jsonify


def configurar_errores(app):

    @app.errorhandler(404)
    def error_404(error):

        return jsonify({
            "success": False,
            "mensaje": "Ruta no encontrada"
        }), 404


    @app.errorhandler(500)
    def error_500(error):

        return jsonify({
            "success": False,
            "mensaje": "Error interno del servidor"
        }), 500


    @app.errorhandler(403)
    def error_403(error):

        return jsonify({
            "success": False,
            "mensaje": "Acceso prohibido"
        }), 403