import importlib

import hashlib


def import_from_path(path: str):
    module_name, attr_name = path.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, attr_name)


def hash_fingerprint(fp: dict) -> str:
    concat = "".join(str(v) for v in fp.values())
    return hashlib.sha256(concat.encode()).hexdigest()

