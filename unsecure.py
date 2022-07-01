from flask import Flask, jsonify, render_template, make_response, request, send_from_directory
import uuid
import hmac

app = Flask(__name__)
app.jinja_env.cache = None

# from flask_wtf.csrf import CSRFProtect
# TODO: CSRF
# SECRET_KEY = os.urandom(32)
# app.config['SECRET_KEY'] = SECRET_KEY
# csrf = CSRFProtect(app)

# =*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=* #
#                                                                  #
# /!\ Pour ajouter une en-tête:                                    #
# response = make_response(render_template('template.html'))       #
# response.headers['MY_HEADER'] = 'value'                          #
# return response                                                  #
#                                                                  #
# =*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=* #


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/cookie-stealing")
def cookie_stealing():
    response = make_response(render_template('cookie-stealing.html'))
    # See https://tedboy.github.io/flask/generated/generated/flask.Response.set_cookie.html
    response.set_cookie('SESSION_ID', str(uuid.uuid4()), httponly=False)
    return response


@app.route("/cookie-secure")
def cookie_secure():
    response = make_response(render_template('cookie-secure.html'))
    response.set_cookie('SECURE_SESSION_ID', str(uuid.uuid4()), secure=None)
    return response


@app.route("/restricted/cookie-scope")
def cookie_scope():
    response = make_response(render_template('restricted/cookie-scope.html'))
    response.set_cookie('RESTRICTED_SESSION_ID', str(uuid.uuid4()))
    return response


@app.route("/cookie-same-site")
def cookie_same_site():
    response = make_response(render_template('cookie-same-site.html'))
    response.set_cookie('SAMESITE_SESSION_ID', str(uuid.uuid4()))
    return response


@app.route("/cookie-scope-attack")
def cookie_scope_attack():
    session_id = request.cookies.get('RESTRICTED_SESSION_ID')
    if session_id is None:
        result = "Je n'arrive plus à lire le cookie!"
    else:
        result = f"Je peux lire le cookie et c'est {session_id}!"
    return render_template('cookie-scope-attack.html', result=result)


@app.route("/csrf-token")
def csrf_token():
    response = make_response(render_template('csrf-token.html'))
    response.set_cookie('SESSION_ID_CSRF', str(uuid.uuid4()))
    return response


@app.route("/csrf-token/transfer-money/account/attacker")
def csrf_token_transfer_money():
    return {
        "from": "account",
        "to": "attacker",
        "status": "transfer done!"
    }


@app.route("/csrf-token/transfer-money")
def POST_csrf_token_transfer_money():
    from_account = request.form.get("from")
    to_account = request.form.get("to")
    return {
        "status": "transfer done!",
        "from": from_account,
        "to": to_account
    }


SECRET = b"s3cr3t"


@app.route("/csrf-double-submit", defaults={'token': None})
@app.route("/csrf-double-submit/<token>", methods=['GET', 'POST'])
def csrf_double_submit(token):
    h = hmac.new(SECRET, digestmod='sha256')
    if request.method == 'GET':
        new_token = str(uuid.uuid4())
        h.update(new_token.encode('utf-8'))
        response = make_response(render_template(
            'csrf-double-submit.html', token=new_token, result=""))
        response.set_cookie('SESSION_ID_CSRF', h.hexdigest())
        return response

    result = 'Failure'
    if token is not None:
        cookie_token = request.cookies['SESSION_ID_CSRF']
        h.update(token.encode('utf-8'))
        print("Comparing")
        print(cookie_token)
        print(h.hexdigest())
        if hmac.compare_digest(
                cookie_token, h.hexdigest()):
            result = 'Success'
    return render_template('csrf-double-submit.html', token="", result=result)


@app.route("/xss-injection")
def xss_injection():
    content = "Content" if "q" not in request.args else request.args["q"]
    return render_template('xss-injection.html', content=content)


@app.route("/css-injection")
def css_injection():
    return render_template('css-injection.html')


@app.route("/cdn-hacked")
def cdn_hacked():
    return render_template('cdn-hacked.html')


@app.route("/trusted-types")
def trusted_types():
    content = "<script>alert('XSS in progress...')</script>" if "unsecure" not in request.args else request.args[
        "unsecure"]
    return render_template('trusted-types.html', content=content)


@app.route("/hsts")
def hsts():
    return render_template('hsts.html')


@app.route("/certificate-transparency")
def certificate_transparency():
    return render_template('certificate-transparency.html')


@app.route("/corb")
def corb():
    return render_template('corb.html')

@app.route("/coop")
def coop():
    response = make_response(render_template('coop.html'))
    response.headers['Cross-Origin-Opener-Policy'] = 'unsafe-none'
    # response.headers['Cross-Origin-Embedder-Policy'] = '???'
    return response 

# UTILS


@app.route("/random")
def random():
    return jsonify({"random": str(uuid.uuid4())})


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)
