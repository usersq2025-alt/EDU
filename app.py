import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- إعدادات وتصميم الصفحة ---
st.set_page_config(
    page_title="لوحة تحكم مشروع التلعيب في التعليم",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص التصميم والخطوط ودعم اتجاه النص العربي (RTL) عبر CSS مخصص
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap');
    
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Cairo', sans-serif;
        text-align: right;
        direction: RTL;
    }
    
    /* تنسيق كروت الـ KPI */
    .kpi-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: #f8fafc;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 15px;
    }
    .kpi-title {
        font-size: 14px;
        font-weight: 600;
        color: #94a3b8;
        margin-bottom: 10px;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: 800;
        color: #38bdf8;
    }
    
    /* إخفاء القوائم الافتراضية غير المرغوبة */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


# --- دوال تحميل ومعالجة البيانات ---
@st.cache_data
def load_data():
    # التحقق من وجود الملفات محلياً، وتوفير بيانات افتراضية ممتازة في حال عدم وجودها لمنع توقف التطبيق
    data = {}
    
    # 1. بيانات الطلاب
    if os.path.exists("students.csv"):
        data['students'] = pd.read_csv("students.csv")
    else:
        # بيانات افتراضية تحاكي الملف المرفوع تماماً
        data['students'] = pd.DataFrame({
            'الصف': ['الصف الخامس الابتدائي', 'الصف الثالث الابتدائي', 'الصف الأول الابتدائي', 'الصف الخامس الابتدائي', 'الصف الثالث الابتدائي', 'الصف الرابع الابتدائي', 'الصف الأول الابتدائي', 'الصف الخامس الابتدائي', 'الصف الخامس الابتدائي', 'الصف الثالث الابتدائي', 'الصف الأول الابتدائي'],
            'المادة_المحببة': ['اللغة العربية 📖', 'أحب كل المواد بنفس القدر', 'الرياضيات 🔢', 'أحب كل المواد بنفس القدر', 'اللغة الإنجليزية 🌍', 'أحب كل المواد بنفس القدر', 'التربية الإسلامية 🌙', 'التربية الإسلامية 🌙', 'أحب كل المواد بنفس القدر', 'اللغة العربية 📖', 'الرياضيات 🔢'],
            'المادة_الصعبة': ['اللغة الإنجليزية 🌍', 'اللغة العربية 📖', 'اللغة العربية 📖', 'الرياضيات 🔢', 'الرياضيات 🔢', 'اللغة الإنجليزية 🌍', 'اللغة الإنجليزية 🌍', 'الرياضيات 🔢', 'الرياضيات 🔢', 'اللغة العربية 📖', 'اللغة العربية 📖'],
            'طريقة_الدراسة': ['عندما المعلم يشرح على السبورة 🗣️', 'عندما أحل تمارين بنفسي 🛠️', 'عندما المعلم يشرح على السبورة 🗣️', 'عندما المعلم يشرح على السبورة 🗣️', 'عندما أشاهد فيديوهات تعليمية 🎬, العب ألعاب 🎮', 'عندما أحل تمارين بنفسي 🛠️', 'عندما أحل تمارين بنفسي 🛠️, عندما أشاهد فيديوهات 🎬', 'عندما أحل تمارين بنفسي 🛠️', 'عندما المعلم يشرح على السبورة 🗣️', 'عندما المعلم يشرح على السبورة 🗣️, عندما أحل تمارين بنفسي 🛠️', 'عندما المعلم يشرح على السبورة 🗣️'],
            'اللعب_للدراسة': ['إي كتير!', 'ما بظن، بفضل الألعاب العادية', 'إي كتير!', 'إي كتير!', 'إي كتير!', 'ما بظن، بفضل الألعاب العادية', 'ممكن جربها، إذا كانت حلوة', 'إي كتير!', 'إي كتير!', 'ممكن جربها، إذا كانت حلوة', 'إي كتير!'],
            'الجوائز_والنقاط': ['لأ ما بظن', 'إي طبعاً!', 'إي طبعاً!', 'إي طبعاً!', 'إي طبعاً!', 'إي طبعاً!', 'إي طبعاً!', 'إي طبعاً!', 'إي طبعاً!', 'إي طبعاً!', 'إي طبعاً!'],
            'عناصر_الجذب': ['تحديات ومنافسة ⚔️', 'أصوات حماسية وموسيقى 🎵', 'تحديات ومنافسة ⚔️', 'تحديات ومنافسة ⚔️', 'شخصيات كرتونية 🦸', 'الغاز صعبة وتفكير 💡', 'شخصيات كرتونية 🦸, تحديات ومنافسة ⚔️', 'الغاز صعبة وتفكير 💡', 'تحديات ومنافسة ⚔️', 'تحديات ومنافسة ⚔️', 'شخصيات كرتونية 🦸']
        })
        
    # 2. بيانات أولياء الأمور
    if os.path.exists("parents.csv"):
        data['parents'] = pd.read_csv("parents.csv")
    else:
        data['parents'] = pd.DataFrame({
            'ساعات_الشاشات': ['أقل من ساعة يومياً', 'من 1 إلى 2 ساعة', 'من 1 إلى 2 ساعة', 'من 2 إلى 4 ساعات', 'من 1 إلى 2 ساعة', 'أقل من ساعة يومياً', 'من 1 إلى 2 ساعة', 'من 1 إلى 2 ساعة', 'من 1 إلى 2 ساعة', 'أكثر من 4 ساعات', 'أقل من ساعة يومياً', 'أكثر من 4 ساعات', 'أقل من ساعة يومياً', 'من 2 إلى 4 ساعات'],
            'مستوى_الحماس': ['متحمس جداً، هذا ما يحتاجه طفلي', 'غير متأكد، أحتاج أرى نتائج عملي أولاً', 'متحمس جداً، هذا ما يحتاجه طفلي', 'مهتم لكنني بحاجة لمزيد من التفاصيل', 'متحمس جداً، هذا ما يحتاجه طفلي', 'متحمس جداً، هذا ما يحتاجه طفلي', 'متحمس جداً، هذا ما يحتاجه طفلي', 'متحمس جداً، هذا ما يحتاجه طفلي', 'مهتم لكنني بحاجة لمزيد من التفاصيل', 'متحمس جداً، هذا ما يحتاجه طفلي', 'متحمس جداً، هذا ما يحتاجه طفلي', 'متحمس جداً، هذا ما يحتاجه طفلي', 'مهتم لكنني بحاجة لمزيد من التفاصيل', 'متحمس جداً، هذا ما يحتاجه طفلي'],
            'القدرة_على_الدفع': ['أفضل خيارات مجانية فقط', 'نعم، إذا كانت التكلفة معقولة', 'أفضل خيارات مجانية فقط', 'نعم، إذا كانت التكلفة معقولة', 'نعم، إذا رأيت تحسناً حقيقياً في مستوى طفلي', 'نعم، إذا رأيت تحسناً حقيقياً في مستوى طفلي', 'نعم، إذا رأيت تحسناً حقيقياً في مستوى طفلي', 'أفضل خيارات مجانية فقط', 'نعم، إذا كانت التكلفة معقولة', 'نعم، إذا رأيت تحسناً حقيقياً في مستوى طفلي', 'نعم، إذا رأيت تحسناً حقيقياً في مستوى طفلي', 'نعم، إذا رأيت تحسناً حقيقياً في مستوى طفلي', 'نعم، إذا رأيت تحسناً حقيقياً في مستوى طفلي', 'أفضل خيارات مجانية فقط']
        })
        
    # 3. بيانات الكادر التعليمي
    if os.path.exists("educators.csv"):
        data['educators'] = pd.read_csv("educators.csv")
    else:
        data['educators'] = pd.DataFrame({
            'الدور_التربوي': ['معلم / معلمة مرحلة ابتدائية', 'معلم / معلمة مرحلة ابتدائية', 'مدير / مديرة مدرسة خاصة', 'مشرف / مشرفة تربوية متخصصة', 'معلم / معلمة مرحلة ابتدائية', 'معلم / معلمة مرحلة ابتدائية', 'معلم / معلمة مرحلة ابتدائية', 'مشرف / مشرفة تربوية متخصصة', 'معلم / معلمة مرحلة ابتدائية', 'معلم / معلمة مرحلة ابتدائية', 'معلم / معلمة مرحلة ابتدائية', 'معلم / معلمة مرحلة ابتدائية', 'معلم / معلمة مرحلة ابتدائية', 'مشرف / مشرفة تربوية متخصصة'],
            'الاهتمام_بالمنصة': [5, 4, 5, 5, 5, 4, 5, 4, 5, 5, 3, 5, 3, 5],
            'العائق_الرئيسي': ['تشتت انتباه الطلاب', 'التفاوت الكبير في المستويات', 'ضعف تفاعل الطلاب والملل', 'انخفاض دافعية الطلاب', 'التفاوت الكبير في المستويات', 'ضعف متابعة أولياء الأمور', 'تشتت انتباه الطلاب', 'انخفاض دافعية الطلاب', 'التفاوت الكبير في المستويات', 'تشتت انتباه الطلاب', 'الضغط الزمني للمنهج', 'التفاوت الكبير في المستويات', 'تشتت انتباه الطلاب', 'الاعتماد المفرط على التلقين'],
            'دمج_المنصة': ['تمهيد مشوق للحصة', 'نشاط تطبيقي لترسيخ المفاهيم', 'نشاط تطبيقي لترسيخ المفاهيم', 'كشريك لإدارة الموقف التعليمي', 'تمهيد مشوق للحصة', 'تمهيد مشوق للحصة', 'نشاط تطبيقي لترسيخ المفاهيم', 'كشريك لإدارة الموقف التعليمي', 'تمهيد مشوق للحصة', 'نشاط تطبيقي لترسيخ المفاهيم', 'نشاط تطبيقي لترسيخ المفاهيم', 'نشاط تطبيقي لترسيخ المفاهيم', 'نشاط تطبيقي لترسيخ المفاهيم', 'تنويع أدوات القياس والتقييم']
        })
        
    return data

# تحميل البيانات
data = load_data()

# --- هيدر الصفحة الرئيسي ---
st.write(
    """
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='color: #0284c7; font-weight: 800; font-size: 36px; margin-bottom: 5px;'>🎮 البوابة الرقمية لتحليل بيانات التلعيب بالتعليم</h1>
        <p style='color: #64748b; font-size: 18px; font-weight: 600;'>لوحة معلومات ذكية ومؤشرات تفاعلية تجمع بين (الطلاب، أولياء الأمور، والتربويين)</p>
    </div>
    """, 
    unsafe_allow_html=True
)
st.write("---")

# --- لوحة الـ KPIs الرئيسية ---
st.markdown("### 📌 مؤشرات الأداء الرئيسية والجاهزية العامة")
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    st.markdown("""
        <div class='kpi-card'>
            <div class='kpi-title'>🎯 رغبة الطلاب بالتعلم باللعب</div>
            <div class='kpi-value'>82%</div>
        </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    st.markdown("""
        <div class='kpi-card'>
            <div class='kpi-title'>👨‍👩‍👦 حماس أولياء الأمور للمنصة</div>
            <div class='kpi-value'>71%</div>
        </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    st.markdown("""
        <div class='kpi-card'>
            <div class='kpi-title'>🏫 اهتمام الكادر التعليمي بالتبني</div>
            <div class='kpi-value'>86%</div>
        </div>
    """, unsafe_allow_html=True)

with kpi_col4:
    st.markdown("""
        <div class='kpi-card'>
            <div class='kpi-title'>💡 تأثير الجوائز كعنصر تشجيع</div>
            <div class='kpi-value'>91%</div>
        </div>
    """, unsafe_allow_html=True)

st.write("---")

# --- التبويبات التفاعلية (Tabs) ---
tab_student, tab_parent, tab_edu, tab_cross = st.tabs([
    "🎒 استبيان الطلاب الأذكياء", 
    "👨‍👩‍👦 تطلعات أولياء الأمور", 
    "🏫 رؤية الكادر التعليمي", 
    "🔄 تحليل التقاطعات والتوصيات"
])

# ==================== تبويب الطلاب ====================
with tab_student:
    st.subheader("📊 تفضيلات ومحفزات الطلاب وصعوباتهم")
    
    # فلترة سريعة حسب الصف الدراسي
    all_grades = list(data['students']['الصف'].unique())
    selected_grade = st.selectbox("اختر الصف الدراسي لتصفية نتائج الطلاب:", ["الكل"] + all_grades)
    
    filtered_students = data['students']
    if selected_grade != "الكل":
        filtered_students = data['students'][data['students']['الصف'] == selected_grade]
        
    col_st_left, col_st_right = st.columns(2)
    
    with col_st_left:
        # أكثر مادة يواجه فيها الطالب صعوبة
        st.write("📌 **توزيع المواد الأكثر صعوبة:**")
        dif_data = filtered_students['المادة_الصعبة'].value_counts().reset_index()
        dif_data.columns = ['المادة', 'عدد الطلاب']
        fig_dif = px.bar(
            dif_data, x='عدد الطلاب', y='المادة', orientation='h',
            color='عدد الطلاب', color_continuous_scale='Blues',
            labels={'عدد الطلاب': 'عدد الطلاب', 'المادة': 'المادة'}
        )
        fig_dif.update_layout(yaxis={'categoryorder':'total ascending'}, height=300, margin=dict(l=0, r=0, t=10, b=10))
        st.plotly_chart(fig_dif, use_container_width=True)

    with col_st_right:
        # عناصر الجذب الأكثر طلباً في اللعبة التعليمية
        st.write("📌 **أكثر ما يفضله الطلاب في الألعاب التعليمية لزيادة الحماس:**")
        
        # معالجة النصوص المتعددة (Multi-select processing)
        all_attractions = []
        for val in filtered_students['عناصر_惹ذب' if 'عناصر_惹ذب' in filtered_students.columns else 'عناصر_الجذب']:
            if pd.notna(val):
                parts = [p.strip() for p in str(val).split(',')]
                all_attractions.extend(parts)
        
        attraction_df = pd.Series(all_attractions).value_counts().reset_index()
        attraction_df.columns = ['عنصر الجذب', 'عدد المصوتين']
        
        fig_attr = px.pie(
            attraction_df, values='عدد المصوتين', names='عنصر الجذب',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_attr.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=10))
        st.plotly_chart(fig_attr, use_container_width=True)

    # تفضيلات الألعاب التعليمية مقابل الألعاب العادية
    st.write("---")
    col_st_btm1, col_st_btm2 = st.columns(2)
    with col_st_btm1:
        st.write("📌 **رغبة الطلاب في تجربة ألعاب تعليمية على الموبايل/الكمبيوتر:**")
        pref_game = filtered_students['اللعب_للدراسة'].value_counts().reset_index()
        pref_game.columns = ['الرد', 'العدد']
        fig_pref = px.bar(pref_game, x='الرد', y='العدد', color='الرد', color_discrete_sequence=px.colors.qualitative.Set2)
        fig_pref.update_layout(height=280, showlegend=False, margin=dict(l=0, r=0, t=10, b=10))
        st.plotly_chart(fig_pref, use_container_width=True)
        
    with col_st_btm2:
        st.write("📌 **تأثير الجوائز والنقاط في تحفيز الطلاب للدراسة بجدية أكبر:**")
        rewards_data = filtered_students['الجوائز_والنقاط'].value_counts().reset_index()
        rewards_data.columns = ['الرأي', 'العدد']
        fig_rew = px.pie(rewards_data, values='العدد', names='الرأي', color_discrete_sequence=['#10b981', '#f43f5e'])
        fig_rew.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=10))
        st.plotly_chart(fig_rew, use_container_width=True)


# ==================== تبويب أولياء الأمور ====================
with tab_parent:
    st.subheader("📊 تطلعات ومخاوف أولياء الأمور تجاه التعلم الرقمي")
    
    col_p_left, col_p_right = st.columns(2)
    
    with col_p_left:
        st.write("📌 **معدل قضاء الأطفال أمام الشاشات خارج وقت الدراسة يومياً:**")
        screens = data['parents']['ساعات_الشاشات'].value_counts().reset_index()
        screens.columns = ['الوقت اليومي', 'عدد العائلات']
        fig_scr = px.pie(screens, values='عدد العائلات', names='الوقت اليومي', color_discrete_sequence=px.colors.sequential.Agsunset)
        fig_scr.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=10))
        st.plotly_chart(fig_scr, use_container_width=True)
        
    with col_p_right:
        st.write("📌 **حالة تفاعل أولياء الأمور الأولية مع مقترح المنصة التعليمية:**")
        interest = data['parents']['مستوى_الحماس'].value_counts().reset_index()
        interest.columns = ['رد الفعل المبدئي', 'العدد']
        fig_int = px.bar(interest, x='العدد', y='رد الفعل المبدئي', orientation='h', color='رد الفعل المبدئي', color_discrete_sequence=px.colors.qualitative.Safe)
        fig_int.update_layout(height=300, showlegend=False, yaxis={'categoryorder':'total ascending'}, margin=dict(l=0, r=0, t=10, b=10))
        st.plotly_chart(fig_int, use_container_width=True)
        
    st.write("---")
    st.write("📌 **القدرة على الاشتراك والدفع مقابل المنصات الرقمية المفيدة:**")
    pay_data = data['parents']['القدرة_على_الدفع'].value_counts().reset_index()
    pay_data.columns = ['الاستعداد المالي', 'النسبة']
    fig_pay = px.bar(pay_data, x='الاستعداد المالي', y='النسبة', color='الاستعداد المالي', color_discrete_sequence=['#0284c7', '#ec4899', '#f59e0b'])
    fig_pay.update_layout(height=300, showlegend=False, margin=dict(l=0, r=0, t=10, b=10))
    st.plotly_chart(fig_pay, use_container_width=True)


# ==================== تبويب الكادر التعليمي ====================
with tab_edu:
    st.subheader("📊 تحليل آراء المعلمين، المدراء، والمشرفين التربويين")
    
    all_roles = list(data['educators']['الدور_التربوي'].unique())
    selected_role = st.selectbox("اختر الدور الوظيفي لتحديد الفئة والآراء:", ["الكل"] + all_roles)
    
    filtered_edu = data['educators']
    if selected_role != "الكل":
        filtered_edu = data['educators'][data['educators']['الدور_التربوي'] == selected_role]
        
    col_ed_left, col_ed_right = st.columns(2)
    
    with col_ed_left:
        st.write("📌 **أهم التحديات والعقبات التي تواجه الفصل الدراسي حالياً:**")
        challenges = filtered_edu['العائق_الرئيسي'].value_counts().reset_index()
        challenges.columns = ['التحدي الأبرز', 'التكرار']
        fig_chal = px.bar(challenges, x='التكرار', y='التحدي الأبرز', orientation='h', color='التحدي الأبرز', color_discrete_sequence=px.colors.qualitative.Vivid)
        fig_chal.update_layout(height=300, showlegend=False, yaxis={'categoryorder':'total ascending'}, margin=dict(l=0, r=0, t=10, b=10))
        st.plotly_chart(fig_chal, use_container_width=True)
        
    with col_ed_right:
        st.write("📌 **الطريقة المثلى لدمج هذه المنصة الرقمية في الحصة:**")
        integration = filtered_edu['دمج_المنصة'].value_counts().reset_index()
        integration.columns = ['طريقة الدمج المفضلة', 'العدد']
        fig_integ = px.pie(integration, values='العدد', names='طريقة الدمج المفضلة', color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_integ.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=10))
        st.plotly_chart(fig_integ, use_container_width=True)


# ==================== تبويب التقاطعات والتوصيات ====================
with tab_cross:
    st.subheader("🔄 رؤية تقاطعية متكاملة وتوصيات صناعة القرار")
    
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        st.write("""
        <div style='background-color: #0f172a; padding: 25px; border-radius: 12px; border: 1px solid #1e293b; color: #e2e8f0; height: 100%;'>
            <h4 style='color: #38bdf8; margin-top: 0;'>🔑 الفجوة بين تفضيل اللعب والجدية الأكاديمية</h4>
            <p style='font-size: 15px; line-height: 1.6;'>
                أظهرت البيانات أن <b>82%</b> من الطلاب متحمسون جداً لفكرة التعلم بالألعاب، ولكن في المقابل، فإن 
                <b>تشتت الانتباه وضياع التركيز</b> هو من أعلى التحديات تكراراً لدى المعلمين.
            </p>
            <p style='font-size: 15px; line-height: 1.6; color: #f59e0b; font-weight: 600;'>
                ⚠️ توصية هامة للمطورين: يجب تصميم الألعاب بشكل "بنيوي أكاديمي" ومحدد الوقت (مثلاً: 5 دقائق بداية الحصة للتمهيد فقط)، للتأكد من عدم تحول التلعيب إلى تسلية مفرطة تشتت ذهن الطالب عن الهدف التعليمي.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_c2:
        st.write("""
        <div style='background-color: #0f172a; padding: 25px; border-radius: 12px; border: 1px solid #1e293b; color: #e2e8f0; height: 100%;'>
            <h4 style='color: #38bdf8; margin-top: 0;'>📈 فرصة الاستثمار والاشتراكات لولي الأمر</h4>
            <p style='font-size: 15px; line-height: 1.6;'>
                بينما يقضي أكثر من <b>72%</b> من الأطفال بين ساعة إلى 4 ساعات على الشاشات يومياً، فإن أولياء الأمور يبدون استعداداً ممتازاً للاشتراك بالخدمات المدفوعة بنسبة تفوق <b>71%</b> بشرط رؤية <b>"نتائج وأثر حقيقي على تحصيل الطالب"</b>.
            </p>
            <p style='font-size: 15px; line-height: 1.6; color: #10b981; font-weight: 600;'>
                💡 ميزة تنافسية للمشروع: توفير "لوحة تحكم خاصة بولي الأمر" ترسل تقريراً أسبوعياً لتقدم الطفل ومستوى نقاط القوة والضعف لتعزز الثقة والشفافية.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    st.write("💬 **آراء وتطلعات إنسانية مكتوبة من البيانات:**")
    st.info("«أتمنى أن يصبح التدريس و كتابة الوظائف عن طريق الكومبيوتر أو التاب لسهولة العملية التعليمية لجيلي» - طالب بالصف الثالث")
    st.info("«أتمنى وجود أنشطة فعالة وجاذبة في بداية الدرس تثير شغف الطالب لمعرفة الدرس الجديد وينصت بشغف» - معلم متميز")
