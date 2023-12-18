from modules.keys import keys, mod
from modules.groups import groups
from modules.layouts import layouts
from modules.mouse import mouse
from modules.hooks import autostart
from modules.widgets import screens

follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True

wmname = "Qtile"

widget_defaults = dict(
    font="JetBrainsMono Nerd Font Bold",
    fontsize=14,
    padding=3,
    background="#202222",
    foreground="#3f545e",
)