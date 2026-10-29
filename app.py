# ==========================================================
# YummyGo Food Delivery Order Cost Calculator
# Framework: Streamlit
# Run with: streamlit run app.py
# ==========================================================

import os
import base64
import streamlit as st

# ----------------------------------------------------------
# PAGE SETUP
# ----------------------------------------------------------
st.set_page_config(page_title="YummyGo Delivery Calculator", page_icon="🍔", layout="centered")

# ----------------------------------------------------------
# CUSTOM STYLING (CSS) - brown and pink look
# ----------------------------------------------------------
# CSS is the language that controls colours and fonts of a web page.
# We pass it to Streamlit as text and tell it to treat it as HTML.
st.markdown("""
<style>
    /* Big brown page heading (no gradient box) */
    .main-title {
        color: #5C3317;
        font-size: 3.6rem;
        font-weight: 800;
        text-align: center;
        line-height: 1.1;
        margin: 10px 0 6px 0;
    }
    .sub-title {
        color: #8B4513;
        font-size: 1.15rem;
        text-align: center;
        margin-bottom: 24px;
    }

    /* Section headings in brown */
    h2, h3 { color: #5C3317 !important; }

    /* Pink buttons with brown text and rounded corners */
    div.stButton > button {
        background-color: #E75480;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 26px;
        font-weight: 600;
    }
    div.stButton > button:hover {
        background-color: #8B4513;
        color: white;
    }

    /* Rounded images */
    img { border-radius: 14px; }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# BACKGROUND WATERMARK - cartoon food doodles (like a chat wallpaper)
# ----------------------------------------------------------
# Each food doodle is a tiny drawing made of simple shapes (SVG).
# Dictionary: doodle name -> the shapes that draw it (centred on 0,0)
DOODLES = {
    "donut": '<circle r="22" fill="#F4A6C0"/><circle r="7" fill="#FFF0F5"/><path d="M-14,-10 l5,-3 M8,-16 l3,5 M14,4 l-5,3 M-4,16 l4,-4 M-16,6 l5,2" stroke="#FFF" stroke-width="2.5"/>',
    "pizza": '<path d="M0,-26 L-19,20 Q0,30 19,20 Z" fill="#FFD58A"/><path d="M-19,20 Q0,30 19,20" fill="none" stroke="#C97B3A" stroke-width="5"/><circle cx="-2" cy="-6" r="4.5" fill="#E75480"/><circle cx="-8" cy="8" r="4" fill="#E75480"/><circle cx="7" cy="9" r="4" fill="#E75480"/>',
    "cookie": '<circle r="21" fill="#E0A96D"/><circle cx="-8" cy="-7" r="3" fill="#8B4513" stroke="none"/><circle cx="7" cy="-9" r="2.5" fill="#8B4513" stroke="none"/><circle cx="3" cy="5" r="3" fill="#8B4513" stroke="none"/><circle cx="-9" cy="9" r="2.5" fill="#8B4513" stroke="none"/><circle cx="12" cy="7" r="2" fill="#8B4513" stroke="none"/>',
    "burger": '<path d="M-24,-4 Q-24,-26 0,-26 Q24,-26 24,-4 Z" fill="#E0A96D"/><path d="M-24,-1 q6,6 12,0 q6,6 12,0 q6,6 12,0 q6,6 12,0" fill="none" stroke="#7BAE5A" stroke-width="4"/><rect x="-25" y="5" width="50" height="9" rx="4.5" fill="#8B4513"/><rect x="-24" y="16" width="48" height="8" rx="4" fill="#E0A96D"/><path d="M-10,-17 l3,2 M3,-20 l3,2 M12,-12 l3,2" stroke="#FFF" stroke-width="2"/>',
    "icecream": '<path d="M-13,2 L13,2 L0,34 Z" fill="#E0A96D"/><path d="M-8,10 L8,10 M-4,19 L4,19" stroke="#8B4513" stroke-width="1.5"/><circle cy="-9" r="15" fill="#F4A6C0"/>',
    "fries": '<rect x="-13" y="-24" width="6" height="26" rx="2" fill="#FFD58A"/><rect x="-5" y="-30" width="6" height="32" rx="2" fill="#FFD58A"/><rect x="3" y="-25" width="6" height="27" rx="2" fill="#FFD58A"/><rect x="10" y="-20" width="5" height="22" rx="2" fill="#FFD58A"/><path d="M-17,0 L17,0 L12,28 L-12,28 Z" fill="#E75480"/>',
    "cup": '<path d="M-13,-12 L13,-12 L10,30 L-10,30 Z" fill="#F8C8DC"/><rect x="-15" y="-18" width="30" height="7" rx="3" fill="#E75480"/><path d="M4,-18 L9,-34 L16,-34" fill="none" stroke-width="3"/><path d="M-9,4 L9,4" stroke="#E75480" stroke-width="5"/>',
}

# List of (doodle name, x position, y position, tilt angle) inside one 320 x 320 tile
PLACEMENTS = [
    ("donut", 50, 55, -15), ("pizza", 165, 50, 15), ("cookie", 275, 62, -10),
    ("burger", 105, 150, 8), ("icecream", 225, 158, -14), ("fries", 45, 255, 12),
    ("cup", 160, 265, -8), ("pizza", 275, 265, -20),
]

# Put every doodle into one SVG picture (one tile of the wallpaper)
shapes = ""
for name, x, y, angle in PLACEMENTS:
    shapes += f'<g transform="translate({x},{y}) rotate({angle})">{DOODLES[name]}</g>'
tile_svg = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="320" height="320">'
    '<g fill="none" stroke="#8B4513" stroke-width="2.5" stroke-linecap="round" '
    f'stroke-linejoin="round" opacity="0.28">{shapes}</g></svg>'
)

# Convert the picture to text (base64) so CSS can use it as a repeating background
tile_b64 = base64.b64encode(tile_svg.encode("utf-8")).decode()
st.markdown(f"""
<style>
    .stApp {{
        background-image: url("data:image/svg+xml;base64,{tile_b64}");
        background-size: 320px 320px;
        background-repeat: repeat;
    }}
    [data-testid="stAppViewContainer"], [data-testid="stMain"], .stMain {{
        background: transparent !important;
    }}
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------
# BUSINESS DATA (stored in dictionaries)
# ----------------------------------------------------------
# Nested dictionary: cuisine -> {dish name: price in rupees}
MENU = {
    "North Indian": {"Butter Chicken": 320, "Paneer Tikka Masala": 280, "Dal Makhani": 220, "Butter Naan": 40},
    "South Indian": {"Masala Dosa": 120, "Idli Sambar": 90, "Medu Vada": 80, "Filter Coffee": 50},
    "Fast Food": {"Veg Burger": 130, "Chicken Burger": 170, "French Fries": 90, "Cold Drink": 60},
    "Pizza & Italian": {"Margherita Pizza": 249, "Farmhouse Pizza": 349, "Pasta Alfredo": 260, "Garlic Bread": 120},
}

# Dictionary: cuisine -> picture file name (without .jpg), stored in the images folder
CUISINE_IMAGES = {
    "North Indian": "north_indian",
    "South Indian": "south_indian",
    "Fast Food": "fast_food",
    "Pizza & Italian": "pizza",
}

# Dictionary: cuisine -> emoji shown in the menu heading
CUISINE_EMOJI = {
    "North Indian": "🍛",
    "South Indian": "🥞",
    "Fast Food": "🍔",
    "Pizza & Italian": "🍕",
}

# Business constants
FOOD_GST_RATE = 0.05        # 5% GST on food
SERVICE_GST_RATE = 0.18     # 18% GST on delivery + platform fee + packaging
PLATFORM_FEE = 5            # fixed platform fee per order (Rs)
PACKAGING_PER_ITEM = 5      # packaging charge per item (Rs)
EXPRESS_CHARGE = 40         # extra charge for express delivery (Rs)


# ----------------------------------------------------------
# HELPER FUNCTION: show a picture safely
# ----------------------------------------------------------
def show_image(name):
    """Show images/<name>.jpg (or .jpeg/.png/.webp). If no file exists, skip quietly."""
    for ext in [".jpg", ".jpeg", ".png", ".webp"]:
        path = os.path.join("images", name + ext)
        if os.path.exists(path):
            try:
                st.image(path, width="stretch")   # newer Streamlit versions
            except Exception:
                st.image(path)                    # older versions
            return True
    return False  # picture not found - the app still works without it


# ----------------------------------------------------------
# FUNCTION 1: delivery fee based on distance
# ----------------------------------------------------------
def get_delivery_fee(distance_km):
    """Return the delivery fee for a distance, or None if too far to deliver."""
    if distance_km <= 3:
        return 30
    elif distance_km <= 7:
        return 50
    elif distance_km <= 15:
        return 80
    else:
        return None  # we do not deliver beyond 15 km


# ----------------------------------------------------------
# FUNCTION 2: coupon discount logic
# ----------------------------------------------------------
def apply_coupon(code, food_total):
    """Return (discount_amount, free_delivery_flag, message) for a coupon code."""
    code = code.strip().upper()  # clean the text typed by the user

    if code == "":
        return 0.0, False, ""

    if code == "WELCOME50":
        if food_total >= 199:
            return min(food_total * 0.50, 100), False, "WELCOME50 applied: 50% off (max Rs 100)"
        return 0.0, False, "WELCOME50 needs a minimum food order of Rs 199"
    elif code == "SAVE20":
        if food_total >= 300:
            return min(food_total * 0.20, 80), False, "SAVE20 applied: 20% off (max Rs 80)"
        return 0.0, False, "SAVE20 needs a minimum food order of Rs 300"
    elif code == "FREEDEL":
        if food_total >= 249:
            return 0.0, True, "FREEDEL applied: delivery is free"
        return 0.0, False, "FREEDEL needs a minimum food order of Rs 249"
    else:
        return 0.0, False, "Invalid coupon code"


# ----------------------------------------------------------
# FUNCTION 3: main bill calculation
# ----------------------------------------------------------
def calculate_bill(food_total, total_items, distance_km, express, is_member, coupon, tip, eco_packaging):
    """Calculate every part of the bill and return the results in a dictionary."""
    delivery_fee = get_delivery_fee(distance_km)
    if delivery_fee is None:
        return None  # not deliverable

    if express:
        delivery_fee += EXPRESS_CHARGE

    discount, free_delivery, coupon_msg = apply_coupon(coupon, food_total)

    if is_member or free_delivery:
        delivery_fee = 0

    packaging = PACKAGING_PER_ITEM * total_items
    if eco_packaging:
        packaging = packaging * 2

    food_after_discount = food_total - discount
    food_gst = food_after_discount * FOOD_GST_RATE
    service_gst = (delivery_fee + PLATFORM_FEE + packaging) * SERVICE_GST_RATE

    total = (food_after_discount + food_gst + delivery_fee
             + PLATFORM_FEE + packaging + service_gst + tip)

    return {
        "food_total": food_total,
        "discount": discount,
        "coupon_msg": coupon_msg,
        "delivery_fee": delivery_fee,
        "platform_fee": PLATFORM_FEE,
        "packaging": packaging,
        "food_gst": food_gst,
        "service_gst": service_gst,
        "tip": tip,
        "total": total,
    }


# ----------------------------------------------------------
# USER INTERFACE
# ----------------------------------------------------------
# Photo at the very top of the page (shown only if images/banner exists)
show_image("banner")

# Header banner (HTML + the CSS defined above)
st.markdown("""
<div class="main-title">🍔 YummyGo Food Delivery</div>
<div class="sub-title">Build your order and see the exact final bill before you pay - no surprises!</div>
""", unsafe_allow_html=True)

# ---- SIDEBAR INPUTS ----
st.sidebar.header("🚚 Delivery Details")

cuisine = st.sidebar.selectbox("Choose Cuisine", list(MENU.keys()))
distance = st.sidebar.number_input("Delivery Distance (km)", min_value=0.0, max_value=50.0, value=2.0, step=0.5)
speed = st.sidebar.radio("Delivery Speed", ["Standard", "Express (+Rs 40)"])
express = speed.startswith("Express")
is_member = st.sidebar.checkbox("I am a YummyGo Premium member (free delivery)")
eco_packaging = st.sidebar.checkbox("Eco-friendly packaging (2x packaging charge)")

# ---- MAIN PAGE: cuisine picture and menu ----
st.subheader(f"{CUISINE_EMOJI[cuisine]} {cuisine} Menu")
show_image(CUISINE_IMAGES[cuisine])
st.caption("Select the quantity for each dish you want.")

order = {}           # dish -> quantity
food_total = 0       # running total of food cost
total_items = 0      # total number of items ordered

for dish, price in MENU[cuisine].items():
    qty = st.number_input(f"{dish} - Rs {price}", min_value=0, max_value=20, value=0, step=1, key=f"{cuisine}_{dish}")
    if qty > 0:
        order[dish] = qty
        food_total += price * qty
        total_items += qty

# ---- Coupon and tip ----
col1, col2 = st.columns(2)
with col1:
    coupon = st.text_input("Coupon Code (try WELCOME50, SAVE20, FREEDEL)")
with col2:
    tip = st.number_input("Tip for Delivery Partner (Rs)", min_value=0.0, max_value=500.0, value=0.0, step=10.0)

# ----------------------------------------------------------
# CALCULATE AND SHOW RESULT
# ----------------------------------------------------------
if st.button("Calculate My Bill", type="primary"):
    try:
        if total_items == 0:
            st.warning("Please select at least one dish before calculating.")
        else:
            bill = calculate_bill(food_total, total_items, distance, express,
                                  is_member, coupon, tip, eco_packaging)

            if bill is None:
                st.error("Sorry, we deliver only within 15 km. Please reduce the distance.")
            else:
                st.subheader("🧾 Your Order")
                rows = []
                for dish, qty in order.items():
                    rows.append({"Dish": dish, "Qty": qty,
                                 "Price (Rs)": MENU[cuisine][dish],
                                 "Amount (Rs)": MENU[cuisine][dish] * qty})
                st.table(rows)

                if bill["coupon_msg"] != "":
                    if "applied" in bill["coupon_msg"]:
                        st.success(bill["coupon_msg"])
                    else:
                        st.warning(bill["coupon_msg"])

                # Three headline numbers side by side
                st.subheader("💰 Bill Summary")
                m1, m2, m3 = st.columns(3)
                m1.metric("Food Total", f"Rs {bill['food_total']:,.2f}")
                m2.metric("Delivery Fee", f"Rs {bill['delivery_fee']:,.2f}")
                m3.metric("Total Payable", f"Rs {bill['total']:,.2f}")

                # Full breakdown inside an expandable section
                with st.expander("See full bill breakdown"):
                    st.write(f"Food Total: Rs {bill['food_total']:,.2f}")
                    st.write(f"Coupon Discount: - Rs {bill['discount']:,.2f}")
                    st.write(f"Delivery Fee: Rs {bill['delivery_fee']:,.2f}")
                    st.write(f"Platform Fee: Rs {bill['platform_fee']:,.2f}")
                    st.write(f"Packaging Charge: Rs {bill['packaging']:,.2f}")
                    st.write(f"GST on Food (5%): Rs {bill['food_gst']:,.2f}")
                    st.write(f"GST on Services (18%): Rs {bill['service_gst']:,.2f}")
                    st.write(f"Delivery Partner Tip: Rs {bill['tip']:,.2f}")

                st.success(f"### Total Payable: Rs {bill['total']:,.2f}")

                minutes = 20 + int(distance * 4)
                if express:
                    minutes = int(minutes * 0.7)
                st.info(f"⏱️ Estimated delivery time: about {minutes} minutes")
    except Exception as error:
        st.error(f"Something went wrong: {error}. Please check your inputs and try again.")
