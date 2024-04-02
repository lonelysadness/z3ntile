from libqtile import bar, widget, qtile
from libqtile.config import Screen
from libqtile.lazy import lazy
from libqtile import hook, qtile
from .windowname_widget import WindowName
from .network_widget import InternetStatusWidget
from .audio_widget_v2 import VolumeWidget

BG_1 = "#282828"
BG_2 = "#3c3836"
COMMON_FG = "#ebdbb2"

GROUP_BOX_SETTINGS = {
    "fontsize": 18,
    "borderwidth": 4,
    "highlight_method": "block",
    "active": "#ebdbb2",
    "block_highlight_text_color": "#bdae93",
    "highlight_color": "#d5c4a1",
    "inactive": "#282828",
    "foreground": "#bdae93",
    "this_current_screen_border": "#3c3836",
    "this_screen_border": "#3c3836",
    "other_current_screen_border": "#3c3836",
    "other_screen_border": "#3c3836",
    "urgent_border": "#3c3836",
    "rounded": False,
    "disable_drag": True
}
BAR_SETTINGS = {
    "size": 28,
    "border_color": BG_1,
    "border_width": [0, 0, 0, 0],
    "margin": [0, 0, 0, 0]
}

def create_image_widget(filename, margin=0, mouse_callbacks=None):
    return widget.Image(filename=filename, margin=margin, background=BG_1, mouse_callbacks=mouse_callbacks)

def create_text_box(text, fontsize=24, padding=0, foreground=BG_1, background=BG_2, mouse_callbacks=None):
    return widget.TextBox(text=text, fontsize=fontsize, padding=padding, foreground=foreground, background=background, mouse_callbacks=mouse_callbacks)

def create_group_box():
    return widget.GroupBox(**GROUP_BOX_SETTINGS)

top_widgets_screen1 = [
    widget.Spacer(length=10, background=BG_1),
    create_image_widget("~/.config/qtile/assets/logo.png", margin=2, mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("sh -c ~/.config/rofi/scripts/power")}),
    create_text_box(""),
    widget.Spacer(length=8),
    create_group_box(),
    widget.Spacer(length=8),
    create_text_box("󰇙", foreground="#ebdbb2"),
    widget.Spacer(length=16),
    widget.CurrentLayoutIcon(custom_icon_paths="~/.config/qtile/assets/icons", scale=0.65),
    widget.CurrentLayout(),
    create_text_box(""),
    widget.Spacer(),
    WindowName(format='  {name}', empty_group_string="Desktop", max_chars=130, width=bar.CALCULATED),
    widget.Spacer(),
    create_text_box(""),
    widget.Systray(padding=7),
    widget.Spacer(length=6),
    create_text_box(""),
    widget.Spacer(length=8, background=BG_1),
    widget.CheckUpdates(colour_have_updates=COMMON_FG,background=BG_1, distro="Arch_paru", execute="kitty -e paru", update_interval=3600),
    widget.Spacer(length=8, background=BG_1),
    InternetStatusWidget(fontsize=16, background=BG_1),
    widget.Spacer(length=16, background=BG_1),
    VolumeWidget(fontsize=16, background=BG_1),
    widget.Spacer(length=8, background=BG_1),
    create_text_box("󰇙", background=BG_1, foreground="#ebdbb2"),
    widget.Spacer(length=8, background=BG_1),
    widget.TextBox(text=" ", background=BG_1),
    widget.Clock(format="%I:%M %p", background=BG_1),
    widget.Spacer(length=18, background=BG_1),
]


top_widgets_screen2 = [
    widget.Spacer(length=10, background=BG_1),
    create_image_widget("~/.config/qtile/assets/logo.png", margin=2, mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("sh -c ~/.config/rofi/scripts/power")}),
    create_text_box(""),
    widget.Spacer(length=8),
    create_group_box(),
    widget.Spacer(length=8),
    create_text_box("󰇙", foreground="#ebdbb2"),
    widget.Spacer(length=16),
    widget.CurrentLayoutIcon(custom_icon_paths="~/.config/qtile/assets/icons", scale=0.65),
    widget.CurrentLayout(),
    create_text_box(""),
    widget.Spacer(),
    WindowName(format='  {name}', empty_group_string="Desktop", max_chars=130, width=bar.CALCULATED),
    widget.Spacer(),
    create_text_box(""),
    widget.TextBox(text=" ", background=BG_1),
    widget.Clock(format="%I:%M %p", background=BG_1),
    widget.Spacer(length=18, background=BG_1),
]


def create_screen(widgets):
    return Screen(top=bar.Bar(widgets, **BAR_SETTINGS))

screen1 = create_screen(top_widgets_screen1)
screen2 = create_screen(top_widgets_screen2)
screens = [screen1,screen2]
