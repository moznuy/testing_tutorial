import os


def collect_stats(path: str, walk=os.walk, stat=os.stat):
    res = 0
    for root, dirs, files in walk(path):
        for file in files:
            res += stat(os.path.join(root, file)).st_size
    return res


def old_collect_stats(path: str):
    res = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            res += os.stat(os.path.join(root, file)).st_size
    return res


class StatsCollector:
    def __init__(self, walk=os.walk, stat=os.stat):
        self._walk = walk
        self._stat = stat

    def __call__(self, path):
        return collect_stats(path, self._walk, self._stat)


if __name__ == '__main__':
    print(collect_stats('/home/lamar/.env/gallery'))
