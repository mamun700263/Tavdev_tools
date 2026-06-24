import os
from typing import Any, List, Optional

import gspread
import pandas as pd
from dotenv import load_dotenv
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
# from app.core import #logger

# Load environment variables
load_dotenv()
#logger = #logger.get_#logger(__name__, "Data_Exporters")
import os
import base64
import json

import datetime

creds_b64 = os.getenv("GOOGLE_CREDS_B64")

if not creds_b64:
    raise ValueError("Missing GOOGLE_CREDS_B64")

try:
    decoded = base64.b64decode(creds_b64 + "==").decode("utf-8")
    creds_json = json.loads(decoded)
except Exception as e:
    raise RuntimeError(f"Invalid GOOGLE_CREDS_B64: {e}")


class GoogleSheetPusher:
    def __init__(self, spreadsheet_name: Optional[str] = None):
        self.scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        self.spreadsheet_name = spreadsheet_name or os.getenv("GOOGLE_SPREADSHEET_NAME")

        if not self.spreadsheet_name:
            raise ValueError("Spreadsheet name required")

        self.client = self._authorize()
        self.sheet = self._open_spreadsheet()

    def _authorize(self):
        try:
            creds = Credentials.from_service_account_info(
                creds_json,
                scopes=self.scope
            )
            #logger.info("✅ Google Sheets authorized successfully.")
            print("✅ Google Sheets authorized successfully.")
            return gspread.authorize(creds)
        except Exception as e:
            #logger.error(f"❌ Auth failed: {e}")
            raise

    def _open_spreadsheet(self):
        try:
            return self.client.open(self.spreadsheet_name)
        except Exception as e:
            #logger.error(f"❌ Cannot open spreadsheet '{self.spreadsheet_name}': {e}")
            print(f"❌ Cannot open spreadsheet '{self.spreadsheet_name}': {e}")
            raise

    def _get_or_create_sheet(self, sheet_name: str, rows=1000, cols=26):
        try:
            return self.sheet.worksheet(sheet_name)
        except gspread.WorksheetNotFound:
            #logger.info(f"➕ Creating worksheet: {sheet_name}")
            print(f"➕ Creating worksheet: {sheet_name}")
            return self.sheet.add_worksheet(
                title=sheet_name, rows=str(rows), cols=str(cols)
            )

    def push_dataframe(self, df: pd.DataFrame, sheet_name: str, clear=True):
        try:
            ws = self._get_or_create_sheet(sheet_name)
            if clear:
                ws.clear()
                #logger.info("🧹 Cleared worksheet before pushing.")
                print("🧹 Cleared worksheet before pushing.")
            set_with_dataframe(ws, df)
            #logger.info(f"✅ DataFrame pushed to '{sheet_name}'")
            print(f"✅ DataFrame pushed to '{sheet_name}'")
        except Exception as e:
            #logger.error(f"❌ Failed to push DataFrame: {e}")
            print(f"❌ Failed to push DataFrame: {e}")

    def append_dataframe(self, df: pd.DataFrame, sheet_name: str):
        try:
            ws = self._get_or_create_sheet(sheet_name)
            existing = ws.get_all_values()
            start_row = len(existing) + 1
            set_with_dataframe(ws, df, row=start_row)
            #logger.info(f"📤 Appended DataFrame at row {start_row}")
            print(f"📤 Appended DataFrame at row {start_row}")
        except Exception as e:
            #logger.error(f"❌ Failed to append DataFrame: {e}")
            print(f"❌ Failed to append DataFrame: {e}")

    def append_row(self, row: dict, sheet_name: str):
        try:
            ws = self._get_or_create_sheet(sheet_name)

            def serialize(v):
                if v is None:
                    return ""
                if hasattr(v, "isoformat"):  # datetime, date, etc.
                    return v.isoformat()
                return v
            columns = list(row.keys())
            ordered_row = [serialize(row.get(col)) for col in columns]

            ws.append_row(ordered_row)

            print(f"📤 Row appended to '{sheet_name}': {ordered_row}")

        except Exception as e:
            print(f"❌ Failed to append row: {e}")
            raise
    def append_rows(self, rows: List[List[Any]], sheet_name: str):
        try:
            ws = self._get_or_create_sheet(sheet_name)
            ws.append_rows(rows)
            #logger.info(f"📤 {len(rows)} rows appended to '{sheet_name}'")
            print(f"📤 {len(rows)} rows appended to '{sheet_name}'")
        except Exception as e:
            #logger.error(f"❌ Failed to append rows: {e}")
            print(f"❌ Failed to append rows: {e}")

    def update_cell(self, sheet_name: str, row: int, col: int, value: Any):
        try:
            ws = self._get_or_create_sheet(sheet_name)
            ws.update_cell(row, col, value)
            #logger.info(f"✏️ Cell ({row},{col}) updated with '{value}'")
            print(f"✏️ Cell ({row},{col}) updated with '{value}'")
        except Exception as e:
            #logger.error(f"❌ Failed to update cell: {e}")
            print(f"❌ Failed to update cell: {e}")

    def read_sheet_as_df(self, sheet_name: str) -> Optional[pd.DataFrame]:
        try:
            ws = self._get_or_create_sheet(sheet_name)
            df = get_as_dataframe(ws, evaluate_formulas=True, dtype=str).dropna(
                how="all"
            )
            #logger.info(f"📥 Sheet '{sheet_name}' read into DataFrame.")
            print(f"📥 Sheet '{sheet_name}' read into DataFrame.")
            return df
        except Exception as e:
            #logger.error(f"❌ Failed to read sheet: {e}")
            print(f"❌ Failed to read sheet: {e}")
            return None

    def get_headers(self, sheet_name: str) -> List[str]:
        try:
            ws = self._get_or_create_sheet(sheet_name)
            headers = ws.row_values(1)
            #logger.info(f"📋 Headers for '{sheet_name}': {headers}")
            print(f"📋 Headers for '{sheet_name}': {headers}")
            return headers
        except Exception as e:
            #logger.error(f"❌ Failed to fetch headers: {e}")
            print(f"❌ Failed to fetch headers: {e}")
            return []

    def delete_worksheet(self, sheet_name: str):
        try:
            ws = self.sheet.worksheet(sheet_name)
            self.sheet.del_worksheet(ws)
            #logger.info(f"🗑️ Deleted worksheet: {sheet_name}")
            print(f"🗑️ Deleted worksheet: {sheet_name}")
        except Exception as e:
            #logger.error(f"❌ Failed to delete worksheet: {e}")
            print(f"❌ Failed to delete worksheet: {e}")
