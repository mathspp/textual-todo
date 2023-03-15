from textual.app import App, ComposeResult
from textual.widgets import Label, TextLog

from textual_todo.editabletext import EditableText


class NameApp(App[None]):
    CSS = """
    TextLog {
        height: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        yield Label("First name")
        yield EditableText(id="first")
        yield Label("Last name")
        yield EditableText(id="last")
        yield Label("Preferred name")
        yield EditableText(id="preferred")
        yield TextLog()

    def on_mount(self) -> None:
        for editable_text in self.query(EditableText):
            editable_text.switch_to_editing_mode()

    def on_editable_text_edit(self, event: EditableText.Edit) -> None:
        self.query_one(TextLog).write(f"Editing @ {event.editable_text.id}")

    def on_editable_text_display(self, event: EditableText.Display) -> None:
        self.query_one(TextLog).write(f"Displaying @ {event.editable_text.id}")


app = NameApp()


if __name__ == "__main__":
    app.run()
