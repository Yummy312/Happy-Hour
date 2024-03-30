import pytest
from httpx import AsyncClient


async def test_get_products(async_client: AsyncClient):
    response = await async_client.get('/products')
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json'
    assert isinstance(response.json(), list)


@pytest.mark.parametrize('product_id, status_code', [
    (1, 200),
    ([], 422),
    (100, 404),
    (999, 404)
])
async def test_get_product(product_id: int, status_code: int, async_client: AsyncClient):
    response = await async_client.get('/products/{}'.format(product_id))

    assert response.status_code == status_code


@pytest.mark.parametrize('name, company_id, description, price, quantity, status_code', [
    (
            'Coca-Cola zero',
            2,
            'carbonated soft drink produced by the Coca-Cola Company',
            55,
            500,
            200
    ),
    (
            'Coca-Cola Lime',
            122,
            'carbonated soft drink produced by the Coca-Cola Company',
            55,
            500,
            404
    ),
    (
            'Coca-Cola zero',
            2,
            {},
            55,
            500,
            422
    )
])
async def test_create_product(name, company_id, description,
                              price, quantity, status_code,
                              async_client: AsyncClient):
    response = await async_client.post('/products', json={
        'name': name,
        'company_id': company_id,
        'description': description,
        'price': price,
        'quantity': quantity

    })
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "product_id, update_data, expected_status_code, expected_response", [
        (
                2,
                {
                    "name": "Sprite",
                    "description": "Sprite is a carbonated soft drink",
                    "price": 30,
                    "quantity": 1000
                },
                200,
                {
                    "name": "Sprite",
                    "description": "Sprite is a carbonated soft drink",
                    "price": 30,
                    "quantity": 1000
                }
        )

    ],

)
async def test_update_product(product_id, update_data, expected_status_code, expected_response,
                              async_client: AsyncClient):
    response = await async_client.put(f'/products/{product_id}', json=update_data)

    assert response.status_code == expected_status_code
    assert response.json() == expected_response


@pytest.mark.parametrize('product_id, status_code', [
    (4, 200),
    (227, 404),
    (True, 422)
])
async def test_delete_product(product_id: int, status_code: int, async_client: AsyncClient):
    response = await async_client.delete('/products/{}'.format(product_id))
    assert response.status_code == status_code
