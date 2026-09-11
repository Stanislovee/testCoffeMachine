class CoffeeMachine:
    def __init__(self, water_level=1000, coffee_beans=500, milk=300):
        self.water_level = water_level
        self.coffee_beans = coffee_beans
        self.milk = milk
        self.coffee_made = 0
        self.is_on = False

    def turn_on(self):
        if not self.is_on:
            self.is_on = True
            return "Coffee machine is ON"
        return "Coffee machine is already ON"

    def turn_off(self):
        if self.is_on:
            self.is_on = False
            return "Coffee machine is OFF"
        return "Coffee machine is already OFF"

    def check_resources(self, water_needed=50, beans_needed=10, milk_needed=0):
        if self.water_level < water_needed:
            return False, f"Not enough water. Available: {self.water_level}ml, Need: {water_needed}ml"
        if self.coffee_beans < beans_needed:
            return False, f"Not enough coffee beans. Available: {self.coffee_beans}g, Need: {beans_needed}g"
        if self.milk < milk_needed:
            return False, f"Not enough milk. Available: {self.milk}ml, Need: {milk_needed}ml"
        return True, "Resources OK"

    def make_coffee(self, coffee_type="espresso"):
        if not self.is_on:
            raise ValueError("Coffee machine is OFF. Please turn it ON first.")

        recipes = {
            "espresso": {"water": 50, "beans": 10, "milk": 0},
            "americano": {"water": 100, "beans": 10, "milk": 0},
            "latte": {"water": 50, "beans": 10, "milk": 100},
            "cappuccino": {"water": 50, "beans": 10, "milk": 80}
        }

        if coffee_type not in recipes:
            raise ValueError(f"Unknown coffee type: {coffee_type}")

        recipe = recipes[coffee_type]

        can_make, message = self.check_resources(
            water_needed=recipe["water"],
            beans_needed=recipe["beans"],
            milk_needed=recipe["milk"]
        )

        if not can_make:
            raise ValueError(f"Cannot make {coffee_type}: {message}")

        self.water_level -= recipe["water"]
        self.coffee_beans -= recipe["beans"]
        self.milk -= recipe["milk"]
        self.coffee_made += 1

        return f"☕ {coffee_type.capitalize()} is ready! Coffee #{self.coffee_made}"

    def add_water(self, amount):
        self.water_level += amount
        return f"Added {amount}ml of water. Current level: {self.water_level}ml"

    def add_coffee_beans(self, amount):
        self.coffee_beans += amount
        return f"Added {amount}g of coffee beans. Current level: {self.coffee_beans}g"

    def add_milk(self, amount):
        self.milk += amount
        return f"Added {amount}ml of milk. Current level: {self.milk}ml"

    def get_status(self):
        return {
            "is_on": self.is_on,
            "water_level": self.water_level,
            "coffee_beans": self.coffee_beans,
            "milk": self.milk,
            "coffee_made": self.coffee_made
        }

    def __str__(self):
        return f"CoffeeMachine(water={self.water_level}ml, beans={self.coffee_beans}g, milk={self.milk}ml, made={self.coffee_made})"