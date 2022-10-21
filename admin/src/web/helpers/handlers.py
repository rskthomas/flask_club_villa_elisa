from flask import render_template


def bad_request(e):
    """Returns a 400 error"""
    kwargs = {
        "error_name": "400 Bad Request",
        "error_description": "La solicitud no es valida",
    }
    return render_template("error.html", **kwargs), 400


def not_found_error(e):
    """Returns a 404 error"""
    kwargs = {
        "error_name": "404 Not Found Error",
        "error_description": "La url a la que quiere ingresar no existe",
    }
    return render_template("error.html", **kwargs), 404


def internal_server_error(e):
    """Returns a 500 error"""
    kwargs = {
        "error_name": "500 Internal Server Error",
        "error_description": "Error interno del servidor",
    }
    return render_template("error.html", **kwargs), 500
