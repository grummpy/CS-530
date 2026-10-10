"""Randomized check of calculate_statistics against the stdlib."""

import math
import random
import statistics

from calculate_statistics import calculate_statistics


def run(trials=5000, seed=530):
    rng = random.Random(seed)
    for _ in range(trials):
        size = rng.randint(1, 200)
        if rng.random() < 0.5:
            data = [rng.randint(-1000, 1000) for _ in range(size)]
        else:
            data = [rng.uniform(-1e3, 1e3) for _ in range(size)]
        before = list(data)
        r = calculate_statistics(data)

        assert data == before
        assert r["count"] == size
        assert r["maximum"] == max(before) and r["minimum"] == min(before)
        assert r["range"] == max(before) - min(before)
        assert math.isclose(r["total"], sum(before), abs_tol=1e-6)
        assert math.isclose(r["average"], statistics.fmean(before),
                            rel_tol=1e-9, abs_tol=1e-9)
        assert r["median"] == statistics.median(before)
        assert r["mode"] == statistics.multimode(before)
        assert r["minimum"] <= r["median"] <= r["maximum"]
        if size >= 2:
            assert math.isclose(r["std_dev"], statistics.stdev(before),
                                rel_tol=1e-9, abs_tol=1e-9)
            assert r["q1"] <= r["median"] <= r["q3"]
            assert r["iqr"] >= 0
            assert all(x in before for x in r["outliers"])
        else:
            assert r["variance"] is None and r["outliers"] == []

    bad_inputs = [[], (), "abc", None, 5, {1: 2}, [1, None], [1, "2"],
                  [True, 2]]
    for bad in bad_inputs:
        try:
            calculate_statistics(bad)
        except (ValueError, TypeError):
            continue
        raise AssertionError(f"not rejected: {bad!r}")
    return trials, len(bad_inputs)


if __name__ == "__main__":
    trials, rejected = run()
    print(f"PASS: {trials} random datasets, {rejected} bad inputs rejected")
