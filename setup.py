from setuptools import find_packages, setup

setup(
  name="tx_custom_boot",
  version='0.1',
  packages=find_packages(),
  include_package_data=True,
  zip_safe=False,
  install_requires=[
    'Click',
    'Flask',
    'PyGithub',
  ],
  entry_points={
    "console_scripts": ["tx_custom_boot_cli=cli.tx_custom_boot_cli:build"],
  },
)
