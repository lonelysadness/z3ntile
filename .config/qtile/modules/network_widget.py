import subprocess
from libqtile.widget import GenPollText
from libqtile import qtile

class InternetStatusWidget(GenPollText):
    colors = {
        "CONNECTED": "#b8bb26",
        "DISCONNECTED": "#cc241d",
    }
    icons = {
        "CONNECTED": "󰲝",
        "DISCONNECTED": "󰲛",
    }

    def __init__(self, **config):
        config.setdefault('update_interval', 2)
        config.setdefault('background', "#3c3836")
        config.setdefault('font', "JetBrainsMono Nerd Font Bold")
        config.setdefault('fontsize', 12)
        super().__init__(**config)
        self.setup_mouse_callbacks()

    def setup_mouse_callbacks(self):
        self.mouse_callbacks = {
            'Button1': self.open_network_script,
        }

    def poll(self):
        return self.get_internet_status()

    def get_internet_status(self):
        cmd = "ping -c 1 8.8.8.8 > /dev/null 2>&1; echo $?"
        status = subprocess.getoutput(cmd)
        if status == "0":
            return f"<span color='{self.colors['CONNECTED']}'>{self.icons['CONNECTED']}</span>"
        else:
            return f"<span color='{self.colors['DISCONNECTED']}'>{self.icons['DISCONNECTED']}</span>"

    def open_network_script(self):
        qtile.cmd_spawn('/bin/sh -c "~/.config/rofi/scripts/network"')


