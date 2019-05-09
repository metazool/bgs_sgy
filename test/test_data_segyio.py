import os

import json
import pytest
import requests
import segyio

from datasets import get_dataset_metadata
from test.utils import fixture_dir, dataset_metadata, make_local_copies, ValidationError

# Skip past files larger than this arbitrary limit
MAX_FILE_SIZE = 320000000



@pytest.fixture
def dataset_ids():
    """Read our hard-coded list of datasets which we know carry .sgy files"""
    with open(fixture_dir('dataset_ids.json')) as ids:
        return json.load(ids)


def test_collect_data(dataset_ids):
    """collect dataset metadata from BGS Accessions webservice, save it"""
    assert len(dataset_ids)
    for _id in dataset_ids:
        if os.path.isfile(fixture_dir('data',f'{_id}.json')):
            continue
        metadata = get_dataset_metadata(_id)
        assert 'attributes' in metadata
        assert 'fileList' in metadata['attributes']
        with open(fixture_dir('data',f'{_id}.json'), 'w') as store_data:
            store_data.write(json.dumps(metadata))


def test_can_open(dataset_ids):
    """Can we run segyio.open without qualification on this data"""
    samples = make_local_copies(limit=5)
    success = []
    failure = []
    for sample in samples:
        try:
            sgy = segyio.open(sample)
            success.append(sample)
        except (RuntimeError, ValueError) as err:
            failure.append({'file': sample,
                            'err': err})

    print(success)
    if len(failure):
        raise ValidationError(failure)

