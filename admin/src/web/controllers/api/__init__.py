from flask import current_app

ALLOWED_ORIGIN = "http://localhost:3000"

"""If a request is a simple one i.e. GET or POST with no fancy header (Content-Type), 
the browser will not send a preflight OPTIONS request (CORS specification) and everything works alright. 
Should a front end request not be simple, headers to the response of the OPTIONS request should be added,
like the ones below """

OPTIONS_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": ALLOWED_ORIGIN,
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Max-Age": "86400",
}

def apply_CORS(response):
    """Sets CORS headers for the main API endpoints."""
    
    if current_app.config["ENV"] == "development":
        print("CORS headers applied")
        response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Content-Type"] = "application/json"
    
    return response