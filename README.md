# ssh-management

Either use manage.sh wrapper which will log command history or directly use manage.py.
```bash
Usage: manage.py [command] (options)

Note: all commands expect list write to a file: newauth which you can update authorized_keys with afterwards.

Commands and options:
  list - show list of keys, their id, enabled/disabled and expiry.
  export - print how authorized_keys should appear considering expiry and enabled/disabled.
  delete [id] - delete a key by id.
    e.g. manage.py delete bakersl
  add [id, public key, expiry (yyyy-MM-dd)] - Add a key with an id and expiry.
    e.g. manage.py add bakersl "AAAAB3NzaC1yc2EA...vIuuRniQ==" 2020-01-01
  enable [id] - enable a key by id.
    e.g. manage.py enable bakersl
  disable [id] - disable a key by id.
    e.g. manage.py disable bakersl
```

TODO: make update.sh able to update authorized_keys file that could be in multiple locations.
