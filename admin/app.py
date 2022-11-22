from src.web import create_app
from pathlib import Path
from os import environ
from flask_wtf.csrf import CSRFProtect

static_folder = Path(__file__).parent.joinpath("public")
app = create_app(static_folder)
app.secret_key = environ.get("FLASK_SECRET_KEY", "this is just a secret")



def main():
    app.run()


if __name__ == "__main__":
    main()
