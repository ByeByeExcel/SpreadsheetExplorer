from unittest.mock import MagicMock

import pytest

from controller.workbook_controller import WorkbookController


@pytest.fixture
def mock_services():
    return {
        "connected_workbook_service": MagicMock(),
        "connection_service": MagicMock()
    }


@pytest.fixture
def controller(mock_services):
    return WorkbookController(
        connected_workbook_service=mock_services["connected_workbook_service"],
        connection_service=mock_services["connection_service"]
    )


def test_get_open_workbooks(controller, mock_services):
    mock_services["connection_service"].get_open_workbooks.return_value = ["Workbook1.xlsx"]
    result = controller.get_open_workbooks()
    assert result == ["Workbook1.xlsx"]
    mock_services["connection_service"].get_open_workbooks.assert_called_once()


def test_connect_and_parse_workbook(controller, mock_services):
    controller.connect_and_parse_workbook("TestWorkbook.xlsx")
    mock_services["connected_workbook_service"].connect_workbook.assert_called_with("TestWorkbook.xlsx")
    mock_services["connected_workbook_service"].parse_connected_workbook.assert_called_once()


def test_parse_connected_workbook(controller, mock_services):
    controller.parse_connected_workbook()
    mock_services["connected_workbook_service"].parse_connected_workbook.assert_called_once()


def test_disconnect_workbook(controller, mock_services):
    controller.disconnect_workbook()
    mock_services["connected_workbook_service"].disconnect_workbook.assert_called_once()


def test_set_tk_root(controller, mock_services):
    dummy_root = object()
    controller.set_tk_root(dummy_root)
    mock_services["connected_workbook_service"].set_root.assert_called_with(dummy_root)
