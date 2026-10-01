#!/usr/bin/env python3
"""Draw public-domain visual cards from The Met Collection API.

The script returns metadata and image URLs. It does not download images unless
the caller explicitly supplies --download-dir, and it never removes source
rights metadata from the output.
"""

from __future__ import annotations

import argparse
import json
import random
import secrets
import urllib.parse
import urllib.request
from pathlib import Path


API_ROOT = "https://collectionapi.metmuseum.org/public/collection/v1.1"
OBJECT_API_ROOT = "https://collectionapi.metmuseum.org/public/collection/v1"
SOURCE_NAME = "The Metropolitan Museum of Art Collection API"
CC0_URL = "https://creativecommons.org/publicdomain/zero/1.0/"


def fetch_json(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "daxuan-journal-palette/0.4.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def search_ids(query: str, rng: random.Random, pool_size: int) -> list[int]:
    base_params = {
        "q": query,
        "hasImages": "true",
        "isPublicDomain": "true",
        "limit": min(max(pool_size, 50), 500),
    }
    first_url = f"{API_ROOT}/search?{urllib.parse.urlencode(base_params)}"
    first_page = fetch_json(first_url)
    total = int(first_page.get("total", 0))
    limit = int(base_params["limit"])
    if total <= limit:
        return [int(value) for value in first_page.get("objectIDs", [])]
    offset = rng.randrange(0, total - limit + 1)
    base_params["offset"] = offset
    page_url = f"{API_ROOT}/search?{urllib.parse.urlencode(base_params)}"
    page = fetch_json(page_url)
    return [int(value) for value in page.get("objectIDs", [])]


def object_record(object_id: int) -> dict | None:
    record = fetch_json(f"{OBJECT_API_ROOT}/objects/{object_id}")
    image_url = record.get("primaryImageSmall") or record.get("primaryImage")
    if not record.get("isPublicDomain") or not image_url:
        return None
    return {
        "source_type": "public-domain",
        "source": SOURCE_NAME,
        "source_url": record.get("objectURL") or record.get("linkResource"),
        "image_url": image_url,
        "thumbnail_url": record.get("primaryImageSmall") or image_url,
        "artwork_id": str(record.get("objectID", object_id)),
        "title": record.get("title") or "Untitled",
        "artist": record.get("artistDisplayName") or "Unknown artist",
        "date": record.get("objectDate") or "",
        "culture": record.get("culture") or "",
        "medium": record.get("medium") or "",
        "rights": "public-domain-as-marked-by-source-api",
        "rights_url": CC0_URL,
        "palette_status": "not-extracted",
    }


def download_image(url: str, target: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "daxuan-journal-palette/0.4.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        target.write_bytes(response.read())


def draw_cards(query: str, count: int, seed: int | None, download_dir: Path | None) -> dict:
    actual_seed = seed if seed is not None else secrets.randbelow(2**32)
    rng = random.Random(actual_seed)
    ids = search_ids(query, rng, max(count * 4, 20))
    rng.shuffle(ids)
    cards: list[dict] = []
    for object_id in ids:
        if len(cards) >= count:
            break
        try:
            card = object_record(object_id)
        except Exception:
            continue
        if card is None:
            continue
        card["card_id"] = f"card-{len(cards) + 1:02d}"
        if download_dir is not None:
            download_dir.mkdir(parents=True, exist_ok=True)
            suffix = Path(urllib.parse.urlparse(card["image_url"]).path).suffix or ".jpg"
            target = download_dir / f"{card['card_id']}-{card['artwork_id']}{suffix}"
            download_image(card["image_url"], target)
            card["local_image"] = str(target)
        cards.append(card)
    if len(cards) < count:
        raise RuntimeError(f"Only found {len(cards)} usable public-domain cards for query {query!r}")
    return {
        "schema_version": "1.0.0",
        "draw_id": f"met-{actual_seed}",
        "query": query,
        "seed": actual_seed,
        "count": len(cards),
        "source": SOURCE_NAME,
        "cards": cards,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", default="painting", help="Met API search phrase")
    parser.add_argument("--count", type=int, default=5, choices=range(3, 6), metavar="3-5")
    parser.add_argument("--seed", type=int, help="Reproduce a draw; omitted means a random seed")
    parser.add_argument("--download-dir", type=Path, help="Explicitly download selected public-domain images")
    parser.add_argument("--output", type=Path, help="Write JSON to this path; otherwise print it")
    args = parser.parse_args()
    payload = draw_cards(args.query, args.count, args.seed, args.download_dir)
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
