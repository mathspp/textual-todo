from __future__ import annotations

import datetime as dt

from textual.message import Message

from .editabletext import EditableText


class DatePicker(EditableText):
    class DateCleared(Message):  # (1)!
        """Posted when the date selected is cleared."""

        date_picker: DatePicker
        """The DatePicker instance that had its date cleared."""

        def __init__(self, date_picker: DatePicker) -> None:
            super().__init__()
            self.date_picker = date_picker

    class Selected(Message):  # (2)!
        """Posted when a valid date is selected."""

        date_picker: DatePicker
        """The DatePicker instance that had its date selected."""
        date: dt.date
        """The date that was selected."""

        def __init__(self, date_picker: DatePicker, date: dt.date) -> None:
            super().__init__()
            self.date_picker = date_picker
            self.date = date

    def on_editable_text_display(self, event: EditableText.Display) -> None:  # (3)!
        event.stop()
        date = self.date
        if date is None:
            self.post_message(self.DateCleared(self))
        else:
            self.post_message(self.Selected(self, date))

    def on_editable_text_edit(self, event: EditableText.Edit) -> None:  # (4)!
        event.stop()

    @property
    def date(self) -> dt.date | None:
        """The date picked or None if not available."""
        try:
            return dt.datetime.strptime(self._input.value, "%d-%m-%Y").date()
        except ValueError:
            return None
