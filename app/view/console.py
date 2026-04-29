import argparse
import shlex

from app.model.notification import (
    ConsoleChannel,
    FileChannel,
    MockChannel,
    NotificationError,
    NotificationService,
)


class ConsoleView:
    def __init__(self):
        channel = ConsoleChannel()
        self.service = NotificationService(channel)

    # ------------------------------------------------------------------
    # Static helpers
    # ------------------------------------------------------------------

    @staticmethod
    def show_welcome_msg():
        print(f"{'=' * 45}")
        print("  WELCOME TO THE NOTIFICATION SERVICE APP  ")
        print(f"{'=' * 45}")
        print("Type 'help' to view available commands.")

    @staticmethod
    def show_help(command: str | None = None):
        if not command:
            print("\nCOMMANDS:")
            print("help          - view this list. Use help <command> for details")
            print("send          - send a single notification")
            print("bulk          - send multiple notifications at once")
            print("history       - view delivery history for this session")
            print("status        - show current channel name and availability")
            print("switch        - switch to a different channel")
            print("exit          - close the application")
        else:
            match command:
                case "help":
                    print("help <command> - view the help message for a specific command")
                case "send":
                    print("Send a single notification through the active channel.")
                    print("Usage: send <message>")
                    print("Example: send 'Server is back online'")
                case "bulk":
                    print("Send multiple notifications (each quoted argument is one message).")
                    print("Usage: bulk <msg1> <msg2> ...")
                    print("Example: bulk 'Alert A' 'Alert B' 'Alert C'")
                case "history":
                    print("Show all messages delivered successfully in this session.")
                    print("Usage: history")
                case "status":
                    print("Show the active channel name and whether it is available.")
                    print("Usage: status")
                case "switch":
                    print("Switch the active channel. Supported types: console, file, mock")
                    print("Usage: switch <channel_type> [file_path]")
                    print("Example: switch file /tmp/notifications.txt")
                    print("Example: switch console")
                case _:
                    print(f">>> ERROR: unknown command '{command}'. Type 'help' to see all commands.")

    # ------------------------------------------------------------------
    # Command handlers
    # ------------------------------------------------------------------

    def send(self, args):
        try:
            self.service.send_notification(args.message)
        except NotificationError as e:
            print(f">>> ERROR: {e}")
        else:
            print("Notification sent successfully.")

    def bulk(self, args):
        count = self.service.send_bulk(args.messages)
        total = len(args.messages)
        print(f"Bulk send complete: {count}/{total} messages delivered.")

    def history(self):
        messages = self.service.get_history()
        if messages:
            print(f"\nDelivery history ({len(messages)} message(s)):")
            for i, msg in enumerate(messages, start=1):
                print(f"  {i}. {msg}")
        else:
            print("No messages delivered yet in this session.")

    def status(self):
        channel = self.service._channel
        available = "available" if channel.is_available() else "NOT available"
        print(f"Active channel: {channel.get_channel_name()} — {available}")

    def switch(self, args):
        match args.channel_type:
            case "console":
                self.service = NotificationService(ConsoleChannel())
                print("Switched to ConsoleChannel.")
            case "file":
                if not args.file_path:
                    print(">>> ERROR: file channel requires a file path. Usage: switch file <path>")
                    return
                self.service = NotificationService(FileChannel(args.file_path))
                print(f"Switched to FileChannel: {args.file_path}")
            case "mock":
                self.service = NotificationService(MockChannel())
                print("Switched to MockChannel (always unavailable — for testing).")
            case _:
                print(f">>> ERROR: unknown channel type '{args.channel_type}'. "
                      f"Choose from: console, file, mock")

    # ------------------------------------------------------------------
    # Command dispatcher
    # ------------------------------------------------------------------

    def process_user_command(self, user_input: str) -> bool:
        try:
            line = shlex.split(user_input)
        except ValueError as e:
            print(f">>> ERROR: could not parse input: {e}")
            return False

        if not line:
            return False

        command = line[0]
        params = line[1:]
        parser = argparse.ArgumentParser(add_help=False)

        match command:
            case "help":
                if params:
                    self.show_help(params[0])
                else:
                    self.show_help()
            case "send":
                parser.add_argument("message", type=str)
                args = parser.parse_args(params)
                self.send(args)
            case "bulk":
                parser.add_argument("messages", type=str, nargs="+")
                args = parser.parse_args(params)
                self.bulk(args)
            case "history":
                self.history()
            case "status":
                self.status()
            case "switch":
                parser.add_argument("channel_type", type=str)
                parser.add_argument("file_path", type=str, nargs="?", default=None)
                args = parser.parse_args(params)
                self.switch(args)
            case "exit":
                print("Goodbye!")
                return True
            case _:
                print(f">>> ERROR: unknown command '{command}'. Type 'help' to see all commands.")

        return False

    def app_loop(self):
        ConsoleView.show_welcome_msg()
        end_app = False
        while not end_app:
            user_input = input("\nNotificationApp > ")
            end_app = self.process_user_command(user_input)
