service_1 = {"name": "serviço 1", "category": "cateogira 1", "price": 10.99}

service_2 = {"name": "serviço 2", "category": "cateogira 1", "price": 20.56}


admin = {
    "username": "admin",
    "first_name": "Admin",
    "last_name": "Teste",
    "password": "1234",
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

manager = {
    "username": "manager",
    "first_name": "Manager",
    "last_name": "Teste",
    "password": "1234",
    "is_manager": True,
    "is_doctor": False,
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
