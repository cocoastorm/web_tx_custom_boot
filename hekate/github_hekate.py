from github import Github
import urllib.request
import tempfile
import shutil
import os

class GithubHekate():
  def __init__(self, github_token=""):
    if github_token == "":
      github_token = os.environ["GITHUB_TOKEN"]

    self.g = Github(github_token)

  def get_hekate(self):
    repo = self.g.get_repo("CTCaer/hekate")
    return repo

  def list_hekate_releases(self):
    hekate = self.get_hekate()
    releases = hekate.get_releases()
    return releases

  def list_named_hekate_releases(self):
    releases = self.list_hekate_releases()
    return [{'id': r.id, 'name': r.tag_name} for r in releases]
  
  def get_release_assets(self, id):
    hekate = self.get_hekate()
    release = hekate.get_release(id)
    return release.get_assets()

  def get_archive_asset(self, id):
    assets = self.get_release_assets(id)

    for asset in assets:
      if ".zip" in asset.name:
        return asset
    
    return None

  def get_download_archive(self, id):
    archive_asset = self.get_archive_asset(id)
    
    with urllib.request.urlopen(archive_asset.browser_download_url) as response:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
          shutil.copyfileobj(response, tmp_file)
          return tmp_file.name
