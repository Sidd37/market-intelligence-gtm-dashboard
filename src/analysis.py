"""Competitive benchmark of 7 software-engineering-services firms from public homepages.
Built to support B2B lead-generation / GTM decisions (see README for limits)."""
import json
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from themes import GROUPS, theme_names, theme_hits

ROOT = Path(__file__).resolve().parents[1]
RAW, OUT, FIG = ROOT / "data/raw", ROOT / "data/processed", ROOT / "reports/figures"
CONTENT_COLS = ["case_studies", "blog", "whitepapers", "testimonials", "client_logos", "podcast_newsletter"]
CONTENT_SCORE = {"Yes": 1.0, "Partial": 0.5}


def load():
    return pd.read_csv(RAW / "brands.csv"), pd.read_csv(RAW / "data_gaps.csv")


def n_items(s):
    return 0 if pd.isna(s) or str(s).strip() == "" else len([x for x in str(s).split(";") if x.strip()])


def group_text(row, group):
    return " ".join("" if pd.isna(row[c]) else str(row[c]) for c in GROUPS[group]["columns"])


def theme_matrix(brands, group):
    rows = []
    for _, r in brands.iterrows():
        hits = theme_hits(group, group_text(r, group))
        rows.append({"brand": r.brand, **{t: int(v > 0) for t, v in hits.items()}})
    return pd.DataFrame(rows)


def metrics(brands):
    m = pd.DataFrame({"brand": brands.brand})
    m["industries_n"] = brands.industries.map(n_items)
    m["engagement_n"] = brands.engagement_models.map(n_items)
    m["cta_n"] = brands.primary_ctas.map(n_items)
    m["partner_n"] = brands.partner_badges.map(n_items)
    m["compliance_n"] = brands.compliance_listed.map(n_items)
    m["content_score"] = sum(brands[c].map(CONTENT_SCORE).fillna(0.0) for c in CONTENT_COLS)
    m["publishes_rate"] = brands.rate_low_usd_hr.notna().map({True: "Yes", False: "No"})
    m["years_claimed"] = brands.years_claimed
    m["team_claimed"] = brands.team_claimed
    return m


def key_numbers(brands, pos, cta, eng, m):
    def s(df, col): return int(df[col].sum())
    return {
        "n_brands": len(brands),
        "ai_led": s(pos, "AI-led"), "vertical_headline": s(pos, "Vertical focus"),
        "publish_rate": int((m.publishes_rate == "Yes").sum()),
        "call_cta": s(cta, "Book a call / consult"), "quote_cta": s(cta, "Get a quote / estimate"),
        "hire_cta": s(cta, "Hire talent"), "proof_cta": s(cta, "Show proof"), "nda_cta": s(cta, "NDA-first trust"),
        "case_yes": int((brands.case_studies == "Yes").sum()),
        "whitepaper_yes": int((brands.whitepapers == "Yes").sum()),
        "podcast_yes": int((brands.podcast_newsletter == "Yes").sum()),
        "clutch_cited": int(brands.rating_claim.fillna("").str.contains("Clutch").sum()),
        "dedicated_team": s(eng, "Dedicated team"), "fixed_price": s(eng, "Fixed price"),
        "median_industries": float(m.industries_n.median()), "median_content": float(m.content_score.median()),
    }


def gtm_plan(k, m, brands):
    n = k["n_brands"]
    lo, hi = int(m.industries_n.min()), int(m.industries_n.max())
    return [
        {"title": "Positioning: AI is table stakes, a specific outcome or vertical is not",
         "evidence": f"{k['ai_led']}/{n} headlines lead with AI; only {k['vertical_headline']}/{n} name a vertical.",
         "recommendation": "Do not make 'AI' the whole headline. Lead with the problem solved for one named buyer, with AI as the how.",
         "test": "A/B two homepage headlines: AI-led vs. outcome/vertical-led.",
         "metric": "Click-through on the main CTA; booked calls per 100 visitors.",
         "caveat": "Homepage headline + subheadline only; says nothing about performance."},
        {"title": "Pricing: almost nobody shows a number",
         "evidence": f"{k['publish_rate']}/{n} brands publish any rate; the rest hide pricing behind a quote.",
         "recommendation": "A 'typical engagement' guide (ranges by team size or scope) can act as trust-builder and lead magnet.",
         "test": "Gated vs. ungated pricing guide.",
         "metric": "Pricing-page visit to qualified-lead rate; sales-accepted lead rate.",
         "caveat": "The one published rate belongs to a healthcare-niche vendor; one data point."},
        {"title": "Lead capture: everyone says 'talk to us', few offer a smaller first step",
         "evidence": f"{k['call_cta']}/{n} push a call/consult CTA and {k['quote_cta']}/{n} an estimate; only {k['nda_cta']}/{n} offer an NDA-first step.",
         "recommendation": "Add a lower-commitment step beside the call CTA (estimate tool, scoping checklist, NDA-first intake).",
         "test": "Call CTA only vs. call CTA + estimate/checklist CTA.",
         "metric": "Total leads, and the share that become sales-qualified.",
         "caveat": "CTA text read from the homepage; placement and form design not captured."},
        {"title": "Content: case studies are the baseline, deeper assets are rare",
         "evidence": f"{k['case_yes']}/{n} show case studies, but only {k['whitepaper_yes']}/{n} show whitepapers and {k['podcast_yes']}/{n} a podcast or newsletter.",
         "recommendation": "Treat case studies as required. Differentiate with a technical point of view for one niche (gated whitepaper, newsletter).",
         "test": "Gate one whitepaper behind an email form; promote it on LinkedIn to the target buyer.",
         "metric": "Downloads, cost per lead, lead-to-call rate.",
         "caveat": "'Not found' means not seen on the homepage, not proven absent."},
        {"title": "Focus: breadth is the norm, a niche is rare",
         "evidence": f"Industries listed per firm range from {lo} to {hi} (median {k['median_industries']:g}); {k['vertical_headline']}/{n} headline a single vertical.",
         "recommendation": "Pick one or two verticals as the ideal customer profile and build proof for them.",
         "test": "Run a vertical-specific landing page against the generic one.",
         "metric": "Conversion by landing page; lead quality by segment.",
         "caveat": "Wingman's own verticals are not known; its site could not be read."},
        {"title": "Proof: borrowed credibility is common",
         "evidence": f"{k['clutch_cited']}/{n} cite a Clutch rating; partner badges per firm (median {float(m.partner_n.median()):g}).",
         "recommendation": "Collect and surface third-party reviews and partner status as trust signals.",
         "test": "Add review/badge strip near the primary CTA.",
         "metric": "CTA click-through before vs. after.",
         "caveat": "Ratings and badges are self-reported on each firm's own site."},
    ]


def figures(brands, m, pos):
    FIG.mkdir(parents=True, exist_ok=True)
    d = m.sort_values("content_score")
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(d.brand, d.content_score, color="#2b6cb0")
    ax.set_xlabel("Content engine score (0-6)"); ax.set_title("Proof & content assets seen on homepage")
    fig.tight_layout(); fig.savefig(FIG / "content_score.png", dpi=150); plt.close(fig)
    t = pos.set_index("brand")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.imshow(t.values, cmap="Blues", vmin=0, vmax=1.4, aspect="auto")
    ax.set_xticks(range(len(t.columns)), t.columns, rotation=40, ha="right")
    ax.set_yticks(range(len(t.index)), t.index); ax.set_title("Positioning themes (1 = keyword present)")
    fig.tight_layout(); fig.savefig(FIG / "positioning_themes.png", dpi=150); plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    brands, gaps = load()
    pos, cta, eng = (theme_matrix(brands, g) for g in ("positioning", "cta", "engagement"))
    m = metrics(brands); k = key_numbers(brands, pos, cta, eng, m); plan = gtm_plan(k, m, brands)
    for name, df in [("positioning", pos), ("cta", cta), ("engagement", eng), ("metrics", m)]:
        df.to_csv(OUT / f"{name}.csv", index=False)
    (OUT / "key_numbers.json").write_text(json.dumps(k, indent=2))
    (OUT / "gtm_plan.json").write_text(json.dumps(plan, indent=2))
    figures(brands, m, pos)
    md = ["# GTM insights (public homepages, accessed 2026-10-12)\n"]
    for p in plan:
        md.append(f"## {p['title']}\n- Evidence: {p['evidence']}\n- Recommendation: {p['recommendation']}\n"
                  f"- Test: {p['test']}\n- Metric: {p['metric']}\n- Caveat: {p['caveat']}\n")
    (ROOT / "reports/insights.md").write_text("\n".join(md))
    print(m.to_string()); print(json.dumps(k, indent=1))
    for df in (pos, cta, eng): print(df.to_string())


if __name__ == "__main__":
    main()
