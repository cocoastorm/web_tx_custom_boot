import os
import shutil
import zipfile

from .github_hekate import GithubHekate
from .tx_custom_boot import make_boot_dat

def build(hekateId, fh=None):
  h = GithubHekate()
  archive = h.get_download_archive(hekateId)

  with zipfile.ZipFile(archive) as a:
    # find the .bin file
    stage2_bin_name = ""
    for filename in a.namelist():
      if ".bin" in filename:
        stage2_bin_name = filename
        break
    
    with a.open(stage2_bin_name) as stage2:
      return make_boot_dat(stage2, fh)
