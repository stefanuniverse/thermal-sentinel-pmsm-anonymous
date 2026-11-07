"""Validate CFF 1.2 using its official schema; print no private field values."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_URL = 'https://raw.githubusercontent.com/citation-file-format/citation-file-format/1.2.0/schema.json'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--download-schema', action='store_true')
    parser.add_argument('--schema', type=Path, default=ROOT / '.local/cff-1.2.0-schema.json')
    args = parser.parse_args()
    try:
        import yaml
        import jsonschema
        if args.download_schema:
            with urllib.request.urlopen(SCHEMA_URL, timeout=30) as response:
                data = response.read()
            json.loads(data)
            args.schema.parent.mkdir(parents=True, exist_ok=True)
            args.schema.write_bytes(data)
        document = yaml.safe_load((ROOT / 'CITATION.cff').read_text(encoding='utf-8'))
        document = json.loads(json.dumps(document, default=lambda v: v.isoformat() if isinstance(v, datetime.date) else str(v)))
        schema = json.loads(args.schema.read_text(encoding='utf-8'))
        validator = jsonschema.validators.validator_for(schema)
        validator.check_schema(schema)
        errors = list(validator(schema).iter_errors(document))
        author_ok = document['authors'] == [{'name': 'StefanUniverse'}]
        result = {'passed': not errors and author_ok,
                  'schema': 'CFF 1.2.0 official tagged schema',
                  'schema_sha256': hashlib.sha256(args.schema.read_bytes()).hexdigest(),
                  'schema_error_count': len(errors), 'pseudonym_author': author_ok}
    except Exception as exc:
        result = {'passed': False, 'error_category': type(exc).__name__}
    print(json.dumps(result))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
