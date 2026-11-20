#!/usr/bin/env python3
"""Update pinned Kototoro release inputs and Arch package version."""
import json, os, re, sys, urllib.request

API = "https://api.github.com"
HEADERS = {"Accept": "application/vnd.github+json", "User-Agent": "kototoro-linux-hidpi-updater"}
token = os.environ.get("GITHUB_TOKEN")
if token:
    HEADERS["Authorization"] = f"Bearer {token}"

def get(path):
    req = urllib.request.Request(API + path, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)

release = get("/repos/Kototoro-app/Kototoro/releases/latest")
tag = release["tag_name"]
version = tag.removeprefix("v")
if not re.fullmatch(r"\d+\.\d+\.\d+", version):
    raise SystemExit(f"Unexpected release tag: {tag}")

assets = {a["name"]: a for a in release.get("assets", [])}
asset = next((a for n, a in assets.items()
              if re.fullmatch(rf"Kototoro-{re.escape(version)}-windows-x64-release\.zip", n)), None)
if not asset:
    raise SystemExit(f"Release {tag} has no Windows x64 ZIP needed by Mihon compatibility preparation")
digest = (asset.get("digest") or "").removeprefix("sha256:")
if not re.fullmatch(r"[0-9a-f]{64}", digest):
    raise SystemExit("GitHub release asset has no valid SHA-256 digest; refusing an unverified update")

ref = get(f"/repos/Kototoro-app/Kototoro/git/ref/tags/{tag}")
obj = ref["object"]
if obj["type"] == "tag":
    obj = get(f"/repos/Kototoro-app/Kototoro/git/tags/{obj['sha']}")["object"]
commit = obj["sha"]
if obj["type"] != "commit" or not re.fullmatch(r"[0-9a-f]{40}", commit):
    raise SystemExit("Could not resolve release tag to a commit")

env_path = ".github/upstream.env"
new_env = (
    "# Verified upstream inputs. Updated by .github/workflows/check-upstream.yml.\n"
    f"KOTOTORO_VERSION={version}\nKOTOTORO_TAG={tag}\nKOTOTORO_COMMIT={commit}\n"
    f"KOTOTORO_WINDOWS_ASSET={asset['name']}\nKOTOTORO_WINDOWS_SHA256={digest}\n"
)
old_env = open(env_path, encoding="utf-8").read() if os.path.exists(env_path) else ""
if old_env == new_env:
    print(f"Already up to date: {tag}")
    sys.exit(0)

with open(env_path, "w", encoding="utf-8") as f:
    f.write(new_env)

pkg = "arch/PKGBUILD"
text = open(pkg, encoding="utf-8").read()
text, n = re.subn(r"(?m)^pkgver=.*$", f"pkgver={version}", text, count=1)
if n != 1:
    raise SystemExit("Could not update pkgver in PKGBUILD")
text, n = re.subn(r"(?m)^pkgrel=.*$", "pkgrel=1", text, count=1)
if n != 1:
    raise SystemExit("Could not update pkgrel in PKGBUILD")
open(pkg, "w", encoding="utf-8").write(text)
print(f"Updated pinned upstream release: {tag} ({commit})")
