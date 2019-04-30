import click
import hekate

def ls(releases):
  click.echo("Hekate Releases:")
  for n, r in enumerate(releases, start=1):
    click.echo(f" {n}: #{r['id']} {r['name']}")

@click.command()
@click.option('-o', '--output', type=click.File('wb'))
def build(output):
  # github asset releases
  h = hekate.GithubHekate()
  releases = h.list_named_hekate_releases()
  
  # list out the releases with indexed numbers
  ls(releases)

  # let user pick the version they want
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
  build()
