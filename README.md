# tephrasec.tech

The website of [Tephra](https://github.com/tephrasec/tephra): Hugo with the
[Hextra](https://github.com/imfing/hextra) theme for the docs, and a home page of its own
(`layouts/home.html`).

```sh
python3 scripts/rules.py ../tephra   # data/rules.json from a Tephra checkout
hugo server                          # http://localhost:1313
```

Pushes to `main` deploy to GitHub Pages (`.github/workflows/pages.yml`), which also rebuilds once a day so
the rules page follows Tephra's `main` branch.
