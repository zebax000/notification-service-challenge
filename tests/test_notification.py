import inspect

import pytest

import app.model.notification as notification_module

# ---------------------------------------------------------------------------
# Introspect available symbols so we can skip missing ones gracefully
# ---------------------------------------------------------------------------

module_members = [item[0] for item in inspect.getmembers(notification_module)]

notification_channel_defined = "NotificationChannel" in module_members
console_channel_defined = "ConsoleChannel" in module_members
file_channel_defined = "FileChannel" in module_members
mock_channel_defined = "MockChannel" in module_members
notification_service_defined = "NotificationService" in module_members
delivery_report_defined = "DeliveryReport" in module_members
notification_error_defined = "NotificationError" in module_members
channel_unavailable_error_defined = "ChannelUnavailableError" in module_members
delivery_error_defined = "DeliveryError" in module_members

if notification_channel_defined:
    from app.model.notification import NotificationChannel

if console_channel_defined:
    from app.model.notification import ConsoleChannel

if file_channel_defined:
    from app.model.notification import FileChannel

if mock_channel_defined:
    from app.model.notification import MockChannel

if notification_service_defined:
    from app.model.notification import NotificationService

if delivery_report_defined:
    from app.model.notification import DeliveryReport

if notification_error_defined:
    from app.model.notification import NotificationError

if channel_unavailable_error_defined:
    from app.model.notification import ChannelUnavailableError

if delivery_error_defined:
    from app.model.notification import DeliveryError


# ---------------------------------------------------------------------------
# TestExceptions
# ---------------------------------------------------------------------------

class TestNotificationChannelAbstraction:
    """Validates that NotificationChannel is defined as a Protocol or an ABC."""

    @pytest.mark.skipif(not notification_channel_defined, reason="NotificationChannel not defined")
    def test_notification_channel_is_protocol_or_abstract_class(self):
        from abc import ABCMeta
        is_protocol = getattr(NotificationChannel, "_is_protocol", False)
        is_pure_abc = (
            isinstance(NotificationChannel, ABCMeta)
            and bool(getattr(NotificationChannel, "__abstractmethods__", frozenset()))
            and not is_protocol
        )
        assert is_protocol or is_pure_abc, (
            "NotificationChannel must be defined as typing.Protocol or abc.ABC with @abstractmethod"
        )

    @pytest.mark.skipif(not notification_channel_defined, reason="NotificationChannel not defined")
    @pytest.mark.parametrize("method_name", ["send", "get_channel_name", "is_available"])
    def test_notification_channel_declares_required_methods(self, method_name):
        assert hasattr(NotificationChannel, method_name), (
            f"NotificationChannel must declare '{method_name}'"
        )


class TestExceptions:

    @pytest.mark.skipif(not notification_error_defined, reason="NotificationError not defined")
    def test_notification_error_is_exception_subclass(self):
        assert issubclass(NotificationError, Exception), (
            "NotificationError must inherit from Exception"
        )

    @pytest.mark.skipif(
        not (notification_error_defined and channel_unavailable_error_defined),
        reason="NotificationError or ChannelUnavailableError not defined",
    )
    def test_channel_unavailable_error_inherits_notification_error(self):
        assert issubclass(ChannelUnavailableError, NotificationError), (
            "ChannelUnavailableError must inherit from NotificationError"
        )

    @pytest.mark.skipif(
        not (notification_error_defined and delivery_error_defined),
        reason="NotificationError or DeliveryError not defined",
    )
    def test_delivery_error_inherits_notification_error(self):
        assert issubclass(DeliveryError, NotificationError), (
            "DeliveryError must inherit from NotificationError"
        )

    @pytest.mark.skipif(
        not (notification_error_defined and channel_unavailable_error_defined),
        reason="NotificationError or ChannelUnavailableError not defined",
    )
    def test_channel_unavailable_error_can_be_caught_as_notification_error(self):
        with pytest.raises(NotificationError):
            raise ChannelUnavailableError("test")

    @pytest.mark.skipif(
        not (notification_error_defined and delivery_error_defined),
        reason="NotificationError or DeliveryError not defined",
    )
    def test_delivery_error_can_be_caught_as_notification_error(self):
        with pytest.raises(NotificationError):
            raise DeliveryError("test")


# ---------------------------------------------------------------------------
# TestConsoleChannel
# ---------------------------------------------------------------------------

class TestConsoleChannel:

    @pytest.mark.skipif(not console_channel_defined, reason="ConsoleChannel not defined")
    def test_console_channel_is_not_dataclass(self):
        assert not hasattr(ConsoleChannel, "__dataclass_params__"), (
            "ConsoleChannel must not be a dataclass"
        )

    @pytest.mark.skipif(not console_channel_defined, reason="ConsoleChannel not defined")
    def test_console_channel_is_always_available(self):
        channel = ConsoleChannel()
        assert channel.is_available() is True, (
            "ConsoleChannel.is_available() must always return True"
        )

    @pytest.mark.skipif(not console_channel_defined, reason="ConsoleChannel not defined")
    def test_console_channel_name_returns_str(self):
        channel = ConsoleChannel()
        assert isinstance(channel.get_channel_name(), str), (
            "get_channel_name() must return a str"
        )

    @pytest.mark.skipif(not console_channel_defined, reason="ConsoleChannel not defined")
    def test_console_channel_name_value(self):
        channel = ConsoleChannel()
        assert channel.get_channel_name() == "console", (
            "get_channel_name() must return 'console'"
        )

    @pytest.mark.skipif(not console_channel_defined, reason="ConsoleChannel not defined")
    def test_console_channel_send_outputs_message(self, capsys):
        channel = ConsoleChannel()
        channel.send("Hello, World!")
        captured = capsys.readouterr()
        assert "Hello, World!" in captured.out, (
            "send() must print the message to stdout"
        )

    @pytest.mark.skipif(not console_channel_defined, reason="ConsoleChannel not defined")
    def test_console_channel_send_returns_none(self, capsys):
        channel = ConsoleChannel()
        result = channel.send("Test")
        assert result is None, "send() must return None"

    @pytest.mark.skipif(
        not (console_channel_defined and notification_channel_defined),
        reason="ConsoleChannel or NotificationChannel not defined",
    )
    def test_console_channel_implements_channel_interface(self):
        channel = ConsoleChannel()
        assert isinstance(channel, NotificationChannel), (
            "ConsoleChannel must implement the NotificationChannel interface"
        )

    @pytest.mark.skipif(not console_channel_defined, reason="ConsoleChannel not defined")
    @pytest.mark.parametrize("method_name", ["send", "get_channel_name", "is_available"])
    def test_console_channel_has_required_methods(self, method_name):
        channel = ConsoleChannel()
        assert hasattr(channel, method_name), (
            f"ConsoleChannel must have a '{method_name}' method"
        )
        assert callable(getattr(channel, method_name)), (
            f"'{method_name}' must be callable"
        )


# ---------------------------------------------------------------------------
# TestFileChannel
# ---------------------------------------------------------------------------

class TestFileChannel:

    @pytest.mark.skipif(not file_channel_defined, reason="FileChannel not defined")
    def test_file_channel_has_file_path_attribute(self, tmp_path):
        channel = FileChannel(str(tmp_path / "notif.txt"))
        assert hasattr(channel, "file_path"), (
            "FileChannel must have a 'file_path' attribute"
        )
        assert isinstance(channel.file_path, str), (
            "file_path must be a str"
        )

    @pytest.mark.skipif(not file_channel_defined, reason="FileChannel not defined")
    def test_file_channel_available_when_parent_dir_exists(self, tmp_path):
        channel = FileChannel(str(tmp_path / "notif.txt"))
        assert channel.is_available() is True, (
            "FileChannel must be available when the parent directory is writable"
        )

    @pytest.mark.skipif(not file_channel_defined, reason="FileChannel not defined")
    def test_file_channel_unavailable_for_nonexistent_parent(self):
        channel = FileChannel("/nonexistent_dir_xyz/notif.txt")
        assert channel.is_available() is False, (
            "FileChannel must not be available when the parent directory does not exist"
        )

    @pytest.mark.skipif(not file_channel_defined, reason="FileChannel not defined")
    def test_file_channel_send_writes_to_file(self, tmp_path):
        file_path = str(tmp_path / "notif.txt")
        channel = FileChannel(file_path)
        channel.send("Test notification")
        with open(file_path, "r") as f:
            content = f.read()
        assert "Test notification" in content, (
            "send() must write the message to the file"
        )

    @pytest.mark.skipif(not file_channel_defined, reason="FileChannel not defined")
    def test_file_channel_send_appends_multiple_messages(self, tmp_path):
        file_path = str(tmp_path / "notif.txt")
        channel = FileChannel(file_path)
        channel.send("First")
        channel.send("Second")
        with open(file_path, "r") as f:
            lines = f.readlines()
        assert len(lines) == 2, (
            "send() must append a new line for each message"
        )
        assert any("First" in l for l in lines), "First message must be in file"
        assert any("Second" in l for l in lines), "Second message must be in file"

    @pytest.mark.skipif(
        not (file_channel_defined and channel_unavailable_error_defined),
        reason="FileChannel or ChannelUnavailableError not defined",
    )
    def test_file_channel_send_raises_when_unavailable(self):
        channel = FileChannel("/nonexistent_dir_xyz/notif.txt")
        with pytest.raises(ChannelUnavailableError):
            channel.send("Test")

    @pytest.mark.skipif(not file_channel_defined, reason="FileChannel not defined")
    def test_file_channel_name_returns_str(self, tmp_path):
        channel = FileChannel(str(tmp_path / "notif.txt"))
        assert isinstance(channel.get_channel_name(), str), (
            "get_channel_name() must return a str"
        )

    @pytest.mark.skipif(
        not (file_channel_defined and notification_channel_defined),
        reason="FileChannel or NotificationChannel not defined",
    )
    def test_file_channel_implements_channel_interface(self, tmp_path):
        channel = FileChannel(str(tmp_path / "notif.txt"))
        assert isinstance(channel, NotificationChannel), (
            "FileChannel must implement the NotificationChannel interface"
        )


# ---------------------------------------------------------------------------
# TestMockChannel
# ---------------------------------------------------------------------------

class TestMockChannel:

    @pytest.mark.skipif(not mock_channel_defined, reason="MockChannel not defined")
    def test_mock_channel_is_never_available(self):
        channel = MockChannel()
        assert channel.is_available() is False, (
            "MockChannel.is_available() must always return False"
        )

    @pytest.mark.skipif(not mock_channel_defined, reason="MockChannel not defined")
    def test_mock_channel_name_returns_str(self):
        channel = MockChannel()
        assert isinstance(channel.get_channel_name(), str), (
            "get_channel_name() must return a str"
        )

    @pytest.mark.skipif(not mock_channel_defined, reason="MockChannel not defined")
    def test_mock_channel_name_value(self):
        channel = MockChannel()
        assert channel.get_channel_name() == "mock", (
            "get_channel_name() must return 'mock'"
        )

    @pytest.mark.skipif(
        not (mock_channel_defined and channel_unavailable_error_defined),
        reason="MockChannel or ChannelUnavailableError not defined",
    )
    def test_mock_channel_send_raises_channel_unavailable_error(self):
        channel = MockChannel()
        with pytest.raises(ChannelUnavailableError):
            channel.send("Any message")

    @pytest.mark.skipif(
        not (mock_channel_defined and notification_channel_defined),
        reason="MockChannel or NotificationChannel not defined",
    )
    def test_mock_channel_implements_channel_interface(self):
        channel = MockChannel()
        assert isinstance(channel, NotificationChannel), (
            "MockChannel must implement the NotificationChannel interface"
        )

    @pytest.mark.skipif(not mock_channel_defined, reason="MockChannel not defined")
    @pytest.mark.parametrize("method_name", ["send", "get_channel_name", "is_available"])
    def test_mock_channel_has_required_methods(self, method_name):
        channel = MockChannel()
        assert hasattr(channel, method_name), (
            f"MockChannel must have a '{method_name}' method"
        )
        assert callable(getattr(channel, method_name)), (
            f"'{method_name}' must be callable"
        )


# ---------------------------------------------------------------------------
# Fixtures for NotificationService tests
# ---------------------------------------------------------------------------

@pytest.fixture()
def console_service():
    return NotificationService(ConsoleChannel())


@pytest.fixture()
def file_service(tmp_path):
    return NotificationService(FileChannel(str(tmp_path / "notif.txt")))


@pytest.fixture()
def mock_service():
    return NotificationService(MockChannel())


# ---------------------------------------------------------------------------
# TestNotificationService
# ---------------------------------------------------------------------------

class TestNotificationService:

    @pytest.mark.skipif(not notification_service_defined, reason="NotificationService not defined")
    def test_service_has_channel_attribute(self, console_service):
        assert hasattr(console_service, "_channel"), (
            "NotificationService must have a '_channel' attribute"
        )

    @pytest.mark.skipif(not notification_service_defined, reason="NotificationService not defined")
    def test_service_has_history_attribute(self, console_service):
        assert hasattr(console_service, "_history"), (
            "NotificationService must have a '_history' attribute"
        )
        assert isinstance(console_service._history, list), (
            "'_history' must be a list"
        )

    @pytest.mark.skipif(not notification_service_defined, reason="NotificationService not defined")
    def test_get_history_initially_empty(self, console_service):
        assert console_service.get_history() == [], (
            "get_history() must return an empty list initially"
        )

    @pytest.mark.skipif(not notification_service_defined, reason="NotificationService not defined")
    def test_send_notification_records_message_in_history(self, console_service, capsys):
        console_service.send_notification("Hello!")
        assert "Hello!" in console_service.get_history(), (
            "Successfully sent messages must appear in history"
        )

    @pytest.mark.skipif(not notification_service_defined, reason="NotificationService not defined")
    def test_send_notification_accumulates_history(self, console_service, capsys):
        console_service.send_notification("First")
        console_service.send_notification("Second")
        history = console_service.get_history()
        assert len(history) == 2, (
            f"Expected 2 messages in history, got {len(history)}: {history}"
        )
        assert "First" in history, "First message must be in history"
        assert "Second" in history, "Second message must be in history"

    @pytest.mark.skipif(
        not (notification_service_defined and channel_unavailable_error_defined),
        reason="NotificationService or ChannelUnavailableError not defined",
    )
    def test_send_notification_raises_when_channel_unavailable(self, mock_service):
        with pytest.raises(ChannelUnavailableError):
            mock_service.send_notification("Test")

    @pytest.mark.skipif(not notification_service_defined, reason="NotificationService not defined")
    def test_failed_send_not_recorded_in_history(self, mock_service):
        try:
            mock_service.send_notification("Test")
        except Exception:
            pass
        assert mock_service.get_history() == [], (
            "Failed sends must not appear in history"
        )

    @pytest.mark.skipif(not notification_service_defined, reason="NotificationService not defined")
    def test_send_bulk_returns_delivered_count(self, console_service, capsys):
        messages = ["msg1", "msg2", "msg3"]
        count = console_service.send_bulk(messages)
        assert count == 3, (
            f"Expected 3 delivered messages, got {count}"
        )

    @pytest.mark.skipif(not notification_service_defined, reason="NotificationService not defined")
    def test_send_bulk_skips_all_when_channel_unavailable(self, mock_service):
        messages = ["msg1", "msg2"]
        count = mock_service.send_bulk(messages)
        assert count == 0, (
            f"Expected 0 delivered messages on unavailable channel, got {count}"
        )

    @pytest.mark.skipif(not notification_service_defined, reason="NotificationService not defined")
    def test_send_bulk_records_only_delivered_in_history(self, console_service, capsys):
        console_service.send_bulk(["A", "B"])
        assert len(console_service.get_history()) == 2, (
            "send_bulk must record each delivered message in history"
        )

    @pytest.mark.skipif(not notification_service_defined, reason="NotificationService not defined")
    def test_get_history_returns_copy(self, console_service, capsys):
        console_service.send_notification("Original")
        history = console_service.get_history()
        history.append("Injected")
        assert "Injected" not in console_service.get_history(), (
            "get_history() must return a copy — mutating it must not affect internal state"
        )

    @pytest.mark.skipif(not notification_service_defined, reason="NotificationService not defined")
    def test_send_notification_returns_none(self, console_service, capsys):
        result = console_service.send_notification("Test")
        assert result is None, "send_notification() must return None"

    @pytest.mark.skipif(not notification_service_defined, reason="NotificationService not defined")
    @pytest.mark.parametrize(
        "method_name, expected_return_type",
        [
            ("send_notification", type(None)),
            ("send_bulk", int),
            ("get_history", list),
        ],
    )
    def test_service_has_required_methods(
        self, console_service, capsys, method_name, expected_return_type
    ):
        assert hasattr(console_service, method_name), (
            f"NotificationService must have a '{method_name}' method"
        )
        assert callable(getattr(console_service, method_name)), (
            f"'{method_name}' must be callable"
        )

    # --- File channel integration ---

    @pytest.mark.skipif(not notification_service_defined, reason="NotificationService not defined")
    def test_service_works_with_file_channel(self, file_service):
        file_service.send_notification("Written to file")
        assert "Written to file" in file_service.get_history(), (
            "FileChannel-backed service must record deliveries in history"
        )


# ---------------------------------------------------------------------------
# TestDeliveryReport (Part 2)
# ---------------------------------------------------------------------------

class TestDeliveryReport:

    @pytest.mark.skipif(not delivery_report_defined, reason="DeliveryReport not defined")
    def test_delivery_report_is_dataclass(self):
        report = DeliveryReport(
            channel_name="console",
            total_attempted=5,
            total_delivered=4,
            messages=["a", "b", "c", "d"],
        )
        assert hasattr(report, "__dataclass_params__"), (
            "DeliveryReport must be a dataclass"
        )

    @pytest.mark.skipif(not delivery_report_defined, reason="DeliveryReport not defined")
    @pytest.mark.parametrize(
        "attr_name, attr_type",
        [
            ("channel_name", str),
            ("total_attempted", int),
            ("total_delivered", int),
            ("messages", list),
            ("report_id", str),
        ],
    )
    def test_delivery_report_has_attributes(self, attr_name, attr_type):
        report = DeliveryReport(
            channel_name="console",
            total_attempted=3,
            total_delivered=3,
            messages=["x", "y", "z"],
        )
        assert hasattr(report, attr_name), (
            f"DeliveryReport must have a '{attr_name}' attribute"
        )
        assert isinstance(getattr(report, attr_name), attr_type), (
            f"'{attr_name}' must be of type {attr_type.__name__}"
        )

    @pytest.mark.skipif(not delivery_report_defined, reason="DeliveryReport not defined")
    def test_delivery_report_success_rate_full(self):
        report = DeliveryReport(
            channel_name="console",
            total_attempted=4,
            total_delivered=4,
        )
        assert report.success_rate() == 1.0, (
            f"Expected success_rate 1.0, got {report.success_rate()}"
        )

    @pytest.mark.skipif(not delivery_report_defined, reason="DeliveryReport not defined")
    def test_delivery_report_success_rate_partial(self):
        report = DeliveryReport(
            channel_name="console",
            total_attempted=4,
            total_delivered=2,
        )
        assert report.success_rate() == 0.5, (
            f"Expected success_rate 0.5, got {report.success_rate()}"
        )

    @pytest.mark.skipif(not delivery_report_defined, reason="DeliveryReport not defined")
    def test_delivery_report_success_rate_zero_attempts(self):
        report = DeliveryReport(
            channel_name="console",
            total_attempted=0,
            total_delivered=0,
        )
        assert report.success_rate() == 0.0, (
            f"Expected success_rate 0.0 when no attempts, got {report.success_rate()}"
        )

    @pytest.mark.skipif(not delivery_report_defined, reason="DeliveryReport not defined")
    def test_delivery_report_is_empty_when_no_delivered(self):
        report = DeliveryReport(
            channel_name="mock",
            total_attempted=3,
            total_delivered=0,
        )
        assert report.is_empty() is True, (
            "is_empty() must return True when total_delivered == 0"
        )

    @pytest.mark.skipif(not delivery_report_defined, reason="DeliveryReport not defined")
    def test_delivery_report_is_not_empty_when_delivered(self):
        report = DeliveryReport(
            channel_name="console",
            total_attempted=2,
            total_delivered=2,
        )
        assert report.is_empty() is False, (
            "is_empty() must return False when total_delivered > 0"
        )

    @pytest.mark.skipif(not delivery_report_defined, reason="DeliveryReport not defined")
    def test_delivery_report_str_contains_expected_fields(self):
        report = DeliveryReport(
            channel_name="console",
            total_attempted=5,
            total_delivered=4,
        )
        report_str = str(report)
        assert report.channel_name in report_str, (
            "__str__ must include channel_name"
        )
        assert str(report.total_attempted) in report_str, (
            "__str__ must include total_attempted"
        )
        assert str(report.total_delivered) in report_str, (
            "__str__ must include total_delivered"
        )

    @pytest.mark.skipif(not delivery_report_defined, reason="DeliveryReport not defined")
    def test_delivery_report_has_unique_id(self):
        r1 = DeliveryReport(channel_name="c", total_attempted=1, total_delivered=1)
        r2 = DeliveryReport(channel_name="c", total_attempted=1, total_delivered=1)
        assert r1.report_id != r2.report_id, (
            "Each DeliveryReport must have a unique report_id"
        )
