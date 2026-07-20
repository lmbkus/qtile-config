from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os

mod = "mod4"
terminal = guess_terminal()

# Keybindings
keys = [
    # Movimiento entre ventanas
    *[
        Key([mod], k, f())
        for k, f in zip("hjkl", [lazy.layout.left, lazy.layout.down, lazy.layout.up, lazy.layout.right])
    ],
    Key([mod], "space", lazy.layout.next()),

    # Mover ventanas
    *[
        Key([mod, "shift"], k, f())
        for k, f in zip("hjkl", [lazy.layout.shuffle_left, lazy.layout.shuffle_down, lazy.layout.shuffle_up, lazy.layout.shuffle_right])
    ],

    # Redimensionar ventanas
    *[
        Key([mod, "control"], k, f())
        for k, f in zip("hjkl", [lazy.layout.grow_left, lazy.layout.grow_down, lazy.layout.grow_up, lazy.layout.grow_right])
    ],
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod], "Tab", lazy.next_layout()),

    # Administración de ventanas
    Key([mod], "w", lazy.window.kill()),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "t", lazy.window.toggle_floating()),

    # Configuración
    Key([mod, "control"], "r", lazy.reload_config()),
    Key([mod, "control"], "q", lazy.shutdown()),
   
    # Abrir Dolphin
    Key([mod], "e", lazy.spawn("thunar")), 
    
    Key([], "XF86AudioRaiseVolume", lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ +2%'), desc="Up the volume"), 
    Key([], "XF86AudioLowerVolume", lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ -2%'), desc="Down the volume"),
    Key([], "XF86AudioMute", lazy.spawn('pactl set-sink-mute @DEFAULT_SINK@ toggle'), desc="Toggle mute"),
    Key([], "XF86AudioMicMute", lazy.spawn('pactl set-source-mute @DEFAULT_SOURCE@ toggle'), desc="Toggle mute the microphone"),
    Key([], "XF86MonBrightnessDown", lazy.spawn('brightnessctl set 2%-'), desc="Down brightness"),
    Key([], "XF86MonBrightnessUp", lazy.spawn('brightnessctl set 2%+'), desc="Up brightness"),  
    Key([], "XF86AudioPlay", lazy.spawn('playerctl play-pause'), desc="Play-pause"),  
    Key([], "XF86AudioNext", lazy.spawn('playerctl next'), desc="Next song"), 
    Key([], "XF86AudioPrev", lazy.spawn('playerctl previous'), desc="Previous song"),    

   
    # Lanzador
    Key(
            [mod], "r",
            lazy.spawn("bash -c '$HOME/rofi/files/launchers/type-4/launcher.sh'")
        ),
    ]



groups = [Group(i) for i in ["1","2","3","4","5","6","7","8"]]

for i in groups:
    keys.extend(
        [
            Key([mod], i.name, lazy.group[i.name].toscreen(), desc="Switch to group {}".format(i.name),),
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=False), desc="Move focused window to group {}".format(i.name),),
        ]
    )


# Layouts
layouts = [
    layout.Columns(
        border_focus="#7b5cb5",
        border_normal="#7b5cb5",
        border_focus_stack=["#d75f5f", "#8f3d3d"],
        border_width=0,
        margin=6,
        ratio=0.5,
    ),
    layout.Max(),
]

# Widgets
widget_defaults = dict(
    font="Fira Code Nerd Font",
    fontsize=13,
    padding=4,
)
extension_defaults = widget_defaults.copy()

# Screens
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    highlight_method="line",
                    rounded=False,
                    inactive="#666666",
                    active="#cccccc",
                    highlight_color="#2e3440",
                    this_current_screen_border="#b48ead",
                    urgent_border="#FF00FF",
                    fontsize=15,
                    margin_x=-1,
                    padding=1,
                    disable_drag=True,
                ),
                widget.WindowName(for_current_screen = True),
                widget.Spacer(length=10),

                widget.Prompt(),

                #widget.Spacer(length=bar.STRETCH),

                widget.Systray(
                    padding=5,
                ),

                widget.TextBox(
                    text="",
                    fontsize=30,
                    padding=-1,
                    foreground="#bf616a",
                    background="#2e3440",
                ),

                widget.CheckUpdates(
                    distro="Arch",
                    update_interval=1800,
                    no_update_string=" ",
                    display_format=" {updates} ",
                    foreground="#b3c4fc",
                    background="#bf616a",
                    colour_have_updates="#000000",
                    colour_no_updates="#000000",
                    mouse_callbacks={
                        'Button1': lazy.spawn("alacritty -e sudo pacman -Syu"),
                    },
                ),
                
                widget.TextBox(
                    text="",
                    fontsize=30,
                    padding=-1,
                    foreground="#a3be8c",
                    background="#bf616a",
                ),
                
                widget.Volume(
                    mute_format=' ', 
                    unmute_format='  {volume}%', 
                    step=5,
                    background="#a3be8c", 
                    foreground="#0d0d0f",
                ),
                
                widget.TextBox(
                    text="",
                    fontsize=30,
                    padding=-1,
                    foreground="#ebcb8b",
                    background="#a3be8c",
                ),
                                
                widget.Net(
                    format=' {down:.1f}{down_suffix}   {up:.1f}{up_suffix}',
                    background="#ebcb8b", 
                    foreground="#0d0d0f",
                ),

                
                widget.TextBox(
                    text="",
                    fontsize=30,
                    padding=-1,
                    foreground="#81a1c1",
                    background="#ebcb8b",
                ),

                widget.Clock(
                    format=" %d/%m/%Y %H:%M",
                    foreground="#000000",
                    background="#81a1c1",
                ),

                #widget.TextBox("", fontsize=34, padding=-1, foreground="#faad48", background="#faad48"),
                #widget.Battery(format=" {percent:2.0%} ", background="#faad48", font="Fira Code Nerd Font", foreground="#ffffff"),

            ],
            25,
            #margin=[3, 3, , 3],
            background="#2e3440",
            
        ),
    ),
]

# Mouse
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

# Floating Layout
floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(title="pinentry"),
    ],
    border_focus="#655ec4",
    border_normal="#7b5cb5",
    border_width=0,
)

# Qtile Settings
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True

wl_input_rules = None
wl_xcursor_theme = None
wl_xcursor_size = 24
wmname = "LG3D"

# Autostart
@hook.subscribe.startup_once
def autostart():
    apps = [
        "picom",
        "feh --bg-fill ~/wall/unu.jpg",
    ]
    for app in apps:
        os.system(f"{app} &")