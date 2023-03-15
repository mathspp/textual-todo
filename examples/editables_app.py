from textual.app import App, ComposeResult

from textual_todo.datepicker import DatePicker
from textual_todo.editabletext import EditableText


class EditablesApp(App[None]):
    def compose(self) -> ComposeResult:
        yield EditableText()
        yield DatePicker()


app = EditablesApp()


if __name__ == "__main__":
    app.run()
