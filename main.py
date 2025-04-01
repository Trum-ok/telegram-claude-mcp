import os

from app.web.app import setup_app

HOST="127.0.0.1"
PORT=8001

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        setup_app(
            config_path=os.path.join(os.path.dirname(__file__), ".env")
        ),
        host=HOST,
        port=PORT
    )
