# Varun — seat 28 daily briefing

`briefing.py` reads Suryodaya and Keystone and prints:

- unread inbox mail that is not a draft and not already answered, with a proposed reply that is not saved
- meetings that overlap today in IST, excluding cancelled events
- open tasks whose due date is before today

It never calls send, reply, create, or booking tools. Tokens stay in this folder as `.token.suryodaya` and `.token.keystone`. The written briefing stays in `briefings/`. Both are ignored by `28-ea/varun/.gitignore`.

```bash
python3 28-ea/varun/briefing.py
python3 -m unittest discover -s 28-ea/varun -p 'test_*.py'
```
