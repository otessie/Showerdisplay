import streamlit as st
import time

#Onthouden wanneer de douche aan staat
if "shower_running" not in st.session_state:
    st.session_state.shower_running = False

#Onthouden wanneer de timer is begonnen
if "start_time" not in st.session_state:
    st.session_state.start_time = None

#Onthouden hoeveel tijd de douche duurde
if "elapsed_time" not in st.session_state:
    st.session_state.elapsed_time = 0

#Water flow maken liters per minuut
if "water_flow" not in st.session_state:
    st.session_state.water_flow = 6

#summary maken
if "show_summary" not in st.session_state:
    st.session_state.show_summary = False

#Page title maken
st.set_page_config(
    page_title="Smart Shower Dashboard",
    page_icon=":shower:",
    layout="centered",
)
#layout display
st.markdown("""
    <style>
    .stApp {
        background-color: #005d72;
        color: #d4f7ff;
    } [data-testid="stHeader"] {
    background: transparent;
    height: 0;
}
[data-testid="stDecoration"] {
    display: none;
}
    </style>
    """, unsafe_allow_html=True)

#Boven title
st.title(":shower: Hydrosense Shower Dashboard")

#Tekstje onder de title
st.write(
    "Making shower consumption visible! "
    "See how much water, energy and money you use."
)
#Devider onder de titles
st.divider()

#start en stop knop voor de douche
col1, col2 = st.columns(2)

with col1:
    if st.button(":record_button: Start shower", use_container_width=True):
        st.session_state.shower_running = True
        st.session_state.start_time = time.time()
        st.session_state.show_summary = False


with col2:
    if st.button(":stop_button: Stop shower", use_container_width=True):
        if st.session_state.shower_running:
            st.session_state.elapsed_time = int(
                time.time() - st.session_state.start_time
            )
            st.session_state.shower_running = False
            st.session_state.show_summary = True

#laten weten of de douche aan of uit staat
if st.session_state.shower_running:
    st.success("Your shower is on!")
else:
    st.info("Your shower is off.")

#Douche timer
st.subheader("Your shower time:")


if st.session_state.shower_running:
    elapsed_time = int(time.time() - st.session_state.start_time)
else:
    elapsed_time = st.session_state.elapsed_time

minutes = elapsed_time // 60
seconds = elapsed_time % 60

st.markdown(
    f"<h1 style='text-align: left; font-size: 55px;'>{minutes:02d}:{seconds:02d}</h1>",
    unsafe_allow_html=True
)

#Berekenen water flow
water_used = (elapsed_time / 60) * st.session_state.water_flow

#Berekenen energy used
energy_used = water_used * 4186 * 25 / 3600000

#Berekenen total cost
total_cost = (energy_used * 0.337) + (water_used * 0.00271)

#Display
st.subheader("Your shower consumption")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True, height=140):
        st.markdown("**:droplet: Water used**")
        st.markdown(f"<h3 style='color: #d4f7ff; white-space: nowrap;'>{water_used:.1f} L</h3>", unsafe_allow_html=True)

with col2:
    with st.container(border=True, height=140):
        st.markdown("**:zap: Energy used**")
        st.markdown(f"<h3 style='color: #d4f7ff; white-space: nowrap;'>{energy_used:.3f} kWh</h3>", unsafe_allow_html=True)

with col3:
    with st.container(border=True, height=140):
        st.markdown("**:euro: Total cost**")
        st.markdown(f"<h3 style='color: #d4f7ff; white-space: nowrap;'>€{total_cost:.2f}</h3>", unsafe_allow_html=True)

st.divider()

#douche samenvatting
if st.session_state.show_summary and not st.session_state.shower_running:
    st.subheader(":shower: Your shower summary")
    st.write(f"**Shower time:** {minutes:02d}:{seconds:02d}")
    st.write(f"**Water used:** {water_used:.1f} L")
    st.write(f"**Energy used:** {energy_used:.3f} kWh")
    st.write(f"**Total cost:** €{total_cost:.2f}")

#Blijven refreshen als de douche aanstaat
if st.session_state.shower_running:
    time.sleep(1)
    st.rerun()




