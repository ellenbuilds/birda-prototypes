#!/usr/bin/env python3
"""Generate the redirect site that stands in for the old Pages URL.

The prototypes moved from ellenbuilds/birda-prototypes to
ChirpBirding/design-prototypes. GitHub redirects repo URLs after a transfer but
NOT Pages URLs, so every link shared as

    https://ellenbuilds.github.io/birda-prototypes/<path>

went dead. Recreating a repo at the old name lets its Pages site answer those
URLs and forward each one to its equivalent under

    https://chirpbirding.github.io/design-prototypes/<path>

Two layers, deliberately:

  * a stub at every real page path, so those get HTTP 200 and redirect with no
    JavaScript (meta refresh) — link unfurlers and crawlers follow these
  * a 404.html catch-all that reconstructs the path in JS, covering deep asset
    links, directory URLs and anything not stubbed

Run:  python3 build.py     (regenerates every file from PAGES below)
"""

import os

NEW_BASE = "https://chirpbirding.github.io/design-prototypes/"
OLD_PREFIX = "/birda-prototypes/"

# Every page published from the old repo, as `git ls-files '*.html'` reported
# it. A directory stub also answers the bare directory URL (…/v2/), because
# Pages serves index.html for a directory.
PAGES = [
    "index.html",
    "PEX-31/v1/index.html",
    "PEX-31/v2/index.html",
    "PEX-31/v3/index.html",
    "PEX-43/v1/index.html",
    "PEX-43/v2/index.html",
    "PEX-44/v1/index.html",
    "PEX-44/v2/index.html",
    "game-of-birda/points-and-levels/v1/index.html",
    "game-of-birda/animation-demos/toast-demo.html",
    "game-of-birda/animation-demos/level-up-demo.html",
    "game-of-birda/animation-demos/upgrade-demo.html",
    "game-of-birda/animation-demos/goal-complete-demo.html",
    "_resources/template.html",
]

STYLE = """    body { margin:0; min-height:100vh; display:flex; align-items:center; justify-content:center;
           background:#EDEFF6; color:#232A44;
           font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,sans-serif; }
    .card { background:#fff; border:1px solid #E5E5EA; border-radius:12px; padding:26px 30px;
            max-width:440px; text-align:center; box-shadow:0 1px 4px rgba(35,42,68,.08); }
    h1 { margin:0 0 8px; font-size:17px; font-weight:600; }
    p { margin:0 0 14px; font-size:13.5px; line-height:1.5; color:#6B6F7B; }
    a { color:#2F7CF6; font-size:13.5px; word-break:break-all; }"""


def stub(target: str) -> str:
    """A page that forwards without JavaScript, and faster with it."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="0; url={target}">
<link rel="canonical" href="{target}">
<title>Moved · Birda Prototypes</title>
<style>
{STYLE}
</style>
</head>
<body>
  <div class="card">
    <h1>This prototype has moved</h1>
    <p>Taking you there now. If nothing happens, follow the link:</p>
    <a href="{target}">{target}</a>
  </div>
  <!-- Several prototypes route on the hash or read a query param, so carry
       both across. The meta refresh above is the no-JS fallback and can only
       manage the bare path. -->
  <script>location.replace({target!r} + location.search + location.hash);</script>
</body>
</html>
"""


NOT_FOUND = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Moved · Birda Prototypes</title>
<style>
{STYLE}
</style>
<script>
/* Catch-all for anything without its own stub — deep asset links, directory
   URLs, old paths since renamed. Rebuilds the path under the new site rather
   than dumping everyone at the root, so a shared deep link still lands where
   it meant to. Query and hash are carried across too. */
(function () {{
  var NEW = {NEW_BASE!r};
  var OLD = {OLD_PREFIX!r};
  var path = location.pathname;
  var rest = path.indexOf(OLD) === 0 ? path.slice(OLD.length) : '';
  location.replace(NEW + rest + location.search + location.hash);
}})();
</script>
</head>
<body>
  <div class="card">
    <h1>This prototype has moved</h1>
    <p>Taking you there now. If nothing happens, the prototypes now live here:</p>
    <a href="{NEW_BASE}">{NEW_BASE}</a>
  </div>
</body>
</html>
"""

root = os.path.dirname(os.path.abspath(__file__))
written = 0
for page in PAGES:
    dest = os.path.join(root, page)
    os.makedirs(os.path.dirname(dest) or root, exist_ok=True)
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(stub(NEW_BASE + page))
    written += 1

with open(os.path.join(root, "404.html"), "w", encoding="utf-8") as fh:
    fh.write(NOT_FOUND)

# Pages skips underscore-prefixed directories unless Jekyll is switched off,
# and _resources is one.
open(os.path.join(root, ".nojekyll"), "w").close()

print(f"wrote {written} stubs + 404.html + .nojekyll")
