import flask
import hekate

app = flask.Flask(__name__)

@app.route('/')
def index():
  h = hekate.GithubHekate()
  releases = h.list_named_hekate_releases()
  return flask.render_template('index.html', releases=releases)

@app.route('/download')
def build_download():
  resp = flask.make_response('To Be Implemented', 501)
  return resp
