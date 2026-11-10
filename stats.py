import math
from typing import Dict, List, Optional, Tuple, Union


def mean(numbers: List[float]) -> float:
    if not numbers:
        raise ValueError("Cannot calculate mean of empty list.")
    return sum(numbers) / len(numbers)


def median(numbers: List[float]) -> float:
    if not numbers:
        raise ValueError("Cannot calculate median of empty list.")
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    mid = n // 2
    if n % 2 == 1:
        return float(sorted_nums[mid])
    return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2.0


def variance(numbers: List[float], sample: bool = True) -> float:
    n = len(numbers)
    if n < 2:
        return 0.0
    avg = mean(numbers)
    sum_sq_diff = sum((x - avg) ** 2 for x in numbers)
    denominator = (n - 1) if sample else n
    return sum_sq_diff / denominator


def standard_deviation(numbers: List[float], sample: bool = True) -> float:
    return math.sqrt(variance(numbers, sample=sample))


def percentile(numbers: List[float], p: float) -> float:
    if not numbers:
        raise ValueError("Cannot calculate percentile of empty list.")
    if not 0.0 <= p <= 100.0:
        raise ValueError("Percentile must be between 0 and 100.")
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    if n == 1:
        return float(sorted_nums[0])
    rank = (p / 100.0) * (n - 1)
    lower_idx = int(rank)
    upper_idx = min(lower_idx + 1, n - 1)
    weight = rank - lower_idx
    return sorted_nums[lower_idx] * (1.0 - weight) + sorted_nums[upper_idx] * weight


def quartiles(numbers: List[float]) -> Tuple[float, float, float]:
    q1 = percentile(numbers, 25.0)
    q2 = percentile(numbers, 50.0)
    q3 = percentile(numbers, 75.0)
    return q1, q2, q3


def interquartile_range(numbers: List[float]) -> float:
    q1, _, q3 = quartiles(numbers)
    return q3 - q1


def detect_outliers_iqr(numbers: List[float], factor: float = 1.5) -> List[float]:
    if len(numbers) < 4:
        return []
    q1, _, q3 = quartiles(numbers)
    iqr = q3 - q1
    lower_bound = q1 - factor * iqr
    upper_bound = q3 + factor * iqr
    return [x for x in numbers if x < lower_bound or x > upper_bound]


def detect_outliers_zscore(numbers: List[float], threshold: float = 2.5) -> List[float]:
    if len(numbers) < 3:
        return []
    std = standard_deviation(numbers)
    if std == 0.0:
        return []
    avg = mean(numbers)
    return [x for x in numbers if abs((x - avg) / std) >= threshold]


def skewness(numbers: List[float]) -> float:
    n = len(numbers)
    if n < 3:
        return 0.0
    std = standard_deviation(numbers, sample=True)
    if std == 0.0:
        return 0.0
    avg = mean(numbers)
    m3 = sum((x - avg) ** 3 for x in numbers) / n
    return m3 / (std ** 3)


def calculate_profile(numbers: List[float]) -> Dict[str, Union[int, float, List[float]]]:
    if not numbers:
        raise ValueError("Dataset is empty.")

    q1, q2, q3 = quartiles(numbers)
    iqr = q3 - q1
    iqr_outliers = detect_outliers_iqr(numbers)
    z_outliers = detect_outliers_zscore(numbers)

    return {
        "count": len(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "range": max(numbers) - min(numbers),
        "mean": round(mean(numbers), 4),
        "median": round(median(numbers), 4),
        "variance": round(variance(numbers), 4),
        "std_dev": round(standard_deviation(numbers), 4),
        "q1": round(q1, 4),
        "q2": round(q2, 4),
        "q3": round(q3, 4),
        "iqr": round(iqr, 4),
        "skewness": round(skewness(numbers), 4),
        "iqr_outliers": iqr_outliers,
        "zscore_outliers": z_outliers,
    }

