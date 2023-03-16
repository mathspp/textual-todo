from __future__ import annotations

import json

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Footer

from .editabletext import EditableText
from .todoitem import TodoItem


DATA_FILE = "items.json"


class TODOApp(App[None]):
    """A simple and elegant TODO app built with Textual."""

    BINDINGS = [
        ("n", "new_todo", "New"),
        ("c", "collapse_all", "Collapse all"),
        ("e", "expand_all", "Expand all"),
    ]

    _todo_container: Vertical
    """Container for all the TODO items that are due."""

    def compose(self) -> ComposeResult:
        self._todo_container = Vertical(id="todo-container")
        yield self._todo_container
        yield Footer()

    async def action_new_todo(self) -> None:
        """Add a new TODO item to the list."""
        new_todo = TodoItem()
        await self._todo_container.mount(new_todo)
        new_todo.scroll_visible()
        new_todo.set_status_message("Add description and due date.")
        self._save_to_file()

    async def on_todo_item_done(self, event: TodoItem.Done) -> None:
        """If an item is done, get rid of it.

        In a more conventional TODO app, completed items would likely be archived
        instead of completely obliterated.
        """
        await event.todo_item.remove()
        self._save_to_file()

    def on_todo_item_due_date_changed(self, event: TodoItem.DueDateChanged) -> None:
        self._sort_todo_item(event.todo_item)
        self._save_to_file()

    def on_todo_item_due_date_cleared(self, event: TodoItem.DueDateCleared) -> None:
        self._sort_todo_item(event.todo_item)
        self._save_to_file()

    def _sort_todo_item(self, item: TodoItem) -> None:
        """Sort the given TODO item in order, by date."""

        if len(self._todo_container.children) == 1:
            return

        date = item.due_date
        for idx, todo in enumerate(self._todo_container.query(TodoItem)):
            if todo is item:
                continue
            if todo.due_date is None or (date is not None and todo.due_date > date):
                self._todo_container.move_child(item, before=idx)
                return

        end = len(self._todo_container.children) - 1
        if self._todo_container.children[end] != item:
            self._todo_container.move_child(item, after=end)

    def action_collapse_all(self) -> None:
        for todo_item in self._todo_container.query(TodoItem):
            todo_item.collapse_description()

    def action_expand_all(self) -> None:
        for todo_item in self._todo_container.query(TodoItem):
            todo_item.expand_description()

    async def on_mount(self) -> None:
        await self._read_from_file(DATA_FILE)

    async def _read_from_file(self, path: str) -> None:
        """Import TODO items from a JSON file."""
        data: list[dict[str, str]]
        try:
            with open(path, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        for item in data:
            new_todo = TodoItem(item["description"], item["date"])
            await self._todo_container.mount(new_todo)
            new_todo.update_style()
            new_todo.reset_status()
            self._sort_todo_item(new_todo)

        self.action_collapse_all()

    def _save_to_file(self) -> None:
        data = [
            {
                "description": str(todo._description._label.renderable),
                "date": str(todo._date_picker._label.renderable),
            }
            for todo in self._todo_container.query(TodoItem)
        ]

        with open(DATA_FILE, "w") as f:
            json.dump(data, f)

    def on_editable_text_display(self, event: EditableText.Display) -> None:
        self._save_to_file()


app = TODOApp()


if __name__ == "__main__":
    app.run()
