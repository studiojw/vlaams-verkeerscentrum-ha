"""Tests for api_helpers."""

from bs4 import BeautifulSoup

from custom_components.vlaams_verkeerscentrum.api_helpers import (
    extract_description,
    extract_trajectory_id,
    extract_title,
    extract_actual_travel_time,
    extract_delay,
)


def test_extract_trajectory_id():
    """Test the extract_trajectory_id function."""
    soup = BeautifulSoup(
        "<div class='details'><a href='/account/traject-123'>test</a></div>",
        "html.parser",
    )
    assert extract_trajectory_id(soup) == "123"


def test_extract_title():
    """Test the extract_title function."""
    soup = BeautifulSoup("<h3>test</h3>", "html.parser")
    assert extract_title(soup) == "test"


def test_extract_description():
    """Test the extract_description function."""
    soup = BeautifulSoup("<div class='points'>test</div>", "html.parser")
    assert extract_description(soup) == "test"


def test_extract_actual_travel_time():
    """Test the extract_actual_travel_time function."""
    soup = BeautifulSoup(
        "<span class='actual-travel-time'>34 min.</span>", "html.parser"
    )
    assert extract_actual_travel_time(soup) == 34


def test_extract_delay():
    """Test the extract_delay function."""
    soup = BeautifulSoup(
        "<span class='text-danger'>8 min. vertraging</span>", "html.parser"
    )
    assert extract_delay(soup) == 8
