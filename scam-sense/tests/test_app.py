from pathlib import Path

from streamlit.testing.v1 import AppTest

APP_PATH = Path(__file__).parents[1] / "app.py"


def test_empty_analysis_has_friendly_validation() -> None:
    app = AppTest.from_file(str(APP_PATH)).run()
    app.button[0].click().run()
    assert "Add a message" in app.warning[0].value
    assert not app.exception


def test_high_risk_sample_renders_explained_result() -> None:
    app = AppTest.from_file(str(APP_PATH)).run()
    sample_labels = [option for option in app.selectbox[0].options if "Bank verification" in option]
    app.selectbox[0].select(sample_labels[0]).run()
    app.button[0].click().run()
    page = " ".join(markdown.value for markdown in app.markdown)
    headings = " ".join(subheader.value for subheader in app.subheader)
    assert "Critical risk" in page
    assert "Indicators detected" in headings
    assert "Safest next step" in headings
    assert "educational screening aid" in app.warning[0].value
    assert not app.exception


def test_clear_removes_message_and_result() -> None:
    app = AppTest.from_file(str(APP_PATH)).run()
    app.text_area[0].input("Urgent: pay $50 now").run()
    app.button[0].click().run()
    app.button[1].click().run()
    assert app.text_area[0].value == ""
    assert "Risk assessment:" not in " ".join(markdown.value for markdown in app.markdown)
