import pytest
from pathlib import Path
from PIL import Image, ImageChops

BASELINES = Path("baselines")
CURRENT = Path("current")
DIFFS = Path("diffs")

@pytest.mark.visual
@pytest.mark.parametrize("theme", ["light", "dark"])
@pytest.mark.parametrize("viewport", [375, 768, 1440])
def test_todo_visual(page, theme, viewport):
    url = "https://todomvc.com/examples/react/dist/"
    page.goto(url, wait_until="networkidle")
    page.evaluate(f"document.documentElement.setAttribute('data-theme', '{theme}')")
    page.set_viewport_size({"width": viewport, "height": 800})
    page.wait_for_selector("header")
    
    CURRENT.mkdir(exist_ok=True)
    BASELINES.mkdir(exist_ok=True)
    DIFFS.mkdir(exist_ok=True)
    
    name = f"todo-{theme}-{viewport}.png"
    current_path = CURRENT / name
    baseline_path = BASELINES / name
    diff_path = DIFFS / name
    
    page.screenshot(path=str(current_path), full_page=False)
    
    if not baseline_path.exists():
        current_path.replace(baseline_path)
        return
    
    img1 = Image.open(baseline_path).convert("RGB")
    img2 = Image.open(current_path).convert("RGB")
    
    diff = ImageChops.difference(img1, img2)
    
    # Create RED highlight
    if diff.getbbox():
        mask = diff.convert("L").point(lambda p: 255 if p > 20 else 0)
        red = Image.new("RGB", img1.size, (255, 0, 0))
        red_diff = Image.composite(red, Image.new("RGB", img1.size, (0,0,0)), mask)
        red_diff.save(diff_path)
    
    diff_pixels = sum(1 for p in diff.getdata() if sum(p) > 20)
    assert diff_pixels <= 150, f"Visual diff {diff_pixels}px > 150 - see {diff_path}"
