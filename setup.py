from distutils.core import setup

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="Tocco",
    version="0.1dev",
    url="http://github.com/synchronizing/Tocco",
    author="Felipe Faria",
    author_email="me@felipefaria.me",
    license="MIT",
    packages=["tocco"],
    install_requires=required,
    zip_safe=False,
)
