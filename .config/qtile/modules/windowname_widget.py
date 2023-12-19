from libqtile import widget

class WindowName(widget.WindowName):
    def update(self, *args):
        if self.for_current_screen:
            w = self.qtile.current_screen.group.current_window
        else:
            w = self.bar.screen.group.current_window

        if w and w.window:
            class_name = w.window.get_wm_class()[0] if w.window.get_wm_class() else ""
        else:
            class_name = self.empty_group_string

        icon = "  " 
        self.text = f'{icon}{class_name}'

        self.bar.draw()


