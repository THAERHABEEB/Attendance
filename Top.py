import streamlit as st

import pandas as pd

import os

from datetime import datetime



# إعداد الصفحة

st.set_page_config(page_title="نظام الحضور بالوجه", page_icon="📸", layout="centered")



# ===================== 🎨 تنسيق CSS + أنيميشن =====================

st.markdown("""



<style>

body {

  background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);

  color: white;

  font-family: "Cairo", sans-serif;

  position:flex;

}



h1 {

  text-align: center;

  color: #00e0ff;

  font-size: 2.5rem;

  animation: glow 2s infinite alternate;

}



@keyframes glow {

  from { text-shadow: 0 0 10px #00e0ff, 0 0 20px #00e0ff; }

  to { text-shadow: 0 0 30px #00e0ff, 0 0 40px #00e0ff; }

}

.HITU{

  position:relative;

  color:#795548;

  bottom:20px;

  

}



button {

  border-radius: 10px !important;

  transition: transform 0.3s ease, box-shadow 0.3s ease !important;

}



button:hover {

  transform: scale(1.05);

  box-shadow: 0 0 15px #00e0ff !important;

}



.pulse-animation {

  width: 130px;

  height: 130px;

  border-radius: 50%;

  margin: auto;

  border: 5px solid #00e0ff;

  animation: pulse 2s infinite;

}



@keyframes pulse {

  0% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(0,224,255, 0.7); }

  70% { transform: scale(1); box-shadow: 0 0 0 20px rgba(0,224,255, 0); }

  100% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(0,224,255, 0); }

}


/* تعديل عرض الأعمدة */
@media (max-width: 600px) {
  .stButton button, .stTextInput, .stCameraInput {
    width: 100% !important;
  }
  .stDataFrame {
    font-size: 0.8rem;
  }
}

@media (min-width: 601px) and (max-width: 1024px) {
  .main-container {
    max-width: 600px;
  }
}

@media (min-width: 1025px) and (max-width: 1600px) {
  .main-container {
    max-width: 800px;
  }
}

@media (min-width: 1601px) {
  .main-container {
    max-width: 1000px;
  }
}

</style>

<h1>Data Science</h1>

""", unsafe_allow_html=True)



# ===================== ⚙️ الإعداد =====================

EXCEL_FILE = r"C:\Users\h p\OneDrive\Desktop\DR.SHEEREF\attendance.xlsx"



if not os.path.exists(EXCEL_FILE):

    df = pd.DataFrame(columns=["Name", "Date", "Time"])

    df.to_excel(EXCEL_FILE, index=False)

else:

    df = pd.read_excel(EXCEL_FILE)



if not os.path.exists("students"):

    os.makedirs("students")



# ===================== 🧠 واجهة المستخدم =====================

st.markdown("<div class='pulse-animation'></div>", unsafe_allow_html=True)

st.title("🎓 نظام تسجيل الحضور الذكي")

st.markdown("---")



name = st.text_input("👤 أدخل اسم الطالب:")

camera_input = st.camera_input("📸 التقط صورة الطالب:")



if st.button("✅ تسجيل الحضور"):

    if not name:

        st.warning("⚠️ من فضلك أدخل اسم الطالب أولاً.")

    elif camera_input is None:

        st.warning("📸 التقط صورة قبل التسجيل.")

    elif name in df["Name"].values:

        st.info(f"🟢 الاسم '{name}' موجود بالفعل في القائمة.")

    else:

        # حفظ الصورة

        img_path = f"students/{name}.jpg"

        with open(img_path, "wb") as f:

            f.write(camera_input.getbuffer())



        # حفظ البيانات في Excel

        now = datetime.now()

        new_row = pd.DataFrame([[name, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")]],

                               columns=["Name", "Date", "Time"])

        df = pd.concat([df, new_row], ignore_index=True)

        df.to_excel(EXCEL_FILE, index=False)



        st.success(f"✅ تم تسجيل {name} بنجاح.")

        st.image(img_path, caption=f"📸 صورة {name}", width=250)



# ===================== 📊 عرض جدول الحضور =====================

st.markdown("---")

st.subheader("📋 قائمة الحضور:")

st.dataframe(df)



# ===================== 💾 تحميل الملف ثم حذفه =====================

with open(EXCEL_FILE, "rb") as file:

    btn = st.download_button(

        label="⬇️ تحميل ملف الحضور Excel",

        data=file,

        file_name="attendance.xlsx",

        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )



# حذف الملف بعد التحميل

if btn:

    try:

        os.remove(EXCEL_FILE)

        st.warning("🗑️ تم حذف ملف Excel من السيرفر بعد التحميل.")

        # إنشاء ملف جديد فاضي بعد الحذف

        

    except Exception as e:

        st.error(f"حدث خطأ أثناء الحذف: {e}")
      
















