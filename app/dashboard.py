"""Market Intelligence & GTM Dashboard: software engineering services firms (public homepages, 2026-10-12)."""
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import analysis as A
from themes import theme_names

st.set_page_config(page_title="Market Intelligence & GTM Dashboard", layout="wide")


@st.cache_data
def get():
    return A.load()


brands_all, gaps = get()
st.title("Market Intelligence & GTM Dashboard")
st.caption("Software engineering services firms. Public data from each firm's own homepage, accessed 2026-10-12. "
           "Not proprietary market research. Claims are the firms' own.")

with st.sidebar:
    st.header("Filters")
    sel = st.multiselect("Brands", list(brands_all.brand), default=list(brands_all.brand))
    conf = st.multiselect("Data confidence", ["High", "Medium"], default=["High", "Medium"])
    focus = st.radio("Focus", ["All", "Vertical specialists", "Generalists"])
b = brands_all[brands_all.brand.isin(sel) & brands_all.confidence.isin(conf)]
if focus == "Vertical specialists":
    b = b[b.vertical_focus.notna()]
elif focus == "Generalists":
    b = b[b.vertical_focus.isna()]
if b.empty:
    st.warning("No brands match the current filters."); st.stop()

pos, cta, eng = (A.theme_matrix(b, g) for g in ("positioning", "cta", "engagement"))
m = A.metrics(b); k = A.key_numbers(b, pos, cta, eng, m)
tabs = st.tabs(["Overview", "Positioning", "Lead-gen funnel", "Pricing & models", "Proof & content", "GTM plan", "Sources & gaps"])

with tabs[0]:
    c = st.columns(4)
    c[0].metric("Brands", k["n_brands"]); c[1].metric("AI-led headlines", f"{k['ai_led']}/{k['n_brands']}")
    c[2].metric("Publish a rate", f"{k['publish_rate']}/{k['n_brands']}")
    c[3].metric("Call/consult CTA", f"{k['call_cta']}/{k['n_brands']}")
    st.dataframe(b[["brand", "positioning_h1", "vertical_focus", "confidence"]], hide_index=True, width="stretch")
    st.caption("Wingman Partners itself is not in the dataset: its website could not be read.")

with tabs[1]:
    st.plotly_chart(px.imshow(pos.set_index("brand"), color_continuous_scale="Blues", aspect="auto",
                              title="Positioning themes in headline + subheadline"), width="stretch")
    st.bar_chart(pos[theme_names("positioning")].sum().rename("brands using theme"))
    st.dataframe(b[["brand", "positioning_h1", "positioning_sub"]], hide_index=True, width="stretch")

with tabs[2]:
    st.plotly_chart(px.imshow(cta.set_index("brand"), color_continuous_scale="Blues", aspect="auto",
                              title="Types of call to action on the homepage"), width="stretch")
    st.dataframe(b[["brand", "primary_ctas"]], hide_index=True, width="stretch")
    st.caption("CTA text only; placement, form length and follow-up are not captured.")

with tabs[3]:
    st.plotly_chart(px.imshow(eng.set_index("brand"), color_continuous_scale="Blues", aspect="auto",
                              title="Engagement models named"), width="stretch")
    r = b[b.rate_low_usd_hr.notna()][["brand", "published_rate_text", "rate_low_usd_hr", "rate_high_usd_hr"]]
    st.subheader("Published rates")
    if r.empty:
        st.info("None of the selected brands publish a rate.")
    else:
        st.dataframe(r, hide_index=True, width="stretch")
    st.dataframe(b[["brand", "engagement_models"]], hide_index=True, width="stretch")

with tabs[4]:
    st.warning("Years, team sizes, ratings and badges are the firms' own claims. Not verified.")
    st.plotly_chart(px.bar(m, x="brand", y="content_score", title="Content engine score (0-6): case studies, blog, "
                           "whitepapers, testimonials, logos, podcast/newsletter"), width="stretch")
    st.plotly_chart(px.bar(m, x="brand", y="industries_n", title="Industries listed (breadth vs. focus)"), width="stretch")
    st.dataframe(b[["brand", "years_claimed", "team_claimed", "projects_claim_text", "rating_claim", "partner_badges",
                    "compliance_listed", "awards_mentioned"]], hide_index=True, width="stretch")
    st.dataframe(b[["brand"] + A.CONTENT_COLS], hide_index=True, width="stretch")

with tabs[5]:
    if k["n_brands"] < 3:
        st.info("Select at least 3 brands to generate recommendations.")
    else:
        st.caption("Hypotheses derived from the selected brands. Each needs testing; none is a proven result.")
        for p in A.gtm_plan(k, m, b):
            st.subheader(p["title"])
            st.write(f"**Evidence:** {p['evidence']}")
            st.write(f"**Recommendation:** {p['recommendation']}")
            st.write(f"**Test:** {p['test']}  \n**Metric:** {p['metric']}")
            st.caption(f"Caveat: {p['caveat']}")

with tabs[6]:
    st.dataframe(b[["brand", "source_url", "confidence", "notes"]], hide_index=True, width="stretch")
    st.subheader("Known data gaps")
    st.dataframe(gaps, hide_index=True, width="stretch")
