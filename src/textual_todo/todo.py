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


app = TODOApp()


if __name__ == "__main__":
    app.run()
