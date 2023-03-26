from aiohttp.web import run_app

from backend.services.web.app import setup_app

if __name__ == "__main__":
    try:
        run_app(
            setup_app()
        )
    except KeyboardInterrupt:
        pass
