"""
conftest.py - центральне місце для налаштувань Pytest
Тут ми створюємо ФІКСТУРИ (fixtures) - підготовку даних для тестів
"""

import pytest
from src.coffee_machine import CoffeeMachine


# ==========================================
# 1. БАЗОВІ ФІКСТУРИ
# ==========================================

@pytest.fixture
def coffee_machine():
    """
    Базова фікстура: створює кавомашину з початковими налаштуваннями
    Використовується в багатьох тестах
    """
    machine = CoffeeMachine()
    machine.turn_on()
    return machine


@pytest.fixture
def empty_coffee_machine():
    """
    Фікстура: кавомашина з мінімальними ресурсами
    Для тестів на перевірку недостатності ресурсів
    """
    machine = CoffeeMachine(water_level=10, coffee_beans=5, milk=5)
    machine.turn_on()
    return machine


@pytest.fixture
def full_coffee_machine():
    """
    Фікстура: кавомашина з великим запасом ресурсів
    Для тестів на багаторазове приготування
    """
    machine = CoffeeMachine(water_level=5000, coffee_beans=2500, milk=1500)
    machine.turn_on()
    return machine


# ==========================================
# 2. ФІКСТУРИ З ПАРАМЕТРАМИ
# ==========================================

@pytest.fixture(params=["espresso", "americano", "latte", "cappuccino"])
def coffee_type(request):
    """
    Фікстура з параметрами: повертає кожен тип кави по черзі
    """
    return request.param


# ==========================================
# 3. ФІКСТУРА З TEARDOWN
# ==========================================

@pytest.fixture
def coffee_machine_with_teardown():
    """
    Фікстура з teardown: робить щось ПІСЛЯ тесту
    """
    print("\n Setting up coffee machine...")
    machine = CoffeeMachine()
    machine.turn_on()

    # Виконуємо тест
    yield machine  # Ось тут відбувається тест

    # Після тесту - очищення
    print("\n Cleaning up: turning off coffee machine...")
    machine.turn_off()


# ==========================================
# 4. ФІКСТУРА ЯКА ВИКОРИСТОВУЄ ІНШІ ФІКСТУРИ
# ==========================================

@pytest.fixture
def prepared_machine(coffee_machine):
    """
    Фікстура, яка використовує іншу фікстуру (coffee_machine)
    і додатково готує кавомашину
    """
    # coffee_machine вже увімкнена та має початкові ресурси
    coffee_machine.add_water(200)
    coffee_machine.add_coffee_beans(100)
    coffee_machine.add_milk(100)
    return coffee_machine


# ==========================================
# 5. РЕЄСТРАЦІЯ КАСТОМНИХ МАРКЕРІВ
# ==========================================

def pytest_configure(config):
    """
    Реєструємо кастомні маркери для Pytest
    """
    config.addinivalue_line("markers", "smoke: тест для швидкої перевірки базової функціональності")
    config.addinivalue_line("markers", "regression: тест для перевірки регресій")
    config.addinivalue_line("markers", "slow: повільний тест, який можна пропустити")
    config.addinivalue_line("markers", "ui: тест для перевірки UI (якщо буде)")