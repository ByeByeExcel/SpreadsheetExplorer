import pytest
import xlwings as xw


@pytest.fixture(scope='session')
def excel_app():
    app = xw.App(visible=False)
    yield app
    app.quit()
