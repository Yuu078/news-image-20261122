# news-image-20261122 — THE MORNING ATLAS

[![make.fun](https://img.shields.io/badge/make.fun-bounty-blue)](https://make.fun/bounty/news-image-20261122)
[![make.fun](https://img.shields.io/badge/make.fun-news--image--20261122-red)](https://make.fun/bounty/news-image-20261122)
[![make.fun](https://img.shields.io/badge/make.fun-35%20stories-green)](https://make.fun/bounty/news-image-20261122)

One-page newspaper poster summing up the world's news of **Sunday 22 November 2026**:
35 stories across 7 regions, led by the COP31 final deal in Antalya.

Built for the [make.fun](https://make.fun/bounty/news-image-20261122) bounty
**news-image-20261122** ("Sum up 22 November's world news in one image").

## What it is

- `entry.png` — the poster itself, 1024×1024 PNG.
- `render_atlas.py` — the program that draws the poster from scratch with
  Pillow (masthead, 6-number strip, hero card, 11 illustrated cards, heat map,
  THE WIRE, DATE CHECK). Run it twice and the bytes are identical.
- `main.py` — the entry program: copies `entry.png` to `/output/entry.png`.

## How to run

```sh
python3 render_atlas.py   # rebuild entry.png (deterministic)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # write out/entry.png
```

## License

MIT — see `LICENSE`.
