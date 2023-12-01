def test_user_signup(client):
    """
    Test user signup
    """
    user_data = {
        "full_name": "John Doe",
        "email_id": "john@example.com",
        "password": "password123",
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201, "User signup failed"


def test_user_login(client):
    """
    Test user login
    """
    user_data = {
        "email_id": "john@example.com",
        "password": "password123",
    }
    response = client.post("/users/sign-in", json=user_data)
    assert response.status_code == 200, "User login failed"


def test_user_login_wrong_password(client):
    """
    Test user login with wrong password
    """
    user_data = {
        "email_id": "john@example.com",
        "password": "wrongpassword",
    }
    response = client.post("/users/sign-in", json=user_data)
    assert response.status_code == 401, "User login with wrong password should fail"


def test_user_signup_duplicate_email(client):
    """
    Test user signup with duplicate email
    """
    user_data = {
        "full_name": "John Doe",
        "email_id": "john@example.com",  # Use the same email as in the previous test
        "password": "password456",
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 400, "User signup with duplicate email should fail"


def test_user_signup_missing_fields(client):
    """
    Test user signup with missing fields
    """
    user_data = {
        "full_name": "Alice",
        "password": "alicepassword",
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 400, "User signup with missing fields should fail"
