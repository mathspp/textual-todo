from textual.app import App, ComposeResult

from textual_todo.todoitem import TodoItem


class DemoApp(App[None]):
    def compose(self) -> ComposeResult:
        yield TodoItem()

    def key_s(self):
        self.save_screenshot()


app = DemoApp()

if __name__ == "__main__":
    app.run()
