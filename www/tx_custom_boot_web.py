import flask
import hekate
from .builder import CachedBuilder

app = flask.Flask(__name__)

@app.route('/')
def index():
  h = hekate.GithubHekate()
  releases = h.list_named_hekate_releases()
  return flask.render_template('index.html', releases=releases)

@app.route('/download')
def build_download():
  version = flask.request.args.get('version')

  if version is None:
    return flask.abort(404)

  cb = CachedBuilder()
  bf = cb.get(int(version))

  if bf:
    return flask.send_file(str(bf), as_attachment=True, attachment_filename="boot.dat")
  else:
    return flask.abort(404)
