#!/usr/bin/env python3

import argparse
import logging
import os
import json
from base64 import b64decode

_log = logging.getLogger(__file__)


def dump_acme_js(acme_js_file_path: str, output_root_dir: str):
    # Read JSON file
    with open(acme_js_file_path) as f:
        data = json.load(f)
    # Determine ACME version
    assert 'acme-v02' in data['Account']['Registration']['uri'], 'Unsupported ACME version or acme.json format'

    # Find certificates
    certs = data['Certificates']
    _log.info(f'Found {len(certs)} certificates')

    certs_flat_dir = os.path.join(output_root_dir, 'certs_flat')
    os.makedirs(certs_flat_dir, exist_ok=True)

    # Loop over all certificates
    for c in certs:
        name = c['Domain']['Main']
        sans = c['Domain']['SANs']
        # Decode private key, certificate and chain
        private_key = b64decode(c['Key']).decode()
        full_chain = b64decode(c['Certificate']).decode()
        start = full_chain.find('-----BEGIN CERTIFICATE-----', 1)
        cert = full_chain[:start]
        chain = full_chain[start:]

        # Write private key, certificate and chain to certs/
        certs_dir = os.path.join(output_root_dir, 'certs', name)
        os.makedirs(certs_dir, exist_ok=True)
        for file_name, content in ('private_key.pem', private_key), ('cert.pem', cert), ('chain.pem', chain), ('full_chain.pem', full_chain):
            with open(os.path.join(certs_dir, file_name), 'w') as f:
                f.write(content)

        # Write private key, certificate and chain to certs_flat/
        cert_names = {name}
        if sans:
            cert_names.update(sans)
        for file_name in cert_names:
            for file_ext, content in ('key', private_key), ('crt', full_chain), ('chain.pem', chain):
                with open(os.path.join(certs_flat_dir, f'{file_name}.{file_ext}'), 'w') as f:
                    f.write(content)

        _log.info(f'Extracted certificate for: {", ".join(cert_names)}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='(Traefik v1, ACME v2) acme.json certs extractor')
    parser.add_argument('-f', '--acme-json-file', required=True, help='location of Traefik v1 acme.json file')
    parser.add_argument('-o', '--output-dir', default='.', help='root directory of generated cert files')
    parser.add_argument('-v', '--verbose', action='store_true', help='print verbose log to STDOUT')
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    dump_acme_js(args.acme_json_file, args.output_dir)
