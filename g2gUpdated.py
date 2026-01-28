import streamlit as st

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(layout="wide", page_title="galley2guest")
st.title("A350 g2g")

# -----------------------------
# Seatmap & Meals
# -----------------------------
seatmap = [
    ["1A", "1C", None, "1D", "1G", None, "1H", "1K"],
    ["2A", "2C", None, "2D", "2G", None, "2H", "2K"],
    ["3A", "3C", None, "3D", "3G", None, "3H", "3K"],
    ["4A", "4C", None, "4D", "4G", None, "4H", "4K"],
    ["5A", "5C", None, "5D", "5G", None, "5H", "5K"],
]

starters = ["VSV", "VSF"]
hotmeals = ["HMC", "HMV", "HMF", "HMR"]

# -----------------------------
# Session State
# -----------------------------
if "seats" not in st.session_state:
    st.session_state.seats = {}

if "catering" not in st.session_state:
    st.session_state.catering = {m: 0 for m in starters + hotmeals}

if "backup" not in st.session_state:
    st.session_state.backup = {m: 0 for m in starters + hotmeals if m != "HMC"}  # HMC kein Backup

if "selected_seat" not in st.session_state:
    st.session_state.selected_seat = None

# -----------------------------
# Catering Eingabe
# -----------------------------
with st.expander("Mealcount"):
    st.markdown("Catering")
    for meal in st.session_state.catering:
        st.session_state.catering[meal] = st.number_input(
            f"{meal}", min_value=0, value=st.session_state.catering[meal], step=1, key=f"catering_{meal}"
        )

with st.expander("Crewmeals(nachladen!))"):
    st.markdown("### Backup")
    for meal in st.session_state.backup:
        st.session_state.backup[meal] = st.number_input(
            f"{meal}", min_value=0, value=st.session_state.backup[meal], step=1, key=f"backup_{meal}"
        )

st.markdown("---")

# -----------------------------
# Funktion: Sitzstatus Label
# -----------------------------
def get_seat_label(seat_data, seat):
    if seat_data.get("quickmeal"):
        return f"🟣 {seat}"
    elif seat_data.get("hotmeal") and seat_data.get("hotmeal") != "Keine":
        return f"🟢 {seat}"
    elif seat_data.get("starter") and seat_data.get("starter") != "Keine":
        return f"🟡 {seat}"
    else:
        return seat

# -----------------------------
# Seatmap Anzeige
# -----------------------------
st.subheader("Seatmap")

for row in seatmap:
    left = [row[0], row[1]]   # A,C
    middle = [row[3], row[4]] # D,G
    right = [row[6], row[7]]  # H,K

    # Links
    cols_left = st.columns(len(left))
    for i, seat in enumerate(left):
        if seat is None:
            cols_left[i].write("")
        else:
            seat_data = st.session_state.seats.get(seat, {})
            label = get_seat_label(seat_data, seat)
            if cols_left[i].button(label, key=f"seat_{seat}"):
                st.session_state.selected_seat = seat

    # Mitte
    cols_middle = st.columns(len(middle))
    for i, seat in enumerate(middle):
        if seat is None:
            cols_middle[i].write("")
        else:
            seat_data = st.session_state.seats.get(seat, {})
            label = get_seat_label(seat_data, seat)
            if cols_middle[i].button(label, key=f"seat_{seat}"):
                st.session_state.selected_seat = seat

    # Rechts
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
# Sitz-Detail Popup (Expander)
# -----------------------------
if st.session_state.selected_seat:
    seat = st.session_state.selected_seat
    if seat not in st.session_state.seats:
        st.session_state.seats[seat] = {
            "starter": "Keine",
            "hotmeal": "Keine",
            "quickmeal": False,
            "pad": False,
            "special": ""
        }

    seat_data = st.session_state.seats[seat]

    with st.expander(f"Sitz {seat} - Bestellung", expanded=True):
        seat_data["starter"] = st.selectbox(
            "Vorspeise",
            ["Keine"] + starters,
            index=(["Keine"] + starters).index(seat_data["starter"]),
            key=f"starter_{seat}"
        )
        seat_data["hotmeal"] = st.selectbox(
            "Hot Meal",
            ["Keine"] + hotmeals,
            index=(["Keine"] + hotmeals).index(seat_data["hotmeal"]),
            key=f"hotmeal_{seat}"
        )
        seat_data["quickmeal"] = st.checkbox(
            "Quick Meal",
            value=seat_data.get("quickmeal", False),
            key=f"quickmeal_{seat}"
        )
        seat_data["pad"] = st.checkbox(
            "PAD",
            value=seat_data.get("pad", False),
            key=f"pad_{seat}"
        )
        seat_data["special"] = st.text_input(
            "Special Request",
            value=seat_data.get("special",""),
            key=f"special_{seat}"
        )

        if st.button("Speichern", key=f"save_{seat}"):
            st.session_state.selected_seat = None
            st.success(f"Sitz {seat} gespeichert!")

st.markdown("---")

# -----------------------------
# Service-Ansicht
# -----------------------------
if st.button("Service-Anzeige"):
    st.subheader("Service Ansicht")
    for row in seatmap:
        row_display = []
        for seat in row:
            if seat is None:
                row_display.append("  ")
            else:
                data = st.session_state.seats.get(seat, {})
                display = seat
                if data.get("starter") and data["starter"] != "Keine":
                    display += f" | {data['starter']}"
                if data.get("hotmeal") and data["hotmeal"] != "Keine":
                    display += f" | {data['hotmeal']}"
                if data.get("quickmeal"):
                    display += " | QuickMeal"
                if data.get("pad"):
                    display += " | PAD"
                if data.get("special"):
                    display += f" | {data['special']}"
                row_display.append(display)
        st.write(" | ".join(row_display))
