"""
Student Placement Prediction System - Web App
--------------------------------------------------------------
DESIGN SYSTEM (so every visual choice is explainable, not decorative):

Palette - a dark "ML dashboard" look instead of a plain light theme,
since this project is meant to double as a resume/portfolio piece:
    Background (deep)     : #0B1120
    Background (panel)     : #131C31
    Card background        : #161F38  (with a soft border + shadow)
    Accent gradient         : #6366F1 -> #22D3EE  (indigo -> cyan)
    Positive / "Placed"     : #10B981 -> #34D399  (emerald gradient)
    Negative / "Not Placed" : #F43F5E -> #FB7185  (rose gradient)
    Heading text            : #F1F5F9
    Body text               : #CBD5E1

Typography: 'Sora' for headings (bold, geometric - reads as "product",
not "generic bootstrap"), 'Inter' for body text (clean and readable
at small sizes for dense ML dashboard content).

Signature element: a circular confidence GAUGE (pure CSS, built with
conic-gradient) instead of a flat progress bar. It's built directly
in Python by computing the gradient's percentage stop and inserting
it into an f-string - no chart library needed, and it reads as a
genuine "ML dashboard" component rather than a form result.

Navigation: st.tabs() as a top navbar (Home | About | Prediction |
Notebook Code) - the same mechanic as before, just restyled.
"""

import streamlit as st
import pandas as pd
import joblib
import json

# =====================================================================
# PAGE CONFIG
# =====================================================================
st.set_page_config(
    page_title="Student Placement Prediction System",
    page_icon="🎓",
    layout="wide"
)

# =====================================================================
# GLOBAL STYLE
# =====================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Inter:wght@400;500;600&display=swap');

    /* Force the dark theme regardless of the visitor's OS/browser
       light/dark setting - .stApp is Streamlit's real root container,
       targeting it directly with !important is what actually sticks. */
    .stApp {
        background: radial-gradient(circle at 15% 0%, #131C31 0%, #0B1120 55%) !important;
    }
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    h1, h2, h3 { font-family: 'Sora', sans-serif; }
    h1, h2, h3, p, span, label, li { color: #F1F5F9 !important; }
    .stMarkdown p, .stMarkdown li { color: #CBD5E1 !important; }

    /* ---------------- Brand / hero bar ---------------- */
    .brand-bar {
        display: flex; align-items: center; gap: 0.9rem;
        padding: 0.75rem 0 1.25rem 0;
        border-bottom: 1px solid #1E293B;
        margin-bottom: 1.75rem;
    }
    .brand-logo {
        background: linear-gradient(135deg, #6366F1, #22D3EE);
        color: #0B1120 !important;
        font-family: 'Sora', sans-serif; font-weight: 800;
        width: 46px; height: 46px; border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.15rem;
        box-shadow: 0 0 24px rgba(99,102,241,0.45);
    }
    .brand-title {
        font-family: 'Sora', sans-serif; font-size: 1.35rem; font-weight: 700;
        background: linear-gradient(90deg, #F1F5F9, #A5B4FC);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .brand-subtitle { font-size: 0.85rem; color: #64748B !important; margin-top: -2px; }

    /* ---------------- Hero banner (Home tab) ---------------- */
    .hero {
        background: linear-gradient(120deg, rgba(99,102,241,0.18), rgba(34,211,238,0.10));
        border: 1px solid #26314D;
        border-radius: 18px;
        padding: 2.2rem 2rem;
        margin-bottom: 1.5rem;
    }
    .hero h1 {
        font-size: 2rem; font-weight: 800; margin-bottom: 0.4rem;
        background: linear-gradient(90deg, #F1F5F9, #67E8F9);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }

    /* ---------------- Stat cards (Home tab) ---------------- */
    .stat-card {
        background: #161F38; border: 1px solid #263156; border-radius: 14px;
        padding: 1.1rem 1.3rem; text-align: left;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .stat-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(99,102,241,0.20); }
    .stat-value {
        font-family: 'Sora', sans-serif; font-size: 1.6rem; font-weight: 800; color: #67E8F9 !important;
    }
    .stat-label { font-size: 0.82rem; color: #94A3B8 !important; }

    /* ---------------- Info cards (About tab) ---------------- */
    .info-card {
        background: #161F38; border: 1px solid #263156; border-radius: 14px;
        padding: 1.4rem 1.6rem; margin-bottom: 1.1rem;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .info-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(99,102,241,0.15); }
    .info-card-title {
        font-family: 'Sora', sans-serif; font-weight: 700; font-size: 1.05rem;
        color: #67E8F9 !important; margin-bottom: 0.6rem;
        display: flex; align-items: center; gap: 0.5rem;
    }
    .info-card p, .info-card li { color: #CBD5E1 !important; font-size: 0.92rem; margin-bottom: 0.4rem; }
    .info-card ol, .info-card ul { margin: 0; padding-left: 1.2rem; }
    .info-card code {
        background: #0B1120; color: #67E8F9 !important; padding: 0.1rem 0.4rem;
        border-radius: 4px; font-size: 0.85rem;
    }

    /* ---------------- Tabs styled as a navbar ---------------- */
    button[data-baseweb="tab"] {
        font-family: 'Sora', sans-serif; font-weight: 600; font-size: 0.95rem;
        color: #94A3B8 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] { color: #67E8F9 !important; }
    div[data-baseweb="tab-highlight"] { background-color: #22D3EE !important; }

    /* ---------------- Buttons ---------------- */
    div.stButton > button {
        background: linear-gradient(135deg, #6366F1, #22D3EE);
        color: #0B1120; border: none; border-radius: 10px;
        padding: 0.6rem 1.6rem; font-weight: 700; font-family: 'Sora', sans-serif;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(34,211,238,0.35);
        color: #0B1120;
    }

    /* ---------------- Result card with gauge ---------------- */
    .result-card {
        display: flex; align-items: center; gap: 1.75rem;
        background: #161F38; border-radius: 16px; padding: 1.5rem 1.75rem;
        margin: 1rem 0; border: 1px solid #263156;
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    }
    .result-card.placed { border-color: #10B98155; }
    .result-card.not-placed { border-color: #F43F5E55; }

    .gauge {
        width: 128px; height: 128px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        flex-shrink: 0;
    }
    .gauge-inner {
        width: 100px; height: 100px; border-radius: 50%;
        background: #161F38;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
    }
    .gauge-percent { font-family: 'Sora', sans-serif; font-size: 1.3rem; font-weight: 800; }
    .gauge-caption { font-size: 0.68rem; color: #94A3B8 !important; }

    .result-title { font-family: 'Sora', sans-serif; font-weight: 800; font-size: 1.3rem; margin-bottom: 0.25rem; }
    .result-desc { font-size: 0.9rem; color: #94A3B8 !important; }

    /* ---------------- Suggestion chips ---------------- */
    .chip-row { display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0.75rem 0 1.25rem 0; }
    .chip {
        border-radius: 999px; padding: 0.45rem 0.9rem; font-size: 0.85rem;
        border: 1px solid #263156; background: #131C31; color: #E2E8F0 !important;
    }
    .chip b { color: #67E8F9 !important; }
    .chip.gap b { color: #FDA4AF !important; }

    footer { visibility: hidden; }
    .app-footer {
        text-align: center; font-size: 0.82rem;
        margin-top: 3rem; padding-top: 1.4rem;
        border-top: 1px solid #1E293B;
    }
    .app-footer .footer-name {
        background: linear-gradient(90deg, #A5B4FC, #67E8F9);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-family: 'Sora', sans-serif; font-weight: 700;
    }
    .app-footer .footer-meta { color: #475569 !important; }
    .app-footer .footer-dot { color: #334155 !important; margin: 0 0.4rem; }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# LOAD MODEL + BENCHMARK STATS
# =====================================================================
model = joblib.load('placement_model.pkl')
placed_avg = joblib.load('placed_avg_stats.pkl')

# -----------------------------------------------------------------
# Pull numeric feature importances directly out of the trained
# Random Forest pipeline. This lets the explanation below be ranked
# by how much each feature actually drives the MODEL's decision,
# instead of by raw unit differences - which is scale-biased (e.g. a
# 40-point Aptitude_Test_Score gap looks bigger than a 1-point CGPA
# gap purely because of its scale, even if CGPA matters more). This
# is exactly what caused only "Backlogs" to show up before: its small
# natural range (0-3) made even a tiny gap look numerically large.
# -----------------------------------------------------------------
_rf_classifier = model.named_steps['classifier']
_preprocessor_step = model.named_steps['preprocessor']
_all_feature_names = _preprocessor_step.get_feature_names_out()
_all_importances = _rf_classifier.feature_importances_

importance_map = {}
for _name, _imp in zip(_all_feature_names, _all_importances):
    if _name.startswith('num__'):
        importance_map[_name.replace('num__', '')] = _imp

# =====================================================================
# BRAND BAR
# =====================================================================
st.markdown("""
<div class="brand-bar">
    <div class="brand-logo">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 3L1 9l11 6 9-4.91V17h2V9L12 3z" fill="#0B1120"/>
            <path d="M5 13.18v4L12 21l7-3.82v-4L12 17l-7-3.82z" fill="#0B1120"/>
        </svg>
    </div>
    <div>
        <div class="brand-title">Student Placement Prediction System</div>
        <div class="brand-subtitle">Basics of AI · Individual Project (Machine Learning)</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# TOP NAVIGATION
# =====================================================================
tab_home, tab_about, tab_predict, tab_code = st.tabs(
    ["   Home", "   About", "   Prediction System", "   Notebook Code"]
)

# ---------------------------------------------------------------------
# HOME TAB
# ---------------------------------------------------------------------
with tab_home:
    st.markdown("""
    <div class="hero">
        <h1>Predict placement outcomes, and know exactly why.</h1>
        <p style="max-width:640px; color:#CBD5E1;">
        A Random Forest model trained on 50,000 student records predicts
        whether a student is likely to be <b>Placed</b> or <b>Not Placed</b>,
        and explains the result using the same feature patterns discovered
        during exploratory data analysis - not a black box.
        </p>
    </div>
    """, unsafe_allow_html=True)

    s1, s2, s3 = st.columns(3)
    stats = [
        ("50,000", "Student records analyzed"),
        ("Random Forest", "Final selected model"),
        ("~99.99%", "5-fold cross-validated accuracy"),
    ]
    for col, (value, label) in zip([s1, s2, s3], stats):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{value}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    st.info("Go to **Prediction System** to try it, or **Notebook Code** to see the full ML workflow behind this app.")

# ---------------------------------------------------------------------
# ABOUT TAB
# ---------------------------------------------------------------------
with tab_about:
    st.header("About this project")

    # Row 1: Problem Statement + Dataset, side by side
    a1, a2 = st.columns(2)
    with a1:
        st.markdown("""
        <div class="info-card">
            <div class="info-card-title">❖ Problem Statement</div>
            <p>Build a Student Placement Prediction System that predicts
            whether a student is Placed or Not Placed during campus
            recruitment, based on academic, technical, aptitude,
            internship, and soft-skill attributes.</p>
        </div>
        """, unsafe_allow_html=True)

    with a2:
        st.markdown("""
        <div class="info-card">
            <div class="info-card-title">❖ Dataset</div>
            <p>50,000 student records across 15 columns, including CGPA,
            Internships, Projects, Coding Skills, Communication Skills,
            Aptitude Test Score, Soft Skills Rating, Certifications,
            Backlogs, Gender, Degree, and Branch.</p>
        </div>
        """, unsafe_allow_html=True)

    # Row 2: Workflow (full width - it's the longest section)
    st.markdown("""
    <div class="info-card">
        <div class="info-card-title">❖ Workflow</div>
        <ol>
            <li>Data understanding &amp; quality check - no missing values or duplicates.</li>
            <li>Exploratory Data Analysis - univariate and bivariate analysis of every feature against Placement Status.</li>
            <li>Data preparation - train-test split performed <i>before</i> encoding, followed by a <code>ColumnTransformer</code> (OneHotEncoder + StandardScaler) to avoid data leakage.</li>
            <li>Model building - Logistic Regression and Random Forest, compared on accuracy, precision, recall, F1-score, and 5-fold cross-validation.</li>
            <li>Deployment - the final Random Forest pipeline was saved with <code>joblib</code> and integrated into this web app.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    # Row 3: Why Random Forest + Why Streamlit, side by side
    a3, a4 = st.columns(2)
    with a3:
        st.markdown("""
        <div class="info-card">
            <div class="info-card-title">❖ Why Random Forest</div>
            <p>It achieved near-perfect, cross-validated accuracy and
            produced feature importances that matched the patterns
            already found during EDA. Logistic Regression was kept
            as an interpretable baseline for comparison.</p>
        </div>
        """, unsafe_allow_html=True)

    with a4:
        st.markdown("""
        <div class="info-card">
            <div class="info-card-title">❖ Why Streamlit, not HTML/CSS/JS</div>
            <p>Streamlit builds an interactive web app using only Python,
            reusing the same pandas and scikit-learn code from the
            notebook - no separate frontend framework or JavaScript
            required, keeping the project's focus on the machine
            learning workflow itself.</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------------------
# PREDICTION SYSTEM TAB
# ---------------------------------------------------------------------
with tab_predict:
    st.header("Try the prediction system")
    st.write("Fill in the student's details, then click **Predict Placement**.")

    col1, col2 = st.columns(2)
    with col1:
        age = st.slider("Age", 18, 24, 21)
        gender = st.selectbox("Gender", ["Male", "Female"])
        degree = st.selectbox("Degree", ["B.Sc", "B.Tech", "BCA", "MCA"])
        branch = st.selectbox("Branch", ["CSE", "IT", "ECE", "ME", "Civil"])
        cgpa = st.slider("CGPA", 4.5, 9.8, 7.0, step=0.1)
        internships = st.slider("Internships", 0, 3, 1)
        projects = st.slider("Projects", 1, 6, 4)

    with col2:
        coding_skills = st.slider("Coding Skills (1-10)", 1, 10, 6)
        communication_skills = st.slider("Communication Skills (1-10)", 1, 10, 5)
        aptitude_score = st.slider("Aptitude Test Score (35-100)", 35, 100, 70)
        soft_skills = st.slider("Soft Skills Rating (1-10)", 1, 10, 5)
        certifications = st.slider("Certifications", 0, 3, 1)
        backlogs = st.slider("Backlogs", 0, 3, 0)

    if st.button("Predict Placement"):

        input_data = pd.DataFrame([{
            'Age': age, 'Gender': gender, 'Degree': degree, 'Branch': branch,
            'CGPA': cgpa, 'Internships': internships, 'Projects': projects,
            'Coding_Skills': coding_skills, 'Communication_Skills': communication_skills,
            'Aptitude_Test_Score': aptitude_score, 'Soft_Skills_Rating': soft_skills,
            'Certifications': certifications, 'Backlogs': backlogs
        }])

        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]
        confidence = probability * 100 if prediction == 1 else (1 - probability) * 100

        # -----------------------------------------------------------
        # Result card: gauge + text live INSIDE the same card, side
        # by side using flexbox - this keeps them one unified size
        # instead of separate, unevenly-sized Streamlit columns.
        # -----------------------------------------------------------
        if prediction == 1:
            grad_start, grad_end, text_color = "#10B981", "#34D399", "#34D399"
            card_class, title, desc = (
                "placed", "✅ Likely to be PLACED",
                "This profile aligns closely with students who were placed historically."
            )
        else:
            grad_start, grad_end, text_color = "#F43F5E", "#FB7185", "#FB7185"
            card_class, title, desc = (
                "not-placed", "❌ Likely to be NOT PLACED",
                "This profile shows meaningful gaps versus the placed-student benchmark."
            )

        # The gauge is a pure-CSS donut: conic-gradient fills clockwise
        # up to `confidence`%, the remaining arc stays background-colored.
        st.markdown(f"""
        <div class="result-card {card_class}">
            <div class="gauge" style="background: conic-gradient({grad_start} 0% {confidence}%, #1E293B {confidence}% 100%);">
                <div class="gauge-inner">
                    <div class="gauge-percent" style="color:{text_color};">{confidence:.1f}%</div>
                    <div class="gauge-caption">confidence</div>
                </div>
            </div>
            <div>
                <div class="result-title" style="color:{text_color};">{title}</div>
                <div class="result-desc">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.caption(
            "This prediction is based on patterns learned from historical "
            "data - an educational demonstration, not a guarantee of "
            "real-world outcomes."
        )

        # -----------------------------------------------------------
        # Explainability: why this result, what can improve it
        #
        # Design: rank ALL numeric features by the Random Forest's own
        # feature_importances_ (computed once, above), not by raw gap
        # size. This guarantees the explanation always reflects what
        # the model actually weighs most heavily - and always surfaces
        # multiple factors (not just whichever single feature happens
        # to have the largest raw-unit difference, like Backlogs did).
        # -----------------------------------------------------------
        st.subheader("📌 Why this result? What can improve it?")

        student_values = {
            'CGPA': cgpa, 'Internships': internships, 'Projects': projects,
            'Coding_Skills': coding_skills, 'Communication_Skills': communication_skills,
            'Aptitude_Test_Score': aptitude_score, 'Soft_Skills_Rating': soft_skills,
            'Certifications': certifications, 'Backlogs': backlogs,
        }
        lower_is_better = {'Backlogs'}  # every other feature: higher is better

        # Rank features by model importance, most influential first.
        ranked_features = sorted(
            student_values.keys(),
            key=lambda f: importance_map.get(f, 0),
            reverse=True
        )

        def is_favorable(feature):
            val, bench = student_values[feature], placed_avg[feature]
            return val <= bench if feature in lower_is_better else val >= bench

        st.write("Top factors driving this prediction, ranked by model importance:")
        chip_parts = []
        for feature in ranked_features[:6]:
            favorable = is_favorable(feature)
            icon = "✓" if favorable else "!"
            css_class = "chip" if favorable else "chip gap"
            chip_parts.append(
                f'<span class="{css_class}"><b>{icon} {feature}</b>: '
                f'{student_values[feature]} (placed avg {placed_avg[feature]:.2f})</span>'
            )
        st.markdown(f'<div class="chip-row">{"".join(chip_parts)}</div>', unsafe_allow_html=True)

        if prediction == 0:
            unfavorable = [f for f in ranked_features if not is_favorable(f)]
            if unfavorable:
                st.write("Top areas to focus on, ranked by model importance (most impactful first):")
                for feature in unfavorable[:5]:
                    verb = "decrease" if feature in lower_is_better else "increase"
                    st.markdown(
                        f'<div class="chip gap" style="display:block; margin-bottom:0.5rem;">'
                        f'<b>{feature}</b> — currently {student_values[feature]}, placed students average '
                        f'{placed_avg[feature]:.2f} → aim to <b>{verb}</b> this.</div>',
                        unsafe_allow_html=True
                    )
            else:
                st.write(
                    "This numeric profile already matches or exceeds the "
                    "placed-student average on every measured factor - the "
                    "prediction may be influenced by Branch, Degree, or "
                    "interactions a simple comparison can't capture."
                )
            st.caption(
                "Suggestions are ranked using the trained model's own feature "
                "importance, combined with comparison against the average "
                "profile of placed students - directional guidance, not a guarantee."
            )

# ---------------------------------------------------------------------
# NOTEBOOK CODE TAB
# ---------------------------------------------------------------------
with tab_code:
    st.header("Notebook code")
    st.write(
        "The full machine learning workflow, read directly from the "
        "project's Jupyter Notebook - from data loading through EDA, "
        "model training, and evaluation."
    )

    try:
        with open('project.ipynb', 'r', encoding='utf-8') as f:
            notebook = json.load(f)

        for cell in notebook['cells']:
            source = ''.join(cell['source'])
            if not source.strip():
                continue
            if cell['cell_type'] == 'code':
                st.code(source, language='python')
            elif cell['cell_type'] == 'markdown':
                st.markdown(source)

    except FileNotFoundError:
        st.warning(
            "project.ipynb was not found in this folder. Place your "
            "notebook file in the same folder as app.py to display it here."
        )

# =====================================================================
# FOOTER
# =====================================================================
st.markdown("""
<div class="app-footer">
    Developed by <span class="footer-name">Shubham Pal</span>
    <span class="footer-dot">•</span>
    <span class="footer-meta">BSc AIML · Thakur College of Science &amp; Commerce · Basics of AI Project</span>
</div>
""", unsafe_allow_html=True)
