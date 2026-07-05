import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------------------------------
# CUSTOM STYLING
# ----------------------------------------------------------------------------
st.markdown("""
    <style>
        /* ---- Global app + sidebar background (theme-consistent, covers whole page) ---- */
        [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {
            background-color: #0e1117 !important;
        }
        section[data-testid="stSidebar"] {
            background-color: #131722 !important;
            border-right: 1px solid #262d3d;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1250px;
        }

        /* ---- Hero banner ---- */
        .hero {
            padding: 26px 30px;
            border-radius: 18px;
            background: linear-gradient(120deg, #4f46e5 0%, #7c3aed 55%, #a855f7 100%);
            color: white;
            margin-bottom: 24px;
            box-shadow: 0 8px 24px rgba(124, 58, 237, 0.25);
        }
        .hero h1 { margin: 0; font-size: 32px; letter-spacing: -0.5px; }
        .hero p  { margin-top: 8px; font-size: 15px; opacity: 0.92; }

        /* ---- Metric cards ---- */
        .metric-card {
            background: linear-gradient(160deg, #1a2033 0%, #12172400 100%), #161b28;
            border-radius: 14px;
            padding: 18px 20px;
            border: 1px solid #2a3247;
            text-align: center;
            transition: border 0.2s ease;
        }
        .metric-card:hover { border: 1px solid #7c3aed; }
        .metric-card h3 {
            margin: 0;
            font-size: 13px;
            color: #9aa4bd;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.4px;
        }
        .metric-card p {
            margin: 6px 0 0 0;
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(90deg, #c4b5fd, #f9fafb);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* ---- Expanders (sidebar sections) ---- */
        div[data-testid="stExpander"] {
            border: 1px solid #2a3247;
            border-radius: 10px;
            background-color: #161b28;
        }
        div[data-testid="stExpander"] summary {
            font-weight: 600;
            color: #e5e7eb !important;
        }

        /* ---- Tabs ---- */
        button[data-baseweb="tab"] {
            font-size: 15px;
            font-weight: 600;
            color: #9aa4bd;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #c4b5fd !important;
        }
        div[data-baseweb="tab-highlight"] {
            background-color: #a855f7 !important;
        }
        div[data-baseweb="tab-border"] {
            background-color: #262d3d !important;
        }

        /* ---- Dataframes / tables ---- */
        div[data-testid="stDataFrame"] {
            border: 1px solid #2a3247;
            border-radius: 10px;
            overflow: hidden;
        }

        /* ---- Buttons ---- */
        button[kind="primary"], .stButton>button {
            background: linear-gradient(120deg, #7c3aed, #a855f7);
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            padding: 0.55rem 1rem;
        }
        .stButton>button:hover {
            background: linear-gradient(120deg, #6d28d9, #9333ea);
            color: white;
        }

        /* ---- Section headers ---- */
        h1, h2, h3, h4, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #f2f4f8 !important; }
        .stCaption, .css-1629p8f { color: #7d8598; }

        /* ---- Expander header text (force contrast in both expanded/collapsed states) ---- */
        div[data-testid="stExpander"] details summary,
        div[data-testid="stExpander"] details summary span,
        div[data-testid="stExpander"] details summary p {
            color: #e5e7eb !important;
            background-color: transparent !important;
        }
        div[data-testid="stExpander"] details {
            background-color: #161b28 !important;
        }

        /* ---- Sidebar text contrast (labels + description were too dim by default) ---- */
        section[data-testid="stSidebar"] p {
            color: #aab2c5 !important;
            opacity: 1 !important;
        }
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] label p,
        section[data-testid="stSidebar"] .stSlider label,
        section[data-testid="stSidebar"] .stSelectbox label,
        section[data-testid="stSidebar"] .stNumberInput label {
            color: #d6dbe8 !important;
            opacity: 1 !important;
            font-weight: 500;
        }
        section[data-testid="stSidebar"] h2 {
            color: #f2f4f8 !important;
        }
        /* Slider min/max range numbers + current value bubble */
        section[data-testid="stSidebar"] [data-testid="stTickBarMin"],
        section[data-testid="stSidebar"] [data-testid="stTickBarMax"] {
            color: #9aa4bd !important;
        }
        section[data-testid="stSidebar"] div[data-baseweb="slider"] div[role="slider"] {
            background-color: #a855f7 !important;
        }

        /* ---- Custom HTML tables (replaces canvas-based st.dataframe for full color control) ---- */
        .custom-table-wrap {
            border: 1px solid #2a3247;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 12px;
        }
        table.custom-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 14.5px;
        }
        table.custom-table thead th {
            background-color: #1c2233;
            color: #c4b5fd;
            text-align: left;
            padding: 10px 16px;
            font-weight: 600;
            border-bottom: 1px solid #2a3247;
        }
        table.custom-table tbody td {
            background-color: #12161f;
            color: #f2f4f8;
            padding: 9px 16px;
            border-bottom: 1px solid #1e2433;
        }
        table.custom-table tbody tr:nth-child(even) td {
            background-color: #161b28;
        }
        table.custom-table tbody tr:hover td {
            background-color: #241f3d;
        }
        table.custom-table td.value-col, table.custom-table th.value-col {
            text-align: right;
        }
    </style>
""", unsafe_allow_html=True)

def render_table(df, value_cols=None):
    """Render a DataFrame as a styled HTML table (avoids the canvas-based
    st.dataframe widget so colors stay consistent regardless of theme)."""
    value_cols = value_cols or []
    html = ['<div class="custom-table-wrap"><table class="custom-table"><thead><tr>']
    for col in df.columns:
        cls = ' class="value-col"' if col in value_cols else ""
        html.append(f"<th{cls}>{col}</th>")
    html.append("</tr></thead><tbody>")
    for _, row in df.iterrows():
        html.append("<tr>")
        for col in df.columns:
            val = row[col]
            if isinstance(val, float):
                val = f"{val:.2f}"
            cls = ' class="value-col"' if col in value_cols else ""
            html.append(f"<td{cls}>{val}</td>")
        html.append("</tr>")
    html.append("</tbody></table></div>")
    st.markdown("".join(html), unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# LOAD MODEL & SCALER
# ----------------------------------------------------------------------------
@st.cache_resource
def load_artifacts():
    model = joblib.load("best_student_model.pkl")
    scaler = joblib.load("scaler.pkl")
    return model, scaler

try:
    model, scaler = load_artifacts()
    artifacts_loaded = True
except Exception as e:
    artifacts_loaded = False
    load_error = str(e)

# ----------------------------------------------------------------------------
# HERO HEADER
# ----------------------------------------------------------------------------
st.markdown("""
    <div class="hero">
        <h1>🎓 Student Performance Analytics</h1>
        <p>Predict Student GPA using Machine Learning — powered by a trained regression model</p>
    </div>
""", unsafe_allow_html=True)

if not artifacts_loaded:
    st.error(f"❌ Could not load model/scaler files. Make sure `best_student_model.pkl` and `scaler.pkl` are in the app directory.\n\nDetails: {load_error}")
    st.stop()

# ----------------------------------------------------------------------------
# SIDEBAR — INPUTS
# ----------------------------------------------------------------------------
st.sidebar.markdown("## 🧑‍🎓 Student Details")
st.sidebar.markdown("Fill in the details below to generate a prediction.")

with st.sidebar.expander("👤 Demographics", expanded=True):
    age = st.number_input("Age", 18, 25, 20)
    gender = st.selectbox("Gender", [0, 1], format_func=lambda x: "Male" if x == 0 else "Female")
    ethnicity = st.selectbox("Ethnicity", [0, 1, 2, 3])
    parent_education = st.selectbox("Parental Education", [0, 1, 2, 3, 4])

with st.sidebar.expander("📚 Academics", expanded=True):
    study_time = st.slider("Study Time Weekly (hrs)", 0.0, 30.0, 10.0)
    absences = st.slider("Absences", 0, 30, 5)
    tutoring = st.selectbox("Tutoring", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    parent_support = st.selectbox("Parental Support", [0, 1, 2, 3, 4])
    grade_class = st.selectbox("Grade Class", [0, 1, 2, 3, 4])

with st.sidebar.expander("⚽ Activities", expanded=True):
    extra = st.selectbox("Extracurricular", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    sports = st.selectbox("Sports", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    music = st.selectbox("Music", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    volunteering = st.selectbox("Volunteering", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")

predict_clicked = st.sidebar.button("🚀 Predict GPA", use_container_width=True, type="primary")

# ----------------------------------------------------------------------------
# FEATURE ENGINEERING
# ----------------------------------------------------------------------------
study_efficiency = study_time / (absences + 1)
academic_support = tutoring + parent_support
activity_score = sports + music + volunteering + extra
total_engagement = study_time + activity_score

input_data = pd.DataFrame({
    "Age": [age],
    "Gender": [gender],
    "Ethnicity": [ethnicity],
    "ParentalEducation": [parent_education],
    "StudyTimeWeekly": [study_time],
    "Absences": [absences],
    "Tutoring": [tutoring],
    "ParentalSupport": [parent_support],
    "Extracurricular": [extra],
    "Sports": [sports],
    "Music": [music],
    "Volunteering": [volunteering],
    "GradeClass": [grade_class],
    "StudyEfficiency": [study_efficiency],
    "AcademicSupport": [academic_support],
    "ActivityScore": [activity_score],
    "TotalEngagement": [total_engagement]
})

numeric_cols = [
    "Age", "StudyTimeWeekly", "Absences", "StudyEfficiency",
    "AcademicSupport", "ActivityScore", "TotalEngagement"
]

scaled_input = input_data.copy()
scaled_input[numeric_cols] = scaler.transform(scaled_input[numeric_cols])

# ----------------------------------------------------------------------------
# TOP METRIC CARDS (raw, human-readable values)
# ----------------------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="metric-card"><h3>📖 Study Time / Week</h3><p>{study_time:.1f} hrs</p></div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="metric-card"><h3>🚫 Absences</h3><p>{absences}</p></div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="metric-card"><h3>⚡ Study Efficiency</h3><p>{study_efficiency:.2f}</p></div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="metric-card"><h3>🏃 Activity Score</h3><p>{activity_score}</p></div>""", unsafe_allow_html=True)

st.write("")

# ----------------------------------------------------------------------------
# TABS — Data / Prediction
# ----------------------------------------------------------------------------
tab1, tab2 = st.tabs(["📋 Student Data", "🔮 GPA Prediction"])

with tab1:
    st.subheader("📋 Raw Input")
    display_df = input_data.T.reset_index()
    display_df.columns = ["Feature", "Value"]
    render_table(display_df, value_cols=["Value"])

    with st.expander("⚙️ Scaled Input (fed to model)"):
        render_table(scaled_input)

with tab2:
    if predict_clicked:
        raw_prediction = float(model.predict(scaled_input)[0])
        raw_prediction = max(0.0, min(4.0, raw_prediction))

        # Convert from the model's native 0-4 GPA scale to a 0-10 scale
        prediction = raw_prediction * 2.5

        colA, colB = st.columns([1, 1.3])

        with colA:
            st.markdown("### 🎯 Predicted GPA")
            st.markdown(f"<h1 style='font-size:64px; color:#a78bfa;'>{prediction:.2f} <span style='font-size:28px; color:#9aa4bd;'>/ 10</span></h1>", unsafe_allow_html=True)

            if prediction >= 8.75:
                st.success("⭐⭐⭐⭐⭐ Excellent Student")
            elif prediction >= 7.5:
                st.info("👍 Good Performance")
            elif prediction >= 5.0:
                st.warning("⚠️ Average Performance")
            else:
                st.error("❌ Needs Improvement")

        with colB:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prediction,
                number={'suffix': " / 10", 'font': {'size': 36}},
                gauge={
                    'axis': {'range': [0, 10], 'tickwidth': 1},
                    'bar': {'color': "#a78bfa"},
                    'steps': [
                        {'range': [0, 5], 'color': "#7f1d1d"},
                        {'range': [5, 7.5], 'color': "#92400e"},
                        {'range': [7.5, 8.75], 'color': "#1e3a8a"},
                        {'range': [8.75, 10], 'color': "#065f46"},
                    ],
                    'threshold': {
                        'line': {'color': "white", 'width': 4},
                        'thickness': 0.8,
                        'value': prediction
                    }
                }
            ))
            fig.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=30, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                font={'color': "#f9fafb"}
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👈 Fill in the student details in the sidebar and click **Predict GPA** to see results here.")

st.markdown("---")
st.caption("Built with Streamlit • Model predictions are estimates and should be used alongside other assessments.")