import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Data Model")

FILE_NAME = "data_model.xlsx"   # wird bei jedem Submit neu erstellt

with st.form("design_form"):
    st.write("Design (Data Dictionary)")

    col1, col2, col3 = st.columns(3)
    with col1:
        mdg_m = st.checkbox("MDG-M")
        mdg_m_fields = st.number_input("Number of expected fields (MDG-M)", min_value=0, value=0, step=1)
        mdg_m_scope = st.checkbox("Implementation in Scope (MDG-M)")
    with col2:
        mdg_c = st.checkbox("MDG-C")
        mdg_c_fields = st.number_input("Number of expected fields (MDG-C)", min_value=0, value=0, step=1)
        mdg_c_scope = st.checkbox("Implementation in Scope (MDG-C)")
    with col3:
        mdg_s = st.checkbox("MDG-S")
        mdg_s_fields = st.number_input("Number of expected fields (MDG-S)", min_value=0, value=0, step=1)
        mdg_s_scope = st.checkbox("Implementation in Scope (MDG-S)")

    submitted = st.form_submit_button("Übernehmen")

if submitted:
    # Exaktes Layout: 3 Zeilen (Design, Expected Fields, Implementation in Scope)
    block = pd.DataFrame({
        "Metric": [
            "Design (Data Dictionary)",
            "Number of expected fields",
            "Implementation in Scope"
        ],
        "MDG-M": [bool(mdg_m), int(mdg_m_fields), bool(mdg_m_scope)],
        "MDG-C": [bool(mdg_c), int(mdg_c_fields), bool(mdg_c_scope)],
        "MDG-S": [bool(mdg_s), int(mdg_s_fields), bool(mdg_s_scope)],
    })

    # Neue Datei erzeugen (keine Anhänge)
    block.to_excel(FILE_NAME, index=False, engine="openpyxl")

    # Download vorbereiten (RAM)
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        block.to_excel(w, index=False, sheet_name="Data")
    buf.seek(0)

    # Anzeige (Strings zur Vermeidung von Arrow-Fehlern)
    display = block.copy()
    for col in ["MDG-M", "MDG-C", "MDG-S"]:
        display[col] = display[col].map(lambda v: "WAHR" if v is True else "FALSCH" if v is False else v)
    st.dataframe(display)

    st.success("✅ Neue Excel-Datei mit zusätzlicher Zeile 'Implementation in Scope' erstellt.")
    st.download_button(
        "💾 Excel herunterladen",
        data=buf.getvalue(),
        file_name=FILE_NAME,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
