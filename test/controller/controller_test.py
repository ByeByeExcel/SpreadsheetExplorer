import os
import tempfile
import time

import openpyxl as pxl
import pytest

from controller.controller import Controller
from model.services.active_workbook_service import ActiveWorkbookService


@pytest.fixture
def simple_excel_sheet():
    fd, path = tempfile.mkstemp(suffix=".xlsx")
    os.close(fd)

    workbook = pxl.Workbook()
    worksheet = workbook.active

    worksheet["A1"] = 5
    worksheet["A2"] = 6
    worksheet["A3"] = "=A1*A2"
    worksheet["A4"] = "=SUM(A1:A3)"
    worksheet["A5"] = "=SUM(A1:A3) + A1 - 2"
    worksheet["A6"] = "=SUM(B3) + A1 - 2"

    workbook.save(path)

    yield path
    os.remove(path)


@pytest.fixture
def simple_excel_sheet2():
    fd, path = tempfile.mkstemp(suffix=".xlsx")
    os.close(fd)

    workbook = pxl.Workbook()
    worksheet = workbook.active

    worksheet["A1"] = 5
    worksheet["A2"] = 6
    worksheet["A3"] = "=A1*A2"
    worksheet["A4"] = "=SUM(A1:A3)"
    worksheet["A5"] = "=SUM(A1:A3) + A1 - 2"
    worksheet["A6"] = "=SUM(B3) + A1 - 2"

    workbook.save(path)

    yield path
    os.remove(path)


def test_listener_loop(simple_excel_sheet, simple_excel_sheet2):
    active_workbook_service = ActiveWorkbookService()
    active_workbook_service.connect_and_parse_workbook(simple_excel_sheet)
    active_workbook_service.connect_and_parse_workbook(simple_excel_sheet2)

    controller = Controller(active_workbook_service)
    controller.highlight_dependents_precedents()
    time.sleep(10)
    controller.stop_watchers()
