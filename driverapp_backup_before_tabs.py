import streamlit as st
import pandas as pd
from datetime import date
import sqlite3
import datetime

# --- Database ---
conn = sqlite3.connect("data.db", check_same_thread=False)
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS records (
entry_date TEXT,
income REAL,
fuel REAL,
toll REAL,
maintenance REAL,
food REAL,
other REAL,
miles REAL,
start_time TEXT,
end_time TEXT,
platform TEXT
)
''')
def add_record(d, income, fuel, toll, maintenance, food, other, miles, start_time, end_time, platform):
    c.execute("INSERT INTO records VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
    (d, income, fuel, toll, maintenance, food, other, miles, start_time, end_time, platform))
    conn.commit()

def get_data():
    return pd.read_sql("SELECT * FROM records", conn)

# --- UI ---
st.title("🦸 Hero's Earnings")

st.subheader("Add Daily Entry")

entry_date = st.date_input("Date", date.today())
income = st.number_input("Daily Income ($)", min_value=0.0)
fuel = st.number_input("Fuel ($)", min_value=0.0)
toll = st.number_input("Tolls ($)", min_value=0.0)
maintenance = st.number_input("Maintenance ($)", min_value=0.0)
food = st.number_input("Food ($)", min_value=0.0)
miles = st.number_input("Miles Driven", min_value=0.0)
time_options = [
"Optional",
"12:00 AM", "1:00 AM", "2:00 AM", "3:00 AM", "4:00 AM", "5:00 AM",
"6:00 AM", "7:00 AM", "8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM",
"12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM",
"6:00 PM", "7:00 PM", "8:00 PM", "9:00 PM", "10:00 PM", "11:00 PM"
]

start_time = st.selectbox("Start Time", time_options, key="start_time_12hr")
end_time = st.selectbox("End Time", time_options, key="end_time_12hr")
st.subheader("Company / Platform")

selected_companies = []

default_companies = ["Uber", "Lyft", "Curb", "Arro", "Blacklane", "Local Base", "Other"]

for company in default_companies:
    if st.checkbox(company, key=f"company_{company}"):
        selected_companies.append(company)

custom_company = st.text_input("Add Custom Company / Base Name", key="custom_company")

if custom_company.strip():
    selected_companies.append(custom_company.strip())

platform = ", ".join(selected_companies)
if platform:
    st.success(f"Selected companies: {platform}")
else:
    st.warning("Please select or enter at least one company.")

other = st.number_input("Other Expenses ($)", min_value=0.0)

if st.button("Save Entry"):
    add_record(entry_date, income, fuel, toll, maintenance, food, other, miles, start_time, end_time, platform)
    st.success("Saved!")

# --- Load Data ---
df = get_data()

if not df.empty:
    df["entry_date"] = pd.to_datetime(df["entry_date"])

    if "food" not in df.columns:
        df["food"] = 0

    if "other" not in df.columns:
        df["other"] = 0

    df["profit"] = df["income"] - (
        df["fuel"] +
        df["toll"] +
        df["maintenance"] +
        df["food"] +
        df["other"]
    )

    st.dataframe(df)

# --- Monthly Target ---
st.subheader("Monthly Target")

monthly_goal = st.number_input("Monthly Profit Goal ($)", min_value=0.0)

# --- Monthly Goal Progress ---
current_month_profit = 0.0
if not df.empty:
    current_month_profit = df[df["entry_date"].dt.month == date.today().month]["profit"].sum()
    
    remaining = monthly_goal - current_month_profit
    
    st.subheader("🎯 Monthly Goal Progress")
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

st.write(f"Total Fixed Monthly Expenses: ${fixed_total:.2f}")
net_after_fixed = current_month_profit - fixed_total
remaining_goal = monthly_goal - net_after_fixed

st.subheader("Real Monthly Position")
st.write(f"Profit Before Fixed Expenses: ${current_month_profit:.2f}")
st.write(f"Fixed Monthly Expenses: ${fixed_total:.2f}")
st.write(f"Net After Fixed Expenses: ${net_after_fixed:.2f}")

if remaining_goal > 0:
    st.warning(f"You still need ${remaining_goal:.2f} to reach your goal.")
else:
    st.success(f"You are ahead by ${abs(remaining_goal):.2f}.")
from datetime import datetime
import calendar

today = datetime.today()
days_in_month = calendar.monthrange(today.year, today.month)[1]
days_left = days_in_month - today.day

if days_left > 0:
    daily_needed = remaining_goal / days_left
    st.subheader("Daily Target Needed")

    if remaining_goal > 0:
        st.warning(f"You need to make about ${daily_needed:.2f} per day for the rest of this month.")
    else:
        st.success("You already reached your goal for this month.")
else:
    st.subheader("Daily Target Needed")
    st.info("Today is the last day of the month.")

st.subheader("Performance Insights")

if df.empty:
    st.info("No entries yet. Add your first earning entry to see best day and worst day.")
else:
    best_day = df.loc[df["profit"].idxmax()]
    slow_day = df.loc[df["profit"].idxmin()]

    st.success(
        f"Best Day: {best_day['entry_date'].date()} — Profit ${best_day['profit']:.2f}"
    )
    st.warning(
        f"Slow day: {slow_day['entry_date'].date()} — Profit ${slow_day['profit']:.2f}"
    )
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
"Driver Support"
],
key="service_category"
)

if service_category == "Mechanics":
    mechanics = [

    {
        "name": "1. Autobody & Repair INC",
        "phone": "Contact Arshad",
        "location": "36-04 Steinway St, Long Island City, NY 11101",
        "services": "Auto body, general repair",
        "notes": "Timing: 10 AM – 10 PM"
    },

    {
        "name": "2. A1 Collision",
        "phone": "Contact Surjit Singh",
        "location": "2208 37th Ave, Long Island City, NY 11101",
        "services": "Collision repair, body work",
        "notes": "Timing: 10 AM – 10 PM"
    },

    {
        "name": "3. Ideal Auto Body Services of LIC",
        "phone": "Contact Aeraj",
        "location": "38-25 23rd St, Astoria, NY 11101",
        "services": "Auto body, repair services",
        "notes": "Trusted local shop"
    },

    {
        "name": "4. Hybrid Auto Tech INC",
        "phone": "N/A",
        "location": "519 W 47th St, New York, NY 10036",
        "services": "Hybrid repair, diagnostics",
        "notes": "Open 24 hours"
    },

    {
        "name": "5. Webster Ave Fuel",
        "phone": "Contact Haji",
        "location": "2103 Webster Ave, Bronx, NY 10457",
        "services": "Fuel services, basic maintenance",
        "notes": "Timing: 8 AM – 12 AM"
    },

    {
        "name": "6. Celeca Auto Repair",
        "phone": "N/A",
        "location": "2236 Cross Bronx Expwy, Bronx, NY",
        "services": "General repair, maintenance",
        "notes": "Mon–Fri: 8 AM – 4 AM | Sat–Sun: 9 AM – 5 PM"
    }

]
    for shop in mechanics:
        st.markdown(f"### {shop['name']}")
        st.write(f"📍 Location: {shop['location']}")
        st.write(f"📞 Phone: {shop['phone']}")
        st.write(f"🛠 Services: {shop['services']}")
        st.write(f"💬 Notes: {shop['notes']}")
        st.divider()

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
        "website": "https://riteawaytowingservices.com/"
    },
    {
        "name": "Xoom Towing NYC",
        "phone": "347-363-6650",
        "address": "Brooklyn, NY",
        "area": "Brooklyn / NYC",
        "services": ["24/7 towing", "roadside assistance", "jump start", "lockout help"],
        "pricing_note": "Mentions transparent and affordable pricing.",
        "review_note": "Reviews mention quick arrival and reasonable service.",
        "website": "https://xoomtowing.com/towing-brooklyn-nyc/"
    },
    {
        "name": "A1 Towing & Collision NYC",
        "phone": "646-542-0049",
        "address": "608 W 47th St, New York, NY 10036",
        "area": "Manhattan / NYC",
        "services": ["24-hour emergency towing", "collision towing", "roadside assistance"],
        "pricing_note": "Advertises competitive rates.",
        "review_note": "Testimonials mention professional service and reasonable pricing.",
        "website": "https://towtruck.nyc/"
    },
    {
        "name": "All City Towing NYC",
        "phone": "917-677-9799",
        "address": "New York, NY",
        "area": "Manhattan / NYC",
        "services": ["24/7 towing", "flatbed towing", "roadside assistance", "lockout help"],
        "pricing_note": "Advertises affordable flat-rate pricing.",
        "review_note": "Public website presents positive service claims and customer-focused pricing.",
        "website": "https://allcitytowingnyc.com/"
    },
    {
        "name": "NYC Towing 24 / Auto Towing NYC",
        "phone": "347-817-6777",
        "address": "New York, NY",
        "area": "Manhattan / NYC",
        "services": ["24/7 towing", "motorcycle towing", "jump start", "fuel delivery", "lockout help"],
        "pricing_note": "Advertises affordable flat-rate pricing.",
        "review_note": "Public website emphasizes fast response and affordable towing.",
        "website": "https://nyctowing24.com/"
    }
]
    for tow in tow_truck_companies:
            st.markdown(f"### {tow['name']}")
            st.write(f"📍 Address: {tow['address']}")
            st.write(f"📞 Phone: {tow['phone']}")
            st.write(f"🌍 Area: {tow['area']}")
            st.write(f"🛠 Services: {', '.join(tow['services'])}")
            st.write(f"💲 Pricing: {tow['pricing_note']}")
            st.write(f"⭐ Notes: {tow['review_note']}")
            st.markdown(f"[Visit Website]({tow['website']})")
            st.divider()

elif service_category == "Tire Shops":
    tire_shops = [

        {
            "name": "1. 106 St. Tire & Wheel",
            "phone": "(718) 446-6769",
            "address": "106-01 Northern Blvd, Corona, NY 11368",
            "services": ["flat tire repair", "used tires", "wheel repair"],
            "notes": "Queens location"
        },

        {
            "name": "2. Flat Fix 24 Hours",
            "phone": "(718) 716-2409",
            "address": "1510 Jerome Ave, Bronx, NY 10452",
            "services": ["flat tire repair", "tire replacement"],
            "notes": "Open late hours"
        },

        {
            "name": "3. JJ Tire Shop",
            "phone": "(212) 927-8473",
            "address": "2240 Amsterdam Ave, New York, NY 10032",
            "services": ["flat tire repair", "new tires", "used tires"],
            "notes": "Manhattan location"
        },

        {
            "name": "4. Express Tire Shop",
            "phone": "(718) 293-5050",
            "address": "1400 Jerome Ave, Bronx, NY 10452",
            "services": ["flat tire repair", "wheel balancing"],
            "notes": "Bronx tire service"
        },

        {
            "name": "5. M&R Tire Shop",
            "phone": "(718) 255-6311",
            "address": "94-10 Astoria Blvd, East Elmhurst, NY 11369",
            "services": ["flat tire repair", "tire installation"],
            "notes": "Near LaGuardia area"
        }
    ]

    for tire in tire_shops:
        st.markdown(f"### {tire['name']}")
        st.write(f"📍 Address: {tire['address']}")
        st.write(f"📞 Phone: {tire['phone']}")
        st.write(f"🛠 Services: {', '.join(tire['services'])}")
        st.write(f"⏰ Notes: {tire['notes']}")
        st.divider()

    st.warning(
        "Disclaimer: Please confirm pricing, tire quality, and repair details before service. This app is not affiliated with these tire shops and is not responsible for pricing, workmanship, delays, or damages."
    )

elif service_category == "Insurance":
    insurance_brokers = [

        {
            "name": "1. Freedom Line Brokerage",
            "phone": "718-937-6180",
            "location": "75-25 31st Ave,East Elmhurst, NY 11370",
            "notes": "TLC insurance, commercial auto insurance,Competitive rates"
        },

        {
            "name": "2. NYAB Insurance",
            "phone": "718-784-1112",
            "location": "34-11 Queens Blvd, Long Island City, NY",
            "notes": "Specializes in TLC, Uber, Lyft insurance"
        },

        {
            "name": "3. Mega Insurance Brokerage",
            "phone": "212-721-0001",
            "location": "32-47 57th St, Woodside, NY",
            "notes": "TLC compliance and competitive rates"
        },

        {
            "name": "4. Asian Insurance NYC",
            "phone": "718-433-4460",
            "location": "New York, NY",
            "notes": "Fast quotes for TLC drivers"
        },

        {
            "name": "5. Pearland Brokerage Inc.",
            "phone": "718-361-0033",
            "location": "36-01 43rd Ave, Long Island City, NY",
            "notes": "Experienced in TLC insurance"
        }
    ]

    for ins in insurance_brokers:
        st.markdown(f"### {ins['name']}")
        st.write(f"📍 Location: {ins['location']}")
        st.write(f"📞 Phone: {ins['phone']}")
        st.write(f"📝 Notes: {ins['notes']}")
        st.divider()

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
            "notes": "Large fleet, instant pay, flexible rental plans"
        },
    {
        "name": "2. Buggy TLC Rentals",
        "location": "445 Empire Blvd, Brooklyn, NY",
        "phone": "347-334-6313",
        "website": "https://www.joinbuggy.com/ny/new-york/",
        "notes": "Popular with Uber/Lyft drivers, weekly rentals"
    },
    {
        "name": "3. Fast Track Mobility",
        "location": "22-11 38th Ave, Long Island City, NY",
        "phone": "718-370-0775",
        "website": "https://fasttrackleasingllc.com/",
        "notes": "Includes insurance & roadside assistance"
    },
    {
        "name": "4. BIRACS TLC Cars",
        "location": "1160 Manhattan Ave, Brooklyn, NY 11222",
        "phone": "Check website",
        "website": "https://www.biracs.com/tlc-rental",
        "notes": "10+ years experience, flexible plans"
    },
    {
        "name": "5. Tower TLC Rentals",
        "location": "31-21 Thomson Ave, Long Island City, NY",
        "phone": "Check website",
        "website": "https://www.towertlcrentals.com/",
        "notes": "Rental + lease-to-own options"
    }
]
    for r in rentals:
        st.markdown(f"### {r['name']}")
        st.write(f"📍 Location: {r['location']}")
        st.write(f"📞 Phone: {r['phone']}")
        st.write(f"📝 Notes: {r['notes']}")
        st.markdown(f"[Visit Website]({r['website']})")
        st.divider()

    st.warning(
        "Disclaimer: We are not affiliated with any rental company. Please verify rental terms, deposits, insurance coverage, and weekly rates before signing any agreement."
    )

elif service_category == "Legal Help":
    st.markdown("## ⚖️ Trusted Traffic & TLC Attorneys")

    attorneys = [
        {
            "name": "1. Weiss & Associates, PC",
            "address": "2 Park Avenue, 20th Floor, Suite 2058, New York, NY 10016",
            "phone": "212-683-7373",
            "notes": "Traffic ticket defense"
        },
        {
            "name": "2. Martin A. Kron & Associates, P.C.",
            "address": "295 Madison Avenue, Floor 12, Suite 1208, New York, NY 10017",
            "phone": "212-235-1525",
            "notes": "Traffic ticket defense"
        },
        {
            "name": "3. Law Office of James Medows",
            "address": "306 Atlantic Avenue, Brooklyn, NY 11201",
            "phone": "917-856-1247",
            "notes": "Traffic ticket defense"
        },
        {
            "name": "4. Gannes & Musico, LLP",
            "address": "325 Broadway, Suite 406, New York, NY 10007",
            "phone": "212-779-1980 / 877-803-2603",
            "notes": "Traffic ticket defense"
        },
        {
            "name": "5. Rosenblum Law / TrafficTickets.com",
            "address": "40 Wall Street, Suite 3602, New York, NY 10005",
            "phone": "888-883-5529 / 917-779-8411",
            "notes": "Traffic ticket defense"
        },
        {
            "name": "6. Law Office of Deborah Maggie",
            "address": "13 Trinity Place, New York, NY 10006",
            "phone": "212-422-1080",
            "notes": "Traffic ticket defense"
        }
    ]

    for lawyer in attorneys:
        st.markdown(f"### {lawyer['name']}")
        st.write(f"📍 Address: {lawyer['address']}")
        st.write(f"📞 Phone: {lawyer['phone']}")
        st.write(f"⚖️ Services: {lawyer['notes']}")
        st.divider()
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
import datetime

st.subheader("📄 Documents & Expiry Tracker")

doc_name = st.selectbox(
    "Select Document",
    [
        "TLC License",
        "Driver License",
        "Vehicle Registration",
        "Insurance Policy",
        "TLC Vehicle License",
        "Full Coverage Insurance",
        "Inspection",
        "Drug Test",
        "Other"
    ],
    key="doc_dropdown"
)
expiry_date = st.date_input("Expiry Date")
custom_doc = ""

if doc_name == "Other":
    custom_doc = st.text_input("Enter Document Name")

final_doc_name = custom_doc if doc_name == "Other" else doc_name

if st.button("Add Document"):
    if final_doc_name:
        if "documents" not in st.session_state:
            st.session_state.documents = []

        st.session_state.documents.append({
            "name": final_doc_name,
            "expiry": expiry_date
        })

        st.success("Document added successfully!")
    else:
        st.error("Please enter a document name.")

if "documents" in st.session_state and st.session_state.documents:
    st.markdown("### 📋 Your Documents")

    today = datetime.date.today()

    for doc in st.session_state.documents:
        days_left = (doc["expiry"] - today).days

        st.write(f"**{doc['name']}** - Expires on {doc['expiry']} ({days_left} days left)")

        if days_left <= 7:
            st.error("🚨 Expiring within 7 days!")
        elif days_left <= 15:
            st.warning("🔶 Expiring within 15 days")
        elif days_left <= 30:
            st.info("⚠️ Expiring within 30 days")