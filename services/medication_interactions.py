import requests


OPENFDA_LABEL_URL = "https://api.fda.gov/drug/label.json"


def _empty_result(medicine: str, message: str) -> dict:
    """Return a consistent unsuccessful lookup result."""
    return {
        "found": False,
        "medicine": medicine,
        "interactions": [],
        "source": "openFDA / FDA drug labeling",
        "message": message,
    }


def _extract_interactions(results: list) -> list[str]:
    """Extract drug-interaction sections from FDA label results."""
    interactions = []

    for result in results:
        values = result.get("drug_interactions", [])

        if isinstance(values, list):
            interactions.extend(
                str(value).strip()
                for value in values
                if str(value).strip()
            )

        elif isinstance(values, str) and values.strip():
            interactions.append(values.strip())

    # Remove duplicate sections while preserving order.
    unique = []
    seen = set()

    for item in interactions:
        key = item.lower()

        if key not in seen:
            seen.add(key)
            unique.append(item)

    return unique


def _search_labels(search_query: str) -> list:
    """Search the openFDA drug-label endpoint."""
    response = requests.get(
        OPENFDA_LABEL_URL,
        params={
            "search": search_query,
            "limit": 5,
        },
        timeout=10,
    )

    if response.status_code == 404:
        return []

    response.raise_for_status()

    data = response.json()
    return data.get("results", [])


def lookup_drug_label(medicine_name: str) -> dict:
    """
    Look up FDA drug-label information for a medicine.

    This is an informational lookup only. It does not diagnose,
    prescribe, or recommend medication changes.
    """

    name = str(medicine_name).strip()

    if not name:
        return _empty_result(
            medicine_name,
            "Please enter a medicine name.",
        )

    # -------------------------------------------------------------
    # 1. Try exact-ish brand-name search.
    # -------------------------------------------------------------
    try:
        results = _search_labels(
            f'openfda.brand_name:"{name}"'
        )

        # ---------------------------------------------------------
        # 2. If no brand match, try generic name.
        # ---------------------------------------------------------
        if not results:
            results = _search_labels(
                f'openfda.generic_name:"{name}"'
            )

        # ---------------------------------------------------------
        # 3. Final fallback: search the complete label dataset.
        # ---------------------------------------------------------
        if not results:
            results = _search_labels(
                f'"{name}"'
            )

        if not results:
            return _empty_result(
                name,
                "No matching FDA drug label was found.",
            )

        interactions = _extract_interactions(results)

        if not interactions:
            return {
                "found": True,
                "medicine": name,
                "interactions": [],
                "source": "openFDA / FDA drug labeling",
                "message": (
                    "FDA drug-label information was found, "
                    "but no drug-interaction section was available "
                    "in the returned labels."
                ),
            }

        return {
            "found": True,
            "medicine": name,
            "interactions": interactions,
            "source": "openFDA / FDA drug labeling",
            "message": (
                "FDA drug-label interaction information "
                "retrieved successfully."
            ),
        }

    except requests.HTTPError as exc:
        return _empty_result(
            name,
            (
                "The FDA medication information service returned "
                f"an HTTP error ({exc.response.status_code})."
            ),
        )

    except requests.RequestException:
        return _empty_result(
            name,
            (
                "The medication information service is temporarily "
                "unavailable. Please try again later."
            ),
        )

    except (ValueError, TypeError):
        return _empty_result(
            name,
            "The medication information could not be processed.",
        )


def check_medication_interactions(medicines: list[str]) -> list[dict]:
    """
    Check the patient's medications against available FDA label
    interaction information.

    Returns informational results only.
    """

    results = []
    cleaned_medicines = []
    seen = set()

    for medicine in medicines:
        name = str(medicine).strip()

        if not name:
            continue

        key = name.lower()

        if key not in seen:
            seen.add(key)
            cleaned_medicines.append(name)

    for medicine in cleaned_medicines:
        results.append(
            lookup_drug_label(medicine)
        )

    return results