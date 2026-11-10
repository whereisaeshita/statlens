import pytest
from profiler.stats import (
    calculate_profile,
    detect_outliers_iqr,
    detect_outliers_zscore,
    interquartile_range,
    mean,
    median,
    percentile,
    quartiles,
    skewness,
    standard_deviation,
    variance,
)
from profiler.reader import parse_numeric_string, read_csv_columns


def test_mean():
    assert mean([1.0, 2.0, 3.0, 4.0, 5.0]) == 3.0
    assert mean([10.0]) == 10.0
    with pytest.raises(ValueError):
        mean([])


def test_median():
    assert median([1, 3, 5]) == 3.0
    assert median([1, 2, 3, 4]) == 2.5
    assert median([9, 1, 5]) == 5.0
    with pytest.raises(ValueError):
        median([])


def test_variance_and_std():
    nums = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
    sample_var = variance(nums, sample=True)
    pop_var = variance(nums, sample=False)
    assert round(sample_var, 2) == 4.57
    assert round(pop_var, 2) == 4.0
    assert round(standard_deviation(nums, sample=True), 2) == 2.14


def test_percentile_and_quartiles():
    data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    q1, q2, q3 = quartiles(data)
    assert q2 == 55.0
    assert interquartile_range(data) == q3 - q1

    with pytest.raises(ValueError):
        percentile(data, -5)
    with pytest.raises(ValueError):
        percentile(data, 105)


def test_outlier_detection_iqr():
    normal_data = [10, 12, 11, 13, 12, 11, 14, 12, 10, 13, 100]
    outliers = detect_outliers_iqr(normal_data)
    assert 100 in outliers
    assert len(outliers) == 1


def test_outlier_detection_zscore():
    data = [10, 10, 10, 10, 10, 10, 10, 10, 10, 100]
    outliers = detect_outliers_zscore(data, threshold=2.5)
    assert 100 in outliers


def test_skewness():
    symmetric = [1, 2, 3, 4, 5]
    assert round(skewness(symmetric), 2) == 0.0

    right_skewed = [1, 1, 2, 2, 3, 10, 20]
    assert skewness(right_skewed) > 0.0


def test_calculate_profile():
    data = [2, 4, 4, 4, 5, 5, 7, 9]
    profile = calculate_profile(data)
    assert profile["count"] == 8
    assert profile["min"] == 2
    assert profile["max"] == 9
    assert profile["mean"] == 5.0


def test_parse_numeric_string():
    res = parse_numeric_string("12, 15.5, invalid, 20\n30 40")
    assert res == [12.0, 15.5, 20.0, 30.0, 40.0]


def test_read_csv_columns(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("col_a,col_b\n10,20\n30,40\n", encoding="utf-8")
    result = read_csv_columns(csv_file)
    assert "col_a" in result
    assert result["col_a"] == [10.0, 30.0]
    assert result["col_b"] == [20.0, 40.0]

