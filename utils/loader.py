import pathlib
import sys
import pandas as pd

def clean_phone(x):
    s = str(x).replace(" ", "").replace("+", "")
    if not s.startswith("91"):
        s = "91" + s
    return "".join(ch for ch in s if ch.isdigit())

def load_contacts(path: str) -> pd.DataFrame:
    path_obj = pathlib.Path(path)
    if not path_obj.exists():
        print(f"ERROR: Contacts file not found: {path}")
        sys.exit(1)

    if path_obj.suffix.lower() in [".xlsx", ".xls"]:
        df = pd.read_excel(path_obj, engine="openpyxl")
    elif path_obj.suffix.lower() == ".csv":
        df = pd.read_csv(path_obj, encoding='utf-8')
    else:
        print("ERROR: Use .xlsx or .csv for contacts.")
        sys.exit(1)

    cols = {c.lower().strip(): c for c in df.columns}
    for r in ["name", "phone"]:
        if r not in cols:
            print(f"ERROR: Missing required column: {r}")
            sys.exit(1)

    std = pd.DataFrame()
    std["name"] = df[cols["name"]].astype(str).fillna("").str.strip()
    std["phone"] = df[cols["phone"]].map(clean_phone)
    std["message"] = df[cols.get("message", "")].fillna("").astype(str) if "message" in cols else ""
    std["attachment"] = df[cols.get("attachment", "")].fillna("").astype(str) if "attachment" in cols else ""
    std = std[std["phone"].str.len() >= 8].reset_index(drop=True)
    return std
