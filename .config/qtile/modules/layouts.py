from libqtile import layout

# Define common layout properties
common_layout_properties = {
    "border_focus": "#ebdbb2",
    "border_normal": "#ebdbb2",
    "margin": 4
}

# Special case for layouts that also need 'border_width'
border_layout_properties = {**common_layout_properties, "border_width": 2}

# Defining layouts with the common properties
layouts = [
    layout.Columns(**border_layout_properties),
    layout.Tile(**border_layout_properties),
    layout.Max(**border_layout_properties),
    layout.Floating(**border_layout_properties),
]


