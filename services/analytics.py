from datetime import date
from database.crud import list_medications, dose_statuses, list_nutrition


def adherence_percentage(patient_id, on_date=None):
    on_date = on_date or date.today()
    meds = list_medications(patient_id, active_only=True)

    if not meds:
        return 0.0

    statuses = dose_statuses(patient_id, on_date)
    taken = sum(statuses.get(med.id) == 'taken' for med in meds)

    return round(taken / len(meds) * 100, 1)


def nutrition_totals(patient_id, on_date=None):
    logs = list_nutrition(patient_id, on_date or date.today())

    return {
        k: round(sum(getattr(x, k) for x in logs), 1)
        for k in ['calories', 'protein_g', 'carbs_g', 'fat_g']
    }