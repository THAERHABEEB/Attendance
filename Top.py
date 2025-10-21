import streamlit as st 

import pandas as pd

import os

from datetime import datetime

from PIL import Image

import io

import base64

import altair as alt

import streamlit.components.v1 as components

import imagehash

from fpdf import FPDF

import time

import cv2

import numpy as np

import webbrowser

import urllib.parse

# from flask import Flask, request, jsonify

# import threading

import openpyxl



# ================= Session =================

if "page" not in st.session_state:

    st.session_state.page = "home"

if "logged_in_student" not in st.session_state:

    st.session_state.logged_in_student = None

if "admin_logged_in" not in st.session_state:

        st.session_state.admin_logged_in = False



# ===================== تحميل كلمة المرور من ملف خارجي =====================

PASSWORD_FILE = "password.txt"

if not os.path.exists(PASSWORD_FILE):

    with open(PASSWORD_FILE, "w") as f:

        f.write("admin123")



with open(PASSWORD_FILE, "r") as f:

    PASSWORD = f.read().strip()



FACE_LOGIN_ENABLED = True

FACE_REF_PATH = "faces/teacher_ref.jpg"

WA_NUMBER = "01121412387"

PDF_REPORT_NAME = "attendance_report.pdf"





def show_toast(message, kind="info", duration=3000):

    color = {"info": "#00a8ff", "success": "#2ecc71", "error": "#ff6b6b"}.get(kind, "#00a8ff")

    html = f"""

    <div id="toast" style="

      position:fixed; right:20px; bottom:20px;

      background:{color}; color:white; padding:12px 18px; border-radius:10px;

      font-weight:700; box-shadow:0 6px 20px rgba(0,0,0,0.3); z-index:99999;">

      {message}

    </div>

    <script>

      setTimeout(()=>{{const t=document.getElementById('toast'); if(t) t.style.display='none';}}, {duration});

    </script>

    """

    components.html(html, height=80)





def is_same_face(uploaded_img, ref_path, threshold=6):

    try:

        ref = Image.open(ref_path).convert("RGB")

    except Exception as e:

        return False, f"ref-image-missing: {e}"

    up = Image.open(uploaded_img).convert("RGB")

    h1 = imagehash.phash(ref)

    h2 = imagehash.phash(up)

    dist = h1 - h2

    return (dist <= threshold), dist





def generate_pdf_summary(df, filename=PDF_REPORT_NAME):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", size=14)

    pdf.cell(200, 10, txt="Attendance Report", ln=True, align='C')

    pdf.ln(6)

    pdf.set_font("Arial", size=11)

    for idx, row in df.iterrows():

        line = f"{row['Date']} {row['Time']}  -  {row['Name']}"

        pdf.multi_cell(0, 8, txt=line)

    pdf.output(filename)

    return filename



# ========== تدريب نموذج التعرف على الوجوه ==========

students_folder = "students"

recognizer = None

students = []



# تحميل صور الطلاب وتدريب النموذج

images = []

labels = []

for i, f in enumerate(os.listdir(students_folder)):

    if f.lower().endswith((".jpg", ".jpeg", ".png")):

        name = os.path.splitext(f)[0]

        img_path = os.path.join(students_folder, f)

        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        if img is None:

            continue

        try:

            img_resized = cv2.resize(img, (200, 200))

            students.append(name)

            images.append(img_resized)

            labels.append(i)

        except:

            continue



if len(images) > 0:

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    recognizer.train(images, np.array(labels))







st.set_page_config(page_title="نظام الحضور بالوجه", page_icon="📸", layout="wide", initial_sidebar_state="expanded")





# ===================== تنسيق الواجهة =====================

# ===================== تنسيق واجهة احترافية متكاملة =====================

st.markdown("""

<style>

<div class="eye-container">

  <div class="eye">

    <div class="pupil"></div>

  </div>

</div>

/* ===== الخلفية العامة ===== */

body {

  background: radial-gradient(circle at top left, #0f2027, #203a43, #2c5364);

  color: #e9faff;

  font-family: "Cairo", sans-serif;

  overflow-x: hidden;

  animation: pageFade 1.2s ease-in-out;

}



/* تأثير دخول الصفحة */

@keyframes pageFade {

  from { opacity: 0; transform: translateY(10px); }

  to { opacity: 1; transform: translateY(0); }

}



.pulse-circle { width: 140px; height: 140px; border-radius: 50%; margin: 30px auto; background: radial-gradient(circle, #00e0ff, #007acc);

 box-shadow: 0 0 0 rgba(0, 224, 255, 0.4); animation: pulse 2s infinite; display: flex; align-items: center; justify-content: center;

 color: white; font-size: 20px; font-weight: bold;}

@keyframes pulse { 0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0,224,255,0.7);} 70% { transform: scale(1);

 box-shadow: 0 0 0 25px rgba(0,224,255,0);} 100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0,224,255,0);} }





/* ===== العناوين ===== */

h1, h2, h3 {

  text-align: center;

  color: #00e0ff;

  text-shadow: 0 0 25px rgba(0,224,255,0.8);

  letter-spacing: 1px;

  animation: fadeSlide 1.5s ease-in-out;

}

@keyframes fadeSlide {

  from { opacity: 0; transform: translateY(-10px); }

  to { opacity: 1; transform: translateY(0); }

}



/* ===== الأزرار ===== */

.stButton>button {

  background: linear-gradient(135deg, rgba(0,224,255,0.15), rgba(0,100,200,0.25));

  border: 1px solid linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);

  border-radius: 14px;

  color: #00e5ff;

  font-weight: 600;

  letter-spacing: 0.5px;

  padding: 0.7em 1.4em;

  transition: all 0.3s ease-in-out;

  box-shadow: 0 0 12px rgba(0,224,255,0.2);

  position: relative;

  overflow: hidden;

}

.stButton>button::before {

  content: "";

  position: absolute;

  top: 0; left: -100%;

  width: 100%; height: 100%;

  background: linear-gradient(120deg, transparent, rgba(0,224,255,0.3), transparent);

  transition: 0.6s;

}

.stButton>button:hover::before {

  left: 100%;

}

.stButton>button:hover {

  background: linear-gradient(135deg, #00e0ff, #0072ff);

  color: white;

  transform: scale(1.07);

  box-shadow: 0 0 30px linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);

}



/* ===== مدخلات النصوص ===== */

.stTextInput>div>div>input {

  background: rgba(255, 255, 255, 0.07);

  border: 1px solid rgba(0,224,255,0.3);

  border-radius: 12px;

  color: #e0f7ff !important;

  padding: 0.8em 1em;

  font-size: 16px;

  transition: all 0.3s ease-in-out;

  box-shadow: inset 0 0 10px rgba(0,224,255,0.1);

}

.stTextInput>div>div>input:focus {

  border-color: #00e5ff;

  box-shadow: 0 0 18px rgba(0,224,255,0.5);

  transform: scale(1.02);

}



/* ===== القوائم المنسدلة (Selectbox) ===== */

.stSelectbox>div>div>div {

  background: rgba(255, 255, 255, 0.07);

  border: 1px solid rgba(0,224,255,0.3);

  border-radius: 12px;

  color: #e0f7ff !important;

  font-size: 15px;

  transition: 0.3s;

}

.stSelectbox>div>div>div:hover {

  box-shadow: 0 0 15px rgba(0,224,255,0.4);

}



/* ===== الجداول ===== */

thead tr th {

  background: rgba(0, 224, 255, 0.15);

  color: #00e5ff;

  text-shadow: 0 0 5px rgba(0,224,255,0.6);

  font-weight: bold;

}

tbody tr:hover {

  background-color: rgba(0, 224, 255, 0.07);

  transition: 0.2s;

}



/* ===== البطاقات والاحصائيات ===== */

div[data-testid="stMetricValue"] {

  color: #00e5ff;

  font-weight: bold;

  text-shadow: 0 0 10px rgba(0,224,255,0.7);

}



/* ===== Sidebar ===== */

[data-testid="stSidebar"] {

  background: rgba(20, 30, 48, 0.88);

  backdrop-filter: blur(12px);

  border-right: 2px solid rgba(0, 224, 255, 0.2);

}

[data-testid="stSidebar"] h2 {

  text-align: center;

  color: #00e5ff;

  font-size: 22px;

  font-weight: bold;

  text-shadow: 0 0 15px #00e5ff;

  animation: glowText 2s ease-in-out infinite alternate;

}

@keyframes glowText {

  from { text-shadow: 0 0 10px #00e5ff; }

  to { text-shadow: 0 0 30px #00e5ff; }

}



/* ===== شريط تمرير مخصص ===== */

::-webkit-scrollbar { width: 8px; }

::-webkit-scrollbar-thumb {

  background: linear-gradient(#00e5ff, #0072ff);

  border-radius: 10px;

}

::-webkit-scrollbar-thumb:hover {

  background: #00b8d4;

}



/* ===== إشعاع حول الصفحة ===== */

html::before {

  content: "";

  position: fixed;

  inset: 0;

  background: radial-gradient(circle at 30% 20%, rgba(0,224,255,0.08), transparent 60%);

  pointer-events: none;

  z-index: -1;

}

.eye-container {

  position: fixed;

  top: 30px;

  right: 60px;

  width: 90px;

  height: 90px;

  display: flex;

  justify-content: center;

  align-items: center;

  z-index: 9999;

  animation: floatEye 4s ease-in-out infinite alternate;

}



@keyframes floatEye {

  from { transform: translateY(0px); }

  to { transform: translateY(10px); }

}



.eye {

  width: 70px;

  height: 70px;

  background: radial-gradient(circle at 30% 30%, #00e5ff, #003d66);

  border-radius: 50%;

  position: relative;

  box-shadow: 0 0 25px rgba(0,224,255,0.6), inset 0 0 20px rgba(0,224,255,0.5);

  display: flex;

  justify-content: center;

  align-items: center;

}



.pupil {

  width: 24px;

  height: 24px;

  background: #0ff;

  border-radius: 50%;

  box-shadow: 0 0 15px #00e5ff;

  position: absolute;

  transition: transform 0.1s ease-out;

}



</style>

<script>

document.addEventListener('mousemove', function(e) {

  const eye = document.querySelector('.eye');

  const pupil = document.querySelector('.pupil');

  if (!eye || !pupil) return;



  const rect = eye.getBoundingClientRect();

  const eyeX = rect.left + rect.width / 2;

  const eyeY = rect.top + rect.height / 2;



  const dx = e.clientX - eyeX;

  const dy = e.clientY - eyeY;

  const angle = Math.atan2(dy, dx);

  const distance = Math.min(12, Math.hypot(dx, dy) / 10);



  const moveX = Math.cos(angle) * distance;

  const moveY = Math.sin(angle) * distance;



  pupil.style.transform = `translate(${moveX}px, ${moveY}px)`;

});

</script>

""", unsafe_allow_html=True)









# ===================== الملفات =====================

EXCEL_FILE = "attendance.xlsx"

if not os.path.exists(EXCEL_FILE):

    df = pd.DataFrame(columns=["Name", "Subject", "Date", "Time", "Phone", "Attendance_Count", "Absence_Count","Attendance_Percent", "Department"])

    df.to_excel(EXCEL_FILE, index=False)

else:

    df = pd.read_excel(EXCEL_FILE)

    needed_cols = ["Name", "Subject", "Date", "Time", "Phone", "Attendance_Count", "Absence_Count","Attendance_Percent", "Department"]

    for col in needed_cols:

        if col not in df.columns:

            df[col] = 0 

# ===================== القوائم =====================

st.sidebar.title("📋 نظام الحضور الذكي")

page = st.sidebar.radio("📂 اختر الصفحة", ["🧑‍🎓 صفحة الطالب", "🧑‍🏫 لوحة الدكتور", "⚙️ الإعدادات", "📞 تواصل معنا"])



# ===================== صفحة الطالب =====================

if page == "🧑‍🎓 صفحة الطالب":

    st.markdown("<div class='pulse-circle'>SCAN</div>", unsafe_allow_html=True)

    st.title("🎓 نظام تسجيل الحضور بالوجه")

    st.markdown("---")



    subject = st.selectbox("📚 اختر المادة:", ["اساسيات علوم البيانات","هندسة وتحليل البيانات","تطوير تطبيقات الانترنت"])

    department = st.selectbox("🏫 اختر القسم:",["Data Science","Artificial Intelligence","Cyber Security"])

    name = st.text_input("👤 الاسم الكامل:")

    phone = st.text_input("📞 رقم الهاتف (إجباري):")

    camera_input = st.camera_input("📸 التقط صورة (أو ارفعها من الأسفل):")

    uploaded_file = st.file_uploader("أو ارفع صورة (jpg/png)", type=["jpg", "jpeg", "png"])

    img_file = camera_input if camera_input else uploaded_file

    



    if st.button("✅ تسجيل الحضور"):

        if not name or not phone or not subject:

            st.warning("⚠️ أدخل الاسم، ورقم الهاتف، واسم المادة أولاً.")

    elif camera_input is None:

        st.warning("📸 التقط صورة قبل التسجيل.")

    else:

        img_path = f"students/{name}_{subject}.jpg"

        with open(img_path, "wb") as f:

            f.write(camera_input.getbuffer())



        now = datetime.now()

        new_row = pd.DataFrame([{

            "Name": name,

            "Subject": subject,

            "Date": now.strftime("%Y-%m-%d"),

            "Time": now.strftime("%H:%M:%S"),

            "Phone":phone,

            "Department":department

            }], columns=["Name", "Subject", "Date", "Time","Phone","Department"])

        df = pd.concat([df, new_row], ignore_index=True)

        df.to_excel(EXCEL_FILE, index=False, engine="openpyxl")

        

        # تحديث الإحصائيات للطالب

        student_data = df[df["Name"] == name]

        subject_data = student_data[student_data["Subject"] == subject]

        attended = len(subject_data)

        total_days = len(df[df["Subject"] == subject]["Date"].unique())

        absences = max(total_days - attended, 0)

        percent = (attended / total_days * 100) if total_days > 0 else 0

        

        

        # df.loc[df["Name"] == name, "Attendance_Count"] = attended

        df.loc[df["Name"] == name, "Absence_Count"] = absences

        df.loc[df["Name"] == name, "Department"] = department

        df.loc[df["Name"] == name, "Attendance_Count"] = df.get("Attendance_Count", 0) + 1

        df.to_excel(EXCEL_FILE, index=False)

        

        

        st.info(f"📘 المادة: {subject} | ✅ حضور: {attended} | ❌ غياب: {absences} ")

        st.success(f"✅ تم تسجيل {name} في مادة {subject} بنجاح.")

        st.image(img_path, caption=f"📸 {name} - {subject}", width=250)

        st.markdown("---")



        personal_df = df[(df["Name"] == name) & (df["Subject"] == subject)][["Name", "Subject", "Date", "Time"]]

        st.markdown(f"### 🕒 سجل حضورك في مادة **{subject}**:")

        st.dataframe(personal_df, use_container_width=True)

            

            

            # تحليل ذكي للمادة

        if not personal_df.empty:

            st.markdown("### 📊 تحليلك الذكي:")



            total_days = df[df["Subject"] == subject]["Date"].nunique()

            student_days = personal_df["Date"].nunique()

            attendance_percent = (student_days / total_days * 100) if total_days > 0 else 0



            last_date = personal_df["Date"].iloc[-1]



            c1, c2, c3 = st.columns(3)

            c1.metric("📅 آخر حضور", str(last_date))

            c2.metric("🔢 عدد مرات الحضور", len(personal_df))

            c3.metric("📈 نسبة الحضور", f"{attendance_percent:.1f}%")



            # رسم بياني للحضور عبر الأيام

            chart_data = personal_df.groupby("Date").size().reset_index(name="Count")

            chart = alt.Chart(chart_data).mark_line(point=True).encode(

                x=alt.X("Date:T", title="التاريخ"),

                y=alt.Y("Count:Q", title="عدد مرات الحضور"),

                tooltip=["Date", "Count"]

            ).properties(width=700, height=300, title=f"📅 تطور حضورك في {subject}")

            st.altair_chart(chart, use_container_width=True)

# ===================== لوحة الدكتور =====================

elif page == "🧑‍🏫 لوحة الدكتور":

    st.title("🧑‍🏫 لوحة تحكم الدكتور")

    st.markdown("---")

    

    subject_filter  = st.selectbox("📘 أدخل اسم المادة لعرض بياناتها:", ["اساسيات علوم البيانات","هندسة وتحليل البيانات","تطوير تطبيقات الانترنت"])



    # 🔹 كلمة مرور الدكتور

    if not st.session_state.admin_logged_in:

        password = st.text_input("🔑 أدخل كلمة مرور الدكتور:", type="password")

        if st.button("تسجيل الدخول"):

            if password == PASSWORD:

                st.session_state.admin_logged_in = True

                st.success("✅ تم تسجيل الدخول بنجاح")

                st.rerun()

            else:

                st.error("❌ كلمة المرور غير صحيحة.")

    



    else:

        df = pd.read_excel(EXCEL_FILE)



        # ✅ فلترة المادة

        if subject_filter:

            df = df[df["Subject"].str.contains(subject_filter, case=False, na=False)]

            st.markdown(f"### 📊 بيانات الحضور لمادة **{subject_filter}** فقط")

        else:

            st.warning("⚠️ أدخل اسم المادة أولًا لعرض بياناتها.")

            st.stop()



        # ✅ حساب عدد مرات الحضور لكل طالب في المادة

        summary = df.groupby(["Name"]).size().reset_index(name="عدد مرات الحضور")

        st.dataframe(summary, use_container_width=True)

        today = datetime.now().strftime("%Y-%m-%d")

        today_count = len(df[df["Date"] == today])

        # 🔹 تحليل المادة ككل

        

        total_students = df["Name"].nunique()

        total_records = len(df)

        last_day = df["Date"].iloc[-1] if not df.empty else "—"

        manual_total = st.number_input("✏️ أدخل إجمالي عدد الطلاب:", min_value=0, value=len(df))

        total = manual_total

        percent = (total_students / total * 100) if total else 0.0



        st.markdown("### 📈 تحليل عام للمادة:")

        

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("👥 عدد الطلاب", total_students)

        c2.metric("إجمالي الطلاب (يدوياً)", total)

        c3.metric("نسبة اليوم", f"{percent:.1f}%")

        c4.metric("📆 آخر يوم تسجيل", last_day)





        # 🔹 رسم بياني للحضور في المادة

        if not df.empty:

            chart_data = df.groupby("Date").size().reset_index(name="عدد الحضور")

            chart = alt.Chart(chart_data).mark_line(point=True).encode(

                x=alt.X("Date:T", title="التاريخ"),

                y=alt.Y("عدد الطلاب  :Q", title="عدد الحضور"),

                tooltip=["Date", "عدد الحضور"]

            ).properties(width=700, height=300, title=f"📅 تطور الحضور في {subject_filter}")

            st.altair_chart(chart, use_container_width=True)



        print(df.columns)

        st.markdown("---")

        st.subheader("🧾 بيانات الحضور")

        st.dataframe(df, use_container_width=True)

        

        # ===================== 📊 مقارنة الحضور بين المواد =====================

        st.markdown("### 📚 مقارنة الحضور بين المواد")



        # قراءة جميع البيانات لتجميع إحصائيات لكل مادة

        df_all = pd.read_excel(EXCEL_FILE)



        if not df_all.empty:

            compare_data = df_all.groupby("Subject")["Attendance_Count"].sum().reset_index()

            compare_chart = alt.Chart(compare_data).mark_line(point=True).encode(

                x=alt.X("Subject:N", title="المادة"),

                y=alt.Y("Attendance_Count:Q", title="إجمالي عدد مرات الحضور"),

                tooltip=["Subject", "Attendance_Count"]

            ).properties(

                width=700,

                height=300,

                title="📊 مقارنة حضور المواد"

            )

            st.altair_chart(compare_chart, use_container_width=True)

        else:

            st.info("لا توجد بيانات كافية بعد لعرض المقارنة بين المواد.")



        

        # 🔍 بحث

        st.markdown("### 🔍 البحث عن طالب")

        search = st.text_input("اكتب الاسم:")

        if search:

            results = df[df["Name"].str.contains(search, case=False, na=False)]

            if not results.empty:

                st.dataframe(results)

            else:

                st.warning("❌ لم يتم العثور عليه.")



        # 🗑️ حذف طالب

        st.markdown("### 🗑️ حذف طالب")

        delete_name = st.text_input("اكتب الاسم لحذفه:")

        if st.button("🗑️ حذف"):

            if delete_name in df["Name"].values:

                df = df[df["Name"] != delete_name]

                df.to_excel(EXCEL_FILE, index=False)

                st.success(f"✅ تم حذف {delete_name}")

            else:

                st.error("⚠️ الاسم غير موجود.")

                

        st.markdown("---")

        st.markdown("### ⬇️ تصدير / تقرير")

        if st.button("تصدير Excel"):

            with open(EXCEL_FILE, "rb") as f:

                st.download_button("تحميل Excel", data=f, file_name="attendance.xlsx",

                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")



        if st.button("تصدير PDF تقرير سريع"):

            if not df.empty:

                pdf_file = generate_pdf_summary(df)

                with open(pdf_file, "rb") as pf:

                    st.download_b





      



















