import hekate
import json
import pathlib
import uuid

class CachedBuilder():
  def __init__(self):
    self.src = pathlib.Path("./www/data/builds.json").resolve()
    with open(self.src, 'r') as src:
      self.builds = json.load(src)

  def _save(self):
    with open(self.src, 'w') as f:
      json.dump(self.builds, f)

  def _build(self, release_id):
    id = str(uuid.uuid4())
    filename = id + ".dat"
    filepath = pathlib.Path("./www/data/" + filename).resolve()

    with open(str(filepath), 'wb') as f:
      hekate.build(release_id, f)
    
    return filepath
  
  def get(self, release_id):
    cache_build = self.builds.get(release_id)

    if cache_build:
      return cache_build

    build = self._build(release_id)

    self.builds[release_id] = str(build)
    self._save()

    return build