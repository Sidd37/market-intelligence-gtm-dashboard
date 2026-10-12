# Market Intelligence & GTM Dashboard: Software Engineering Services

A competitive-intelligence dashboard for **B2B lead generation and go-to-market (GTM) decisions** in software engineering services. It benchmarks seven firms on **positioning, lead-capture funnel, pricing transparency, engagement models, proof and content**, then turns the gaps into testable GTM hypotheses. Built with **Python, Excel and Streamlit**.

**Firms:** Simform, Appinventiv, Hyperlink InfoSystem, Space-O (healthcare site), Intellectsoft, Netguru, Thoughtworks.
**Data:** each firm's own homepage, accessed **2026-10-12**. Every row carries `source_url`, `date_accessed` and a `confidence` level.

## Questions it answers
- How do firms position themselves, and what is crowded vs. open? (7/7 lead with AI; 2/7 name a vertical)
- How do they capture leads? (call vs. quote vs. NDA-first vs. proof CTAs)
- Who shows pricing? (1/7)
- What proof and content assets back them up?
- What should a firm of this type test next? (GTM plan tab: evidence, recommendation, test, metric, caveat)

## Run it
```
pip install -r requirements.txt
streamlit run app/dashboard.py       # interactive dashboard
python run_all.py                    # optional: rebuild analysis outputs + Excel workbook
python tests/test_app.py             # dashboard edge cases (empty selection, filters)
python tests/test_parity.py          # Excel values == Python values (on the recalculated workbook)
```
`excel/gtm_workbook.xlsx` is formula-driven (blue = sourced input, black = formula). Pick a brand on the **Dashboard** sheet; edit keywords on **Positioning / CTA Funnel / Engagement** to re-run the detection. The parity test needs the workbook's saved values; the shipped file has them, a file rebuilt by `run_all.py` gets them once opened and saved in Excel.

## Data rules
- Official pages only. A value not seen on the page is left **blank**, never filled in.
- Core stats (years, team, ratings, CTAs) were fetched twice for 5 of 7 firms; the confidence column records this.
- Years, team sizes, ratings, badges and awards are the firms' own **claims**, not verified data. Netguru's page contradicts itself (recorded in notes).
- "Not found" means not seen in the homepage text, not proven absent.
- Themes are keyword matches (rules in `src/themes.py`, mirrored by Excel formulas).

## Limits
- **Wingman Partners is not in the dataset**: its own site is JavaScript-rendered and could not be read. The GTM plan is framed for a firm of its type, not for Wingman specifically.
- iMOBDEV (robots-disallowed) and Fablian Technolab (domain redirect, identity unconfirmed) were excluded.
- Homepages only, read via a page-fetch summarizer: spot-check quotes against the live pages.
- Not collected: traffic, SEO, ad spend, LinkedIn activity, review-site text, win rates, revenue. This is a public-homepage benchmark, not market research.
- GTM recommendations are hypotheses to test, not results.

## Layout
```
data/raw/        brands.csv (sourced), data_gaps.csv
data/processed/  generated outputs
src/             analysis.py, themes.py, build_excel.py
app/             dashboard.py (Streamlit)
excel/           gtm_workbook.xlsx
reports/         insights.md, figures/
tests/           app + parity tests
```
