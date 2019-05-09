import os

import json
import pytest
import requests
import segyio

from datasets import file_url

# Skip past files larger than this arbitrary limit
MAX_FILE_SIZE = 320000000

class ValidationError(Exception):
    pass


def fixture_dir(*args):
    dir_path = os.path.join(os.path.dirname(__file__), 'fixtures', *args)
    if not os.path.isdir(os.path.dirname(dir_path)):
        os.makedirs(os.path.dirname(dir_path))
    return dir_path


def dataset_metadata():
    """Read whatever metadata previous tests left in the fixtures"""
    md = []
    data_dir = fixture_dir('data')
    for _file in os.listdir(data_dir):
        filepath = os.path.join(data_dir, _file)
        if not os.path.isfile(filepath):
            continue
        with open(filepath) as data:
            md.append(json.load(data)['attributes'])
    return md


def make_local_copies(limit=5, repeat=False):
    """Download and cache data. TODO limit results rather than sizes / samples"""
    samples = []
    sampled_datasets = []
    md = dataset_metadata()

    for dataset in md:
        for item in dataset.get('fileList',[]):
            if dataset['id'] in sampled_datasets:
                continue
            url = file_url(dataset['id'], item['name'])

            # TODO this better
            if 'sgy' not in url:
                continue
            if int(item['size']) > MAX_FILE_SIZE:
                continue

            local_copy = fixture_dir('data', 'samples', item['name'])

            if not os.path.isfile(local_copy):
                with requests.get(url, stream=True, verify=False) as response:
                    with open(local_copy,'wb') as data:
                        data.write(response.content)
            # If this is one of a set, blithely assume all have same behaviour
            if not repeat:
                sampled_datasets.append(dataset['id'])
            samples.append(local_copy)

    return samples


