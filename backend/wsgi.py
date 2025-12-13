import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Useful for `docker run` without gunicorn
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 5002))
    app.run(host=host, port=port, debug=False)
