import streamlit as st
import pandas as pd
from datetime import datetime
from collections import Counter
import altair as alt

# Set page config
st.set_page_config(page_title="WomenLead Library Admin", layout="wide")

# -----------------------------
# Section: Basic login (placeholder logic)
# -----------------------------
PASSWORD = "womenlead2025"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 WomenLead Library Admin Login")
    password = st.text_input("Enter password to continue:", type="password")
    if password == PASSWORD:
        st.session_state.authenticated = True
        st.experimental_rerun()
    else:
        st.stop()

# -----------------------------
# Style
# -----------------------------
st.markdown("""
    <style>
        .header {
            background-color: #003366;
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        .section-title {
            color: #C60C30;
            font-weight: bold;
        }
        .content-box {
            background-color: #F0F2F6;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown("""
    <div class='header'>
        <h1>WomenLead Digital Library Dashboard</h1>
        <h4>Robinson College of Business · Georgia State University</h4>
    </div>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.title("📚 Dashboard Menu")
page = st.sidebar.radio("Go to", [
    "Home", "Content Repository", "Analytics", "Add Content", "Suggestions", "Support Requests", "SharePoint"
])

# -----------------------------
# Session Storage
# -----------------------------
if "library_df" not in st.session_state:
    st.session_state.library_df = pd.DataFrame(columns=["Title", "Source", "Tags", "Upload Date"])

if "suggestions" not in st.session_state:
    st.session_state.suggestions = []

if "support_logs" not in st.session_state:
    st.session_state.support_logs = []

# -----------------------------
# Page: Home
# -----------------------------
if page == "Home":
    st.subheader("📖 Welcome to the WomenLead Library Admin Panel")
    st.markdown("""
        This dashboard allows you to:
        - Manage content uploads from multiple platforms (Dropbox, iCollege, Teams)
        - Suggest new content areas
        - Track support issues
        - View analytics on uploads
        - Export content data
        - Integrate with SharePoint (preview iframe)
    """)

# -----------------------------
# Page: Content Repository
# -----------------------------
elif page == "Content Repository":
    st.subheader("🗂️ Digital Library Repository")

    uploaded_file = st.file_uploader("Upload New File", type=["pdf", "docx", "pptx", "xlsx", "zip"])
    if uploaded_file:
        title = st.text_input("Enter Title", value=uploaded_file.name.split('.')[0])
        source = st.selectbox("Source", ["Dropbox", "Teams", "iCollege", "Other"])
        tags = st.text_input("Tags (comma-separated)", value="")
        if st.button("Add to Library"):
            st.session_state.library_df.loc[len(st.session_state.library_df)] = [
                title, source, tags, datetime.now().strftime("%Y-%m-%d")
            ]
            st.success(f"'{title}' added to repository!")

    st.markdown("### 📂 All Files")
    st.dataframe(st.session_state.library_df)

    if not st.session_state.library_df.empty:
        st.download_button(
            "📥 Export as CSV",
            st.session_state.library_df.to_csv(index=False),
            file_name="womenlead_repository.csv",
            mime="text/csv"
        )

# -----------------------------
# Page: Analytics
# -----------------------------
elif page == "Analytics":
    st.subheader("📊 Repository Analytics")

    df = st.session_state.library_df

    if df.empty:
        st.info("No content uploaded yet.")
    else:
        st.markdown("#### Uploads by Source")
        source_count = df["Source"].value_counts().reset_index()
        source_count.columns = ["Source", "Count"]
        chart = alt.Chart(source_count).mark_bar().encode(
            x="Source", y="Count", color="Source"
        ).properties(width=600)
        st.altair_chart(chart)

        st.markdown("#### Most Common Tags")
        all_tags = ", ".join(df["Tags"].dropna()).split(",")
        tag_freq = pd.DataFrame(Counter(tag.strip() for tag in all_tags if tag).most_common(10), columns=["Tag", "Count"])
        st.bar_chart(tag_freq.set_index("Tag"))

# -----------------------------
# Page: Add New Content
# -----------------------------
elif page == "Add Content":
    st.subheader("➕ Suggest New Content Area")
    topic = st.text_input("New Content Topic")
    rationale = st.text_area("Why should this be included?")
    if st.button("Submit Suggestion"):
        st.session_state.suggestions.append({"Topic": topic, "Rationale": rationale})
        st.success("Suggestion submitted!")

# -----------------------------
# Page: Suggestions
# -----------------------------
elif page == "Suggestions":
    st.subheader("📌 Content Suggestions")
    if st.session_state.suggestions:
        st.table(pd.DataFrame(st.session_state.suggestions))
    else:
        st.info("No suggestions submitted yet.")

# -----------------------------
# Page: Support Requests
# -----------------------------
elif page == "Support Requests":
    st.subheader("🛠️ Support Requests")
    name = st.text_input("Your Name")
    issue = st.text_area("Describe the Issue")
    if st.button("Log Issue"):
        st.session_state.support_logs.append({
            "Name": name,
            "Issue": issue,
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        st.success("Issue logged.")

    if st.session_state.support_logs:
        st.markdown("### 📝 Logged Issues")
        st.table(pd.DataFrame(st.session_state.support_logs))

# -----------------------------
# Page: SharePoint Integration
# -----------------------------
elif page == "SharePoint":
    st.subheader("🔗 SharePoint Integration (Placeholder)")

    st.markdown("""
        <iframe src="https://gsu.sharepoint.com" width="100%" height="500px" style="border: 2px solid #003366; border-radius: 8px;"></iframe>
    """, unsafe_allow_html=True)
