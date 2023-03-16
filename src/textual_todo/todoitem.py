from __future__ import annotations

import datetime as dt

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.message import Message
from textual.widgets import Button, Input, Label, Static, Switch

from .datepicker import DatePicker
from .editabletext import EditableText


class TodoItem(Static):
    """Widget that represents a TODO item with a description and a due date."""

    DEFAULT_CSS = """
    TodoItem {
        background: $boost;
        /* May seem redundant but prevents resizing when date is selected/cleared. */
        border: heavy $panel-lighten-3;
        padding: 0 1;
    }

    /* Make sure the top row can be as tall as needed. */
    .todoitem--top-row {
        height: auto;
    }

    .todoitem--top-row .editabletext--label {
        height: auto;
    }

    TodoItem EditableText {
        height: auto;
    }

    /* On the other hand, the bottom row is always 3 lines tall. */
    .todoitem--bot-row {
        height: 3;
        align-horizontal: right;
    }

    /* Style some sub-widgets. */
    .todoitem--show-more {
        min-width: 0;
        width: auto;
    }

    .todoitem--status {
        height: 100%;
        width: 1fr;
        content-align-vertical: middle;
        text-opacity: 70%;
        padding-left: 3;
    }

    .todoitem--duedate {
        height: 100%;
        content-align-vertical: middle;
        padding-right: 1;
    }

    .todoitem--datepicker {
        width: 21;
        box-sizing: content-box;
    }

    .todoitem--datepicker .editabletext--label {
        border: tall $primary;
        padding: 0 2;
        height: 100%;
    }

    /* Restyle top row when collapsed and remove bottom row. */
    .todoitem--top-row .todoitem--collapsed {
        height: 3;
    }

    .todoitem--top-row .editabletext--label .todoitem--collapsed {
        height: 3;
    }

    TodoItem.todoitem--collapsed .editabletext--label {
        height: 3;
    }

    .todoitem--collapsed .todoitem--bot-row {
        display: none;
    }

    /* Change border colour according to due date status. */
    TodoItem.todoitem--due-late {
        border: heavy $error;
    }

    TodoItem.todoitem--due-today {
        border: heavy $warning;
    }

    TodoItem.todoitem--due-in-time {
        border: heavy $accent;
    }
    """

    class DueDateChanged(Message):
        """Posted when the due date changes."""

        todo_item: TodoItem

        def __init__(self, todo_item: TodoItem, date: dt.date) -> None:
            self.todo_item = todo_item
            self.date = date
            super().__init__()

    class DueDateCleared(Message):
        """Posted when the due date is reset."""

        todo_item: TodoItem

        def __init__(self, todo_item: TodoItem) -> None:
            self.todo_item = todo_item
            super().__init__()

    class Done(Message):
        """Posted when the TODO item is checked off."""

        todo_item: TodoItem

        def __init__(self, todo_item: TodoItem) -> None:
            self.todo_item = todo_item
            super().__init__()

    _show_more: Button
    """Sub widget to toggle the extra details about the TODO item."""
    _done: Switch
    """Sub widget to tick a TODO item as complete."""
    _description: EditableText
    """Sub widget holding the description of the TODO item."""
    _top_row: Horizontal
    """The top row of the widget."""
    _status: Label
    """Sub widget showing status information."""
    _due_date_label: Label
    """Sub widget labeling the date picker."""
    _date_picker: DatePicker
    """Sub widget to select due date."""
    _bot_row: Horizontal
    """The bottom row of the widget."""

    _cached_date: None | dt.date = None
    """The date in cache."""

    _initial_description: str = ""
    """The initial description to initialise the instance with."""
    _initial_date: str = ""
    """Date string to initialise the instance with."""

    def __init__(self, description: str = "", date: str = "", *args, **kwargs) -> None:
        self._initial_description = description
        self._initial_date = date
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        self._show_more = Button("v", classes="todoitem--show-more")
        self._done = Switch(classes="todoitem--done")
        self._description = EditableText(
            self._initial_description, classes="todoitem--description"
        )
        self._top_row = Horizontal(
            self._show_more,
            self._done,
            self._description,
            classes="todoitem--top-row",
        )

        self._due_date_label = Label("Due date:", classes="todoitem--duedate")
        self._date_picker = DatePicker(
            self._initial_date, classes="todoitem--datepicker"
        )
        self._status = Label("", classes="todoitem--status")
        self._bot_row = Horizontal(
            self._status,
            self._due_date_label,
            self._date_picker,
            classes="todoitem--bot-row",
        )

        yield self._top_row
        yield self._bot_row

    def on_mount(self) -> None:
        if not self._initial_description:
            self._description.switch_to_editing_mode()
            self.query(Input).first().focus()
        if self.due_date is None:
            self._date_picker.switch_to_editing_mode()
            if self._initial_description:
                self.query(Input).last().focus()

    @property
    def due_date(self) -> dt.date | None:
        """Date the item is due by, or None if not set."""
        if self._cached_date is None:
            self._cached_date = self._date_picker.date
        return self._cached_date

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Toggle the collapsed state."""
        event.stop()
        if self.is_collapsed:
            self.expand_description()
        else:
            self.collapse_description()

    def collapse_description(self) -> None:
        """Collapse this item if not yet collapsed."""
        self.add_class("todoitem--collapsed")
        self._show_more.label = ">"
        self.refresh(layout=True)

    def expand_description(self) -> None:
        """Expand this item if not yet expanded."""
        self.remove_class("todoitem--collapsed")
        self._show_more.label = "v"
        self.refresh(layout=True)

    @property
    def is_collapsed(self) -> bool:
        """Is the item collapsed?"""
        return self.has_class("todoitem--collapsed")

    def set_status_message(self, status: str, duration: float | None = None) -> None:
        """Set the status for a determined period of time.

        Args:
            status: The new status message.
            duration: How many seconds to keep the status message for.
                Setting this to None will keep it there until it is changed again.
        """
        self._status.renderable = status
        self._status.refresh()

        if duration is not None:
            self.set_timer(duration, self.reset_status)

    def reset_status(self) -> None:
        """Resets the status message to indicate time to deadline."""
        self._status.renderable = ""
        today = dt.date.today()
        date = self.due_date

        if date is None:
            self.set_status_message("")
            return

        delta = (date - today).days
        if delta > 1:
            self.set_status_message(f"Due in {delta} days.")
        elif delta == 1:
            self.set_status_message("Due in 1 day.")
        elif delta == 0:
            self.set_status_message("Due today.")
        elif delta == -1:
            self.set_status_message("1 day late!")
        else:
            self.set_status_message(f"{abs(delta)} days late!")

    def on_date_picker_selected(self, event: DatePicker.Selected) -> None:
        """Colour the TODO item according to its deadline."""
        event.stop()
        date = event.date
        if date == self._cached_date:
            return

        self._cached_date = date
        self.set_status_message("Date updated.", 1)

        self.update_style()

        self.post_message(self.DueDateChanged(self, date))

    def on_date_picker_cleared(self, event: DatePicker.DateCleared) -> None:
        """Clear all styling from a TODO item with no due date."""

        event.stop()
        if self._cached_date is None:
            return

        self._cached_date = None
        self.set_status_message("Date cleared.", 1)
        self.remove_class(
            "todoitem--due-late",
            "todoitem--due-today",
            "todoitem--due-in-time",
        )

        self.post_message(self.DueDateCleared(self))

    def on_switch_changed(self, event: Switch.Changed) -> None:
        """Emit event saying the TODO item was completed."""
        event.stop()
        self.post_message(self.Done(self))

    def update_style(self) -> None:
        """Update the class associated with the TODO item."""
        date = self._cached_date
        if date is None:
            return

        today = dt.date.today()
        self.remove_class(
            "todoitem--due-late", "todoitem--due-today", "todoitem--due-in-time"
        )
        if date < today:
            self.add_class("todoitem--due-late")
        elif date == today:
            self.add_class("todoitem--due-today")
        else:
            self.add_class("todoitem--due-in-time")
