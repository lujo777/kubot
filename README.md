# Kubot
Nice foundation for bot using [kutana](https://github.com/ekonda/kutana/)
engine.

## Installation
- Download and install python (3.5.3+)

```
https://www.python.org/downloads/
```

- Install required modules (use python3 if needed)

```
python -m pip install -r requirements.txt
```

- Copy `config.json.example` and rename it to `config.json`. Enter your tokens
    into lists of tokens for your service.

```
...
    "tokens": {
        "vkontakte": [
            "YOUR VK GROUP API TOKEN"
        ]
    }
...
```

## Run
- Run file `run.py` with python (use python3 if needed)

```
python run.py
```

## Authors
- **Michael Krukov** - [@michaelkrukov](https://github.com/michaelkrukov)
- [Other contributors](CONTRIBUTORS.md)
