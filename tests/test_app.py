import pathlib
from streamlit.testing.v1 import AppTest
at = AppTest.from_file(str(pathlib.Path(__file__).resolve().parents[1] / "app/dashboard.py"), default_timeout=60).run()
assert not at.exception, at.exception
print("default ok; tabs:", len(at.tabs), "metrics:", [m.value for m in at.metric])
def run(label, ms=None, conf=None, focus=None):
    if ms is not None: at.sidebar.multiselect[0].set_value(ms)
    if conf is not None: at.sidebar.multiselect[1].set_value(conf)
    if focus is not None: at.sidebar.radio[0].set_value(focus)
    at.run(); assert not at.exception, (label, at.exception); print(label, "ok", [m.value for m in at.metric], len(at.warning), "warn")
run("single brand", ms=["Netguru"])
run("two brands (no plan)", ms=["Netguru", "Simform"])
run("empty brands", ms=[])
assert at.warning
run("all brands", ms=list(at.sidebar.multiselect[0].options))
run("medium only", conf=["Medium"])
run("no confidence", conf=[])
run("reset conf", conf=["High", "Medium"])
run("specialists", focus="Vertical specialists")
run("generalists", focus="Generalists")
run("generalists no-rate case", ms=["Simform", "Appinventiv", "Hyperlink InfoSystem"], focus="Generalists")
