import calendar
import os
import sqlite3
from datetime import date

import pandas as pd
import streamlit as st


st.set_page_config(page_title="Ride Hero", layout="wide")
st.markdown("""
    <style>
        :root {
            --rh-bg: #071014;
            --rh-panel: #0d191f;
            --rh-panel-soft: #11242c;
            --rh-border: rgba(151, 179, 166, 0.18);
            --rh-text: #edf7f2;
            --rh-muted: #9fb2ab;
            --rh-accent: #39d98a;
            --rh-accent-2: #5cc8ff;
            --rh-danger: #ff6b6b;
            --rh-warning: #ffd166;
        }

        html, body, [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #061014 0%, #08161b 48%, #0b171d 100%);
            color: var(--rh-text);
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        [data-testid="stHeader"] {
            background: rgba(7, 16, 20, 0.72);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid rgba(151, 179, 166, 0.10);
        }

        .block-container {
            max-width: 1280px;
            padding: 2rem 2.5rem 3rem;
            margin: auto;
        }

        .ride-hero-header {
            border: 1px solid var(--rh-border);
            background:
                linear-gradient(135deg, rgba(57, 217, 138, 0.12), rgba(92, 200, 255, 0.06)),
                rgba(13, 25, 31, 0.92);
            border-radius: 8px;
            padding: 1.35rem 1.5rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 24px 60px rgba(0, 0, 0, 0.28);
        }

        .ride-hero-eyebrow {
            color: var(--rh-accent);
            font-size: 0.76rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            margin-bottom: 0.35rem;
            text-transform: uppercase;
        }

        .ride-hero-title {
            color: var(--rh-text);
            font-size: 2.15rem;
            font-weight: 850;
            line-height: 1.1;
            margin: 0;
        }

        .ride-hero-subtitle {
            color: var(--rh-muted);
            font-size: 1rem;
            margin: 0.55rem 0 0;
        }

        .welcome-shell {
            min-height: calc(100vh - 7rem);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem 0;
        }

        .welcome-card {
            width: min(920px, 100%);
            border: 1px solid var(--rh-border);
            background:
                linear-gradient(135deg, rgba(57, 217, 138, 0.13), rgba(92, 200, 255, 0.07)),
                rgba(13, 25, 31, 0.94);
            border-radius: 8px;
            padding: 2rem;
            box-shadow: 0 28px 70px rgba(0, 0, 0, 0.34);
        }

        .welcome-logo {
            width: 3.6rem;
            height: 3.6rem;
            display: grid;
            place-items: center;
            border: 1px solid rgba(57, 217, 138, 0.35);
            border-radius: 8px;
            background: rgba(57, 217, 138, 0.10);
            color: var(--rh-accent);
            font-weight: 900;
            font-size: 1.25rem;
            margin-bottom: 1.2rem;
        }

        .welcome-title {
            color: var(--rh-text);
            font-size: 3rem;
            font-weight: 900;
            line-height: 1;
            margin: 0;
        }

        .welcome-tagline {
            color: var(--rh-accent);
            font-size: 1.1rem;
            font-weight: 800;
            margin: 0.85rem 0 0;
        }

        .welcome-copy {
            color: var(--rh-muted);
            font-size: 1.03rem;
            max-width: 46rem;
            margin: 1rem 0 1.35rem;
        }

        .welcome-grid {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 0.75rem;
            margin: 1.4rem 0 1.8rem;
        }

        .welcome-feature {
            border: 1px solid rgba(151, 179, 166, 0.15);
            background: rgba(7, 16, 20, 0.38);
            border-radius: 8px;
            color: var(--rh-text);
            font-size: 0.9rem;
            font-weight: 750;
            padding: 0.9rem;
            min-height: 4.25rem;
        }

        h1, h2, h3, h4, h5, h6,
        [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3 {
            color: var(--rh-text);
            letter-spacing: 0;
        }

        [data-testid="stMarkdownContainer"] p,
        [data-testid="stCaptionContainer"],
        label, .st-emotion-cache-1dj0hjr {
            color: var(--rh-muted);
        }

        div[data-testid="stTabs"] {
            margin-top: 0.35rem;
        }

        div[data-testid="stTabs"] button {
            color: var(--rh-muted);
            border-radius: 8px 8px 0 0;
            font-weight: 700;
            padding: 0.75rem 1rem;
        }

        div[data-testid="stTabs"] button[aria-selected="true"] {
            color: var(--rh-text);
            background: rgba(57, 217, 138, 0.08);
            border-bottom-color: var(--rh-accent);
        }

        div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"],
        div[data-testid="stForm"],
        div[data-testid="stExpander"],
        [data-testid="stMetric"],
        [data-testid="stDataFrame"] {
            background: rgba(13, 25, 31, 0.86);
            border: 1px solid var(--rh-border);
            border-radius: 8px;
            box-shadow: 0 18px 48px rgba(0, 0, 0, 0.18);
        }

        div[data-testid="stForm"] {
            padding: 1rem;
        }

        [data-testid="stMetric"] {
            padding: 1rem;
        }

        [data-testid="stMetricLabel"] p {
            color: var(--rh-muted);
            font-weight: 700;
        }

        [data-testid="stMetricValue"] {
            color: var(--rh-text);
            font-weight: 850;
        }

        [data-testid="stAlert"] {
            border-radius: 8px;
            border: 1px solid rgba(151, 179, 166, 0.16);
            background: rgba(17, 36, 44, 0.92);
        }

        [data-baseweb="input"] > div,
        [data-baseweb="select"] > div,
        [data-baseweb="textarea"] > div,
        [data-baseweb="base-input"],
        textarea,
        input {
            background-color: #0a151a !important;
            border-color: rgba(151, 179, 166, 0.24) !important;
            color: var(--rh-text) !important;
            border-radius: 8px !important;
        }

        [data-baseweb="input"]:focus-within > div,
        [data-baseweb="select"]:focus-within > div,
        [data-baseweb="textarea"]:focus-within > div {
            border-color: var(--rh-accent) !important;
            box-shadow: 0 0 0 1px rgba(57, 217, 138, 0.38) !important;
        }

        .stButton > button,
        .stFormSubmitButton > button {
            width: 100%;
            border: 1px solid rgba(57, 217, 138, 0.42);
            border-radius: 8px;
            background: linear-gradient(135deg, #31c77f 0%, #1f9d70 100%);
            color: #04100b;
            font-weight: 850;
            min-height: 2.75rem;
            box-shadow: 0 10px 26px rgba(57, 217, 138, 0.20);
        }

        .stButton > button:hover,
        .stFormSubmitButton > button:hover {
            border-color: rgba(92, 200, 255, 0.56);
            color: #03100b;
            transform: translateY(-1px);
        }

        [data-testid="stDataFrame"] {
            overflow: hidden;
        }

        hr {
            border-color: rgba(151, 179, 166, 0.14);
        }

        a {
            color: var(--rh-accent-2) !important;
            font-weight: 700;
            text-decoration: none;
        }

        @media (max-width: 760px) {
            .block-container {
                padding: 1rem 0.85rem 2rem;
            }

            .ride-hero-header {
                padding: 1rem;
            }

            .ride-hero-title {
                font-size: 1.7rem;
            }

            .welcome-shell {
                min-height: auto;
                padding: 0.75rem 0 1.5rem;
            }

            .welcome-card {
                padding: 1.15rem;
            }

            .welcome-title {
                font-size: 2.15rem;
            }

            .welcome-grid {
                grid-template-columns: 1fr;
            }

            div[data-testid="stTabs"] button {
                padding: 0.65rem 0.55rem;
                font-size: 0.86rem;
            }
        }
    </style>
""", unsafe_allow_html=True)


# --- Database layer ---
DB_PATH = "data.db"
DB_BACKEND = os.getenv("RIDE_HERO_DB_BACKEND", "sqlite").lower()
SUPABASE_TABLE = "records"

RECORD_COLUMNS = {
    "entry_date": "TEXT",
    "income": "REAL DEFAULT 0",
    "fuel": "REAL DEFAULT 0",
    "toll": "REAL DEFAULT 0",
    "maintenance": "REAL DEFAULT 0",
    "food": "REAL DEFAULT 0",
    "other": "REAL DEFAULT 0",
    "miles": "REAL DEFAULT 0",
    "start_time": "TEXT",
    "end_time": "TEXT",
    "platform": "TEXT",
}


def record_payload(entry_date, income, fuel, toll, maintenance, food, other, miles, start_time, end_time, platform):
    """Create one normalized record payload shared by SQLite and future Supabase writes."""
    return {
        "entry_date": entry_date.isoformat() if hasattr(entry_date, "isoformat") else entry_date,
        "income": income,
        "fuel": fuel,
        "toll": toll,
        "maintenance": maintenance,
        "food": food,
        "other": other,
        "miles": miles,
        "start_time": start_time,
        "end_time": end_time,
        "platform": platform,
    }


class SQLiteDatabase:
    """Local database backend. Kept as the default until Supabase is enabled."""

    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)

    def _column_names(self):
        return [
            row[1]
            for row in self.conn.execute("PRAGMA table_info(records)").fetchall()
        ]

    def _create_records_table(self, table_name="records"):
        columns_sql = ",\n                ".join(
            f"{column_name} {column_type}"
            for column_name, column_type in RECORD_COLUMNS.items()
        )
        self.conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {columns_sql}
            )
            """
        )

    def init(self):
        """Create or migrate the records table without deleting saved entries."""
        with self.conn:
            table_exists = self.conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'records'"
            ).fetchone()

            if not table_exists:
                self._create_records_table()
                return

            existing_columns = self._column_names()

            # Older versions saved records without an ID. Rebuild the table once so
            # Streamlit can reliably delete by ID while preserving existing rows.
            if "id" not in existing_columns:
                self.conn.execute("DROP TABLE IF EXISTS records_migrated")
                self._create_records_table("records_migrated")
                shared_columns = [
                    column_name
                    for column_name in RECORD_COLUMNS
                    if column_name in existing_columns
                ]
                if shared_columns:
                    columns_sql = ", ".join(shared_columns)
                    self.conn.execute(
                        f"""
                        INSERT INTO records_migrated ({columns_sql})
                        SELECT {columns_sql}
                        FROM records
                        """
                    )
                self.conn.execute("DROP TABLE records")
                self.conn.execute("ALTER TABLE records_migrated RENAME TO records")
                existing_columns = self._column_names()

            for column_name, column_type in RECORD_COLUMNS.items():
                if column_name not in existing_columns:
                    self.conn.execute(
                        f"ALTER TABLE records ADD COLUMN {column_name} {column_type}"
                    )

    def add_record(self, payload):
        """Insert one earnings record and commit immediately."""
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO records (
                    entry_date,
                    income,
                    fuel,
                    toll,
                    maintenance,
                    food,
                    other,
                    miles,
                    start_time,
                    end_time,
                    platform
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload["entry_date"],
                    payload["income"],
                    payload["fuel"],
                    payload["toll"],
                    payload["maintenance"],
                    payload["food"],
                    payload["other"],
                    payload["miles"],
                    payload["start_time"],
                    payload["end_time"],
                    payload["platform"],
                ),
            )

    def delete_record(self, record_id):
        """Delete one earnings record by ID."""
        with self.conn:
            result = self.conn.execute(
                "DELETE FROM records WHERE id = ?",
                (int(record_id),),
            )
        return result.rowcount > 0

    def get_records(self):
        return pd.read_sql(
            "SELECT * FROM records ORDER BY entry_date DESC, id DESC",
            self.conn,
        )


def get_config_value(name, default=None):
    """Read settings from Streamlit secrets first, then environment variables."""
    try:
        return st.secrets.get(name, os.getenv(name, default))
    except Exception:
        return os.getenv(name, default)


class SupabaseDatabase:
    """Optional Supabase backend with the same interface as SQLiteDatabase."""

    def __init__(self):
        try:
            from supabase import create_client
        except ImportError as exc:
            raise RuntimeError(
                "Supabase backend selected, but the 'supabase' package is not installed. "
                "Add supabase to requirements before enabling RIDE_HERO_DB_BACKEND=supabase."
            ) from exc

        supabase_url = get_config_value("SUPABASE_URL")
        supabase_key = (
            get_config_value("SUPABASE_SERVICE_ROLE_KEY")
            or get_config_value("SUPABASE_ANON_KEY")
        )

        if not supabase_url or not supabase_key:
            raise RuntimeError(
                "Supabase backend selected, but SUPABASE_URL and a Supabase key are missing."
            )

        self.client = create_client(supabase_url, supabase_key)
        self.table_name = get_config_value("SUPABASE_TABLE", SUPABASE_TABLE)

    def init(self):
        """Supabase schema is managed outside the app with SQL migrations."""
        return None

    def add_record(self, payload):
        self.client.table(self.table_name).insert(payload).execute()

    def delete_record(self, record_id):
        response = (
            self.client.table(self.table_name)
            .delete()
            .eq("id", int(record_id))
            .execute()
        )
        return bool(getattr(response, "data", None))

    def get_records(self):
        response = (
            self.client.table(self.table_name)
            .select("*")
            .order("entry_date", desc=True)
            .order("id", desc=True)
            .execute()
        )
        return pd.DataFrame(getattr(response, "data", []) or [])


def get_database():
    """Select the active database backend. SQLite remains the safe local default."""
    if DB_BACKEND == "supabase":
        return SupabaseDatabase()
    return SQLiteDatabase(DB_PATH)


db = get_database()


def init_db():
    db.init()


def add_record(entry_date, income, fuel, toll, maintenance, food, other, miles, start_time, end_time, platform):
    db.add_record(
        record_payload(
            entry_date,
            income,
            fuel,
            toll,
            maintenance,
            food,
            other,
            miles,
            start_time,
            end_time,
            platform,
        )
    )


def delete_record(record_id):
    return db.delete_record(record_id)


def get_data():
    return db.get_records()


def prepare_records(df):
    """Normalize saved records for totals, display, and insights."""
    if df.empty:
        return df

    df = df.copy()
    df["entry_date"] = pd.to_datetime(df["entry_date"], errors="coerce")

    for column in ["income", "fuel", "toll", "maintenance", "food", "other", "miles"]:
        if column not in df.columns:
            df[column] = 0.0
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0.0)

    df["profit"] = df["income"] - (
        df["fuel"] + df["toll"] + df["maintenance"] + df["food"] + df["other"]
    )
    return df


def render_service_cards(items, fields):
    """Render service directory entries with consistent spacing."""
    for item in items:
        st.markdown(f"### {item['name']}")
        for label, key in fields:
            value = item.get(key)
            if isinstance(value, list):
                value = ", ".join(value)
            if value:
                st.write(f"**{label}:** {value}")
        if item.get("website"):
            st.markdown(f"[Visit Website]({item['website']})")
        st.divider()


def clear_entry_form():
    """Reset earnings entry widgets without touching saved database records."""
    for key in [
        "income_input",
        "fuel_input",
        "toll_input",
        "maintenance_input",
        "food_input",
        "other_input",
        "miles_input",
        "start_time_12hr",
        "end_time_12hr",
    ]:
        st.session_state.pop(key, None)


def current_platform_value():
    """Build the active platform label from Streamlit widget state."""
    selected_companies = st.session_state.get("selected_companies", [])
    custom_company = st.session_state.get("custom_company_input", "").strip()
    platform_list = list(selected_companies)

    if custom_company:
        platform_list.append(custom_company)

    return ", ".join(dict.fromkeys(platform_list))


def draft_entry_signature(platform):
    """Identify the current draft so platform switching does not duplicate a manual save."""
    return (
        st.session_state.get("entry_date_input", date.today()),
        st.session_state.get("income_input", 0.0),
        st.session_state.get("fuel_input", 0.0),
        st.session_state.get("toll_input", 0.0),
        st.session_state.get("maintenance_input", 0.0),
        st.session_state.get("food_input", 0.0),
        st.session_state.get("other_input", 0.0),
        st.session_state.get("miles_input", 0.0),
        st.session_state.get("start_time_12hr", "Optional"),
        st.session_state.get("end_time_12hr", "Optional"),
        platform,
    )


def save_current_entry_before_platform_switch():
    """Save a positive-income draft, then clear entry fields for the new platform."""
    new_platform = current_platform_value()
    previous_platform = st.session_state.get("active_platform")

    if previous_platform is None:
        st.session_state["active_platform"] = new_platform
        return

    if new_platform == previous_platform:
        return

    if st.session_state.get("income_input", 0.0) > 0:
        save_platform = previous_platform or new_platform
        signature = draft_entry_signature(save_platform)
        if signature != st.session_state.get("last_saved_entry_signature"):
            add_record(
                st.session_state.get("entry_date_input", date.today()),
                st.session_state.get("income_input", 0.0),
                st.session_state.get("fuel_input", 0.0),
                st.session_state.get("toll_input", 0.0),
                st.session_state.get("maintenance_input", 0.0),
                st.session_state.get("food_input", 0.0),
                st.session_state.get("other_input", 0.0),
                st.session_state.get("miles_input", 0.0),
                st.session_state.get("start_time_12hr", "Optional"),
                st.session_state.get("end_time_12hr", "Optional"),
                save_platform,
            )
            st.session_state["last_saved_entry_signature"] = signature
            st.session_state["platform_switch_saved"] = True

    for key in [
        "income_input",
        "fuel_input",
        "toll_input",
        "maintenance_input",
        "food_input",
        "other_input",
        "miles_input",
        "start_time_12hr",
        "end_time_12hr",
    ]:
        st.session_state.pop(key, None)

    st.session_state["active_platform"] = new_platform


def reset_entry_and_platform():
    """Clear the entry workflow and platform selection for a fresh manual start."""
    clear_entry_form()
    for key in [
        "custom_company_input",
        "selected_companies",
        "active_platform",
    ]:
        st.session_state.pop(key, None)


def enter_dashboard():
    """Persist the welcome-screen choice for the current Streamlit session."""
    st.session_state["ride_hero_dashboard_open"] = True


def render_welcome_page():
    """Premium first-run welcome screen before the main dashboard."""
    st.markdown(
        """
        <div class="welcome-shell">
            <div class="welcome-card">
                <div class="welcome-logo">RH</div>
                <h1 class="welcome-title">Ride Hero</h1>
                <p class="welcome-tagline">Built by a driver, for drivers.</p>
                <p class="welcome-copy">
                    A focused command center for FHV drivers to understand daily profit,
                    stay ahead of obligations, and make better driving decisions.
                </p>
                <div class="welcome-grid">
                    <div class="welcome-feature">Track earnings</div>
                    <div class="welcome-feature">Track expenses</div>
                    <div class="welcome-feature">Monitor goals</div>
                    <div class="welcome-feature">Manage documents and bills</div>
                    <div class="welcome-feature">Ask RideHero assistant</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, button_col, _ = st.columns([1, 2, 1])
    with button_col:
        st.button(
            "Enter Dashboard",
            key="enter_dashboard_button",
            on_click=enter_dashboard,
        )


init_db()


# --- UI ---
if not st.session_state.get("ride_hero_dashboard_open", False):
    render_welcome_page()
    st.stop()

st.markdown(
    """
    <div class="ride-hero-header" style="display:flex; align-items:center; gap:20px;">

        <img src="https://raw.githubusercontent.com/Attiq1006/Ride-Hero/main/ride_hero_logo.png"
        width="140"
        style="border-radius:18px;"/>

        <div>

            <div class="ride-hero-eyebrow"
            style="
            font-size:22px;
            font-weight:700;
            letter-spacing:2px;
            color:#39d98a;
            ">
            RIDE HERO
            </div>

            <h1 class="ride-hero-title"
            style="
            font-size:56px;
            margin-top:4px;
            margin-bottom:8px;
            ">
            Driver Earnings Command Center
            </h1>

            <p class="ride-hero-subtitle"
            style="
            font-size:18px;
            color:#b8c4d6;
            ">
            Smart tools for FHV drivers to track profit, documents, bills, fares, services, and deals.
            </p>

        </div>

    </div>
    """,
    unsafe_allow_html=True,
)
today = date.today()
holiday_alerts = {
    "New Year's Day": date(today.year, 1, 1),
    "Memorial Day": date(today.year, 5, 25),
    "Independence Day": date(today.year, 7, 4),
    "Labor Day": date(today.year, 9, 7),
    "Columbus Day / Indigenous Peoples' Day": date(today.year, 10, 12),
    "Thanksgiving": date(today.year, 11, 26),
    "Christmas Day": date(today.year, 12, 25),
    "New Year's Eve": date(today.year, 12, 31),
}

for holiday_name, holiday_date in holiday_alerts.items():
    days_until = (holiday_date - today).days
    if days_until == 1:
        st.warning(
            f"Tomorrow is {holiday_name}. Big driving day expected. "
            "Plan fuel, rest, documents, and working hours."
        )
    elif days_until == 0:
        st.success(
            f"Today is {holiday_name}. Drive smart, stay safe, and watch demand patterns."
        )


tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "Earnings",
        "Documents",
        "Bills",
        "Services",
        "Check My Fare",
        "Ask Ride Hero",
        "Deals",
    ]
)


# ===== TAB 1: EARNINGS =====
with tab1:
    st.subheader("Earnings Tracker")

    st.subheader("Monthly Target")
    monthly_goal = st.number_input("Monthly Profit Goal ($)", min_value=0.0)

    df = prepare_records(get_data())
    current_month_profit = 0.0

    if not df.empty:
        monthly_df = df[
            (df["entry_date"].dt.month == date.today().month)
            & (df["entry_date"].dt.year == date.today().year)
        ]
        current_month_profit = monthly_df["profit"].sum()

    remaining = monthly_goal - current_month_profit

    st.subheader("Monthly Goal Progress")
    st.write(f"Monthly Goal: ${monthly_goal:.2f}")
    st.write(f"Current Month Profit: ${current_month_profit:.2f}")

    if remaining > 0:
        st.warning(f"You still need to make ${remaining:.2f} this month.")
    else:
        st.success(f"You passed your monthly goal by ${abs(remaining):.2f}!")

    st.subheader("Fixed Monthly Expenses")

    rent = st.number_input("Rent / Home Expense ($)", min_value=0.0, key="rent_expense")
    insurance = st.number_input("Insurance ($)", min_value=0.0, key="insurance_expense")
    car_payment = st.number_input("Car Payment ($)", min_value=0.0, key="car_payment_expense")
    phone = st.number_input("Phone Bill ($)", min_value=0.0, key="phone_expense")
    other_fixed = st.number_input("Other Fixed Expenses ($)", min_value=0.0, key="other_fixed_expense")

    fixed_total = rent + insurance + car_payment + phone + other_fixed
    net_after_fixed = current_month_profit - fixed_total
    remaining_goal = monthly_goal - net_after_fixed

    st.write(f"Total Fixed Monthly Expenses: ${fixed_total:.2f}")

    st.subheader("Real Monthly Position")
    st.write(f"Profit Before Fixed Expenses: ${current_month_profit:.2f}")
    st.write(f"Fixed Monthly Expenses: ${fixed_total:.2f}")
    st.write(f"Net After Fixed Expenses: ${net_after_fixed:.2f}")

    if remaining_goal > 0:
        st.warning(f"You still need ${remaining_goal:.2f} to reach your goal.")
    else:
        st.success(f"You are ahead by ${abs(remaining_goal):.2f}.")

    if not df.empty:
        total_income = df["income"].sum()
        total_expenses = (
            df["fuel"].sum()
            + df["toll"].sum()
            + df["maintenance"].sum()
            + df["food"].sum()
            + df["other"].sum()
        )
        total_profit = df["profit"].sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Income", f"${total_income:.2f}")
        col2.metric("Total Expenses", f"${total_expenses:.2f}")
        col3.metric("Net Profit", f"${total_profit:.2f}")

    st.subheader("Company / Platform")
    company_options = [
        "Uber",
        "Lyft",
        "Curb",
        "Journey",
        "Myle",
        "Arro",
        "Blacklane",
        "Local Base",
        "Other",
    ]

    selected_companies = st.multiselect(
        "Select Companies",
        company_options,
        key="selected_companies",
        on_change=save_current_entry_before_platform_switch,
    )
    custom_company = st.text_input(
        "Add Custom Company / Base Name",
        key="custom_company_input",
        on_change=save_current_entry_before_platform_switch,
    )

    platform = current_platform_value()
    st.session_state.setdefault("active_platform", platform)

    if st.session_state.pop("platform_switch_saved", False):
        st.success("Previous entry saved. New entry started for the selected company.")

    if platform:
        st.success(f"Selected companies: {platform}")
    else:
        st.warning("Please select or enter at least one company.")

    entry_date = st.date_input("Date", date.today(), key="entry_date_input")
    income = st.number_input("Daily Income ($)", min_value=0.0, key="income_input")
    fuel = st.number_input("Fuel ($)", min_value=0.0, key="fuel_input")
    toll = st.number_input("Tolls ($)", min_value=0.0, key="toll_input")
    maintenance = st.number_input("Maintenance ($)", min_value=0.0, key="maintenance_input")
    food = st.number_input("Food ($)", min_value=0.0, key="food_input")
    other = st.number_input("Other Expenses ($)", min_value=0.0, key="other_input")
    miles = st.number_input("Miles Driven", min_value=0.0, key="miles_input")

    expenses_total = fuel + toll + maintenance + food + other
    net_profit = income - expenses_total
    st.success(f"Estimated Net Profit: ${net_profit:.2f}")

    time_options = [
        "Optional",
        "12:00 AM", "1:00 AM", "2:00 AM", "3:00 AM", "4:00 AM", "5:00 AM",
        "6:00 AM", "7:00 AM", "8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM",
        "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM",
        "6:00 PM", "7:00 PM", "8:00 PM", "9:00 PM", "10:00 PM", "11:00 PM",
    ]

    start_time = st.selectbox("Start Time", time_options, key="start_time_12hr")
    end_time = st.selectbox("End Time", time_options, key="end_time_12hr")

    if st.button("Save Entry", key="save_entry_button"):
        add_record(
            entry_date,
            income,
            fuel,
            toll,
            maintenance,
            food,
            other,
            miles,
            start_time,
            end_time,
            platform,
        )
        st.session_state["last_saved_entry_signature"] = draft_entry_signature(platform)
        st.success("Entry saved successfully!")
        st.rerun()

    st.button("Clear Form / New Entry", on_click=reset_entry_and_platform)

    df = prepare_records(get_data())
    st.subheader("Saved Records")

    if df.empty:
        st.info("No saved records yet.")
    else:
        st.dataframe(df, use_container_width=True)

        st.subheader("Delete Entry")

        delete_id = st.number_input(
            "Enter Record ID to Delete",
            min_value=1,
            step=1,
            key="delete_record_id",
        )

        if st.button("Delete Entry", key="delete_entry_button"):
            if delete_record(delete_id):
                st.success(f"Entry ID {delete_id} deleted successfully.")
                st.rerun()
            else:
                st.error(f"No saved entry found with ID {delete_id}.")

        days_in_month = calendar.monthrange(today.year, today.month)[1]
        days_left = days_in_month - today.day

        st.subheader("Daily Target Needed")
        if days_left > 0:
            daily_needed = remaining_goal / days_left
            if remaining_goal > 0:
                st.warning(f"You need to make about ${daily_needed:.2f} per day for the rest of this month.")
            else:
                st.success("You already reached your goal for this month.")
        else:
            st.info("Today is the last day of the month.")

        st.subheader("Performance Insights")
        valid_profit_df = df.dropna(subset=["entry_date"])

        if valid_profit_df.empty:
            st.info("Add a dated entry to see performance insights.")
        else:
            daily_profit = (
                valid_profit_df.assign(day=valid_profit_df["entry_date"].dt.date)
                .groupby("day", as_index=False)["profit"]
                .sum()
            )

            best_day = daily_profit.loc[daily_profit["profit"].idxmax()]
            slow_day = daily_profit.loc[daily_profit["profit"].idxmin()]

            best_col, slow_col = st.columns(2)
            with best_col:
                st.success(
                    f"Best Day: {best_day['day']} - Total Profit ${best_day['profit']:.2f}"
                )
            with slow_col:
                st.warning(
                    f"Slow Day: {slow_day['day']} - Total Profit ${slow_day['profit']:.2f}"
                )


with tab2:
    st.subheader("Documents & Expiry Tracker")

    doc_name = st.selectbox(
        "Select Document",
        [
            "TLC License",
            "Driver License",
            "Vehicle Registration",
            "Insurance Certificate",
            "Inspection Certificate",
            "Vehicle Title",
            "Insurance Policy",
            "TLC Vehicle License",
            "Full Coverage Insurance",
            "Drug Test",
            "Other",
        ],
        key="doc_dropdown",
    )
    expiry_date = st.date_input("Expiry Date", key="doc_expiry")
    custom_doc = ""

    if doc_name == "Other":
        custom_doc = st.text_input("Enter Document Name", key="custom_doc")

    final_doc_name = custom_doc if doc_name == "Other" else doc_name

    if st.button("Add Document", key="doc_button"):
        if final_doc_name:
            st.session_state.setdefault("documents", [])
            st.session_state.documents.append(
                {
                    "name": final_doc_name,
                    "expiry": expiry_date,
                }
            )
            st.success("Document added successfully!")
        else:
            st.error("Please enter a document name.")

    st.subheader("Your Documents")
    if st.session_state.get("documents"):
        for doc in st.session_state.documents:
            days_left = (doc["expiry"] - date.today()).days
            st.write(f"**{doc['name']}** - Expires on {doc['expiry']} ({days_left} days left)")

            if days_left <= 7:
                st.error("Expiring within 7 days!")
            elif days_left <= 15:
                st.warning("Expiring within 15 days")
            elif days_left <= 30:
                st.info("Expiring within 30 days")
    else:
        st.info("Document tracking will be saved here. Regular reminders for expiry dates coming soon!")


# ===== TAB 3: BILLS =====
with tab3:
    st.subheader("Bills & Payment Reminders")

    bills = [
        "Car Payment",
        "Liability Insurance",
        "Full Coverage Insurance",
        "Car Wash / Maintenance",
        "Phone Bill",
        "Other Bill",
    ]

    for i, bill in enumerate(bills):
        with st.expander(bill, expanded=True):
            amount = st.number_input(
                "Amount ($)",
                min_value=0.0,
                step=1.0,
                key=f"bill_amount_{i}",
            )
            due_date = st.date_input("Due Date", key=f"bill_due_date_{i}")
            days_left = (due_date - date.today()).days

            st.write(f"Amount: ${amount:.2f}")
            st.write(f"Due in: {days_left} days")

            if days_left < 0:
                st.error(f"{bill} is overdue by {abs(days_left)} days.")
            elif days_left == 0:
                st.error(f"{bill} is due today.")
            elif days_left <= 7:
                st.warning(f"{bill} is due in {days_left} days.")
            elif days_left <= 15:
                st.info(f"{bill} is due in {days_left} days.")
            else:
                st.success(f"{bill} is due in {days_left} days.")


# ===== TAB 4: SERVICES =====
with tab4:
    st.subheader("Driver Services Directory")

    service_category = st.selectbox(
        "Select Service",
        [
            "Mechanics",
            "Tow Trucks",
            "Tire Shops",
            "Insurance",
            "TLC Rentals",
            "Legal Help",
            "Driver Support",
        ],
        key="service_category",
    )

    if service_category == "Mechanics":
        mechanics = [
            {
                "name": "1. Autobody & Repair INC",
                "phone": "Contact Arshad",
                "location": "36-04 Steinway St, Long Island City, NY 11101",
                "services": "Auto body, general repair",
                "notes": "Timing: 10 AM - 10 PM",
            },
            {
                "name": "2. A1 Collision",
                "phone": "Contact Surjit Singh",
                "location": "2208 37th Ave, Long Island City, NY 11101",
                "services": "Collision repair, body work",
                "notes": "Timing: 10 AM - 10 PM",
            },
            {
                "name": "3. Ideal Auto Body Services of LIC",
                "phone": "Contact Aeraj",
                "location": "38-25 23rd St, Astoria, NY 11101",
                "services": "Auto body, repair services",
                "notes": "Trusted local shop",
            },
            {
                "name": "4. Hybrid Auto Tech INC",
                "phone": "N/A",
                "location": "519 W 47th St, New York, NY 10036",
                "services": "Hybrid repair, diagnostics",
                "notes": "Open 24 hours",
            },
            {
                "name": "5. Webster Ave Fuel",
                "phone": "Contact Haji",
                "location": "2103 Webster Ave, Bronx, NY 10457",
                "services": "Fuel services, basic maintenance",
                "notes": "Timing: 8 AM - 12 AM",
            },
            {
                "name": "6. Celeca Auto Repair",
                "phone": "N/A",
                "location": "2236 Cross Bronx Expwy, Bronx, NY",
                "services": "General repair, maintenance",
                "notes": "Mon-Fri: 8 AM - 4 AM | Sat-Sun: 9 AM - 5 PM",
            },
        ]
        render_service_cards(
            mechanics,
            [
                ("Location", "location"),
                ("Phone", "phone"),
                ("Services", "services"),
                ("Notes", "notes"),
            ],
        )
        st.warning(
            "Disclaimer: Drivers should confirm pricing, estimates, and repair details directly with the shop before authorizing any work. This app is not affiliated with or financially partnered with the listed mechanics and is not responsible for repair quality, pricing, delays, or disputes."
        )

    elif service_category == "Tow Trucks":
        tow_truck_companies = [
            {
                "name": "Rite Away Towing & Recovery",
                "phone": "917-361-0493",
                "address": "688 Henry St, Brooklyn, NY 11231",
                "area": "Brooklyn / NYC",
                "services": ["24/7 towing", "roadside assistance", "recovery", "heavy-duty towing"],
                "pricing_note": "Advertises upfront and affordable towing with no hidden fees.",
                "review_note": "Publicly shows positive Google review signals.",
                "website": "https://riteawaytowingservices.com/",
            },
            {
                "name": "Xoom Towing NYC",
                "phone": "347-363-6650",
                "address": "Brooklyn, NY",
                "area": "Brooklyn / NYC",
                "services": ["24/7 towing", "roadside assistance", "jump start", "lockout help"],
                "pricing_note": "Mentions transparent and affordable pricing.",
                "review_note": "Reviews mention quick arrival and reasonable service.",
                "website": "https://xoomtowing.com/towing-brooklyn-nyc/",
            },
            {
                "name": "A1 Towing & Collision NYC",
                "phone": "646-542-0049",
                "address": "608 W 47th St, New York, NY 10036",
                "area": "Manhattan / NYC",
                "services": ["24-hour emergency towing", "collision towing", "roadside assistance"],
                "pricing_note": "Advertises competitive rates.",
                "review_note": "Testimonials mention professional service and reasonable pricing.",
                "website": "https://towtruck.nyc/",
            },
            {
                "name": "All City Towing NYC",
                "phone": "917-677-9799",
                "address": "New York, NY",
                "area": "Manhattan / NYC",
                "services": ["24/7 towing", "flatbed towing", "roadside assistance", "lockout help"],
                "pricing_note": "Advertises affordable flat-rate pricing.",
                "review_note": "Public website presents positive service claims and customer-focused pricing.",
                "website": "https://allcitytowingnyc.com/",
            },
            {
                "name": "NYC Towing 24 / Auto Towing NYC",
                "phone": "347-817-6777",
                "address": "New York, NY",
                "area": "Manhattan / NYC",
                "services": ["24/7 towing", "motorcycle towing", "jump start", "fuel delivery", "lockout help"],
                "pricing_note": "Advertises affordable flat-rate pricing.",
                "review_note": "Public website emphasizes fast response and affordable towing.",
                "website": "https://nyctowing24.com/",
            },
        ]
        render_service_cards(
            tow_truck_companies,
            [
                ("Address", "address"),
                ("Phone", "phone"),
                ("Area", "area"),
                ("Services", "services"),
                ("Pricing", "pricing_note"),
                ("Notes", "review_note"),
            ],
        )

    elif service_category == "Tire Shops":
        tire_shops = [
            {
                "name": "1. 106 St. Tire & Wheel",
                "phone": "(718) 446-6769",
                "address": "106-01 Northern Blvd, Corona, NY 11368",
                "services": ["flat tire repair", "used tires", "wheel repair"],
                "notes": "Queens location",
            },
            {
                "name": "2. Flat Fix 24 Hours",
                "phone": "(718) 716-2409",
                "address": "1510 Jerome Ave, Bronx, NY 10452",
                "services": ["flat tire repair", "tire replacement"],
                "notes": "Open late hours",
            },
            {
                "name": "3. JJ Tire Shop",
                "phone": "(212) 927-8473",
                "address": "2240 Amsterdam Ave, New York, NY 10032",
                "services": ["flat tire repair", "new tires", "used tires"],
                "notes": "Manhattan location",
            },
            {
                "name": "4. Express Tire Shop",
                "phone": "(718) 293-5050",
                "address": "1400 Jerome Ave, Bronx, NY 10452",
                "services": ["flat tire repair", "wheel balancing"],
                "notes": "Bronx tire service",
            },
            {
                "name": "5. M&R Tire Shop",
                "phone": "(718) 255-6311",
                "address": "94-10 Astoria Blvd, East Elmhurst, NY 11369",
                "services": ["flat tire repair", "tire installation"],
                "notes": "Near LaGuardia area",
            },
        ]
        render_service_cards(
            tire_shops,
            [
                ("Address", "address"),
                ("Phone", "phone"),
                ("Services", "services"),
                ("Notes", "notes"),
            ],
        )
        st.warning(
            "Disclaimer: Please confirm pricing, tire quality, and repair details before service. This app is not affiliated with these tire shops and is not responsible for pricing, workmanship, delays, or damages."
        )

    elif service_category == "Insurance":
        insurance_brokers = [
            {
                "name": "1. Freedom Line Brokerage",
                "phone": "718-937-6180",
                "location": "75-25 31st Ave, East Elmhurst, NY 11370",
                "notes": "TLC insurance, commercial auto insurance, competitive rates",
            },
            {
                "name": "2. NYAB Insurance",
                "phone": "718-784-1112",
                "location": "34-11 Queens Blvd, Long Island City, NY",
                "notes": "Specializes in TLC, Uber, Lyft insurance",
            },
            {
                "name": "3. Mega Insurance Brokerage",
                "phone": "212-721-0001",
                "location": "32-47 57th St, Woodside, NY",
                "notes": "TLC compliance and competitive rates",
            },
            {
                "name": "4. Asian Insurance NYC",
                "phone": "718-433-4460",
                "location": "New York, NY",
                "notes": "Fast quotes for TLC drivers",
            },
            {
                "name": "5. Pearland Brokerage Inc.",
                "phone": "718-361-0033",
                "location": "36-01 43rd Ave, Long Island City, NY",
                "notes": "Experienced in TLC insurance",
            },
        ]
        render_service_cards(
            insurance_brokers,
            [
                ("Location", "location"),
                ("Phone", "phone"),
                ("Notes", "notes"),
            ],
        )
        st.warning(
            "Disclaimer: We are not affiliated with these insurance brokers. Please compare rates, coverage, deductibles, and policy terms before purchasing any insurance policy."
        )

    elif service_category == "TLC Rentals":
        rentals = [
            {
                "name": "1. American Lease & Management",
                "location": "Brooklyn, NY",
                "phone": "Check website/app",
                "website": "https://americanlease.com/",
                "notes": "Large fleet, instant pay, flexible rental plans",
            },
            {
                "name": "2. Buggy TLC Rentals",
                "location": "445 Empire Blvd, Brooklyn, NY",
                "phone": "347-334-6313",
                "website": "https://www.joinbuggy.com/ny/new-york/",
                "notes": "Popular with Uber/Lyft drivers, weekly rentals",
            },
            {
                "name": "3. Fast Track Mobility",
                "location": "22-11 38th Ave, Long Island City, NY",
                "phone": "718-370-0775",
                "website": "https://fasttrackleasingllc.com/",
                "notes": "Includes insurance & roadside assistance",
            },
            {
                "name": "4. BIRACS TLC Cars",
                "location": "1160 Manhattan Ave, Brooklyn, NY 11222",
                "phone": "Check website",
                "website": "https://www.biracs.com/tlc-rental",
                "notes": "10+ years experience, flexible plans",
            },
            {
                "name": "5. Tower TLC Rentals",
                "location": "31-21 Thomson Ave, Long Island City, NY",
                "phone": "Check website",
                "website": "https://www.towertlcrentals.com/",
                "notes": "Rental + lease-to-own options",
            },
        ]
        render_service_cards(
            rentals,
            [
                ("Location", "location"),
                ("Phone", "phone"),
                ("Notes", "notes"),
            ],
        )
        st.warning(
            "Disclaimer: We are not affiliated with any rental company. Please verify rental terms, deposits, insurance coverage, and weekly rates before signing any agreement."
        )

    elif service_category == "Legal Help":
        st.markdown("## Trusted Traffic & TLC Attorneys")
        attorneys = [
            {
                "name": "1. Weiss & Associates, PC",
                "address": "2 Park Avenue, 20th Floor, Suite 2058, New York, NY 10016",
                "phone": "212-683-7373",
                "notes": "Traffic ticket defense",
            },
            {
                "name": "2. Martin A. Kron & Associates, P.C.",
                "address": "295 Madison Avenue, Floor 12, Suite 1208, New York, NY 10017",
                "phone": "212-235-1525",
                "notes": "Traffic ticket defense",
            },
            {
                "name": "3. Law Office of James Medows",
                "address": "306 Atlantic Avenue, Brooklyn, NY 11201",
                "phone": "917-856-1247",
                "notes": "Traffic ticket defense",
            },
            {
                "name": "4. Gannes & Musico, LLP",
                "address": "325 Broadway, Suite 406, New York, NY 10007",
                "phone": "212-779-1980 / 877-803-2603",
                "notes": "Traffic ticket defense",
            },
            {
                "name": "5. Rosenblum Law / TrafficTickets.com",
                "address": "40 Wall Street, Suite 3602, New York, NY 10005",
                "phone": "888-883-5529 / 917-779-8411",
                "notes": "Traffic ticket defense",
            },
            {
                "name": "6. Law Office of Deborah Maggie",
                "address": "13 Trinity Place, New York, NY 10006",
                "phone": "212-422-1080",
                "notes": "Traffic ticket defense",
            },
        ]
        render_service_cards(
            attorneys,
            [
                ("Address", "address"),
                ("Phone", "phone"),
                ("Services", "notes"),
            ],
        )
        st.warning(
            "Disclaimer: The listed attorneys and legal resources are provided for informational purposes only. Drivers should independently verify legal fees, services, and qualifications before hiring any attorney. This app is not partnered with or responsible for any legal service provider listed."
        )

    elif service_category == "Driver Support":
        st.markdown("### Free Driver Support Organizations")
        st.write("**Independent Drivers Guild (IDG)**")
        st.markdown("- [Driver advocacy and deactivation support](https://driversguild.org/deactivation/)")
        st.markdown("- [Financial coaching](https://ny.driversguild.org/services/financial-coaching/)")
        st.markdown("- [Safety education classes](https://driversguild.org/education/)")
        st.markdown("- [IDG main website](https://driversguild.org/)")

        st.write("**NYC TLC Driver Resource Center**")
        st.markdown("- [TLC Driver Resources](https://www.nyc.gov/site/tlc/drivers/driver-resources.page)")

        st.write("**OATH Help Center**")
        st.markdown("- [Free legal assistance / TLC summons help](https://www.nyc.gov/site/oath/help-center/free-legal-assistance.page)")


# ===== TAB 5: CHECK MY FARE =====
with tab5:
    st.subheader("Check My TLC Minimum Pay")

    st.info("For NYC Uber/Lyft/FHV drivers. This estimates TLC minimum driver pay, not passenger fare.")

    trip_type = st.selectbox(
        "Trip Type",
        ["Inside NYC - Non-WAV", "Inside NYC - WAV", "Out of Town - Non-WAV", "Out of Town - WAV"],
    )

    trip_miles = st.number_input("Trip Miles", min_value=0.0, value=1.0, step=0.1)
    trip_minutes = st.number_input("Trip Minutes", min_value=0.0, value=10.0, step=1.0)

    if trip_type == "Inside NYC - Non-WAV":
        mile_rate = 1.283
        minute_rate = 0.681
    elif trip_type == "Inside NYC - WAV":
        mile_rate = 1.601
        minute_rate = 0.681
    elif trip_type == "Out of Town - Non-WAV":
        mile_rate = 1.757
        minute_rate = 0.725
    else:
        mile_rate = 2.193
        minute_rate = 0.725

    estimated_pay = (trip_miles * mile_rate) + (trip_minutes * minute_rate)

    st.success(f"Estimated TLC Minimum Driver Pay: ${estimated_pay:.2f}")
    st.caption(
        "Estimate only. TLC rates may change periodically. "
        "Uber/Lyft may pay more because of tips, bonuses, surge, incentives, or adjustments."
    )
    st.markdown("[Official TLC Driver Pay Rates](https://www.nyc.gov/site/tlc/about/driver-pay-rates.page)")

# ===== TAB 6: ASK RIDE HERO =====
with tab6:
    st.subheader("🤖 Ask RideHero")

    df = prepare_records(get_data())

    question = st.text_input(
        "Ask something like: How much did I make today? How much this month?"
    )

    if not df.empty:
        df["entry_date"] = pd.to_datetime(df["entry_date"])

        today_total = df[df["entry_date"].dt.date == date.today()]["income"].sum()
        month_total = df[df["entry_date"].dt.month == date.today().month]["income"].sum()
        total_expenses = df[["fuel", "toll", "maintenance", "food", "other"]].sum().sum()
        net_profit = month_total - total_expenses

        if question:
            q = question.lower()

            if "today" in q:
                st.success(f"You made ${today_total:.2f} today.")
            elif "month" in q:
                st.success(f"You made ${month_total:.2f} this month.")
            elif "profit" in q or "net" in q:
                st.success(f"Your estimated net profit this month is ${net_profit:.2f}.")
            elif "expense" in q:
                st.success(f"Your total recorded expenses are ${total_expenses:.2f}.")
            else:
                st.info("Try asking: How much did I make today? How much this month? What is my net profit?")
    else:
        st.info("No records yet. Add earnings first.")
# ===== TAB 7: DEALS & PROMOTIONS =====
with tab7:
    st.subheader("Deals & Promotions")
    st.info("Coming soon: driver discounts, referral offers, and featured promotions.")


st.divider()
st.caption("RideHero (c) 2026 | Built for FHV Drivers | Independent driver utility platform")
