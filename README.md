# Telegram Knowledge Base Bot

## Commands

`/def term here goes long term definition with links etc.`

_Bot saves definition in the database per channel with username of user executing the command_

`/wtf term`

_Bot outputs definition along with nick of the user who defined it_

`/list`

_Bot outputs all definitions_

`/rm term`

_Bot removes definition if it exists_

## Proposed features

* Admins of a channel should be able to override and remove definitions of other users
* Bot should be able to fetch markdown pages from a specified GitHub repository
* Optional ability to share (import) terms between channels

## Development

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