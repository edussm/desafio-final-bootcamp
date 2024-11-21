import pytest
from faker import Faker

from app.repository.customer_repository import CustomerRepository
from app.schema.customer import CustomerCreate, CustomerUpdate

customer_repository = CustomerRepository()
fake = Faker("pt_BR")


@pytest.mark.asyncio
class TestOderRepository:
    @pytest.fixture
    def customer_payload(self):
        def _get_payload():
            return {
                "name": fake.name(),
                "email": fake.email(),
                "document": fake.cpf(),
                "phone_number": fake.phone_number(),
                "type": "individual",
            }

        return _get_payload

    @pytest.fixture
    def get_test_customers(self, session, customer_payload):
        async def _create(count: int = 2):
            customers_create = [
                CustomerCreate(**customer_payload()) for _ in range(count)
            ]
            customers = await customer_repository.create_many(
                session, customers_create, return_models=True
            )
            customers = sorted(customers, key=lambda x: x.id)
            return customers

        return _create

    async def test_create(self, session, customer_payload):
        customer_create = CustomerCreate(**customer_payload())
        customer = await customer_repository.create(session, customer_create)
        assert customer.id is not None
        assert customer.created_at is not None
        assert customer.updated_at is not None
        assert customer.is_active == customer_create.is_active

    async def test_create_many(self, session, customer_payload):
        customers_create = [
            CustomerCreate(**customer_payload()),
            CustomerCreate(**customer_payload()),
        ]

        customers = await customer_repository.create_many(
            session, customers_create, return_models=True
        )
        customers = sorted(customers, key=lambda x: x.id)

        for i in range(0, 1):
            assert customers[i].id is not None
            assert customers[i].created_at is not None
            assert customers[i].updated_at is not None
            assert customers[i].is_active == customers_create[i].is_active

    async def test_get_many(self, session, get_test_customers):
        customers = await get_test_customers(count=5)

        all_customers = await customer_repository.get_many(session)
        assert len(all_customers) == len(customers)

    async def test_get_many_with_pages(self, session, get_test_customers):
        await get_test_customers(count=5)
        page_limit = 2

        all_customers = await customer_repository.get_many(session, limit=page_limit)
        assert len(all_customers) == page_limit

    async def test_get_one_by_id(self, session, get_test_customers):
        customers = await get_test_customers()

        customer = await customer_repository.get_one_by_id(session, customers[0].id)

        assert customer.id == customers[0].id
        assert customer.name == customers[0].name
        assert customer.is_active == customers[0].is_active

    async def test_update_by_id(self, session, get_test_customers):
        customers = await get_test_customers()
        customer_update = CustomerUpdate(name="new name")

        customer = await customer_repository.update_by_id(
            session, customer_update, customers[0].id
        )

        assert customer.name == customer_update.name

    async def test_remove_by_id(self, session, get_test_customers):
        customers = await get_test_customers(count=3)

        row_count = await customer_repository.remove_by_id(session, customers[0].id)

        assert row_count == 1

        all_customers = await customer_repository.get_many(session)
        assert len(all_customers) == 2

        row_count = await customer_repository.remove_by_id(session, customers[0].id)
        assert row_count == 0
