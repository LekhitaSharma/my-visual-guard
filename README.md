# my-visual-guard

[![Visual Tests](https://github.com/LekhitaSharma/my-visual-guard/actions/workflows/visual.yml/badge.svg)](https://github.com/LekhitaSharma/my-visual-guard/actions)

> I broke button padding in a side project and didn't notice for 2 weeks. Built this so it never happens again.

A lightweight visual regression framework that screenshots UI in light/dark mode across mobile, tablet, desktop — and fails CI if pixels change.

**Stack:** Playwright + pytest + Pillow + GitHub Actions

### How it works
- 6 parallel visual tests (2 themes × 3 viewports)
- Compares against Linux-generated baselines
- Saves red diff images on failure and uploads them as CI artifacts

### Run locally
```bash
pip install -r requirements.txt
playwright install chromium
pytest -m visual -n 3
