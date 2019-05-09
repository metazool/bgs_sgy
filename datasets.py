import json
import logging

import requests
requests.packages.urllib3.disable_warnings()

logging.basicConfig(level=logging.INFO)

API = 'https://webservices.bgs.ac.uk/accessions'


def download_urls(datasets, suffix=None):
    """Given a list of dataset IDs, return a list of associated downloadable files"""
    downloadable = []
    for _id in datasets:
        metadata = dataset_metadata(_id)
        downloadable += file_urls(metadata.get('attributes', {}), suffix=suffix)
        metadata = dataset_metadata(_id)

    return downloadable


def dataset_metadata(_id):
    """Given an ID collect the dataset metadata from BGS accessions"""
    response = requests.get(f'{API}/item/{_id}', verify=False)
    metadata = {}
    try:
        metadata = response.json()
    except json.decoder.JSONDecodeError:
        logging.error(f"no valid data for {_id}")
    return metadata


def file_urls(metadata, suffix=None):
    """Given the metadata for a dataset create list of file URLS"""
    downloadable = []

    for item in metadata.get('fileList', []):
        url = f"{API}/download/{metadata['id']}?fileName={item['name']}"
        if suffix and item.get('type') != suffix:
            continue
        downloadable.append(url)

    return downloadable


if __name__ == '__main__':
    with open('dataset_ids.json') as datasets:
        print('\n'.join(download_urls(json.load(datasets), suffix='sgy')))


