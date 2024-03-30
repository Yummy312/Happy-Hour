from httpx import AsyncClient
import pytest


async def test_get_all_companies(async_client: AsyncClient):
    response = await async_client.get('/companies')

    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json'
    assert isinstance(response.json(), list)


@pytest.mark.parametrize('company_id, status_code', [
    (1, 200),
    (True, 422),
    (1000, 404),
    (-4, 404)
])
async def test_get_company(company_id: int, status_code: int, async_client: AsyncClient):
    response = await async_client.get('/companies/{}'.format(company_id))
    assert response.status_code == status_code


@pytest.mark.parametrize('name, description, location, hours_of_operation, status_code', [
    (
            'Navi',
            'The Dota 2 division of the Ukrainian multi-gaming esports organization Natus Vincere',
            'Ukraine',
            'from 9 to 17:00',
            200
    ),
    (       # ожидается статус код 409 потому, что, клиент пытается создать снова один и тот же продукт
            'Navi',
            'The  multi-gaming esports organization ',
            'Russia',
            'from 9 to 20:00',
            409
    ),
    (
            True,
            'The  multi-gaming esports organization ',
            'Russia',
            'from 9 to 20:00',
            422
    )
])
async def test_create_company(name, description,
                              location, hours_of_operation,
                              status_code, async_client: AsyncClient):
    response = await async_client.post('/companies', json={
        'name': name,
        'description': description,
        'location': location,
        'hours_of_operation': hours_of_operation

    })
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "company_id, update_data, expected_status_code, expected_response",
    [
        (
                1,
                {
                    "name": "PepsiCo",
                    "description": "Pepsi is a carbonated soft drink modified by PepsiCo, created in 1893",
                    "location": "Virginia\n",
                    "hours_of_operation": "Unlimited"
                },
                200,
                {
                    "name": "PepsiCo",
                    "description": "Pepsi is a carbonated soft drink modified by PepsiCo, created in 1893",
                    "location": "Virginia\n",
                    "hours_of_operation": "Unlimited"
                }
        )

    ]
)
async def test_update_company(company_id, update_data, expected_status_code, expected_response,
                              async_client: AsyncClient):
    response = await async_client.put(f'/companies/{company_id}', json=update_data)

    assert response.status_code == expected_status_code
    assert response.json() == expected_response


@pytest.mark.parametrize('company_id, status_code', [
    (4, 200),
    (777, 404),
    ({}, 422)
])
async def test_delete_company(company_id: int, status_code: int, async_client: AsyncClient):
    response = await async_client.delete('/companies/{}'.format(company_id))
    assert response.status_code == status_code
