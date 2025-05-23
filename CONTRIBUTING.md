# Contribution Guidelines of Useful Tools for Windows

## Issues

### Create a new issue

If you spot a problem with the docs, [search if an issue already exists](https://docs.github.com/en/github/searching-for-information-on-github/searching-on-github/searching-issues-and-pull-requests#search-by-the-title-body-or-comments).
If a related issue doesn't exist,
you can open a new issue using a relevant [issue form](https://github.com/fluentmoheshwar/useful-tools/issues/new/choose).

### Solve an issue

Scan through our
[existing issues](https://github.com/fluentmoheshwar/useful-tools/issues/)
to find one that interests you.
You can narrow down the search using `labels` as filters. If you find an issue to
work on, you are welcome to open a PR with a fix.

## Make Changes

Following dependencies are required to build this app.

- [Python](https://www.python.org/) >= 3.10
  (Microsoft Store version will work as well)
- [Inno Setup](https://jrsoftware.org/isinfo.php) >= 6.2.0
  (only required to build installer)
- [upx](https://upx.github.io/) (optional)
- [bun](https://bun.sh)
- [uv](https://github.com/astral-sh/uv)

Then create venv using:

```powershell
python -m venv .venv
```

Then activate venv using:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then install all dependencies using:

```powershell
uv pip install -r requirements.txt && bun install
```

Running development version (UI only):

```powershell
bun dev
```

Building:

```powershell
build.bat
```
