# sdks

Repository with public SDKs of Blockchain venues
currently integrating with "Paradigm Co.".

## Development

To contribute to this package you may set up a dedicated container:

```bash
$ git clone git@github.com:tradeparadigm/sdks.git
$ cd ribbon
$ pwd
[...]/sdks/ribbon

# open a container with python
$ docker run -it --rm \
    -v $(pwd):/tmp/code -w /tmp/code \
    -p 8888:8888 \
    python:3.10 \
    bash

# install the library in development mode
pip3 install -e /tmp/code

# run code that accesses the ribbon sdk, e.g.
python3 test.py

# optional: add and use ipython/jypiter
pip3 install ipython jupyter
jupyter notebook --allow-root --no-browser --ip=0.0.0.0
# now browse the http://127.0.0.1:8888/?token=... link in the output
```

### Code guidelines

To improve quality and readibility of code,
please make sure to use `pre-commit` hooks.

Either execute `pre-commit run` before pushing the final version of your
pull request, or `pre-commit install` to have automatic checks before
each commit.
