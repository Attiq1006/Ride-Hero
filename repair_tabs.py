from pathlib import Path

path = Path("Driverapp.py")
text = path.read_text(encoding="utf-8", errors="replace")
first = text.index("with tab1:")
second = text.index("with tab1:", first + 1)
replacement = (
    "with tab1:\n"
    "    st.subheader(\"💰 Earnings Tracker\")\n\n"
    "with tab2:\n"
    "    st.subheader(\"📄 Documents & Expiry Tracker\")\n\n"
    "with tab3:\n"
    "    st.subheader(\"📅 Bills & Payment Reminders\")\n"
    "    st.info(\"Bills and payment reminders will appear here once configured.\")\n\n"
    "with tab4:\n"
    "    st.subheader(\"🛠 Driver Services Directory\")\n\n"
    "with tab5:\n"
    "    st.subheader(\"🧾 Check My Fare\")\n"
    "    st.info(\"Check My Fare content will appear here once configured.\")\n\n"
    "with tab6:\n"
    "    st.subheader(\"🔥 Deals & Promotions\")\n"
    "    st.info(\"Deals and promotions content will appear here once configured.\")\n"
)
path.write_text(text[:first] + replacement + text[second:], encoding="utf-8")
print("Repaired top tab placeholders.")