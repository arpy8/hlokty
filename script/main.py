from flask import Flask, Response

with open("./script/.sh", "r") as f:
    SHELL_SCRIPT = f.read()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return Response(SHELL_SCRIPT, mimetype="text/plain")

if __name__ == "__main__":
    app.run()