import pytest
from pathlib import Path
from PIL import Image, ImageChops

COMPONENTS = [("todo", "/todomvc", "header")]

BASELINES = Path("baselines")
CURRENT = Path("current")
BASELINES.mkdir(exist_ok=True)
CURRENT.mkdir(exist_ok=True)

def images_match(baseline, current, max_diff=100):
    img1 = Image.open(baseline).convert("RGB")
    img2 = Image.open(current).convert("RGB")
    diff = ImageChops.difference(img1, img2)
    diff_pixels = sum(1 for p in diff.getdata() if p != (0,0,0))
    return diff_pixels <= max_diff

@pytest.mark.visual
@pytest.mark.parametrize("name,path,selector", COMPONENTS)
def test_visual(page, goto_demo, theme, viewport_width, name, path, selector):
    goto_demo(path)
    
    filename = f"{name}-{theme}-{viewport_width}.png"
    baseline = BASELINES / filename
    current = CURRENT / filename
    
    page.screenshot(path=str(current), full_page=True)
    
    if not baseline.exists():
        baseline.write_bytes(current.read_bytes())
        pytest.skip(f"Baseline created: {filename}")
    
    assert images_match(baseline, current), f"Visual diff: {filename}"
