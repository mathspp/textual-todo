from __future__ import annotations

from textual.app import App, ComposeResult
from textual.message import Message
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
        height: 3;
    }

    .editabletext--label {
        width: 1fr;
        height: 3;
        border: round $primary;
    }

    .editabletext--edit {
        min-width: 0;
        width: 4;
    }

    .editabletext--confirm {
        min-width: 0;
        width: 4;
    }

    EditableText .ethidden {
        display: none;
    }
    """

    _confirm_button: Button
    """The button to confirm changes to the text."""
    _edit_button: Button
    """The button to start editing the text."""
    _input: Input
    """The field that allows editing text."""
    _label: Label
    """The label that displays the text."""

    _initial_value: str = ""
    """The initial value to initialise the instance with."""

    class Display(Message):
        """The user switched to display mode."""

        editable_text: EditableText
        """The EditableText instance that changed into display mode."""

        def __init__(self, editable_text: EditableText) -> None:
            self.editable_text = editable_text
            super().__init__()

    class Edit(Message):
        """The user switched to edit mode."""

        editable_text: EditableText
        """The EditableText instance that changed into edit mode."""

        def __init__(self, editable_text: EditableText) -> None:
            self.editable_text = editable_text
            super().__init__()

    def __init__(self, value: str = "", *args, **kwargs) -> None:
        self._initial_value = value
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        self._input = Input(
            value=self._initial_value,
            placeholder="Type something...",
            classes="editabletext--input ethidden",
        )
        self._label = Label(self._initial_value, classes="editabletext--label")
        self._edit_button = Button("📝", classes="editabletext--edit")
        self._confirm_button = Button(
            "✅", classes="editabletext--confirm ethidden", disabled=True
        )

        yield self._input
        yield self._label
        yield self._edit_button
        yield self._confirm_button

    @property
    def is_editing(self) -> bool:
        """Is the text being edited?"""
        return not self._input.has_class("ethidden")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        event.stop()
        if self.is_editing:
            self.switch_to_display_mode()
        else:
            self.switch_to_editing_mode()

    def switch_to_editing_mode(self) -> None:
        if self.is_editing:
            return

        self._input.value = str(self._label.renderable)

        self._label.add_class("ethidden")
        self._input.remove_class("ethidden")

        self._edit_button.disabled = True
        self._edit_button.add_class("ethidden")
        self._confirm_button.disabled = False
        self._confirm_button.remove_class("ethidden")

        self.post_message(self.Edit(self))

    def switch_to_display_mode(self) -> None:
        if not self.is_editing:
            return

        self._label.renderable = self._input.value

        self._input.add_class("ethidden")
        self._label.remove_class("ethidden")

        self._confirm_button.disabled = True
        self._confirm_button.add_class("ethidden")
        self._edit_button.disabled = False
        self._edit_button.remove_class("ethidden")

        self.post_message(self.Display(self))


class EditableTextApp(App[None]):
    def compose(self) -> ComposeResult:
        yield EditableText()


app = EditableTextApp()


if __name__ == "__main__":
    app.run()
