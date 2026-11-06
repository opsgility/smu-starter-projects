"""Meridian Devworks greeter — a tiny Flask app used during onboarding
demos and the warehouse-floor status board.

Author convention check: `app_name` here is leaking into the welcome
copy. The team's naming guideline switched to `service_name` three
months ago but this file never got updated. Rename it in-place.
"""

import logging

from flask import Flask

app = Flask(__name__)

app_name = "meridian-greeter"


@app.route("/")
def home() -> str:
    logging.info("home page served for %s", app_name)
    return (
        f"<h1>Welcome to {app_name}</h1>"
        f"<p>Hello from Meridian Devworks!</p>"
        f"<p><small>Service: {app_name}</small></p>"
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(f"[meridian] starting {app_name} on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000)
