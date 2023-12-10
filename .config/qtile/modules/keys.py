from libqtile.lazy import lazy
from libqtile.config import Key

mod = "mod4"
terminal = "kitty"

def unminimize_all(qtile):
    for window in qtile.current_group.windows:
        if window.minimized:
            window.cmd_toggle_minimize()

keys = [
    # Basic window management
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "c", lazy.window.kill(), desc="Kill focused window"),

    # Window resizing and layout adjustments
    Key([mod, "shift"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "shift"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "shift"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "shift"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Window states toggling
    Key([mod], "m", lazy.window.toggle_minimize(), desc="Toggle window minimize"),
    Key([mod, "shift"], "m", lazy.function(unminimize_all), desc="Unminimize all windows"),
    Key([mod, "control"], "m", lazy.window.toggle_maximize(), desc="Toggle window maximize"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen mode"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),

    # Qtile system commands
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    # Application launchers
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Launch application launcher"),
    Key([mod], "e", lazy.spawn("thunar"), desc="Open file manager"),
    Key([mod], "s", lazy.spawn("flameshot gui"), desc="Take a screenshot"),
    Key([mod], "p", lazy.spawn("sh -c ~/.config/rofi/scripts/power"), desc="powermenu"),

    # Media keys
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%"), desc="Volume up"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%"), desc="Volume down"),
    Key([], "XF86AudioMute", lazy.spawn("pulsemixer --toggle-mute"), desc="Mute volume"),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Play/Pause media"),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Next media track"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Previous media track"),
]

