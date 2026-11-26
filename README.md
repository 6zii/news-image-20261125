# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/6zii/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/6zii/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A one-day newspaper front page summing up Wednesday 25 November 2026's world news in a single 1024×1024 image: twelve stories, every one with its own real news photograph — the mined tankers in the Strait of Hormuz, the Houthi strikes on Riyadh and Ras Tanura, Gaza, Odesa and Kyiv, Sudan, the failed COP31 talks, the Solomon Islands treaty, Huawei's conviction, Shenzhou-24 carrying Pakistan's first astronaut, Trump's new tariffs, the Netanyahu case and Bangladesh's wage rise. The page is drawn at build time by `draw_page.py` (Pillow + OFL fonts); `main.py` copies the finished `entry.png` to the output directory.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To redraw the page from its sources (needs Pillow, build time only):

```sh
python3 draw_page.py
```

## Photographs

All twelve photographs are file pictures from Wikimedia Commons, credited beneath each story on the page:

- Strait of Hormuz: USS Porter damaged in collision with an oil tanker — DVIDSHUB (CC BY 2.0)
- Riyadh: Kingdom Centre — Wajahat Mahmood (CC BY-SA 2.0)
- Gaza: Damage in the Gaza Strip — WAFA / APAimages (CC BY-SA 3.0)
- Kyiv: Residential building damaged by a Russian strike, 2024-07-08 — Kyiv City State Administration (CC BY 4.0)
- Sudan: El Fasher, Darfur — INPE (CC BY-SA 2.0)
- Pope Leo XIV — Edgar Beltrán / The Pillar (CC BY-SA 4.0)
- Honiara, Solomon Islands — Jenny Scott (CC BY 2.0)
- Huawei headquarters, Shenzhen — RG72 (CC BY-SA 4.0)
- Shenzhou / Long March 2F launch — China News Service (CC BY 4.0)
- Donald Trump in the Oval Office — The White House (public domain)
- Donald Trump and Benjamin Netanyahu at the White House — Dan Scavino (public domain)
- Garment workers, Bangladesh — Fahad Faisal (CC BY-SA 4.0)

Fonts are OFL-licensed: Playfair Display, PT Serif and Oswald (Google Fonts).

---

<sub>Entered on [make.fun](https://make.fun/?ref=831b3jbq&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
