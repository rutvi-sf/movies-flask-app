def test_create_movies_with_admin_user(client, admin_access_token):
    """
    Test to create Movies with Admin User
    """
    response = client.post(
        "/movies",
        headers={"Authorization": f"Bearer {admin_access_token}"},
        json=[
            {
                "99popularity": 83.0,
                "director": "Victor Fleming",
                "imdb_score": 8.3,
                "name": "The Wizard of Oz",
            }
        ],
    )
    assert response.status_code == 201, "Couldn't Create Movies with admin user"


def test_create_movies_with_authenticated_user(client, user_access_token):
    """
    Test to create Movies with Normal User
    """
    response = client.post(
        "/movies",
        headers={"Authorization": f"Bearer {user_access_token}"},
        json=[
            {
                "99popularity": 83.0,
                "director": "Victor Fleming",
                "imdb_score": 8.3,
                "name": "The Wizard of Oz",
            }
        ],
    )
    assert response.status_code == 403, "Was able to create Movie as a Normal user"


def test_get_movies_with_admin_user(client, admin_access_token):
    """
    Test to get Movies with Admin User
    """
    response = client.get(
        "/movies",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )

    assert response.status_code == 200, "Admin was not able to fetch Movies"


def test_get_movies_with_authenticated_user(client, user_access_token):
    """
    Test to get Movies with Normal User
    """
    response = client.get(
        "/movies",
        headers={"Authorization": f"Bearer {user_access_token}"},
    )

    assert response.status_code == 200, "User was not able to fetch Movies"


def test_get_movies_with_anonymous_user(client):
    """
    Test to get Movies with Anonymous User
    """
    response = client.get(
        "/movies",
    )

    assert response.status_code == 200, "Anonymous User was not able to fetch Movies"
