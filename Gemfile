# GitHub Pages — the `github-pages` gem transitively pins the exact Jekyll
# version and the whitelisted plugins that GitHub Pages runs, so a local
# `bundle exec jekyll build` matches the deployed build.
source "https://rubygems.org"

gem "github-pages", group: :jekyll_plugins
# Required for `jekyll serve` on Ruby 3.x (webrick was removed from stdlib).
gem "webrick", "~> 1.8"

# Stdlib gems extracted from default Ruby in 3.4 / 3.5 / 4.0. GitHub Pages builds
# server-side with its own pinned gem set and ignores these, so they only enable
# a LOCAL `bundle exec jekyll build` on a modern Ruby (e.g. 4.0). Harmless on Pages.
gem "csv"
gem "base64"
gem "bigdecimal"
gem "logger"
gem "ostruct"
