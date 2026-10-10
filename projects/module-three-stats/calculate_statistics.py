"""Module 3: basic statistics calculator."""

from numbers import Real


def validate_numbers(numbers):
    """Raise if `numbers` is not a non-empty list/tuple of real numbers."""
    if not isinstance(numbers, (list, tuple)):
        raise TypeError("numbers must be a list or tuple")
    if len(numbers) == 0:
        raise ValueError("numbers must not be empty")
    for value in numbers:
        if isinstance(value, bool) or not isinstance(value, Real):
            raise TypeError(f"non-numeric value: {value!r}")


def calculate_statistics(numbers):
    """Return total, count, average, maximum, minimum and positive flag."""
    validate_numbers(numbers)

    total = sum(numbers)
    count = len(numbers)

    return {
        "total": total,
        "count": count,
        "average": total / count,
        "maximum": max(numbers),
        "minimum": min(numbers),
        "positive": total > 0,
    }


def format_summary(stats):
    return (
        f"Avg: {stats['average']} Max: {stats['maximum']} "
        f"Min: {stats['minimum']}"
    )


if __name__ == "__main__":
    result = calculate_statistics([1, 2, 3, 4, 5])
    print(result)
    print(format_summary(result))
