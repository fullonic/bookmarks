import pytest
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_get_all_bookmarks(api_client):
    req = api_client.get(reverse("bookmarks-list"))
    assert req.status_code == 200


@pytest.mark.django_db
def test_add_bookmarks(api_client_authenticate, test_data_dict):
    book = test_data_dict[0]
    req = api_client_authenticate.post(reverse("bookmarks-list"), data=book)
    assert req.status_code == 201


@pytest.mark.django_db
def test_add_multiple_bookmarks(api_client_authenticate, test_data_dict):
    req = api_client_authenticate.post(
        reverse("bookmarks-list"), data={"data": test_data_dict}
    )
    assert req.status_code == 201
