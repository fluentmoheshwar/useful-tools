# Contribution Guidelines of Useful Tools for Windows

## Getting started

### Issues

#### Create a new issue

If you spot a problem with the docs, [search if an issue already exists](https://docs.github.com/en/github/searching-for-information-on-github/searching-on-github/searching-issues-and-pull-requests#search-by-the-title-body-or-comments). If a related issue doesn't exist, you can open a new issue using a relevant [issue form](https://github.com/fluentmoheshwar/useful-tools/issues/new/choose).

#### Solve an issue

Scan through our [existing issues](https://github.com/fluentmoheshwar/useful-tools/issues/) to find one that interests you. You can narrow down the search using `labels` as filters. If you find an issue to work on, you are welcome to open a PR with a fix.

### Make Changes

Following dependencies are needed to build this app.

-   [Node.js](https://nodejs.org/) >= 16
-   [Python](https://www.python.org/) >= 3.10 (Microsoft Store version will work too)
-   [Inno Setup](https://jrsoftware.org/isinfo.php) >= 6.2.0 (Not Required for running dev build)
-   [pnpm](https://pnpm.io/)

For some reason inno setup don't add itself to path. Add this to path
`C:\Program Files (x86)\Inno Setup 6`

Then create venv using:

```powershell
python -m venv .venv
```

Then activate venv using:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install wheel to avoid errors and get better performance (optional)

```powershell
pip install wheel
```

Then install all dependencies using:

```powershell
pip install -r requirements.txt && pnpm install
```

Running development version:

```powershell
pnpm dev
```

Building:

```powershell
pnpm build
```
