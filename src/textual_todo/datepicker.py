from __future__ import annotations

import datetime as dt

from textual.app import ComposeResult
from textual.message import Message

from .editabletext import EditableText


class DatePicker(EditableText):
    DEFAULT_CSS = """
    DatePicker {
        width: 21;
    }
    """

    class DateCleared(Message):
        """Posted when the date selected is cleared."""

        date_picker: DatePicker
        """The DatePicker instance that had its date cleared."""

        def __init__(self, date_picker: DatePicker) -> None:
            super().__init__()
            self.date_picker = date_picker

    class Selected(Message):
        """Posted when a valid date is selected."""

        date_picker: DatePicker
        """The DatePicker instance that had its date selected."""
        date: dt.date
        """The date that was selected."""

        def __init__(self, date_picker: DatePicker, date: dt.date) -> None:
            super().__init__()
            self.date_picker = date_picker
            self.date = date

    def compose(self) -> ComposeResult:
        super_compose = list(super().compose())
        self._input.placeholder = "dd-mm-yy"
        yield from super_compose

    def switch_to_display_mode(self) -> None:
        """Switch to display mode only if the date is empty or valid."""
        if self._input.value and self.date is None:
            self.app.bell()
            return
        return super().switch_to_display_mode()

    def on_editable_text_display(self, event: EditableText.Display) -> None:
        event.stop()
        date = self.date
        if date is None:
            self.post_message(self.DateCleared(self))
        else:
            self.post_message(self.Selected(self, date))

    def on_editable_text_edit(self, event: EditableText.Edit) -> None:
        event.stop()

    @property
    def date(self) -> dt.date | None:
        """The date picked or None if not available."""
        try:
            return dt.datetime.strptime(self._input.value, "%d-%m-%Y").date()
        except ValueError:
            return None
