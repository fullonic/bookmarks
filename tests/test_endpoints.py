from markers.models import Bookmark
import pytest
from rest_framework.reverse import reverse
from rest_framework import status
from django.utils import timezone


@pytest.mark.django_db
def test_get_all_bookmarks(api_client):
    req = api_client.get(reverse("bookmark-list"))
    assert req.status_code == 200


@pytest.mark.django_db
def test_add_bookmarks(api_client_authenticate, test_data_dict):
    book = test_data_dict[0]
    req = api_client_authenticate.post(reverse("bookmark-list"), data=book)
    assert req.status_code == 201


@pytest.mark.django_db
@pytest.mark.skip
def test_add_multiple_bookmarks(api_client_authenticate, test_data_dict):
    req = api_client_authenticate.post(
        reverse("bookmark-list"), data={"data": test_data_dict}
    )
    assert req.status_code == 201


@pytest.mark.django_db
def test_last_time_visited(api_client_authenticate, bookmarks):
    now = timezone.now()
    req = api_client_authenticate.patch(
        reverse("bookmark-update", args=(2,)),
        data={"last_time_visited": now},
    )
    assert req.status_code == 200


@pytest.mark.django_db
def test_delete_bookmark(api_client_authenticate, bookmarks):
    delete_entry_pk = 2
    
    req = api_client_authenticate.delete(
        reverse("bookmark-update", args=(delete_entry_pk,)),
    )
    
    assert req.status_code == 204
    assert not Bookmark.objects.filter(pk=delete_entry_pk).exists()


@pytest.mark.django_db
def test_single_search_query(api_client, bookmarks):
    resp = api_client.get(reverse("bookmark-list", args=("python",)))
    response = resp.json()
    assert any(
        (
            "python" in response[0]["title"].lower(),
            "python" in response[0]["url"].lower(),
        )
    )


@pytest.mark.django_db
def test_multiple_search_query(api_client, bookmarks):
    resp = api_client.get(reverse("bookmark-list", args=("python postgresql",)))
    response = resp.json()
    assert any(
        (
            "python" in response[0]["title"].lower(),
            "python" in response[0]["url"].lower(),
        )
    )
    assert any(
        (
            "postgresql" in response[1]["title"].lower(),
            "postgresql" in response[1]["url"].lower(),
        )
    )
