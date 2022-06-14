import functools
import PySimpleGUI as sg

# Prevents an issue on macOS when using night mode where disabled input fields are rendered with black text on a black background.
uInput = functools.partial(
    sg.Input,
    disabled_readonly_background_color='white',
    disabled_readonly_text_color='black'
)
sg.Input = uInput

# Prevents an issue on macOS where the window is rendered transparent.
uWindow = functools.partial(
    sg.Window,
    alpha_channel=0.99,
)
sg.Window = uWindow
