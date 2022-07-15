store = {
    "name": "Store Test",
    "address": "Address 1",
    "city": "Cidade Teste",
    "state": "SP",
    "is_active": True,
}

superuser = {
    "username": "admin",
    "first_name": "Super",
    "last_name": "User",
    "password": "1234",
}

manager = {
    "username": "manager",
    "first_name": "Manager",
    "last_name": "Teste",
    "password": "1234",
    "is_manager": True,
    "is_doctor": True,
    "is_staff": False,
}

doctor = {
    "username": "doctor",
    "first_name": "Doctor",
    "last_name": "Teste",
    "password": "1234",
    "is_manager": False,
    "is_doctor": True,
    "is_staff": False,
}

staff = {
    "username": "staff",
    "first_name": "Staff",
    "last_name": "Teste",
    "password": "1234",
    "is_manager": False,
    "is_doctor": False,
    "is_staff": True,
}
