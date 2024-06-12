from libqtile import layout
from libqtile.config import Match

# Define common layout properties
common_layout_properties = {
    "border_focus": "#ebdbb2",
    "border_normal": "#3d4555",
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


floating_layout = layout.Floating(
	border_focus="#ebdbb2",
	border_normal="#3d4555",
	border_width=2,
    float_rules=[
        *layout.Floating.default_float_rules,
    ]
)
