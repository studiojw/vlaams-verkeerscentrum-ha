"""Get data from the Verkeerscentrum API."""

from dataclasses import asdict, dataclass
from datetime import datetime
import time

import aiohttp
from bs4 import BeautifulSoup

from .exceptions import InvalidCredentialsException
from .api_helpers import (
    extract_actual_travel_time,
    extract_delay,
    extract_title,
    extract_description,
    extract_trajectory_id,
)


@dataclass
class Trajectory:
    """Data class for a trajectory."""

    id: str
    name: str
    description: str
    actual_travel_time: str
    delay: int

    def __eq__(self, other):
        """Override the default Equals behavior."""
        if not isinstance(other, Trajectory):
            return False
        return (
            self.id == other.id
            and self.name == other.name
            and self.description == other.description
            and self.actual_travel_time == other.actual_travel_time
            and self.delay == other.delay
        )


class VerkeersCentrumApi:
    """Verkeerscentrum API."""

    BASE_URL = "https://www.verkeerscentrum.be"
    LOGIN_URL = BASE_URL + "/user/login"
    USER_TRAJECTORIES_URL = BASE_URL + "/mijn-trajecten"

    def __init__(self, email, password) -> None:
        """Initialize."""
        self._email = email
        self._password = password
        self._session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))

    async def close(self):
        """Close the session."""
        await self._session.close()

    async def __session_cookie_is_valid(self):
        if not self._session:
            return False
        for cookie in self._session.cookie_jar:
            if cookie.key.startswith("SSESS"):
                expires = cookie["expires"]
                expires_datetime = datetime.strptime(
                    expires, "%a, %d-%b-%Y %H:%M:%S %Z"
                )
                expires_timestamp = expires_datetime.timestamp()
                return expires_timestamp > time.time()
        return False

    async def login(self):
        """Login to Verkeerscentrum."""
        form_data = {
            "form_id": "user_login_form",
            "op": "Inloggen",
            "name": self._email,
            "pass": self._password,
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        async with self._session.post(
            self.LOGIN_URL, data=form_data, headers=headers
        ) as response:
            if response.status != 200:
                raise InvalidCredentialsException
            soup = BeautifulSoup(await response.text(), "html.parser")
            account_element = soup.find("a", class_="account")
            if account_element is None:
                raise InvalidCredentialsException

    @staticmethod
    def _parse_trajectories_from_html(html: str) -> list[Trajectory]:
        soup = BeautifulSoup(html, "html.parser")
        trajectory_elements = soup.find_all("div", class_="user-trajectory")
        trajectories = []
        for element in trajectory_elements:
            trajectory_id = extract_trajectory_id(element)
            title = extract_title(element)
            description = extract_description(element)
            actual_travel_time = extract_actual_travel_time(element)
            delay = extract_delay(element) or 0
            trajectories.append(
                Trajectory(
                    id=trajectory_id,
                    name=title,
                    description=description,
                    actual_travel_time=actual_travel_time,
                    delay=delay,
                )
            )
        return trajectories

    async def get_user_trajectories(self) -> list[Trajectory]:
        """Get the user trajectories."""
        trajectories: list[Trajectory] = []
        if not await self.__session_cookie_is_valid():
            await self.login()
        async with self._session.get(self.USER_TRAJECTORIES_URL) as response:
            if response.status == 200:
                html = await response.text()
                trajectories = self._parse_trajectories_from_html(html)
        return trajectories

    async def get_user_trajectory(self, trajectory_id: str) -> dict[str, any] | None:
        """Get a user trajectory by its id."""
        trajectories = await self.get_user_trajectories()
        if trajectories:
            for traj in trajectories:
                if traj.id == trajectory_id:
                    return asdict(traj)
        return None
