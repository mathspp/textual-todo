from __future__ import annotations

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Footer


class TODOApp(App[None]):
    _todo_container: Vertical
    """Container for all the TODO items that are due."""

    def compose(self) -> ComposeResult:
        self._todo_container = Vertical(id="todo-container")
        yield self._todo_container
        yield Footer()


app = TODOApp()


if __name__ == "__main__":
    app.run()
