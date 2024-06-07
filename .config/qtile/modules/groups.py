from libqtile.config import Key, Group
from libqtile.lazy import lazy  # Updated import path for lazy
from .keys import keys, mod
import subprocess

def switch_to_group_screen(name: str):
    """Function to switch to the specified group and focus on the appropriate screen."""
    def inner(qtile) -> None:
        screen_index = 0 if name in ["1", "2", "3", "4"] else 1
        qtile.focus_screen(screen_index)
        qtile.groups_map[name].toscreen()
    return inner

def move_window_to_group(group_name: str):
    """Function to move the current window to the specified group and handle screen focus."""
    def inner(qtile):
        current_group = qtile.current_group.name
        current_screen = qtile.current_screen.index
        target_screen = 0 if group_name in ["1", "2", "3", "4"] else 1

        if qtile.current_window:  # Check if current_window is not None
            qtile.current_window.togroup(group_name)
            handle_screen_switch(qtile, target_screen, current_screen, group_name, current_group)
    return inner

def handle_screen_switch(qtile, target_screen, current_screen, target_group, current_group):
    """Function to handle screen switching logic when moving windows between groups."""
    if target_screen != current_screen:
        qtile.to_screen(target_screen)
        qtile.groups_map[target_group].toscreen()
        qtile.to_screen(current_screen)
        qtile.groups_map[current_group].toscreen()
    else:
        qtile.groups_map[target_group].toscreen()

def get_keyboard_layout():
    """Function to retrieve the current keyboard layout."""
    try:
        output = subprocess.check_output(["setxkbmap", "-query"])
        layout_line = next(line for line in output.decode().split("\n") if "layout" in line)
        return layout_line.split(":")[1].strip()
    except Exception as e:
        print(f"Failed to get keyboard layout: {e}")
        return "us"

keyboard_layout = get_keyboard_layout()
key_names = {
    "fr": ["ampersand", "eacute", "quotedbl", "apostrophe", "parenleft", "minus", "egrave", "underscore"],
    "us": ["1", "2", "3", "4", "5", "6", "7", "8"]
}.get(keyboard_layout, ["1", "2", "3", "4", "5", "6", "7", "8"])
labels = ["", "", "", "", "󰙯", "󰖟", "", "󰛓"]

groups = [Group(f"{i+1}", label=labels[i]) for i in range(8)]

for idx, group in enumerate(groups):
    keys.extend([
        Key([mod], key_names[idx], lazy.function(switch_to_group_screen(group.name))),
        Key([mod, "shift"], key_names[idx], lazy.function(move_window_to_group(group.name))),
    ])

