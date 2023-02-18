# birthdays-today
Who should you sing Happy Birthday to (twice) while washing your hands?
[singtowho.site](https://singtowho.site)


# Development

## Installation

Must have `pip-tools` installed in your environment (suggestion: `pipx install pip-tools`).  Suggest running a virtualenv, or doing everything by Docker container.

```
pip-sync requirements.txt
```

## Updating dependencies

```
pip-compile --generate-hashes requirements.in
```
