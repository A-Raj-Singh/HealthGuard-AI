import requests
from urllib.parse import quote


OPENFDA_LABEL_URL = "https://api.fda.gov/drug/label.json"


def lookup_drug_label(medicine_name: str) -> dict:
    """
    Look up FDA drug-label information for a medicine.

    This is an informational lookup only. It does not diagnose,
    prescribe, or recommend medication changes.
    """

    name = medicine_name.strip()

    if not name:
        return {
            "found": False,
            "medicine": medicine_name,
            "interactions": [],
            "source": "openFDA",
            "message": "Please enter a medicine name.",
        }

    try:
        response = requests.get(
            OPENFDA_LABEL_URL,
            params={
                "search": f'openfda.brand_name:"{quote(name)}"',
                "limit": 5,
            },
            timeout=10,
        )

        if response.status_code != 200:
            return {
                "found": False,
                "medicine": name,
                "interactions": [],
                "source": "openFDA",
                "message": "No reliable drug-label information was found.",
            }

        data = response.json()
        results = data.get("results", [])

        if not results:
            return {
                "found": False,
                "medicine": name,
                "interactions": [],
                "source": "openFDA",
                "message": "No matching FDA drug label was found.",
            }

        interactions = []

        for result in results:
            values = result.get("drug_interactions", [])

            if isinstance(values, list):
                interactions.extend(values)
            elif isinstance(values, str):
                interactions.append(values)

        return {
            "found": True,
            "medicine": name,
            "interactions": interactions,
            "source": "openFDA",
            "message": (
                "FDA drug-label information retrieved successfully."
            ),
        }

    except requests.RequestException:
        return {
            "found": False,
            "medicine": name,
            "interactions": [],
            "source": "openFDA",
            "message": (
                "The medication information service is temporarily "
                "unavailable. Please try again later."
            ),
        }

    except (ValueError, TypeError):
        return {
            "found": False,
            "medicine": name,
            "interactions": [],
            "source": "openFDA",
            "message": (
                "The medication information could not be processed."
            ),
        }


def check_medication_interactions(medicines: list[str]) -> list[dict]:
    """
    Check the patient's medications against available FDA label
    interaction information.

    Returns informational results only.
    """

    results = []

    cleaned_medicines = []

    for medicine in medicines:
        name = medicine.strip()

        if name and name.lower() not in {
            item.lower() for item in cleaned_medicines
        }:
            cleaned_medicines.append(name)

    for medicine in cleaned_medicines:
        results.append(
            lookup_drug_label(medicine)
        )

    return results
