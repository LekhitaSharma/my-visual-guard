import pytest
from pathlib import Path
from PIL import Image, ImageChops

COMPONENTS = [("todo", "/todomvc", "header")]

BASELINES = Path("baselines")
CURRENT = Path("current")
DIFFS = Path("current/diffs")
for p in [BASELINES, CURRENT, DIFFS]: p.mkdir(exist_ok=True)

def images_match(baseline, current, diff_path, max_diff=8000):
    img1 = Image.open(baseline).convert("RGB")
    img2 = Image.open(current).convert("RGB")
    diff = ImageChops.difference(img1, img2)
    diff.save(diff_path)  # <-- saves red diff image
    
    diff_pixels = sum(1 for p in diff.getdata() if p != (0,0,0))
    return diff_pixels <= max_diff

@pytest.mark.visual
@pytest.mark.parametrize("name,path,selector", COMPONENTS)
def test_visual(page, goto_demo, theme, viewport_width, name, path, selector):
    goto_demo(path)
    filename = f"{name}-{theme}-{viewport_width}.png"
    
    baseline = BASELINES / filename
    current = CURRENT / filename
    diff_img = DIFFS / f"diff-{filename}"
    
    page.screenshot(path=str(current), full_page=True)
    
    if not baseline.exists():
        baseline.write_bytes(current.read_bytes())
        pytest.skip("Baseline created")
    
    assert images_match(baseline, current, diff_img), f"Visual change - see {diff_img}"
