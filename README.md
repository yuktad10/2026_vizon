# The Composers: A Duet of Names — Streamlit deploy

A VizCon 2026 data story. Two parent-composers, **Aria** (the global voice, blue) and
**Cormac** (the local voice, purple), argue in data visuals over naming their newborn,
then write one song together. The experience is a static site of seven sheets stitched
by `flow.html`; this folder wraps it so it runs on Streamlit (including Streamlit
Community Cloud).

## How it works

The whole story is plain HTML/CSS/JS under [`static/`](static/):

```
static/
  flow.html        # stitches the 7 sheets into one scroll via <iframe>s
  cover.html  score.html  orchestra.html  aria.html
  cormac.html  quiz.html  encore.html
  lookup.json      # 16,452-name database (aria.html / cormac.html fetch this)
  assets/          # images, cutouts, audio (.mp3/.wav), certificate.png
```

`streamlit_app.py` does two things:

1. Turns on Streamlit **static file serving** (`server.enableStaticServing = true` in
   `.streamlit/config.toml`), which exposes `./static` as real files at
   `/app/static/<path>`.
2. Embeds `flow.html` in a single full-viewport `<iframe>` pointed at that origin.

Because the sheets are served as real files (not inlined), every relative path works
exactly as under `python -m http.server`: the sub-iframes load, `fetch('lookup.json')`
resolves, audio plays, and the encore's certificate `<canvas>` draws.

### The one sizing subtlety

Each sheet is `height:100vh`. Inside a nested iframe, `100vh` resolves against **that
iframe's** height, not the browser window. So `streamlit_app.py` pins the component
iframe to `100vh` (via injected CSS) and lets `flow.html` scroll internally. Then one
sheet == one real screen. If you instead give the component a tall fixed height, every
sheet balloons to that height and floats in empty space — don't do that.

## Run locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Open http://localhost:8501. You should land on the cover; scroll through
cover -> score -> orchestra -> aria -> cormac -> quiz -> encore. In the encore, pick a
sex then a first + middle name, and "Get the certificate" to see the canvas certificate.

The standalone build still works without Streamlit too:

```bash
cd static && python3 -m http.server 8520   # then open /flow.html
```

## Push to GitHub

This folder is already a git repo with one commit. Point it at your new empty GitHub repo
and push:

```bash
git remote add origin https://github.com/<you>/<repo>.git
git branch -M main
git push -u origin main
```

Or, without git: on github.com create a repo, click **Add file -> Upload files**, and drag
in everything from this folder (the files must land at the repo root, i.e. `streamlit_app.py`
and `requirements.txt` at the top level, `static/` and `.streamlit/` as folders).

## Deploy to Streamlit Community Cloud

1. Push this folder to a GitHub repo (keep `static/`, `.streamlit/`, `streamlit_app.py`,
   and `requirements.txt` together at the repo root, or note the subpath in step 3).
2. Go to https://share.streamlit.io and sign in with GitHub.
3. **New app** -> pick the repo/branch, set **Main file path** to `streamlit_app.py`
   (prefix with the subfolder if this isn't at the repo root).
4. Deploy. `.streamlit/config.toml` (with `enableStaticServing = true`) is picked up
   automatically, so `/app/static/...` serves the story with no extra setup.

> Note: `static/` is ~9 MB (mostly `lookup.json` and audio). That's fine for Community
> Cloud. Git LFS is not required.

## Editing the story

Edit the canonical build in `../composers-duet-v3/`, then re-sync the copy here:

```bash
./sync_static.sh                 # defaults to ../composers-duet-v3
./sync_static.sh /path/to/build  # or point it elsewhere
```

## Conventions (for future edits)

- Fonts: Caveat (display), Quicksand (body), Fraunces (serif italic labels).
- Blue = Aria / global; purple = Cormac / local.
- No em dashes in copy. Each sheet fits one screen. The baby is never gendered in prose
  (only the Girl/Boy toggle in the encore game).
