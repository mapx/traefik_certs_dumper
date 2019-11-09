# traefik_certs_dumper
Minimalists' acme.json certs extractor for (Traefik v1 &amp; ACME v2).

Designed to be part of cli toolchain, it dumps all certs of `acme.json` as `private key`, `chain body`, and `full chain` pem files.

## Usage
```sh
usage: dump_traefik_certs.py [-h] -f ACME_JSON_FILE [-o OUTPUT_DIR] [-v]

(Traefik v1, ACME v2) acme.json certs extractor

optional arguments:
  -h, --help            show this help message and exit
  -f ACME_JSON_FILE, --acme-json-file ACME_JSON_FILE
                        location of Traefik v1 acme.json file
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        root directory of generated cert files
  -v, --verbose         print verbose log to STDOUT
```

## Rich feature alternatives
* https://github.com/ldez/traefik-certs-dumper
* https://github.com/DanielHuisman/traefik-certificate-extractor
