# birda-prototypes → redirect only

This repo contains no prototypes. It exists so that links shared before the
move keep working.

The prototypes are now served from the internal web app, at:

    https://internal-web-birda.vercel.app/design-prototypes/

That host sits behind the app's login. Signing in returns you to the path you
asked for, so a forwarded deep link still lands on the right prototype.

GitHub redirects repository URLs after a transfer, but **not GitHub Pages
URLs** — so every link of the form

    https://ellenbuilds.github.io/birda-prototypes/<path>

broke. Recreating a repo under the old name lets its Pages site answer those
URLs and forward each one to the matching page on the new site.

## How it works

- **A stub at every real page path.** These return HTTP 200 and redirect with
  a `<meta http-equiv="refresh">`, so they work with JavaScript disabled and
  are followed by link unfurlers and crawlers. A script tag redirects sooner
  where JS is available, and carries any `?query` / `#hash` across.
- **`404.html` as a catch-all.** GitHub Pages serves it for any unmatched
  path; it rebuilds the path under the new site in JS. This covers deep asset
  links, directory URLs and anything not stubbed.

## Changing it

Edit `build.py` and re-run it — every HTML file here is generated:

    python3 build.py

`PAGES` lists the paths that get their own stub. Nothing else needs editing;
the catch-all handles the rest.

## When this can be retired

Once the old links have aged out of Slack, Linear and anywhere else they were
shared. There's no rush — the whole thing is a few KB.
