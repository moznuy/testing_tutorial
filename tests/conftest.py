import os
import random
import string
import tempfile
import uuid
from dataclasses import dataclass
from typing import List, Dict

import pytest


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@pytest.fixture
def prepare_testing_directory():
    with tempfile.TemporaryDirectory() as folder:
        n = random.randrange(1, 10)
        res = 0
        for _ in range(n):
            with open(os.path.join(folder, id_generator()), 'w') as file:
                for _ in range(random.randrange(5, 25)):
                    rand_string = id_generator(random.randrange(20, 300))
                    file.write(rand_string)
                    res += len(rand_string)

        yield folder, res


class MockWalkStat:
    @dataclass
    class File:
        name: str
        size: int

    def __init__(self):
        self.dirs: List[str] = [id_generator() for _ in range(random.randrange(5, 10))]
        self.files: Dict[str, List['MockWalkStat.File']] = {
            folder: [self.File(str(uuid.uuid4()), random.randrange(50, 5000)) for _ in range(random.randrange(5, 15))]
            for folder in self.dirs
        }

        self._file_by_name: Dict[str, 'MockWalkStat.File'] = {
            os.path.join(folder_name, file.name): file
            for folder_name, file_lists in self.files.items()
            for file in file_lists
        }
        self.total_size = sum(
            file.size
            for file_lists in self.files.values()
            for file in file_lists
        )

    def walk(self, path):
        for folder, folder_files in self.files.items():
            yield os.path.join(path, folder), [], [folder_file.name for folder_file in folder_files]

    @dataclass
    class MockFileInfo:
        st_size: int

    def stat(self, path):
        return self.MockFileInfo(self._file_by_name[path].size)


@pytest.fixture
def mock_walk_stat():
    return MockWalkStat()
