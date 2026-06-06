# This code is dedicated to standardizing the dataset we are given.

import pandas as pd
import numpy as np
'''import the pandas and numpy packages, and naming them the terms 'pd' and 'np' respectively'''

def _clean_text_series(s: pd.Series) -> pd.Series:
    return (
        s.astype("string")
        .str.strip()
        .str.lower()
    )
'''cleans up data entries by standardizing capitalization'''

def _clean_drug_name_series(s: pd.Series) -> pd.Series:
    return (
        _clean_text_series(s)
        .str.replace(r"\s+\d+\s*(mg|mcg|g|ml)\b", "", regex=True)
        .str.replace(r"\s*(hcl)\b", "", regex=True)
        .str.strip()
    )
'''cleans up dataset by removing dosage (mg, ml, etc.) and formulation (in this case, only hcl)'''

def _to_numeric_clean(s: pd.Series) -> pd.Series:
    cleaned = (
        s.astype(str)
        .str.replace(r"[\$,]", "", regex=True)
        .str.strip()
        .str.extract(r"(-?\d+(?:\.\d+)?)", expand=False)
    )
    return pd.to_numeric(cleaned, errors="coerce")
'''cleans dataset by removing unnecessary symbols such as $ \ , etc. while also extracting a raw number value'''

def clean_prescription_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Standardize column names
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
'''standardizes columns by replacing spaces and dashes with an underscore'''

    df = df.replace(["", " ", "None", "NA", "N/A", "null"], np.nan)
    #########################
'''standardizes empty values into "NaN"'''
    #TODO: clean patient_id
    df["patient_id"] = _clean_text_series(df["patient_id"]).str.upper()
'''Runs the text standardization code from above'''
    #TODO: clean fill_date
    df["fill_date"] = pd.to_datetime(df["fill_date"], errors="coerce", format="mixed")
'''standardizes dates into a single date format'''
    #TODO: clean drug_name
    df["drug_name"] = _clean_drug_name_series(df["drug_name"])
'''Runs the drug name standardization code from above'''
    #TODO: clean days_supply
    df["days_supply"] = _to_numeric_clean(df["days_supply"])
    df.loc[df["days_supply"] <=0, "days_supply"] = np.nan
'''Runs the symbol removal and number extractor code from above'''
    #TODO: clean quantity_dispensed
    df["quantity_dispensed"] = _to_numeric_clean(df["quantity_dispensed"])
    df.loc[df["quantity_dispensed"] <=0, "quantity_dispensed"] = np.nan
'''Runs the symbol removal and number extractor code from above'''
    #TODO: clean refill_number
    df["refill_number"] = _to_numeric_clean(df["refill_number"])
    df.loc[df["refill_number"] < 0, "refill_number"] = np.nan
'''Runs the symbol removal and number extractor code from above'''
    #TODO: clean patient_age
    df["patient_age"] = _to_numeric_clean(df["patient_age"])
    df.loc[(df["patient_age"] < 0) | (df["patient_age"] > 120), "patient_age"] = np.nan
'''Runs the symbol removal and number extractor code from above'''
    #TODO: clean sex
    df["sex"] = _clean_text_series(df["sex"]).replace({"m" : "male", "f" : "female"})
'''Runs the text standardization code from above'''
    #TODO: zip_code
    df["zip_code"] = _clean_text_series(df["zip_code"])
'''Runs the text standardization code from above'''
    #TODO: prescriber_id
    df["prescriber_id"] = _clean_text_series(df["prescriber_id"]).str.upper()
'''Runs the text standardization code from above'''
    #TODO: pharmacy_name
    df["pharmacy_name"] = _clean_text_series(df["pharmacy_name"])
    df["pharmacy_name"] = df["pharmacy_name"].str.replace(r"#\d+$", "", regex = True).str.strip()
    df["pharmacy_name"] = df["pharmacy_name"].replace({"csv pharmacy" : "cvs", "csv" : "cvs", "walgreens pharmacy" : "walgreens", "cvs pharmacy" : "cvs"})
'''Runs the text standardization code from above'''
    #TODO: copay_amount
    df["copay_amount"] = _to_numeric_clean(df["copay_amount"])
    df.loc[df["copay_amount"] < 0, "copay_amount"] = np.nan
'''Runs the symbol removal and number extractor code from above'''
    #TODO: adherence_flag
    df["adherence_flag"] = _to_numeric_clean(df["adherence_flag"])
    df.loc[~df["adherence_flag"].isin([0, 1])] = np.nan
'''Runs the symbol removal and number extractor code from above'''
    #TODO: proportion_days_covered (pdc)
    df["proportion_days_covered"] = _to_numeric_clean(df["proportion_days_covered"])
    df.loc[
            (df["proportion_days_covered"] < 0) | (df["proportion_days_covered"] > 1), 
            "proportion_days_covered"
        ] = np.nan
'''Runs the symbol removal and number extractor code from above'''
    #########################

    #TODO: Drop all duplicate rows
    df = df.drop_duplicates()

    #TODO: Drop rows if missing critical fields: "patient_id", "fill_date", "drug_name"
    critical_cols = ["patient_id", "fill_date", "drug_name"]
    df = df.dropna(subset=critical_cols)

    #TODO: Sort by "patient_id", "fill_date"
    sort_cols = ["patient_id", "fill_date"]
    df = df.sort_values(sort_cols)

    df = df.reset_index(drop=True)

    return df
