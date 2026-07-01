# my-visual-guard

I broke a button padding in my last side-project and didn't notice for 2 weeks.
I built this so it never happens again.

A tiny visual regression framework that screenshots my UI in light/dark mode
across mobile, tablet, and desktop — and fails CI if even 100 pixels change.

Built with Playwright + pytest + Pillow because the built-in
`to_have_screenshot` kept crashing on my Windows machine.

## What it does
- Runs 6 visual tests in parallel (2 themes × 3 viewports)
- Compares against committed baselines
- Generates red diff images on failure

## Run it
```bash
pip install -r requirements.txt
playwright install chromium
pytest -m visual -n0  # create baselines first time
pytest -m visual -n 3 # run tests
