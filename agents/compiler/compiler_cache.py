import json
from pathlib import Path

CACHE_FILE = Path(
    "data/compiler_cache.json"
)

CACHE_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

if not CACHE_FILE.exists():

    CACHE_FILE.write_text(
        "{}",
        encoding="utf-8"
    )


def load_cache():

    try:

        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            content = f.read().strip()

            if not content:

                return {}

            return json.loads(
                content
            )

    except Exception:

        return {}


def save_cache(cache):

    with open(
        CACHE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            cache,
            f,
            indent=4
        )


def get_cached(condition):

    cache = load_cache()

    return cache.get(
        condition.lower()
    )


def set_cached(
    condition,
    dsl
):

    cache = load_cache()

    cache[
        condition.lower()
    ] = dsl

    save_cache(cache)