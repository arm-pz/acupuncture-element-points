#!/usr/bin/env bash
# Build and deploy the site to acu.caffeinity.com (Worker "shu-atlas").
# Credentials stay out of the repo: put CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID in
# ~/.config/shu-atlas/cf.env (or export them) before running.
set -euo pipefail
cd "$(dirname "$0")/.."
[ -f "$HOME/.config/shu-atlas/cf.env" ] && . "$HOME/.config/shu-atlas/cf.env"
: "${CLOUDFLARE_API_TOKEN:?set CLOUDFLARE_API_TOKEN}" "${CLOUDFLARE_ACCOUNT_ID:?set CLOUDFLARE_ACCOUNT_ID}"
export CLOUDFLARE_API_TOKEN CLOUDFLARE_ACCOUNT_ID
python3 tools/sync-points.py --check
python3 tools/sync-footer.py && python3 tools/sync-favicon.py
python3 tools/build-site.py
npx -y wrangler@4 deploy
