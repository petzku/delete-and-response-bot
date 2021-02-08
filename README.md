# Delete-and-Response Bot

Simple discord bot, which deletes users' messages and warns them based on certain conditions.

## Usage

The bot needs a recent version of Python 3 (>=3.5) to work. The latest version is recommended (3.9 at the time of writing).

To use, first install the dependencies from `requirements.txt` using `pip`:

```
$ pip install -r requirements.txt
```

Note that you may need to use `pip3` or `python3 -m pip install ...` instead.

Copy the `config.py.sample` file to `config.py`, and set the options as you wish. `TOKEN` should be your bot token, which you can get from the [Discord Developer Portal][dev-portal].

Then simply run the `main.py` file:

```
$ python3 main.py
```

[dev-portal]: https://discord.com/developers/applications
