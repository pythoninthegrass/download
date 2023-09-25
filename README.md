# download

[**Download**](https://www.youtube.com/watch?v=T5jHO4jMPxA)  
<img src="static/sfa_radiator.png" width="300">

## Summary
Feed `requests` a URL, extension, and local directory to download files scraped from a website.

Cache initial response to avoid too many requests to server.

**Table of Contents**
* [download](#download)
  * [Summary](#summary)
  * [Setup](#setup)
  * [Quickstart](#quickstart)
  * [Development](#development)
  * [TODO](#todo)
  * [Further Reading](#further-reading)

## Setup
* Dependencies
  * make
    * [Linux](https://www.gnu.org/software/make/)
    * [macOS](https://www.freecodecamp.org/news/install-xcode-command-line-tools/)
  * [editorconfig](https://editorconfig.org/)
* Install python and tooling
    ```bash
    # install python and dependencies (e.g., git, ansible, etc.)
    ./bootstrap install
    ```

## Quickstart
```bash
# run script with defaults
./main.py

# add environment variables for url, ext, and path
cp .env.example .env

# fill out (e.g., 'EXT=".csv"')

# run with overrides
./main.py
```

## Development
```bash
# install tools and runtimes (cf. xcode, brew, asdf, poetry, etc.)
./bootstrap <run|run-dev>   # dev only runs plays w/tags and is verbose

# install git hooks
./bootstrap install-precommit

# update git hooks
./bootstrap update-precommit
```

## TODO
* [Open Issues](https://github.com/pythoninthegrass/download/issues)

## Further Reading
* [python](https://www.python.org/)
* [asdf](https://asdf-vm.com/guide/getting-started.html#_2-download-asdf)
* [poetry](https://python-poetry.org/docs/)
* [docker-compose](https://docs.docker.com/compose/install/)
* [pre-commit hooks](https://pre-commit.com/)
