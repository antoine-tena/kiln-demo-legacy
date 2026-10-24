# kiln-demo-legacy

**Deliberately outdated.** A small Django app (a lending shelf for books) written the way many
repos were around 2020, so that [kiln](https://github.com/antoine-tena/kiln) can be shown
rescuing it: Python 3.8, Django 3.2, loose requirements, actions pinned to moving tags, a
hard-coded secret key, no tests. Nothing here is a real project, and nothing should be deployed.

The demo, replayed by anyone:

```sh
git clone https://github.com/antoine-tena/kiln-demo-legacy
cd kiln-demo-legacy
uvx --from kiln-cli kiln score       # where it stands
uvx --from kiln-cli kiln adopt       # kiln's rules, checks and instructions for Claude Code
kiln fix                             # every gap a script can close
kiln score --roadmap                 # what is left, for Claude Code
claude "/kiln:modernize"             # Claude Code closes it, one proven gap at a time
kiln score
```

The `main` branch stays as it is, so that the demo can be replayed.
