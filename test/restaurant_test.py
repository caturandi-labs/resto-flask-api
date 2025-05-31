def test_get_empty_restaurant(client):
    """
    When No Restaurant exists, return an empty list
    """
    response = client.get('/api/v1/restaurants?page=1&per_page=10')
    assert response.status_code == 200
    assert response.json == []

def test_get_paginate_restaurant(client):
    """
    When No Restaurant exists, return an empty list
    """
    response = client.get('/api/v1/restaurants?page=1&per_page=10')
    assert response.status_code == 200
    assert response.json != []



