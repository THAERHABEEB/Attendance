import streamlit as st
import pandas as pd
import os
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="نظام الحضور بالوجه", page_icon="📸", layout="wide")

# ===================== 🎨 تنسيق CSS متجاوب =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');

html, body {
  background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
  color: white;
  font-family: "Cairo", sans-serif;
  margin: 0;
  padding: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

h1 {
  color: #00e0ff;
  font-size: clamp(1.8rem, 4vw, 3rem);
  text-align: center;
  animation: glow 2s infinite alternate;
  margin-top: 20px;
}

@keyframes glow {
  from { text-shadow: 0 0 10px #00e0ff, 0 0 20px #00e0ff; }
  to { text-shadow: 0 0 30px #00e0ff, 0 0 40px #00e0ff; }
}

.pulse-animation {
  width: clamp(80px, 15vw, 150px);
  height: clamp(80px, 15vw, 150px);
  border-radius: 50%;
  margin: 20px auto;
  border: 5px solid #00e0ff;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(0,224,255, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 20px rgba(0,224,255, 0); }
  100% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(0,224,255, 0); }
}

/* تحسين شكل الأزرار */
button[kind="primary"] {
  border-radius: 10px !important;
  transition: all 0.3s ease-in-out !important;
}

button[kind="primary"]:hover {
  transform: scale(1.05);
  box-shadow: 0 0 15px #00e0ff !important;
}

/* حاوية المحتوى */
.main-container {
  max-width: 800px;
  width: 90%;
  background: rgba(255, 255, 255, 0.05);
  padding: 25px;
  border-radius: 20px;
  box-shadow: 0 0 20px rgba(0,224,255, 0.3);
  margin: 20px auto;
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
""", unsafe_allow_html=True)

# ===================== ⚙️ الإعداد =====================
EXCEL_FILE = "attendance.xlsx"

if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["Name", "Date", "Time"])
    df.to_excel(EXCEL_FILE, index=False)
else:
    df = pd.read_excel(EXCEL_FILE)

if not os.path.exists("students"):
    os.makedirs("students")

# ===================== 🧠 واجهة المستخدم =====================
st.markdown("<div class='pulse-animation'></div>", unsafe_allow_html=True)
st.title("🎓 نظام تسجيل الحضور الذكي بالوجه")
st.markdown("---")

st.markdown("<div class='main-container'>", unsafe_allow_html=True)

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

st.markdown("</div>", unsafe_allow_html=True)

# ===================== 📊 عرض جدول الحضور =====================
st.markdown("---")
st.subheader("📋 قائمة الحضور:")
st.dataframe(df, use_container_width=True)

# ===================== 💾 تحميل الملف ثم حذفه =====================
with open(EXCEL_FILE, "rb") as file:
    btn = st.download_button(
        label="⬇️ تحميل ملف الحضور Excel",
        data=file,
        file_name="attendance.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if btn:
    try:
        os.remove(EXCEL_FILE)
        st.warning("🗑️ تم حذف ملف Excel من السيرفر بعد التحميل.")
        pd.DataFrame(columns=["Name", "Date", "Time"]).to_excel(EXCEL_FILE, index=False)
    except Exception as e:
        st.error(f"حدث خطأ أثناء الحذف: {e}")
      















