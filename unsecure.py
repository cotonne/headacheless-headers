from flask import Flask, jsonify, render_template, make_response, request, send_from_directory
import uuid

app = Flask(__name__)
app.jinja_env.cache = None


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/cookie-stealing")
def cookie_stealing():
    response = make_response(render_template('cookie-stealing.html'))
    response.set_cookie('SESSION_ID', str(uuid.uuid4()))
    return response


@app.route("/restricted/cookie-scope")
def cookie_scope():
    response = make_response(render_template('restricted/cookie-scope.html'))
    response.set_cookie('RESTRICTED_SESSION_ID', str(uuid.uuid4()))
    return response


@app.route("/cookie-scope-attack")
def cookie_scope_attack():
    session_id = request.cookies.get('RESTRICTED_SESSION_ID')
    if session_id is None:
        result = "Je n'arrive plus à lire le cookie!"
    else:
        result = f"Je peux lire le cookie et c'est {session_id}!"
    return render_template('cookie-scope-attack.html', result=result)


@app.route("/css-injection")
def css_injection():
    return render_template('css-injection.html')


@app.route("/cdn-hacked")
def cdn_hacked():
    return render_template('cdn-hacked.html')


# UTILS
@app.route("/random")
def random():
    return jsonify({"random": str(uuid.uuid4())})


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)
