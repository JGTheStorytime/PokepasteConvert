from flask import Flask, render_template, request
from converter import fetch_pokepaste, process_team

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    original = ""
    converted = ""
    error = ""

    if request.method == "POST":
        user_input = request.form.get("input")

        try:
            if "pokepast.es" in user_input:
                original = fetch_pokepaste(user_input)
            else:
                original = user_input

            converted = process_team(original)

        except Exception as e:
            error = str(e)

    return render_template(
        "index.html",
        original=original,
        converted=converted,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)