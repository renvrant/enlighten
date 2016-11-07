## Enlighten (Hey, it's a working title...)

Simple python app made for the purpose of sharing stories with others
about difficulties and transgressions that minority groups experience in
the work place. The goal of this project is to raise awareness for people
about the challenges that minority groups experience
(and hopefully to inspire change).

### Setting up

This project uses PostgreSQL, SQLite (for test env), and python with Flask. You'll
need to have these things installed locally in order to run the project.



Start by cloning this repo
```bash
git clone https://github.com/riavalon/enlighten.git
```

Navigate to the project directory and create a virutal environment
```bash
virtualenv env/
```

Activate the environment (there are different activate scripts depending on which shell you use. Ex: zsh, fish, etc)
```bash
source env/bin/activate
```

Note: if you have trouble running python sourced to the virtual env despite having the environment activated, you can run
it directly like `./env/bin/python`, `./env/bin/pip`

Install the requirements
```bash
pip install -r requirements.txt
```

At this point the only thing left to do is start postgresql and create a database to work with locally:

`http://postgresapp.com/` or `brew install postgres` will instal PostgreSQL for you. You can then run:
```bash
$ psql postgres
$ CREATE USER username WITH PASSWORD 'password'
$ CREATE DATABASE enlightendb WITH OWNER username
```

Edit `config-sample.py` with the url for the postgres database, username, password, etc and save it as `config.py`.

You can run the app with
```bash
python run.py
```


#### Creating a Moderator to use

If you don't have a moderator created for yourself yet, you'll need to do so from the console. (there is no way
to 'sign up' as a mod from the app... another moderator must make an account for you.) To start shell, run `python` (or  `env/bin/python` if you have trouble running in virtual env)

```python
# Import the moderator model and the database object
from app import db
from app.Moderator.models import Moderator

# Create a new moderator (name, email, password)
me = Moderator.create('raven', 'raven@example.com', 'super_secure')

# Commit moderator to the database
db.session.add(me)
db.session.commit()
```

You can save the above snippet and run it in your environment. The moderator account should be ready to go!

### Running tests

If you've followed the previous steps for getting the project setup, you should just be able to run this command while in your activated virtual environment

```bash
nosetests
```

If you're having trouble running this command despite being in your virtual env, you may have to run this command directly like the others:

```bash
env/bin/nosetests
```

Use the `-s` flag in order to see any stdout to the console. This is useful if you're using print statements or (preferably) pdb to do some debugging with your tests

```python
# Some test
def test_that_it_works(self):
    import pdb; pdb.set_trace()  # start interactive debugger here
    a = 2 + 2
    self.assertEqual(a, 4)
```

```bash
env/bin/nosetests -s
```

### Contributing

If you find any issues running the project, have some ideas for how to improve it, or any other kind
of feedback, please open an issue on this repository and tag the issue appropriately (feature-request, bug, feedback, etc).
