"""Module 3: statistics calculator (basic + descriptive enhancements)."""

import math
import statistics
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
    maximum = max(numbers)
    minimum = min(numbers)
    average = total / count

    stats = {
        "total": total,
        "count": count,
        "average": average,
        "maximum": maximum,
        "minimum": minimum,
        "positive": total > 0,
        "range": maximum - minimum,
        "median": statistics.median(numbers),
        "mode": statistics.multimode(numbers),
        "variance": None,
        "std_dev": None,
        "q1": None,
        "q3": None,
        "iqr": None,
        "outliers": [],
    }

    if count >= 2:
        stats["variance"] = statistics.variance(numbers)
        stats["std_dev"] = math.sqrt(stats["variance"])
        q1, _, q3 = statistics.quantiles(numbers, n=4, method="inclusive")
        iqr = q3 - q1
        low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        stats.update(q1=q1, q3=q3, iqr=iqr)
        stats["outliers"] = [x for x in numbers if x < low or x > high]

    return stats


def format_summary(stats):
    return (
        f"Avg: {stats['average']} Max: {stats['maximum']} "
        f"Min: {stats['minimum']}"
    )


def format_report(stats):
    """Multi-line report of every statistic."""
    lines = [format_summary(stats)]
    for key in ("total", "count", "range", "median", "mode", "variance",
                "std_dev", "q1", "q3", "iqr", "outliers", "positive"):
        lines.append(f"{key}: {stats[key]}")
    return "\n".join(lines)


if __name__ == "__main__":
    result = calculate_statistics([1, 2, 3, 4, 5])
    print(result)
    print(format_report(result))
