import os

from waitress import serve

import wsgi


PORT = int(os.environ.get("PORT", "8000"))


if __name__ == "__main__":
    serve(
        wsgi.application,
        port=PORT,
    )
