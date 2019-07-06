import flask
import datetime
import time
import hekate
from .builder import CachedBuilder

app = flask.Flask(__name__)

@app.route('/')
def index():
  h = hekate.GithubHekate()
  releases = h.list_named_hekate_releases()

  return flask.render_template('index.html', releases=releases)

def limit_download():
  now_unix = time.time()

  if not 'downloads' in flask.session or flask.session['downloads'] is None:
    flask.session['downloads'] = 0
  
  if not 'date_last_access' in flask.session or flask.session['date_last_access'] is None:
    flask.session['date_last_access'] = str(now_unix)

  downloads = flask.session['downloads']
  date_last_access = flask.session['date_last_access']

  last_unix = float(date_last_access)

  now_dt = datetime.date.fromtimestamp(now_unix)
  last_dt = datetime.date.fromtimestamp(last_unix)
  date_difference = now_dt.day - last_dt.day

  num_downloads = int(downloads)

  # reset condition
  if date_difference > 0:
    flask.session['downloads'] = 0
    flask.session['date_last_access'] = None

    return 0, False

  # limit exceeded
  if num_downloads >= 5 or date_difference < 0:
    return num_downloads, True

  # increment count
  flask.session['downloads'] = num_downloads + 1

  if not flask.session['date_last_access']:
    flask.session['date_last_access'] = str(now_unix)

  return num_downloads, False

@app.route('/download')
def build_download():
  version = flask.request.args.get('version')

  if version is None:
    return flask.abort(404)

  num_downloads, is_reject = limit_download()

  if is_reject:
    flask.flash(f'Uh oh! Limit has been reached! ({num_downloads})')
    return flask.redirect(flask.url_for('index'))

  try:
    r_id = int(version)
    boot_file = CachedBuilder().get(r_id)

    if boot_file:
      return flask.send_file(str(boot_file), as_attachment=True, attachment_filename="boot.dat")
    else:
      flask.flash('Uh oh! Version was not found!')
      return flask.redirect(flask.url_for('index'))
  except:
    flask.flash('Uh oh! An unexpected error occurred!')
    return flask.redirect(flask.url_for('index'))