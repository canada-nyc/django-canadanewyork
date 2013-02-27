import os

from waitress import serve

import manage


PORT = int(os.environ.get("PORT", 5000))


if __name__ == "__main__":
    serve(
        manage.application,
        port=PORT,
    )
