import streamlit as st

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(layout="wide", page_title="Menu")
st.title("A350 Business Class")

# -----------------------------
# Seatmap A350
# -----------------------------
seatmap = [
    ["1A", "1C", None, "1D", "1G", None, "1H", "1K"],
    ["2A", "2C", None, "2D", "2G", None, "2H", "2K"],
    ["3A", "3C", None, "3D", "3G", None, "3H", "3K"],
    ["4A", "4C", None, "4D", "4G", None, "4H", "4K"],
    ["5A", "5C", None, "5D", "5G", None, "5H", "5K"],
]

# -----------------------------
# Meal Codes
# -----------------------------
starters = ["—", "VSV", "VSF"]
hotmeals = ["—", "HMV", "HMF", "HMR", "HMC"]

# -----------------------------
# Session State Initialisierung
# -----------------------------
if "selected_seat" not in st.session_state:
    st.session_state.selected_seat = None

if "seats" not in st.session_state:
    st.session_state.seats = {}

if "catering" not in st.session_state:
    st.session_state.catering = {m: 0 for m in ["VSV", "VSF", "HMR", "HMF", "HMC", "HMV"]}

if "backup" not in st.session_state:
    st.session_state.backup = {m: 0 for m in ["VSV", "VSF", "HMR", "HMF", "HMV"]}  # HMC kein Backup

# -----------------------------
# Catering Popups
# -----------------------------
with st.expander("Catering"):
    st.markdown("Catering")
    for meal in st.session_state.catering:
        st.session_state.catering[meal] = st.number_input(
            f"{meal}",
            min_value=0,
            value=st.session_state.catering[meal],
            step=1,
            key=f"catering_{meal}"
        )

with st.expander("Crewmeals, AUS DEM TROLLEY NEHMEN!"):
    st.markdown("### Backup")
    for meal in st.session_state.backup:
        st.session_state.backup[meal] = st.number_input(
            f"{meal}",
            min_value=0,
            value=st.session_state.backup[meal],
            step=1,
            key=f"backup_{meal}"
        )

st.markdown("---")

# -----------------------------
# Funktion: Sitzstatus Label
# -----------------------------
def get_seat_label(seat_data, seat):
    starter = seat_data.get("starter", "Keine")
    hotmeal = seat_data.get("hotmeal", "Keine")
    quickmeal = seat_data.get("quickmeal", False)

    if quickmeal:
        return f"🟣 {seat}"  # Quick Meal
    elif hotmeal not in (None, "—", "Keine"):
        return f"🟢 {seat}"  # Hot Meal gewählt
    elif starter not in (None, "—", "Keine"):
        return f"🟡 {seat}"  # Nur Vorspeise
    else:
        return f"{seat}"  # noch nichts gewählt

# -----------------------------
# Seatmap Anzeige (Mobilefreundlich)
# -----------------------------
st.subheader("Seatmap")
for row in seatmap:
    # 3 Blöcke: links (A,C), middle (D,G), right (H,K)
    left = [row[0], row[1]]   # A,C
    middle = [row[3], row[4]] # D,G
    right = [row[6], row[7]]  # H,K

    cols_left = st.columns(len(left))
    for i, seat in enumerate(left):
        if seat is None:
            cols_left[i].write("")
        else:
            seat_data = st.session_state.seats.get(seat, {})
            label = get_seat_label(seat_data, seat)
            if cols_left[i].button(label, key=f"seat_{seat}"):
                st.session_state.selected_seat = seat

    cols_middle = st.columns(len(middle))
    for i, seat in enumerate(middle):
        if seat is None:
            cols_middle[i].write("")
        else:
            seat_data = st.session_state.seats.get(seat, {})
            label = get_seat_label(seat_data, seat)
            if cols_middle[i].button(label, key=f"seat_{seat}"):
                st.session_state.selected_seat = seat

    cols_right = st.columns(len(right))
    for i, seat in enumerate(right):
        if seat is None:
            cols_right[i].write("")
        else:
            seat_data = st.session_state.seats.get(seat, {})
            label = get_seat_label(seat_data, seat)
            if cols_right[i].button(label, key=f"seat_{seat}"):
                st.session_state.selected_seat = seat

st.markdown("---")

# -----------------------------
# Catering Übersicht auf Hauptseite
# -----------------------------
st.subheader("Cateringzahlen")
catering_cols = st.columns(len(st.session_state.catering))
for i, meal in enumerate(st.session_state.catering):
    remaining = st.session_state.catering[meal]
    backup_num = st.session_state.backup.get(meal, 0)
    total_display = str(remaining)
    if remaining <= 0 and backup_num > 0:
        total_display = f"0 ({backup_num})"
    elif remaining <= 0 and backup_num <= 0:
        total_display = "0"

    # Rot färben, wenn nichts mehr verfügbar
    if remaining <= 0 and backup_num <= 0:
        catering_cols[i].markdown(f"<span style='color:red'>{meal}: {total_display}</span>", unsafe_allow_html=True)
    else:
        catering_cols[i].markdown(f"{meal}: {total_display}")

st.markdown("---")

# -----------------------------
# Sitz-Detailbereich (Expander = Popup Ersatz)
# -----------------------------
if st.session_state.selected_seat:
    seat = st.session_state.selected_seat

    # Sitzdaten anlegen, falls noch nicht vorhanden
    if seat not in st.session_state.seats:
        st.session_state.seats[seat] = {
            "starter": "Keine",
            "hotmeal": "Keine",
            "special": "",
            "quickmeal": False,
            "pad": False  # PAD Checkbox
        }

    seat_data = st.session_state.seats[seat]

    # Expander automatisch geöffnet
    with st.expander(f"Sitz {seat} - Details", expanded=True):
        # Vorspeise
        seat_data["starter"] = st.selectbox(
            "Vorspeise",
            ["Keine"] + starters[1:],
            index=(["Keine"] + starters[1:]).index(seat_data["starter"]),
            key=f"starter_{seat}"
        )

        # Hot Meal
        seat_data["hotmeal"] = st.selectbox(
            "Hot Meal",
            ["Keine"] + hotmeals[1:],
            index=(["Keine"] + hotmeals[1:]).index(seat_data["hotmeal"]),
            key=f"hotmeal_{seat}"
        )

        # Quick Meal Checkbox
        seat_data["quickmeal"] = st.checkbox(
            "Quick Meal",
            value=seat_data.get("quickmeal", False),
            key=f"quickmeal_{seat}"
        )

        # PAD Checkbox
        seat_data["pad"] = st.checkbox(
            "PAD",
            value=seat_data.get("pad", False),
            key=f"pad_{seat}"
        )

        # Special Request
        seat_data["special"] = st.text_input(
            "Special Request",
            value=seat_data["special"],
            key=f"special_{seat}"
        )

        # Speichern Button
        if st.button("Speichern", key=f"save_{seat}"):
            st.session_state.selected_seat = None
            st.success(f"Sitz {seat} gespeichert!")

