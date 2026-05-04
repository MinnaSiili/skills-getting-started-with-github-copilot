import pytest

from src import app as app_module


def test_signup_registers_new_participant(client):
    # Arrange
    activity_name = "Basketball Team"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity_name]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_registration(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


@pytest.mark.xfail(reason="Max participant limit is not enforced yet", strict=True)
def test_signup_rejects_when_activity_is_at_max_capacity(client):
    # Arrange
    activity_name = "Tennis Club"
    activity = app_module.activities[activity_name]
    activity["participants"] = [f"student{i}@mergington.edu" for i in range(activity["max_participants"])]

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": "overflow.student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
