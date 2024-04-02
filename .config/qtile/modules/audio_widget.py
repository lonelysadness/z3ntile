import subprocess
from libqtile.widget import GenPollText

class AudioWidget(GenPollText):
    colors = {
        "ON3": "#b8bb26",  # Jaune vif pour ON3
        "ON2": "#fabd2f",  # Jaune orange pour ON2
        "ON1": "#98971a",  # Vert olive pour ON1
        "MUTE": "#cc241d",  # Rouge pour MUTE
        "REC": "#b8bb26",  # Jaune vif pour REC
    }

    def __init__(self, **config):
        config.setdefault('update_interval', 1)
        config.setdefault('background', "#3c3836")
        config.setdefault('font', "JetBrainsMono Nerd Font Bold")
        config.setdefault('fontsize', 12)
        super().__init__(**config)
        self.font = f"{self.font} {self.fontsize}"
        self.setup_mouse_callbacks()
    def setup_mouse_callbacks(self):
        self.mouse_callbacks = {
            "Button1": self.toggle_audio,
            "Button2": self.toggle_microphone,
            "Button3": self.choose_device,
            "Button4": self.volume_up,
            "Button5": self.volume_down,
        }

    @staticmethod
    def execute_command(command):
        try:
            process = subprocess.Popen(
                command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            stdout, _ = process.communicate()
            return stdout.decode("utf-8").strip()
        except Exception as e:
            print(f"AudioWidget Error: {e}")
            return ""

    def toggle_audio(self):
        self.execute_command("pactl set-sink-mute @DEFAULT_SINK@ toggle")

    def toggle_microphone(self):
        self.execute_command("pactl set-source-mute @DEFAULT_SOURCE@ toggle")

    def volume_up(self):
        self.execute_command("pactl set-sink-volume @DEFAULT_SINK@ +5%")

    def volume_down(self):
        self.execute_command("pactl set-sink-volume @DEFAULT_SINK@ -5%")

    def choose_device(self):
        try:
            old_sink = self.execute_command("pactl get-default-sink")
            sink_output = self.execute_command("LC_ALL=C pactl list sinks")
            sinks = {}
            for block in sink_output.split("\n\n"):
                name = description = None
                for line in block.split("\n"):
                    if "Name: " in line:
                        name = line.split("Name: ")[1]
                    if "Description: " in line:
                        description = line.split("Description: ")[1]
                    if name and description:
                        sinks[description] = name

            chosen_sink_desc = subprocess.run(
                ["rofi", "-dmenu", "-i", "-p", "Output"],
                input="\n".join(sinks.keys()),
                text=True,
                capture_output=True,
            ).stdout.strip()

            if chosen_sink_desc:
                chosen_sink_name = sinks.get(chosen_sink_desc)
                if chosen_sink_name and chosen_sink_name != old_sink:
                    self.execute_command(f"pactl set-default-sink {chosen_sink_name}")
                    self.execute_command(
                        f"notify-send 'Audio output changed to {chosen_sink_desc}'"
                    )

            old_source = self.execute_command("pactl get-default-source")
            source_output = self.execute_command("LC_ALL=C pactl list sources")
            sources = {}
            for block in source_output.split("\n\n"):
                name = description = None
                for line in block.split("\n"):
                    if "Name: " in line:
                        name = line.split("Name: ")[1]
                    if "Description: " in line:
                        description = line.split("Description: ")[1]
                    if name and description:
                        sources[description] = name

            chosen_source_desc = subprocess.run(
                ["rofi", "-dmenu", "-i", "-p", "Input"],
                input="\n".join(sources.keys()),
                text=True,
                capture_output=True,
            ).stdout.strip()

            if chosen_source_desc:
                chosen_source_name = sources.get(chosen_source_desc)
                if chosen_source_name and chosen_source_name != old_source:
                    self.execute_command(
                        f"pactl set-default-source {chosen_source_name}"
                    )
                    self.execute_command(
                        f"notify-send 'Audio input changed to {chosen_source_desc}'"
                    )

        except Exception as e:
            print(f"Error: {e}")

    def poll(self):
        audio_state, mic_state = self.get_audio_states()
        return self.format_widget_output(audio_state, mic_state)

    def get_audio_states(self):
        audio_muted = self.execute_command("LC_ALL=C pactl get-sink-mute @DEFAULT_SINK@").split(": ")[1]
        microphone_muted = self.execute_command("LC_ALL=C pactl get-source-mute @DEFAULT_SOURCE@").split(": ")[1]
        volume = self.get_volume_level()

        audio_state = self.determine_audio_state(audio_muted, volume)
        microphone_state = "MUTE" if microphone_muted == "yes" else "REC"
        return audio_state, microphone_state

    @staticmethod
    def get_volume_level():
        try:
            volume_output = AudioWidget.execute_command("pactl get-sink-volume @DEFAULT_SINK@")
            return int(volume_output.split("/")[1].strip().replace("%", ""))
        except Exception:
            return 0

    def determine_audio_state(self, audio_muted, volume):
        if audio_muted == "yes":
            return "MUTE"
        if 0 < volume <= 50:
            return "ON1"
        if 51 <= volume <= 100:
            return "ON2"
        return "ON3"

    def format_widget_output(self, audio_state, microphone_state):
        audio_icon = self.get_icon_for_state(audio_state, is_microphone=False)
        mic_icon = self.get_icon_for_state(microphone_state, is_microphone=True)

        audio_color = self.colors[audio_state]
        mic_color = self.colors[microphone_state]

        return f"<span color='{audio_color}'>{audio_icon}</span>  <span color='{mic_color}'>{mic_icon}</span>"

    @staticmethod
    def get_icon_for_state(state, is_microphone=False):
        if is_microphone:
            return "" if state == "REC" else ""
        else:
            return {
                "ON3": "󰕾",
                "ON2": "󰖀",
                "ON1": "",
                "MUTE": "󰖁"
            }.get(state, "")
