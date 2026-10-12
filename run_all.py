"""Rebuild everything: analysis -> Excel -> checks. Run from the repo root: python run_all.py"""
import subprocess, sys
steps = [[sys.executable, "src/analysis.py"], [sys.executable, "src/build_excel.py"]]
for s in steps:
    subprocess.run(s, check=True)
print("\nDone. Open excel/gtm_workbook.xlsx or run: streamlit run app/dashboard.py")
