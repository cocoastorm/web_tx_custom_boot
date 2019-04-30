from setuptools import setup

setup(
  name="tx_custom_boot_cli",
  version='0.1',
  py_modules=['tx_custom_boot_cli'],
  install_requires=[
    'PyGithub',
    'Click',
  ],
  entry_points='''
    [console_scripts]
    tx_custom_boot_cli=tx_custom_boot_cli:build
  ''',
)
