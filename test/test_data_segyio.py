import os

import json
import pytest
import segyio

from datasets import dataset_metadata

MAX_FILE_SIZE = 1000000

def fixture_dir(*args):
    dir_path = os.path.join(os.path.dirname(__file__), 'fixtures', *args)
    if not os.path.isdir(os.path.dirname(dir_path)):
        os.makedirs(os.path.dirname(dir_path))
    return dir_path


@pytest.fixture
def dataset_ids():
    with open(fixture_dir('dataset_ids.json')) as ids:
        return json.load(ids)


def test_collect_data(dataset_ids):
    assert len(dataset_ids)
    for _id in dataset_ids:
        metadata = dataset_metadata(_id)
        assert 'attributes' in metadata
        assert 'fileList' in metadata['attributes']
        with open(fixture_dir('data',f'{_id}.json'), 'w') as store_data:
            store_data.write(json.dumps(metadata))


