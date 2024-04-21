from constant import BASE_URL, HEADERS
import requests

class TestBookings:

    def test_create_booking(self, auth_session, booking_data):

        create_booking = auth_session.post(f"{BASE_URL}/booking", json = booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"
        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"

        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data["totalprice"], "Заданная стоимость не совпадает"

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не найдена"

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 404, "Бронь не удалилась"

    def test_get_booking(self, auth_session, booking_data):
        get_booking = auth_session.get(f"{BASE_URL}/booking", json = booking_data)
        assert get_booking.status_code == 200, "Ошибка получения брони"
        booking_list = get_booking.json()
        assert len(booking_list) > 0, "Список бронирований пуст"
        first_booking = booking_list[0]
        booking_id = first_booking.get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"


    def test_update_booking(self, auth_session, create_booking):
        booking_id = create_booking
        updated_booking_data = {
            "firstname": "Alisa",
            "lastname": "Hard",
            "totalprice": 100500,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-04-25",
                "checkout": "2024-04-27"
            },
            "additionalneeds": "Big TV"
        }
        update_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=updated_booking_data)
        assert update_booking.status_code == 200, "Ошибка при обновлении бронирования"

        updated_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        updated_booking_data_response = updated_booking.json()
        assert updated_booking_data_response["firstname"] == updated_booking_data[
            "firstname"], "Имя бронирования не обновлено"
        assert updated_booking_data_response["lastname"] == updated_booking_data[
            "lastname"], "Фамилия бронирования не обновлена"

    def test_update_booking_without_token(self, create_booking):
        booking_id = create_booking
        updated_booking_data = {
            "firstname": "Alisa",
            "lastname": "Hard",
            "totalprice": 100500,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-04-25",
                "checkout": "2024-04-27"
            },
            "additionalneeds": "Big TV"
        }
        update_booking = requests.put(f"{BASE_URL}/booking/{booking_id}", json=updated_booking_data)
        assert update_booking.status_code in [403], "Ошибка аутентификации"

    def test_patch_booking(self, auth_session, create_booking):
        booking_id = create_booking

        updated_booking_data = {
            "firstname": "James",
            "lastname": "Brown"
        }
        patch_booking = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json=updated_booking_data)
        assert patch_booking.status_code == 200, "Ошибка при обновлении имени и фамилии бронирования"

    def test_patch_without_token(self, create_booking):
        booking_id = create_booking
        updated_booking_data = {
            "firstname": "James",
            "lastname": "Brown"
        }

        patch_booking = requests.patch(f"{BASE_URL}/booking/{booking_id}", json=updated_booking_data)
        assert patch_booking.status_code in [403], "Ошибка аутентификации"