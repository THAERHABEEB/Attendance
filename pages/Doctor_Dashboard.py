import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# ===================== ⚙️ إعداد الصفحة =====================
st.set_page_config(page_title="لوحة تحكم الدكتور", page_icon="🧑‍🏫", layout="wide")

EXCEL_FILE = "attendance.xlsx"
PASSWORD = "12345"  # 🔐 كلمة السر (يمكنك تغييرها)

# ===================== 🔒 نظام تسجيل الدخول =====================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 تسجيل الدخول للدكتور")
    password_input = st.text_input("أدخل كلمة المرور:", type="password")

    if st.button("تسجيل الدخول"):
        if password_input == PASSWORD:
            st.session_state.logged_in = True
            st.success("✅ تم تسجيل الدخول بنجاح.")
            st.experimental_rerun()
        else:
            st.error("❌ كلمة المرور غير صحيحة.")
    st.stop()

# ===================== 🎯 بعد تسجيل الدخول =====================
st.title("🧑‍🏫 لوحة تحكم الدكتور")
st.markdown("---")

# زر لتسجيل الخروج
if st.button("🚪 تسجيل الخروج"):
    st.session_state.logged_in = False
    st.success("👋 تم تسجيل الخروج بنجاح.")
    st.stop()

# ===================== 📂 تحميل بيانات الحضور =====================
if os.path.exists(EXCEL_FILE):
    df = pd.read_excel(EXCEL_FILE)
else:
    st.warning("⚠️ لا يوجد ملف حضور بعد.")
    df = pd.DataFrame(columns=["Name", "Date", "Time"])

# ===================== 📊 الإحصائيات =====================
col1, col2, col3 = st.columns(3)

with col1:
    total_students = df["Name"].nunique() if not df.empty else 0
    st.metric("👨‍🎓 عدد الطلاب المسجلين", total_students)

with col2:
    today = pd.Timestamp.now().strftime("%Y-%m-%d")
    today_count = len(df[df["Date"] == today])
    st.metric("📅 عدد حضور اليوم", today_count)

with col3:
    total_records = len(df)
    st.metric("🧾 عدد السجلات الكلي", total_records)

st.markdown("---")

# ===================== 🔍 البحث =====================
search_name = st.text_input("🔍 ابحث عن طالب بالاسم:")
filtered_df = df.copy()

if search_name:
    filtered_df = df[df["Name"].str.contains(search_name, case=False, na=False)]

# ===================== 📋 عرض الجدول =====================
st.subheader("📋 قائمة الحضور:")
st.dataframe(filtered_df, use_container_width=True)

# ===================== 🗑️ حذف طالب =====================
if not df.empty:
    name_to_delete = st.selectbox("🗑️ اختر اسم لحذفه:", df["Name"].unique())
    if st.button("حذف الاسم"):
        df = df[df["Name"] != name_to_delete]
        df.to_excel(EXCEL_FILE, index=False)
        st.success(f"❌ تم حذف {name_to_delete} بنجاح.")
        st.rerun()

# ===================== 📈 الرسم البياني =====================
if not df.empty:
    st.markdown("---")
    st.subheader("📊 إحصائيات الحضور حسب الأيام")

    # حساب عدد الحضور لكل يوم
    daily_counts = df["Date"].value_counts().sort_index()

    fig, ax = plt.subplots()
    ax.plot(daily_counts.index, daily_counts.values, marker='o')
    ax.set_xlabel("📅 التاريخ")
    ax.set_ylabel("👨‍🎓 عدد الحضور")
    ax.set_title("📈 توزيع الحضور اليومي")
    plt.xticks(rotation=45)

    st.pyplot(fig)

# ===================== 💾 تحميل ملف Excel =====================
st.markdown("---")
if os.path.exists(EXCEL_FILE):
    with open(EXCEL_FILE, "rb") as file:
        st.download_button(
            label="⬇️ تحميل ملف Excel",
            data=file,
            file_name="attendance.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

st.info("👈 يمكنك الرجوع لصفحة تسجيل الحضور من القائمة الجانبية.")
