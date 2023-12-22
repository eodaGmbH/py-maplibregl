def fix_keys(d: dict) -> dict:
    return {k.replace("_", "-"): v for k, v in d.items()}
