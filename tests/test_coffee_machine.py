"""
Тести для кавомашини
Використовуємо Pytest для перевірки всіх сценаріїв
"""

import pytest
from src.coffee_machine import CoffeeMachine


# ==========================================
# 1. ТЕСТИ ІНІЦІАЛІЗАЦІЇ
# ==========================================

def test_coffee_machine_initialization():
    """Тест: перевірка початкових параметрів"""
    machine = CoffeeMachine()


    assert machine.water_level == 1000
    assert machine.coffee_beans == 500
    assert machine.milk == 300
    assert machine.is_on is False
    assert machine.coffee_made == 0


def test_coffee_machine_custom_initialization():
    """Тест: перевірка кастомних параметрів"""
    machine = CoffeeMachine(water_level=500, coffee_beans=200, milk=100)

    assert machine.water_level == 500
    assert machine.coffee_beans == 200
    assert machine.milk == 100


# ==========================================
# 2. ТЕСТИ ВМИКАННЯ/ВИМИКАННЯ
# ==========================================

def test_turn_on():
    """Тест: увімкнення кавомашини"""
    machine = CoffeeMachine()

    result = machine.turn_on()
    assert result == "Coffee machine is ON"
    assert machine.is_on is True

    # Повторне увімкнення
    result = machine.turn_on()
    assert result == "Coffee machine is already ON"


def test_turn_off():
    """Тест: вимкнення кавомашини"""
    machine = CoffeeMachine()
    machine.turn_on()  # Спочатку вмикаємо

    result = machine.turn_off()
    assert result == "Coffee machine is OFF"
    assert machine.is_on is False

    # Повторне вимкнення
    result = machine.turn_off()
    assert result == "Coffee machine is already OFF"


# ==========================================
# 3. ТЕСТИ ПРИГОТУВАННЯ КАВИ
# ==========================================

def test_make_espresso():
    """Тест: приготування еспресо"""
    machine = CoffeeMachine()
    machine.turn_on()

    result = machine.make_coffee("espresso")

    assert result == "☕ Espresso is ready! Coffee #1"
    assert machine.water_level == 950  # 1000 - 50
    assert machine.coffee_beans == 490  # 500 - 10
    assert machine.milk == 300  # Не змінюється
    assert machine.coffee_made == 1


def test_make_americano():
    """Тест: приготування американо"""
    machine = CoffeeMachine()
    machine.turn_on()

    result = machine.make_coffee("americano")

    assert result == "☕ Americano is ready! Coffee #1"
    assert machine.water_level == 900  # 1000 - 100
    assert machine.coffee_beans == 490  # 500 - 10
    assert machine.coffee_made == 1


def test_make_latte():
    """Тест: приготування лате"""
    machine = CoffeeMachine()
    machine.turn_on()

    result = machine.make_coffee("latte")

    assert result == "☕ Latte is ready! Coffee #1"
    assert machine.water_level == 950  # 1000 - 50
    assert machine.coffee_beans == 490  # 500 - 10
    assert machine.milk == 200  # 300 - 100
    assert machine.coffee_made == 1


def test_make_cappuccino():
    """Тест: приготування капучіно"""
    machine = CoffeeMachine()
    machine.turn_on()

    result = machine.make_coffee("cappuccino")

    assert result == "☕ Cappuccino is ready! Coffee #1"
    assert machine.water_level == 950  # 1000 - 50
    assert machine.coffee_beans == 490  # 500 - 10
    assert machine.milk == 220  # 300 - 80
    assert machine.coffee_made == 1


# ==========================================
# 4. ТЕСТИ ПОМИЛОК ТА КРАЙОВИХ ВИПАДКІВ
# ==========================================

def test_make_coffee_when_off():
    """Тест: спроба приготувати каву при вимкненій машині"""
    machine = CoffeeMachine()
    # Машина вимкнена за замовчуванням

    with pytest.raises(ValueError) as exc_info:
        machine.make_coffee("espresso")

    assert "Coffee machine is OFF" in str(exc_info.value)


def test_make_coffee_unknown_type():
    """Тест: спроба приготувати невідомий тип кави"""
    machine = CoffeeMachine()
    machine.turn_on()

    with pytest.raises(ValueError) as exc_info:
        machine.make_coffee("mocha")  # Невідомий тип

    assert "Unknown coffee type: mocha" in str(exc_info.value)


def test_make_coffee_not_enough_water():
    """Тест: недостатньо води для кави"""
    machine = CoffeeMachine(water_level=30)  # Мало води
    machine.turn_on()

    with pytest.raises(ValueError) as exc_info:
        machine.make_coffee("espresso")

    assert "Not enough water" in str(exc_info.value)


def test_make_coffee_not_enough_beans():
    """Тест: недостатньо зерен для кави"""
    machine = CoffeeMachine(coffee_beans=5)  # Мало зерен
    machine.turn_on()

    with pytest.raises(ValueError) as exc_info:
        machine.make_coffee("espresso")

    assert "Not enough coffee beans" in str(exc_info.value)


def test_make_coffee_not_enough_milk():
    """Тест: недостатньо молока для кави"""
    machine = CoffeeMachine(milk=20)  # Мало молока
    machine.turn_on()

    with pytest.raises(ValueError) as exc_info:
        machine.make_coffee("latte")

    assert "Not enough milk" in str(exc_info.value)


# ==========================================
# 5. ТЕСТИ ДОДАВАННЯ РЕСУРСІВ
# ==========================================

def test_add_water():
    """Тест: додавання води"""
    machine = CoffeeMachine()
    initial_water = machine.water_level

    result = machine.add_water(100)

    assert result == f"Added 100ml of water. Current level: {initial_water + 100}ml"
    assert machine.water_level == initial_water + 100


def test_add_coffee_beans():
    """Тест: додавання зерен"""
    machine = CoffeeMachine()
    initial_beans = machine.coffee_beans

    result = machine.add_coffee_beans(50)

    assert result == f"Added 50g of coffee beans. Current level: {initial_beans + 50}g"
    assert machine.coffee_beans == initial_beans + 50


def test_add_milk():
    """Тест: додавання молока"""
    machine = CoffeeMachine()
    initial_milk = machine.milk

    result = machine.add_milk(50)

    assert result == f"Added 50ml of milk. Current level: {initial_milk + 50}ml"
    assert machine.milk == initial_milk + 50


# ==========================================
# 6. ТЕСТИ СТАТУСУ
# ==========================================

def test_get_status():
    """Тест: отримання статусу"""
    machine = CoffeeMachine(water_level=500, coffee_beans=200, milk=100)
    machine.turn_on()
    machine.make_coffee("espresso")

    status = machine.get_status()

    assert status["is_on"] is True
    assert status["water_level"] == 450  # 500 - 50
    assert status["coffee_beans"] == 190  # 200 - 10
    assert status["milk"] == 100
    assert status["coffee_made"] == 1


# ==========================================
# 7. ТЕСТИ З ВИКОРИСТАННЯМ ФІКСТУР (ЗАРАЗ ПОЯСНИМО)
# ==========================================

def test_multiple_coffees():
    """Тест: приготування декількох кав"""
    machine = CoffeeMachine()
    machine.turn_on()

    # Приготування декількох кав
    machine.make_coffee("espresso")
    machine.make_coffee("latte")
    machine.make_coffee("americano")

    # Перевірка ресурсів
    assert machine.water_level == 1000 - 50 - 50 - 100  # 800
    assert machine.coffee_beans == 500 - 10 - 10 - 10  # 470
    assert machine.milk == 300 - 100  # 200
    assert machine.coffee_made == 3


# ==========================================
# 8. ПАРАМЕТРИЗОВАНІ ТЕСТИ (ВАЖЛИВА ФІЧА!)
# ==========================================

@pytest.mark.parametrize("coffee_type, water_used, beans_used, milk_used", [
    ("espresso", 50, 10, 0),
    ("americano", 100, 10, 0),
    ("latte", 50, 10, 100),
    ("cappuccino", 50, 10, 80),
])
def test_all_coffee_types_resources(coffee_type, water_used, beans_used, milk_used):
    """
    Параметризований тест: перевірка всіх типів кави
    Один тест - багато наборів даних!
    """
    machine = CoffeeMachine()
    machine.turn_on()

    # Початкові значення
    initial_water = machine.water_level
    initial_beans = machine.coffee_beans
    initial_milk = machine.milk

    # Приготування
    machine.make_coffee(coffee_type)

    # Перевірка витрачених ресурсів
    assert machine.water_level == initial_water - water_used
    assert machine.coffee_beans == initial_beans - beans_used
    assert machine.milk == initial_milk - milk_used


@pytest.mark.parametrize("water, beans, milk, should_pass", [
    (100, 50, 100, True),  # Достатньо всього
    (30, 50, 100, False),  # Не вистачає води
    (100, 5, 100, False),  # Не вистачає зерен
    (100, 50, 20, False),  # Не вистачає молока
    (30, 5, 20, False),  # Не вистачає всього
])
def test_check_resources_parametrized(water, beans, milk, should_pass):
    """Параметризований тест для перевірки ресурсів"""
    machine = CoffeeMachine(water_level=water, coffee_beans=beans, milk=milk)

    can_make, message = machine.check_resources(water_needed=50, beans_needed=10, milk_needed=50)

    assert can_make is should_pass
    if not should_pass:
        assert "Not enough" in message


# ==========================================
# 9. ВИКОРИСТАННЯ МАРКЕРІВ
# ==========================================

@pytest.mark.smoke
def test_smoke_basic_flow():
    """Smoke тест: базовий сценарій роботи кавомашини"""
    machine = CoffeeMachine()
    machine.turn_on()

    result = machine.make_coffee("espresso")
    assert "ready" in result.lower()
    assert machine.coffee_made == 1


@pytest.mark.regression
@pytest.mark.parametrize("coffee_type", ["espresso", "americano", "latte", "cappuccino"])
def test_regression_all_coffee_types(coffee_type):
    """Regression тест: всі типи кави мають працювати"""
    machine = CoffeeMachine()
    machine.turn_on()

    try:
        result = machine.make_coffee(coffee_type)
        assert "ready" in result.lower()
    except ValueError as e:
        # Якщо не вистачає ресурсів - це окремий тест
        assert "Not enough" in str(e)


@pytest.mark.slow
def test_slow_make_100_coffees():
    """Позначаємо тест як 'slow' для пропуску при швидкому запуску"""
    machine = CoffeeMachine(water_level=10000, coffee_beans=5000, milk=3000)
    machine.turn_on()

    for i in range(100):
        machine.make_coffee("espresso")

    assert machine.coffee_made == 100