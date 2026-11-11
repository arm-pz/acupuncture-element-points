import subprocess
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
ARTIFACTS = pathlib.Path(r'C:\Users\abdul\.gemini\antigravity\brain\8aabb083-e170-4acf-84b2-0047221a9782')

def snap(url_suffix, out_name):
    target = f"file:///{ROOT.as_posix()}/channels.html{url_suffix}"
    out_file = ARTIFACTS / out_name
    cmd = [
        CHROME,
        '--headless=new',
        '--disable-gpu',
        '--window-size=1280,960',
        f'--screenshot={out_file}',
        target
    ]
    subprocess.run(cmd, check=True)
    print(f"Captured {out_name}: {out_file.stat().st_size} bytes")

snap("", "screen-channels-default.png")
snap("?rank=2", "screen-channels-stream.png")
snap("?q=knee", "screen-channels-search-knee.png")
snap("?yy=yin&limb=hand", "screen-channels-hand-yin.png")
print("All interactive states snapped successfully!")
