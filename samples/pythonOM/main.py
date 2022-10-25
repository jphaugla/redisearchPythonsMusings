from Customer import Customer
from pydantic import ValidationError
from redis_om import Migrator
import datetime

try:
    andrew = Customer(
        first_name="Andrew",
        last_name="Brookins",
        email="andrew.brookins@example.com",
        join_date=datetime.date.today(),
        # join_date="2020-01-02",
        age=38,
        bio="Python developer, works at Redis, Inc."
    )

except ValidationError as e:
    print(e)
    """
    pydantic.error_wrappers.ValidationError: 1 validation error for Customer
    join_date
      invalid date format (type=value_error.date)
    """

print(andrew.bio)
print(andrew.pk)
print(andrew.join_date)
print(type(andrew.join_date))
andrew.save()
print(andrew.key())
# Before running queries, we need to run migrations to set up the
# indexes that Redis OM will use. You can also use the `migrate`
# CLI tool for this!
Migrator().run()

# Find all customers with the last name "Brookins"
print(Customer.find(Customer.last_name == "Brookins").all())

# Find all customers that do NOT have the last name "Brookins"
print(Customer.find(Customer.last_name != "Brookins").all())

# Find all customers whose last name is "Brookins" OR whose age is
# 100 AND whose last name is "Smith"
print(Customer.find((Customer.last_name == "Brookins") | (
        Customer.age == 100
) & (Customer.last_name == "Smith")).all())

# run commands directly
redis_conn = Customer.db()
redis_conn.sadd("myset", "a", "b", "c", "d")
print(redis_conn.sismember("myset", "b"))