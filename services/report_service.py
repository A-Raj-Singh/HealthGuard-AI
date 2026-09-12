import io
import json
import xml.etree.ElementTree as ET

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from database.crud import (
    get_patient,
    list_metrics,
    list_medications,
    list_nutrition,
)


def report_data(patient_id):
    return (
        get_patient(patient_id),
        list_metrics(patient_id),
        list_medications(patient_id),
        list_nutrition(patient_id),
    )


def metrics_csv(metrics):
    df = pd.DataFrame(
        [
            {
                "Date": m.metric_date,
                "Steps": m.steps,
                "Calories Burned": m.calories_burned,
                "Sleep Hours": m.sleep_hours,
                "Heart Rate": m.heart_rate,
            }
            for m in metrics
        ]
    )

    return df.to_csv(index=False).encode("utf-8")


def health_json(patient, metrics, medications, nutrition):
    data = {
        "patient": {
            "name": patient.name,
            "age": patient.age,
            "gender": patient.gender,
        },
        "medications": [
            {
                "medicine": medication.medicine_name,
                "dosage": medication.dosage,
                "reminder_time": (
                    medication.reminder_time.strftime("%H:%M")
                    if medication.reminder_time
                    else None
                ),
                "active": medication.active,
            }
            for medication in medications
        ],
        "health_metrics": [
            {
                "date": str(metric.metric_date),
                "steps": metric.steps,
                "calories_burned": metric.calories_burned,
                "sleep_hours": metric.sleep_hours,
                "heart_rate": metric.heart_rate,
            }
            for metric in metrics
        ],
        "nutrition": [
            {
                "date": str(log.log_date),
                "food": log.food_name,
                "calories": log.calories,
                "protein_g": log.protein_g,
                "carbs_g": log.carbs_g,
                "fat_g": log.fat_g,
                "source": log.source,
            }
            for log in nutrition
        ],
    }

    return json.dumps(
        data,
        indent=2,
    ).encode("utf-8")


def health_xml(patient, metrics, medications, nutrition):
    root = ET.Element("healthguard_report")

    patient_node = ET.SubElement(root, "patient")

    ET.SubElement(
        patient_node,
        "name",
    ).text = str(patient.name)

    ET.SubElement(
        patient_node,
        "age",
    ).text = str(patient.age)

    ET.SubElement(
        patient_node,
        "gender",
    ).text = str(patient.gender)

    medications_node = ET.SubElement(
        root,
        "medications",
    )

    for medication in medications:
        medication_node = ET.SubElement(
            medications_node,
            "medication",
        )

        ET.SubElement(
            medication_node,
            "medicine",
        ).text = str(medication.medicine_name)

        ET.SubElement(
            medication_node,
            "dosage",
        ).text = str(medication.dosage)

        ET.SubElement(
            medication_node,
            "reminder_time",
        ).text = (
            medication.reminder_time.strftime("%H:%M")
            if medication.reminder_time
            else ""
        )

        ET.SubElement(
            medication_node,
            "active",
        ).text = str(medication.active)

    metrics_node = ET.SubElement(
        root,
        "health_metrics",
    )

    for metric in metrics:
        metric_node = ET.SubElement(
            metrics_node,
            "metric",
        )

        ET.SubElement(
            metric_node,
            "date",
        ).text = str(metric.metric_date)

        ET.SubElement(
            metric_node,
            "steps",
        ).text = str(metric.steps)

        ET.SubElement(
            metric_node,
            "calories_burned",
        ).text = str(metric.calories_burned)

        ET.SubElement(
            metric_node,
            "sleep_hours",
        ).text = str(metric.sleep_hours)

        ET.SubElement(
            metric_node,
            "heart_rate",
        ).text = str(metric.heart_rate)

    nutrition_node = ET.SubElement(
        root,
        "nutrition",
    )

    for log in nutrition:
        log_node = ET.SubElement(
            nutrition_node,
            "entry",
        )

        ET.SubElement(
            log_node,
            "date",
        ).text = str(log.log_date)

        ET.SubElement(
            log_node,
            "food",
        ).text = str(log.food_name)

        ET.SubElement(
            log_node,
            "calories",
        ).text = str(log.calories)

        ET.SubElement(
            log_node,
            "protein_g",
        ).text = str(log.protein_g)

        ET.SubElement(
            log_node,
            "carbs_g",
        ).text = str(log.carbs_g)

        ET.SubElement(
            log_node,
            "fat_g",
        ).text = str(log.fat_g)

        ET.SubElement(
            log_node,
            "source",
        ).text = str(log.source)

    return ET.tostring(
        root,
        encoding="utf-8",
        xml_declaration=True,
    )


def health_pdf(patient, metrics, medications):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    story = [
        Paragraph(
            "HealthGuard AI - Health Report",
            styles["Title"],
        ),
        Spacer(1, 10),
    ]

    story.append(
        Paragraph(
            f"Patient: {patient.name} | "
            f"Age: {patient.age} | "
            f"Gender: {patient.gender}",
            styles["BodyText"],
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "Medications",
            styles["Heading2"],
        )
    )

    med_rows = [
        ["Medicine", "Dosage", "Reminder"]
    ] + [
        [
            medication.medicine_name,
            medication.dosage,
            (
                medication.reminder_time.strftime("%H:%M")
                if medication.reminder_time
                else ""
            ),
        ]
        for medication in medications
    ]

    story.append(
        Table(
            med_rows,
            repeatRows=1,
            style=TableStyle(
                [
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey,
                    ),
                ]
            ),
        )
    )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            "Health Metrics",
            styles["Heading2"],
        )
    )

    metric_rows = [
        ["Date", "Steps", "Calories", "Sleep", "Heart Rate"]
    ] + [
        [
            str(metric.metric_date),
            metric.steps,
            metric.calories_burned,
            metric.sleep_hours,
            metric.heart_rate,
        ]
        for metric in metrics
    ]

    story.append(
        Table(
            metric_rows,
            repeatRows=1,
            style=TableStyle(
                [
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey,
                    ),
                ]
            ),
        )
    )

    doc.build(story)

    return buffer.getvalue()
