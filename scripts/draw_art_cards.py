#!/usr/bin/env python3
"""Draw public-domain visual cards from The Met Collection API.

The script returns metadata and image URLs. It does not download images unless
the caller explicitly supplies --download-dir, and it never removes source
rights metadata from the output.
"""

from __future__ import annotations

import argparse
import colorsys
from concurrent.futures import ThreadPoolExecutor
import io
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
    request = urllib.request.Request(url, headers={"User-Agent": "daxuan-journal-palette/0.5.5"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def fetch_bytes(url: str, timeout: int = 60) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "daxuan-journal-palette/0.5.5"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def _search_ids_single(query: str, rng: random.Random, pool_size: int) -> list[int]:
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
    first_ids = [int(value) for value in (first_page.get("objectIDs") or [])]
    if total <= limit:
        return first_ids
    # The Met endpoint occasionally returns `objectIDs: null` for a valid
    # high-offset page. Retry a few offsets, then fall back to the first page
    # rather than silently returning an empty candidate pool.
    for _ in range(4):
        offset = rng.randrange(0, total - limit + 1)
        base_params["offset"] = offset
        page_url = f"{API_ROOT}/search?{urllib.parse.urlencode(base_params)}"
        page = fetch_json(page_url)
        page_ids = [int(value) for value in (page.get("objectIDs") or [])]
        if page_ids:
            return page_ids
    return first_ids


def search_ids(query: str, rng: random.Random, pool_size: int) -> list[int]:
    """Search one term or several `|`-separated terms and de-duplicate IDs."""
    queries = [part.strip() for part in query.split("|") if part.strip()]
    if len(queries) <= 1:
        return _search_ids_single(queries[0] if queries else query, rng, pool_size)
    per_query = max(20, pool_size // len(queries))
    combined: list[int] = []
    for term in queries:
        combined.extend(_search_ids_single(term, rng, per_query))
    unique = list(dict.fromkeys(combined))
    rng.shuffle(unique)
    return unique[:pool_size]


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


def colorfulness_from_pixels(
    pixels: list[tuple[int, int, int]], min_saturation: float = 0.25
) -> dict:
    """Return a transparent, bounded colorfulness diagnostic for RGB pixels.

    The score is not a color-vision or publication certification. It is used
    only to avoid drawing mostly grayscale/sepia images when the user asks for
    palette-rich cards. Mean saturation captures the overall color signal,
    the 75th percentile preserves colorful regions in images with white space,
    and colorful_fraction prevents a single saturated pixel from dominating.
    """
    if not pixels:
        raise ValueError("image contains no pixels")
    saturations: list[float] = []
    hues: list[float] = []
    for red, green, blue in pixels:
        hue, saturation, value = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
        saturations.append(saturation)
        if saturation >= min_saturation and value >= 0.15:
            hues.append(hue)
    ordered = sorted(saturations)
    p75 = ordered[min(len(ordered) - 1, int(round(0.75 * (len(ordered) - 1))))]
    mean_saturation = sum(saturations) / len(saturations)
    colorful_fraction = sum(value >= min_saturation for value in saturations) / len(saturations)
    hue_bins = len({min(11, int(hue * 12)) for hue in hues}) / 12
    score = 0.45 * mean_saturation + 0.30 * p75 + 0.15 * colorful_fraction + 0.10 * hue_bins
    return {
        "score": round(score, 6),
        "mean_saturation": round(mean_saturation, 6),
        "p75_saturation": round(p75, 6),
        "colorful_fraction": round(colorful_fraction, 6),
        "hue_coverage": round(hue_bins, 6),
        "min_saturation": min_saturation,
    }


def colorfulness_from_bytes(
    payload: bytes, max_side: int = 120, min_saturation: float = 0.25
) -> dict:
    try:
        from PIL import Image
    except ImportError as error:
        raise RuntimeError(
            "Pillow is required for --palette-friendly screening; install it or omit that flag"
        ) from error
    with Image.open(io.BytesIO(payload)) as image:
        image = image.convert("RGB")
        image.thumbnail((max_side, max_side))
        pixels = list(image.get_flattened_data() if hasattr(image, "get_flattened_data") else image.getdata())
    result = colorfulness_from_pixels(pixels, min_saturation=min_saturation)
    result["max_side"] = max_side
    result["pixel_count"] = len(pixels)
    return result


def screen_record_colorfulness(
    record: dict,
    max_side: int = 120,
    min_saturation: float = 0.25,
) -> dict:
    """Download one thumbnail transiently and attach its palette-rich score."""
    metrics = colorfulness_from_bytes(
        fetch_bytes(record["image_url"]),
        max_side=max_side,
        min_saturation=min_saturation,
    )
    record = dict(record)
    record["colorfulness"] = metrics
    return record


def download_image(url: str, target: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "daxuan-journal-palette/0.5.5"})
    with urllib.request.urlopen(request, timeout=60) as response:
        target.write_bytes(response.read())


def draw_cards(
    query: str,
    count: int,
    seed: int | None,
    download_dir: Path | None,
    palette_friendly: bool = False,
    min_colorfulness: float = 0.22,
    min_saturation: float = 0.25,
    candidate_pool: int | None = None,
    workers: int = 8,
) -> dict:
    if count < 1:
        raise ValueError("count must be at least 1")
    actual_seed = seed if seed is not None else secrets.randbelow(2**32)
    rng = random.Random(actual_seed)
    pool_size = max(candidate_pool or max(count * (12 if palette_friendly else 4), 20), count)
    ids = search_ids(query, rng, min(max(pool_size, 20), 500))
    rng.shuffle(ids)
    def prepare_record(object_id: int) -> dict | None:
        try:
            card = object_record(object_id)
        except Exception:
            return None
        if card is None:
            return None
        if palette_friendly:
            try:
                card = screen_record_colorfulness(
                    card,
                    max_side=120,
                    min_saturation=min_saturation,
                )
            except Exception:
                return None
        return card

    candidate_ids = ids[:pool_size]
    with ThreadPoolExecutor(max_workers=max(1, workers)) as executor:
        records = [card for card in executor.map(prepare_record, candidate_ids) if card is not None]

    if palette_friendly:
        eligible = [
            card
            for card in records
            if card.get("colorfulness", {}).get("score", 0) >= min_colorfulness
        ]
        if len(eligible) < count:
            best = sorted(
                (card.get("colorfulness", {}).get("score", 0) for card in records),
                reverse=True,
            )[:5]
            raise RuntimeError(
                f"Only found {len(eligible)} palette-rich cards for query {query!r}; "
                f"requested {count}, threshold={min_colorfulness}. Top scores={best}. "
                "Try a broader query or lower --min-colorfulness."
            )
        # Keep the draw reproducible but allow visual variety: sample from the
        # strongest three-count candidates rather than taking one deterministic
        # top-ranked image repeatedly.
        eligible.sort(key=lambda card: card["colorfulness"]["score"], reverse=True)
        shortlist = eligible[: min(len(eligible), max(count * 3, count))]
        chosen = rng.sample(shortlist, count)
    else:
        chosen = records[:count]

    cards: list[dict] = []
    for card in chosen:
        card = dict(card)
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
        "screen": {
            "palette_friendly": palette_friendly,
            "min_colorfulness": min_colorfulness if palette_friendly else None,
            "min_saturation": min_saturation if palette_friendly else None,
            "candidate_pool": pool_size,
            "candidate_records": len(records),
            "workers": max(1, workers),
        },
        "cards": cards,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", default="painting", help="Met API search phrase")
    parser.add_argument("--count", type=int, default=5, choices=range(1, 11), metavar="1-10")
    parser.add_argument("--seed", type=int, help="Reproduce a draw; omitted means a random seed")
    parser.add_argument("--download-dir", type=Path, help="Explicitly download selected public-domain images")
    parser.add_argument(
        "--palette-friendly",
        action="store_true",
        help="Screen thumbnails for colorfulness and reject mostly grayscale/sepia cards",
    )
    parser.add_argument(
        "--min-colorfulness",
        type=float,
        default=0.22,
        help="Minimum bounded colorfulness score used with --palette-friendly (default: 0.22)",
    )
    parser.add_argument(
        "--min-saturation",
        type=float,
        default=0.25,
        help="Saturation threshold used by the colorfulness diagnostic (default: 0.25)",
    )
    parser.add_argument(
        "--candidate-pool",
        type=int,
        help="Number of candidates to screen before selection; defaults to 12x count in palette-friendly mode",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="Concurrent metadata/thumbnail workers used during screening (default: 8)",
    )
    parser.add_argument("--output", type=Path, help="Write JSON to this path; otherwise print it")
    args = parser.parse_args()
    payload = draw_cards(
        args.query,
        args.count,
        args.seed,
        args.download_dir,
        palette_friendly=args.palette_friendly,
        min_colorfulness=args.min_colorfulness,
        min_saturation=args.min_saturation,
        candidate_pool=args.candidate_pool,
        workers=args.workers,
    )
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
