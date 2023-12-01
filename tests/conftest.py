import flask_migrate
import pytest

from create_app import create_app


@pytest.fixture
def client():
    app = create_app(for_testing=True)

    with app.test_client() as client:
        app.config["TESTING"] = True
        with app.app_context():
            flask_migrate.upgrade()

        yield client

        with app.app_context():
            flask_migrate.downgrade(revision="base")


@pytest.fixture
def admin_access_token(client):
    admin_user_json = {
        "full_name": "John Doe",
        "email_id": "admin@gmail.com",
        "password": "Test@123",
        "role": "ADMIN",
    }

    response = client.post("/users", json=admin_user_json)
    assert response.status_code == 201, "Couldn't Signup for admin user"

    admin_user_login_json = {
        "email_id": "admin@gmail.com",
        "password": "Test@123",
    }
    response = client.post("/users/sign-in", json=admin_user_login_json)
    assert response.status_code == 200, "Couldn't login with admin user"

    return response.json["access_token"]


@pytest.fixture
def user_access_token(client):
    admin_user_json = {
        "full_name": "John Doe user",
        "email_id": "user@gmail.com",
        "password": "Test@123",
        "role": "USER",
    }

    response = client.post("/users", json=admin_user_json)
    assert response.status_code == 201, "Couldn't Signup for admin user"

    admin_user_login_json = {
        "email_id": "user@gmail.com",
        "password": "Test@123",
    }
    response = client.post("/users/sign-in", json=admin_user_login_json)
    assert response.status_code == 200, "Couldn't login with admin user"

    return response.json["access_token"]
