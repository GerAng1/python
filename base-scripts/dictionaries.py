"""Some of the many things you can do with dictionaries.
Try to use them to be more pythonic.
"""


def reducing_conditionals():
    """Example of why to use dicitonaries"""

    name = "Ted"

    """Don't do this:

    if name == "John":
        print("This is John, he is an artist.")
    elif name == "Ted":
        print("This is Ted, he is an engineer.")
    elif name == "Kennedy":
        print("This is Kennedy, he is a teacher.")
    """
    """Do this!"""

    name_job_dict = {
        "Josh": "This is John, he is an artist.",
        "Ted": "This is Ted, he is an engineer.",
        "Kenedy": "This is Kennedy, he is a teacher."
        }

    print(name_job_dict[name])


def pop_example():
    """Pops() items from dictionary"""
    available_items = {
            "health potion": 10,
            "cake of the cure": 5,
            "green elixir": 20,
            "strength sandwich": 25,
            "stamina grains": 15,
            "power stew": 30}

    health_points = 20

    health_points += available_items.pop("stamina grains", 0)
    health_points += available_items.pop("power stew", 0)
    health_points += available_items.pop("mystic bread", 0)

    print(available_items)
    print(health_points)
    print()


pop_example()
reducing_conditionals()
