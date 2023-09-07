import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_subscription(subscription, test_client_data):
    client = APIClient()
    request = client.get("/api/subscriptions/", format="json")
    total_amount = request.data["total_amount"]
    client_name = request.data["resoult"][0]["client_name"]

    assert request.status_code == 200
    assert total_amount == 0.9
    assert client_name == test_client_data["company_name"]
