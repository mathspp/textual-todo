from textual.app import App, ComposeResult
from textual.widgets import Button, Input, Label, Static


class EditableText(Static):
    """Custom widget to show (editable) static text."""

    DEFAULT_CSS = """
    EditableText {
        layout: horizontal;
        width: 1fr;
        height: 3;
    }

    .editabletext--input {
        width: 1fr;
    }

    .editabletext--label {
        width: 1fr;
        height: 3;
        padding-left: 2;
        border: round $primary;
    }

    .editabletext--edit {
        box-sizing: border-box;
        min-width: 0;
        width: 4;
    }

    .editabletext--confirm {
        box-sizing: border-box;
        min-width: 0;
        width: 4;
    }

    EditableText .ethidden {
        display: none;
    }
    """

    def compose(self) -> ComposeResult:
        yield Input(
            placeholder="Type something...", classes="editabletext--input ethidden"
        )
        yield Label("", classes="editabletext--label")
        yield Button("📝", classes="editabletext--edit")
        yield Button("✅", classes="editabletext--confirm ethidden")


class EditableTextApp(App[None]):
    def compose(self) -> ComposeResult:
        yield EditableText()


app = EditableTextApp()


if __name__ == "__main__":
    app.run()
