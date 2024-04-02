import subprocess
from libqtile.widget import GenPollText
from libqtile import qtile

class VolumeWidget(GenPollText):
    colors = {
        "MUTE": "#cc241d",
        "LOW": "#fabd2f",
        "MEDIUM": "#b8bb26",
        "HIGH": "#83a598",
    }
    icons = {
        "MUTE": "󰝟",
        "LOW": "󰕿",
        "MEDIUM": "󰖀",
        "HIGH": "󰕾",
    }
    thresholds = {
        "LOW": 30,
        "MEDIUM": 60,
        "HIGH": 100,
    }

    def __init__(self, **config):
        config.setdefault('update_interval', 1)
        config.setdefault('font', "JetBrainsMono Nerd Font Bold")
        config.setdefault('fontsize', 18)
        super().__init__(**config)
        self.setup_mouse_callbacks()

    def setup_mouse_callbacks(self):
        self.mouse_callbacks = {
            'Button1': self.open_volume_script,
            'Button4': self.increase_volume,
            'Button5': self.decrease_volume,
        }

    def poll(self):
        return self.get_volume_status()

    def get_volume_status(self):
        volume, mute = self.get_volume_info()
        if mute == "yes" or volume == 0:
            color = self.colors["MUTE"]
            icon = self.icons["MUTE"]
        elif volume < self.thresholds["LOW"]:
            color = self.colors["LOW"]
            icon = self.icons["LOW"]
        elif volume < self.thresholds["MEDIUM"]:
            color = self.colors["MEDIUM"]
            icon = self.icons["MEDIUM"]
        else:
            color = self.colors["HIGH"]
            icon = self.icons["HIGH"]
        return f"<span color='{color}'>{icon} {volume}%</span>"

    def get_volume_info(self):
        cmd_volume = "pactl get-sink-volume @DEFAULT_SINK@ | grep -oP '\\d+%' | head -1 | tr -d '%'"
        cmd_mute = "pactl get-sink-mute @DEFAULT_SINK@ | awk '/Mute/ {print $2}'"
        volume = int(subprocess.getoutput(cmd_volume))
        mute = subprocess.getoutput(cmd_mute)
        return volume, mute

    def open_volume_script(self):
        qtile.cmd_spawn('/bin/sh -c "~/.config/rofi/scripts/volume"')

    def increase_volume(self):
        subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+5%"])

    def decrease_volume(self):
        subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "-5%"])

