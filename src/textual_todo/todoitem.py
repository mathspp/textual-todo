from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Horizontal
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
    """

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

    def compose(self) -> ComposeResult:
        self._show_more = Button("v", classes="todoitem--show-more")
        self._done = Switch(classes="todoitem--done")
        self._description = EditableText(classes="todoitem--description")
        self._top_row = Horizontal(
            self._show_more,
            self._done,
            self._description,
            classes="todoitem--top-row",
        )

        self._due_date_label = Label("Due date:", classes="todoitem--duedate")
        self._date_picker = DatePicker(classes="todoitem--datepicker")
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
        self._description.switch_to_editing_mode()
        self._date_picker.switch_to_editing_mode()
        self.query(Input).first().focus()
