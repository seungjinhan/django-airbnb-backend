from rest_framework.test import APITestCase

from . import models

from users.models import User


class TestAmenities(APITestCase):

    URL = "/api/v1/rooms/amenities/"
    NAME = "Amenity Test"
    DESC = "Amenity DESC"

    def setUp(self) -> None:
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_all_amenites(self):
        res = self.client.get(self.URL)
        data = res.json()
        self.assertEqual(res.status_code, 200, "Status code isn't 200")
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], self.NAME)

    def test_create_amenity(self):
        name = "new amenity"
        description = "new amenity desc"
        res = self.client.post(
            self.URL, data={"name": name, "description": description}
        )
        data = res.json()
        self.assertEqual(res.status_code, 200, "Not status 200")
        self.assertEqual(data["name"], name)
        self.assertEqual(data["description"], description)

        res = self.client.post(self.URL)
        self.assertEqual(res.status_code, 400)


class TestAmenity(APITestCase):
    URL = "/api/v1/rooms/amenities"
    NAME = "Amenity Test"
    DESC = "Amenity DESC"

    def setUp(self) -> None:
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_get_amenity(self):
        res = self.client.get(f"{self.URL}/2")
        self.assertEqual(res.status_code, 404)

        res = res.client.get(f"{self.URL}/1")
        self.assertEqual(res.status_code, 200)

    def test_put_amenity(self):
        modiry_name = "modify name"
        res = self.client.put(f"{self.URL}/1", data={"name": modiry_name})
        self.assertEqual(res.status_code, 200)

        res = res.client.get(f"{self.URL}/1")
        self.assertEqual(res.json()["name"], modiry_name)


class TestRoom(APITestCase):

    def setUp(self):
        user = User.objects.create(
            username="test",
        )
        user.set_password("1234")
        user.save()
        self.user = user

    def login(self):
        self.client.force_login(self.user)

    def test_create_room(self):
        res = self.client.post("/api/v1/rooms/")
        self.assertEqual(res.status_code, 403)

        self.login()
        res = self.client.post("/api/v1/rooms/")
        print(res.json())
        self.assertEqual(res.status_code, 200)
