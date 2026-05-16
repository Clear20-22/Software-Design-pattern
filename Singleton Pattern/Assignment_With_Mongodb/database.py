from singleton import get_bill, get_double, get_eager, get_enum, get_lazy, get_safe


choices = {
    "1": ("Eager Singleton", get_eager),
    "2": ("Lazy Singleton", get_lazy),
    "3": ("Thread-Safe Singleton", get_safe),
    "4": ("Double-Checked Locking Singleton", get_double),
    "5": ("Bill Pugh Singleton", get_bill),
    "6": ("Enum-Style Singleton", get_enum),
}


def test_one(name: str, make_one) -> None:
    print("\n" + "=" * 70)
    print(name.upper())
    print("=" * 70)

    first = make_one()
    second = make_one()
    third = make_one()

    print(f"First call  -> object id: {first.get_instance_id()}")
    print(f"Second call -> object id: {second.get_instance_id()}")
    print(f"Third call  -> object id: {third.get_instance_id()}")
    print(f"Same object  : {first is second is third}")
    print(f"Same id      : {id(first) == id(second) == id(third)}")

    try:
        users = first.get_all_users()
        print(f"MongoDB users: {len(users)}")
    except Exception as exc:
        print(f"MongoDB note : {exc}")


def menu() -> None:
    print("\n" + "=" * 70)
    print("SINGLETON PATTERN TESTER")
    print("=" * 70)
    print("Choose one option:")
    for option, (name, _) in choices.items():
        print(f"  {option}. {name}")
    print("  7. Test all patterns")
    print("  0. Exit")


def run_one(option: str) -> None:
    if option == "7":
        for name, make_one in choices.values():
            test_one(name, make_one)
        return

    if option in choices:
        name, make_one = choices[option]
        test_one(name, make_one)
        return

    print("Invalid option. Please choose 0 to 7.")


def main() -> None:
    while True:
        menu()
        choice = input("Enter your choice: ").strip()

        if choice == "0":
            print("Goodbye.")
            break

        run_one(choice)


if __name__ == "__main__":
    main()
