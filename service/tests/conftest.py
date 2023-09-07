import pytest
from clients.models import Client
from services.models import Plan
from services.models import Service
from services.models import Subscription


@pytest.fixture()
def test_user_data():
    return {"username": "username", "email": "test1@test.com", "password": "test1"}


@pytest.fixture()
def test_service_data():
    return {"name": "test_service", "full_price": 1}


@pytest.fixture()
def test_plan_data():
    return {"plan_type": "student", "discount_percent": 10}


@pytest.fixture()
def test_subscription_data():
    return {"price2": "5", "comment": "some comment", "field_a": "field_asfve", "field_b": "field_b1234"}


@pytest.fixture()
def test_client_data():
    return {"company_name": "test_company_name", "full_address": "test_full_address"}


@pytest.fixture
def service(test_service_data):
    service = Service.objects.create(
        name=test_service_data["name"],
        full_price=test_service_data["full_price"],
    )
    return service


@pytest.fixture
def plan(test_plan_data):
    plan = Plan.objects.create(
        plan_type=test_plan_data["plan_type"],
        discount_percent=test_plan_data["discount_percent"],
    )
    return plan


@pytest.fixture
def create_user(db, django_user_model):
    def make_user(**kwargs):
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def user(create_user, test_user_data):
    user = create_user(
        username=test_user_data["username"],
        email=test_user_data["email"],
        password=test_user_data["password"],
    )
    return user


@pytest.fixture
def client(create_user, user, test_client_data, test_user_data):
    client = Client.objects.create(
        user=user,
        company_name=test_client_data["company_name"],
        full_address=test_client_data["full_address"],
    )
    return client


@pytest.fixture
def subscription(client, user, service, plan, test_client_data, test_subscription_data):
    subscription = Subscription.objects.create(
        client=client,
        service=service,
        plan=plan,
        price2=test_subscription_data["price2"],
        comment=test_subscription_data["comment"],
        field_a=test_subscription_data["field_a"],
        field_b=test_subscription_data["field_b"],
    )
    return subscription
