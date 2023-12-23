from libqtile import hook
from libqtile import qtile
import subprocess
import os

@hook.subscribe.startup_once
def autostart():
    """Execute tasks on Qtile startup."""
    autostart_script = os.path.expanduser("~/.config/qtile/autostart_once.sh")
    if os.path.exists(autostart_script):
        subprocess.call([autostart_script])
    else:
        print(f"Autostart script not found: {autostart_script}")
    setup_screen()

def setup_screen():
    """Setup initial screen and group configuration."""
    screen_group_pairs = [(0, "1"), (1, "5")]
    for screen_index, group_name in screen_group_pairs:
        if group_name in qtile.groups_map:
            screen = qtile.screens[screen_index]
            group = qtile.groups_map[group_name]
            screen.set_group(group)


