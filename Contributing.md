Clone this repo. Install dependencies with `pip install -r requirements.txt`. It's better to use virtualenv.

### Database update

Current database is placed in `bot.sqlite`. Models are defined in `models.py` via SQLAlchemy.

In case of updating models it's necessary to run migration with Alembic package.

```
alembic revision --autogenerate -m "Revision description bla-bla"
alembic upgrade head
``` 

You can see migration history with:
```
alembic history --verbose
```

Do not forget to commit files which are in `alembic` dir
