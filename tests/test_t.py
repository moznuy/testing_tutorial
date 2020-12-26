from unittest import mock

from collector import stats


def test_collector_true(prepare_testing_directory):
    path, actual_stats = prepare_testing_directory
    res = stats.collect_stats(path)
    assert res == actual_stats


def test_collector_di(mock_walk_stat):
    res = stats.collect_stats('', mock_walk_stat.walk, mock_walk_stat.stat)
    assert res == mock_walk_stat.total_size


def test_oop_collector_di(mock_walk_stat):
    sc = stats.StatsCollector(mock_walk_stat.walk, mock_walk_stat.stat)
    res = sc('')
    assert res == mock_walk_stat.total_size


def test_collector_mock(mock_walk_stat):
    with (mock.patch.object(stats.os, 'walk', mock_walk_stat.walk),
          mock.patch.object(stats.os, 'stat', mock_walk_stat.stat)):
        res = stats.old_collect_stats('')
        assert res == mock_walk_stat.total_size
