import streamlit as st
import pandas as pd
import os

EXCEL_FILE = "attendance.xlsx"

st.set_page_config(page_title="لوحة تحكم الدكتور", page_icon="🧑‍🏫", layout="centered")

st.title("🧑‍🏫 لوحة تحكم الدكتور")
st.markdown("---")

# تحميل الملف
if os.path.exists(EXCEL_FILE):
    df = pd.read_excel(EXCEL_FILE)
else:
    st.warning("⚠️ لا يوجد ملف حضور حالياً.")
    df = pd.DataFrame(columns=["Name", "Date", "Time"])

# عرض البيانات
st.subheader("📋 قائمة الحضور:")
st.dataframe(df, use_container_width=True)

# إمكانية حذف سجل معين
if not df.empty:
    name_to_delete = st.selectbox("🗑️ اختر اسم لحذفه:", df["Name"].unique())
    if st.button("حذف الاسم"):
        df = df[df["Name"] != name_to_delete]
        df.to_excel(EXCEL_FILE, index=False)
        st.success(f"❌ تم حذف {name_to_delete} بنجاح.")

# زر تحميل الملف
if os.path.exists(EXCEL_FILE):
    with open(EXCEL_FILE, "rb") as file:
        st.download_button(
            label="⬇️ تحميل ملف Excel",
            data=file,
            file_name="attendance.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

st.markdown("---")
st.info("👈 يمكنك الرجوع لصفحة تسجيل الحضور من القائمة الجانبية.")
