import urllib.request
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
        if self.is_connected():
            return f"<span color='{self.colors['CONNECTED']}'>{self.icons['CONNECTED']}</span>"
        else:
            return f"<span color='{self.colors['DISCONNECTED']}'>{self.icons['DISCONNECTED']}</span>"

    def is_connected(self):
        try:
            # Check internet connection by opening a URL
            urllib.request.urlopen("http://clients3.google.com/generate_204", timeout=2)
            return True
        except Exception:
            return False

    def open_network_script(self):
        qtile.cmd_spawn('/bin/sh -c "~/.config/rofi/scripts/network"')

# Example usage in your qtile config
internet_widget = InternetStatusWidget()

