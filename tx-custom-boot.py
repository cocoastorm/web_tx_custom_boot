import click
import hekate

# TODO: wtf do i do here?
releases = []

def init():
  h = hekate.GithubHekate()
  releases = h.list_named_hekate_releases()

  def by_name_version(r):
    return r["name"]
  
  releases.sort(key=by_name_version, reverse=True)

  return releases

def ls():
  click.echo("Hekate Releases:")
  for n, r in enumerate(releases, start=1):
    click.echo(f" {n}: #{r['id']} {r['name']}")

@click.command()
@click.option('-o', '--output', type=click.File('wb'))
def build(output):
  choice = click.prompt('Please enter your the release you want (#)', type=int)

  try:
    release = releases[choice - 1]
  except:
    click.echo('invalid selection')

  if output:
    hekate.build(release['id'], output)
  else:
    boot = hekate.build(release['id'])
    click.echo(f"boot.dat: {boot}")

if __name__ == '__main__':
    releases = init()
    
    ls()
    build()
