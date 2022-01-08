from prompt_toolkit import print_formatted_text, HTML, Application
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings

KEY_BINDINGS = KeyBindings()

root_container = HSplit([
    Window(content=FormattedTextControl(text='Test 1 2 3 4 5'))
])

@KEY_BINDINGS.add('c-q')
def exit(event) -> None:
    (type(event))
    event.app.exit()

def main() -> None:
    wolfbot_app = Application(key_bindings=KEY_BINDINGS, full_screen=True, layout=Layout(root_container))
    wolfbot_app.run()

if __name__ == '__main__':
    main()