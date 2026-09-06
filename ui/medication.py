import streamlit as st
from datetime import datetime, time, date
from database.crud import (
    add_medication,
    list_medications,
    delete_medication,
    mark_dose,
    dose_statuses,
)

def render(patient_id):
    st.title('💊 Medication Tracker')
    st.info('Reminders are shown in the app when their scheduled time is reached. This prototype does not run a background process or send SMS/email alerts.')
    with st.form('add_med'):
        a,b,c = st.columns(3)
        name = a.text_input('Medicine name')
        dosage = b.text_input('Dosage', placeholder='e.g. 1 tablet')
        reminder = c.time_input('Daily time', value=time(9,0))
        if st.form_submit_button('Add medication', type='primary'):
            if name.strip() and dosage.strip(): add_medication(patient_id, name.strip(), dosage.strip(), reminder); st.success('Medication added.'); st.rerun()
            else: st.error('Enter medicine name and dosage.')
    meds = list_medications(patient_id, active_only=True)
    st.subheader('Today’s schedule')
    now = datetime.now().time()
    statuses = dose_statuses(patient_id, date.today())

    for med in meds:
        status = statuses.get(med.id, 'pending')
        cols = st.columns([3,2,2,1])
        cols[0].write(f'**{med.medicine_name}** — {med.dosage}')
        cols[1].write(med.reminder_time.strftime('%I:%M %p'))
        if status == 'taken': cols[2].success('Taken')
        elif now >= med.reminder_time: cols[2].warning('Due')
        else: cols[2].info('Upcoming')
        if status != 'taken' and cols[3].button('✓', key=f'take_{med.id}'):
            mark_dose(med.id, patient_id); st.rerun()
        if cols[3].button('×', key=f'del_{med.id}'):
            delete_medication(med.id, patient_id); st.rerun()
