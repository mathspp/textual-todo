from __future__ import annotations

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Footer

from .todoitem import TodoItem


class TODOApp(App[None]):
    """A simple and elegant TODO app built with Textual."""

    BINDINGS = [
        ("n", "new_todo", "New"),
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

    async def on_todo_item_done(self, event: TodoItem.Done) -> None:
        """If an item is done, get rid of it.

        In a more conventional TODO app, completed items would likely be archived
        instead of completely obliterated.
        """
        await event.todo_item.remove()

    def on_todo_item_due_date_changed(self, event: TodoItem.DueDateChanged) -> None:
        self._sort_todo_item(event.todo_item)

    def on_todo_item_due_date_cleared(self, event: TodoItem.DueDateCleared) -> None:
        self._sort_todo_item(event.todo_item)

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


app = TODOApp()


if __name__ == "__main__":
    app.run()
