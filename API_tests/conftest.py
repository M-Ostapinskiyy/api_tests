import requests
import pytest
from faker import Faker
from constant import HEADERS, BASE_URL

faker = Faker()

@pytest.fixture(scope="session")
def auth_session():
    session = requests.Session()
    session.headers.update(HEADERS)

    auth_response = session.post(f"{BASE_URL}/auth", json={"username": "admin", "password": "password123"})
    assert auth_response.status_code == 200, "Ошибка авторизации, статус код не 200"
    token = auth_response.json().get("token")
    assert token is not None, "Токен не найден в ответе"

    session.headers.update({"Cookie": f"token={token}"})
    return session

@pytest.fixture()
def booking_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=100000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Cigars"
    }

@pytest.fixture
def create_booking(auth_session):
    booking_data = {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=100000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-20",
            "checkout": "2024-04-22"
        },
        "additionalneeds": "Breakfast"
    }
    response = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
    assert response.status_code == 200, "Ошибка при создании бронирования"

    booking_id = response.json().get("bookingid")
    assert booking_id is not None, "Идентификатор бронирования не найден в ответе"
    yield booking_id