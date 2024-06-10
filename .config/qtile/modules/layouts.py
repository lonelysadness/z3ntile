from libqtile import layout

# Define common layout properties
common_layout_properties = {
    "border_focus": "#ebdbb2",
    "border_normal": "#666666",
    "margin": 4
}

# Special case for layouts that also need 'border_width'
border_layout_properties = {**common_layout_properties, "border_width": 2}

# Defining layouts
layouts = [
    layout.Columns(**border_layout_properties),
    layout.Tile(**border_layout_properties),
    layout.Max(**common_layout_properties),
    layout.Floating(**common_layout_properties),
]

