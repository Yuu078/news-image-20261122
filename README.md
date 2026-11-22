# news-image-20261122 — THE MORNING ATLAS

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Yuu078/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Yuu078/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One-page newspaper poster summing up the world's news of **Sunday 22 November 2026**:
10 stories across 7 regions, led by the collapse of the COP31 climate talks in Antalya.

Built for the [make.fun](https://make.fun/bounty/news-image-20261122) bounty
**news-image-20261122** ("Sum up 22 November's world news in one image").

## What it is

- `entry.png` — the poster itself, 1024×1024 PNG.
- `render_atlas_v5.py` — the program that draws the poster from scratch
  with Pillow (masthead, 4-number strip, hero card with an empty summit
  hall under a giant 0, 9 fully illustrated story cards in a 3×3 grid,
  a region chip row generated from the story ledger, DATE CHECK).
  Run it twice and the bytes are identical.
- `main.py` — the entry program: renders the poster twice, verifies the
  bytes agree and pass the kit gates, and writes `entry.png` to
  `MAKEFUN_OUTPUT_DIR` (default: the repo folder).

## How to run

```sh
python3 render_atlas_v5.py   # rebuild entry.png (deterministic)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # write out/entry.png
```

## License

MIT — see `LICENSE`.
