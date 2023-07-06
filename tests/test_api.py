from link_shortening_service.core.settings import settings


async def test_create_short_url__get(application, client, link):
    response = await client.post(
        url=application.url_path_for("create_short_url"),
        json={"url": "test_url"},
    )
    assert response.status_code == 200
    assert response.json() == {"url": settings.BASE_URL + "test_token"}


async def test_create_short_url__create(application, client):
    response = await client.post(
        url=application.url_path_for("create_short_url"),
        json={"url": "test_url"},
    )
    assert response.status_code == 200
    assert response.json()["url"].find(settings.BASE_URL) != -1


async def test_get_full_url(application, client, link):
    response = await client.post(
        url=application.url_path_for("get_full_url"),
        json={"url": settings.BASE_URL + "test_token"},
    )
    assert response.status_code == 200
    assert response.json() == {"url": "test_url"}


async def test_get_full_url__not_found(application, client):
    response = await client.post(
        url=application.url_path_for("get_full_url"),
        json={"url": settings.BASE_URL + "test_token"},
    )
    assert response.status_code == 404


async def test_get_full_url__invalid_url(application, client):
    response = await client.post(
        url=application.url_path_for("get_full_url"),
        json={"url": "test_token"},
    )
    assert response.status_code == 400


async def test_delete_url(application, client, link):
    response = await client.request(
        method='delete',
        url=application.url_path_for("delete_url"),
        json={"url": settings.BASE_URL + "test_token"},
    )
    assert response.status_code == 200


async def test_delete_url__not_found(application, client):
    response = await client.request(
        method='delete',
        url=application.url_path_for("delete_url"),
        json={"url": settings.BASE_URL + "test_token"},
    )
    assert response.status_code == 404


async def test_delete_url__invalid_url(application, client):
    response = await client.request(
        method='delete',
        url=application.url_path_for("delete_url"),
        json={"url": "test_token"},
    )
    assert response.status_code == 400
