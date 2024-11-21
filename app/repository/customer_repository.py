from app.model.customer import Customer

from .base import CrudFactory


class CustomerRepository(CrudFactory(Customer)): ...
