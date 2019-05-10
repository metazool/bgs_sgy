import os

import json
import pytest
import requests
import segyio

from datasets import get_dataset_metadata
from test.utils import fixture_dir, dataset_metadata, get_local_copies, ValidationError

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


def test_can_open():
    """Can we run segyio.open without qualification on this data"""
    samples = get_local_copies(limit=5)
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


def test_ignore_geometry():
    """If open fails, then why? First step is to pass ignore_geometry
    and inspect some of the header lines as per
    https://github.com/equinor/segyio/issues/322#issuecomment-438517387"""
    samples = get_local_copies()
    attributes = {}
    for sample in samples:
        attrs = {}
        useful_indexes = [5, 21, 37]
        with segyio.open(sample, ignore_geometry=True) as sgy:
            for i in useful_indexes:
                attrs[i] = sgy.attributes(i)[:]
            attributes[sample] = attrs
    # For now just dump the output into the logs
    print(attributes)
