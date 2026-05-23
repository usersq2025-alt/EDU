import streamlit as st
import plotly.express as px
import pandas as pd

# إعدادات الصفحة العامة
st.set_page_config(page_title="داشبورد مشروع التلعيب", layout="wide", initial_sidebar_state="expanded")

# العنوان الرئيسي (نصوص نظيفة بدون تشكيل)
st.title("📊 لوحة تحكم مشروع التلعيب فى التعليم")
st.markdown("### تحليل استبيانات الطلاب، اولياء الامور، والكادر التعليمى")
st.write("---")

# القائمة الجانبية للفلاتر
st.sidebar.header("فلاتر التصفية التفاعلية")
selected_grade = st.sidebar.multiselect(
    "تصفية حسب الصف الدراسى للطلاب:",
    options=["الاول الابتدائى", "الثالث الابتدائى", "الرابع الابتدائى", "الخامس الابتدائى"],
    default=["الاول الابتدائى", "الثالث الابتدائى", "الرابع الابتدائى", "الخامس الابتدائى"]
)

# تقسيم الشاشة إلى بطاقات أرقام رئيسية KPI
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="حماس الطلاب لتعلم المواد عبر الالعاب", value="87%")
with col2:
    st.metric(label="قبول اولياء الامور المبدئى للمنصة", value="71%")
with col3:
    st.metric(label="المعلمين المطالبين بانشطة جاهزة للمنهج", value="73%")

st.write("---")

# تصميم التبويبات للشاشات المختلفة
tab1, tab2, tab3 = st.tabs(["💡 الكادر التعليمى", "👨‍👩‍👦 اولياء الامور", "🎒 صوت الطالب"])

with tab1:
    st.subheader("تحليل بيانات الكادر التعليمى والتربوى")
    # بيانات تحديات المعلمين
    teacher_challenges = {
        "التحدى": ["تفاوت مستويات الطلاب", "تشتت الانتباه وضياع التركيز", "ضعف متابعة الاهلى"],
        "التكرار": [12, 8, 5]
    }
    df_teacher = pd.DataFrame(teacher_challenges)
    fig_teacher = px.bar(df_teacher, x="التكرار", y="التحدى", orientation='h', title="ابرز التحديات داخل الفصل")
    st.plotly_chart(fig_teacher, use_container_width=True)

with tab2:
    st.subheader("تحليل بيانات اولياء الامور")
    # بيانات ساعات الشاشة
    screen_time_data = {
        "عدد الساعات": ["اقل من ساعة", "من 1 الى 2 ساعة", "من 2 الى 4 ساعات واكثر"],
        "النسبة": [28, 50, 22]
    }
    df_screen = pd.DataFrame(screen_time_data)
    fig_screen = px.pie(df_screen, values="النسبة", names="عدد الساعات", title="ساعات قضاء الاطفال امام الشاشات يوميا")
    st.plotly_chart(fig_screen, use_container_width=True)

with tab3:
    st.subheader("تحليل تفضيلات وصعوبات الطلاب")
    # محفزات الطلاب داخل اللعبة
    student_motivators = {
        "العنصر الجاذب": ["المنافسة والتحدى مع الرفاق", "الجوائز والنقاط والكروت", "الغاز صعبة وتفكير", "شخصيات كرتونية واصوات"],
        "عدد الاصوات": [10, 9, 4, 3]
    }
    df_student = pd.DataFrame(student_motivators)
    fig_student = px.bar(df_student, x="العنصر الجاذب", y="عدد الاصوات", title="اكثر ما يحبه الطلاب فى الالعاب التعليمية")
    st.plotly_chart(fig_student, use_container_width=True)
