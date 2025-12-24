import streamlit as st
import pandas as pd
import textwrap

# Page Config
st.set_page_config(layout="wide", page_title="NetCompare")

# Custom CSS to match the original React Dark Theme
st.markdown(textwrap.dedent("""
    <style>
    /* Global Background & Text */
    .stApp {
        background-color: #0b1121; /* Darker navy background for the page */
        color: #ffffff;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #0f172a; /* Slightly lighter than main bg */
        border-right: 1px solid #1e293b;
    }
    
    /* Target the Containers used for Cards */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%); /* Subtle gradient */
        border: 1px solid #334155;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        padding: 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); /* Smoother transition */
        height: 100%; 
        min-height: 620px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        overflow: hidden; /* For image zoom containment */
        position: relative;
    }
    
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #60a5fa; /* Lighter blue border */
        box-shadow: 0 0 25px rgba(59, 130, 246, 0.4), 0 10px 10px rgba(0,0,0,0.5); /* Blue glow */
        transform: translateY(-8px); /* Higher lift */
        z-index: 10;
    }

    /* Remove default padding from the container inner wrapper to control layout */
    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        gap: 0.5rem;
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    /* Push the last element (Button) to the bottom */
    div[data-testid="stVerticalBlockBorderWrapper"] > div > div:last-child {
        margin-top: auto;
    }
    
    /* Ensure images have consistent height container and Zoom Effect */
    div[data-testid="stVerticalBlockBorderWrapper"] > div > div:nth-child(4) {
        min-height: 180px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }
    
    /* Target the image element for Zoom */
    div[data-testid="stVerticalBlockBorderWrapper"]:hover img {
        transform: scale(1.1);
        transition: transform 0.4s ease;
    }
    
    img {
        transition: transform 0.4s ease; /* Smooth zoom out */
    }
    
    /* Button Styling */
    .stButton button {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
        width: 100%;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    .stButton button:hover {
        background: linear-gradient(90deg, #60a5fa 0%, #3b82f6 100%);
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.5);
    }
    .stButton button:active {
        transform: scale(0.98);
        box-shadow: none;
    }

    /* Specs Grid */
    .specs-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
        border-top: 1px solid #334155; 
        padding-top: 1rem;
        min-height: 120px; /* Fix height for specs area */
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
        font-weight: 700;
        letter-spacing: -0.025em;
    }

    /* Custom classes for content */
    .card-label {
        color: #94a3b8;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
    }
    
    .card-title {
        color: #ffffff;
        font-size: 1.125rem;
        font-weight: 600;
        line-height: 1.3;
        margin-bottom: 0.5rem;
        height: 3rem; /* Fixed height for 2 lines */
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }
    
    .spec-row {
        display: flex;
        align-items: flex-start;
        font-size: 0.8rem;
        color: #cbd5e1;
        line-height: 1.4;
    }
    
    .spec-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 20px;
        height: 20px;
        margin-right: 6px;
        flex-shrink: 0;
        color: #94a3b8; /* Muted icon color */
    }
    
    /* Comparison Table Styling */
    .comparison-header {
        background-color: #1e293b;
        padding: 1rem;
        border-bottom: 1px solid #334155;
        text-align: center;
        font-weight: 700;
    }
    .comparison-cell {
        padding: 1rem;
        border-bottom: 1px solid #334155;
        color: #e2e8f0;
        font-size: 0.9rem;
    }
    
    /* Badges */
    .badge {
        font-size: 0.7rem;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-weight: 600;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
    .badge-wifi7 { background-color: rgba(16, 185, 129, 0.2); color: #34d399; }
    .badge-wifi6e { background-color: rgba(139, 92, 246, 0.2); color: #a78bfa; }
    .badge-wifi6 { background-color: rgba(59, 130, 246, 0.2); color: #60a5fa; }
    
    /* Block Container Padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }
    </style>
"""), unsafe_allow_html=True)

# Data
aps = [
    {
        "id": 1,
        "model": "Aruba AP-754/755",
        "vendor": "Aruba",
        "standard": "Wi-Fi 7",
        "throughput": "28.8 Gbps",
        "radios": "4x4:4 (All bands)",
        "ports": "2x 10GbE SmartRate",
        "image": "https://www.arubanetworks.com/assets/images/Aruba_AP-750_Series_Front_Right_Angle_Shadow.png",
        "details": {
            "Antenna Type": "Internal/External",
            "Max Power Consumption": "42.5W (DC)",
            "Max Clients": "2048 per radio",
            "Bluetooth/Zigbee": "Yes (Gen 2)",
            "Controller-less": "Yes",
            "Dimensions": "260mm x 260mm x 56mm"
        }
    },
    {
        "id": 2,
        "model": "Aruba AP-745",
        "vendor": "Aruba",
        "standard": "Wi-Fi 7",
        "throughput": "9.33 Gbps",
        "radios": "4x4 (6/5GHz) / 2x2 (2.4GHz)",
        "ports": "1x 5GbE SmartRate",
        "image": "https://www.arubanetworks.com/assets/images/Aruba_AP-745_Front_Right_Angle_Shadow.png",
        "details": {
            "Antenna Type": "Internal",
            "Max Power Consumption": "25.0W (PoE)",
            "Max Clients": "1024 per radio",
            "Bluetooth/Zigbee": "Yes (Gen 2)",
            "Controller-less": "Yes",
            "Dimensions": "210mm x 210mm x 57mm"
        }
    },
    {
        "id": 3,
        "model": "Aruba AP-734/735",
        "vendor": "Aruba",
        "standard": "Wi-Fi 7",
        "throughput": "14.4 Gbps",
        "radios": "2x2:2 (All bands)",
        "ports": "2x 5GbE SmartRate",
        "image": "https://www.arubanetworks.com/assets/images/Aruba_AP-735_Front_Right_Angle_Shadow.png",
        "details": {
            "Antenna Type": "Internal/External",
            "Max Power Consumption": "26.4W (PoE)",
            "Max Clients": "512 per radio",
            "Bluetooth/Zigbee": "Yes (Gen 2)",
            "Controller-less": "Yes",
            "Dimensions": "200mm x 200mm x 45mm"
        }
    },
    {
        "id": 4,
        "model": "Aruba AP-655",
        "vendor": "Aruba",
        "standard": "Wi-Fi 6E",
        "throughput": "7.8 Gbps",
        "radios": "4x4:4 (All bands)",
        "ports": "2x 5GbE SmartRate",
        "image": "https://www.arubanetworks.com/assets/og/OG_Aruba-650-Series-Campus-Access-Points.jpg",
        "details": {
            "Antenna Type": "Internal",
            "Max Power Consumption": "51W",
            "Max Clients": "1024 per radio",
            "Bluetooth/Zigbee": "Yes",
            "Controller-less": "Yes",
            "Dimensions": "260mm x 260mm x 60mm"
        }
    },
    {
        "id": 5,
        "model": "Juniper AP45",
        "vendor": "Juniper",
        "standard": "Wi-Fi 6",
        "throughput": "5.95 Gbps",
        "radios": "4x4:4 (5GHz) + 2x2:2 (2.4GHz)",
        "ports": "1x 5GbE / 1x 1GbE",
        "image": "https://www.juniper.net/content/dam/www/assets/images/us/en/products/access-points/ap45-front.png/jcr:content/renditions/cq5dam.web.1280.1280.png",
        "details": {
            "Antenna Type": "Internal vBLE",
            "Max Power Consumption": "33W",
            "Max Clients": "1024",
            "Bluetooth": "Virtual (vBLE)",
            "Controller-less": "Cloud Managed (Mist)",
            "Dimensions": "260mm x 260mm x 76mm"
        }
    },
    {
        "id": 6,
        "model": "Juniper AP34",
        "vendor": "Juniper",
        "standard": "Wi-Fi 6E",
        "throughput": "3.9 Gbps",
        "radios": "2x2:2 (6/5/2.4GHz)",
        "ports": "1x 2.5GbE",
        "image": "https://www.juniper.net/content/dam/www/assets/images/us/en/products/access-points/ap34-front.png/jcr:content/renditions/cq5dam.web.1280.1280.png",
        "details": {
            "Antenna Type": "Omni-directional",
            "Max Power Consumption": "26W",
            "Max Clients": "512",
            "Bluetooth": "Integrated",
            "Controller-less": "Cloud Managed (Mist)",
            "Dimensions": "180mm x 180mm x 38mm"
        }
    },
    {
        "id": 7,
        "model": "Juniper AP24",
        "vendor": "Juniper",
        "standard": "Wi-Fi 6E",
        "throughput": "3.6 Gbps",
        "radios": "2x2:2 (6/5/2.4GHz)",
        "ports": "1x 1GbE",
        "image": "https://www.juniper.net/content/dam/www/assets/images/us/en/products/access-points/ap24-front.png/jcr:content/renditions/cq5dam.web.1280.1280.png",
        "details": {
            "Antenna Type": "Internal",
            "Max Power Consumption": "18W",
            "Max Clients": "256",
            "Bluetooth": "Integrated",
            "Controller-less": "Cloud Managed (Mist)",
            "Dimensions": "150mm x 150mm x 35mm"
        }
    },
    {
        "id": 8,
        "model": "Aruba AP-635",
        "vendor": "Aruba",
        "standard": "Wi-Fi 6E",
        "throughput": "3.9 Gbps",
        "radios": "2x2:2 (All bands)",
        "ports": "2x 2.5GbE SmartRate",
        "image": "https://www.arubanetworks.com/assets/images/Aruba_AP-635_Front_Center_Shadow_Parent.png",
        "details": {
            "Antenna Type": "Internal",
            "Max Power Consumption": "26.8W",
            "Max Clients": "512 per radio",
            "Bluetooth/Zigbee": "Yes",
            "Controller-less": "Yes",
            "Dimensions": "210mm x 210mm x 57mm"
        }
    }
]

df = pd.DataFrame(aps)

# State Initialization
if 'selected_products' not in st.session_state:
    st.session_state.selected_products = set()
    
if 'filters_vendor' not in st.session_state:
    st.session_state.filters_vendor = []

if 'filters_standard' not in st.session_state:
    st.session_state.filters_standard = []

# Helper Functions
def toggle_product_selection(product_id):
    if product_id in st.session_state.selected_products:
        st.session_state.selected_products.remove(product_id)
    else:
        st.session_state.selected_products.add(product_id)

def view_details_page(product_id):
    st.query_params["view"] = "details"
    st.query_params["product_id"] = product_id

def view_comparison_page():
    st.query_params["view"] = "compare"

def back_to_dashboard():
    st.query_params.clear()

# --- VIEWS ---

def show_comparison():
    st.button("← Back to Dashboard", on_click=back_to_dashboard)
    st.title("Compare Products")
    
    selected_ids = st.session_state.selected_products
    if not selected_ids:
        st.warning("No products selected for comparison.")
        return

    # Filter selected products
    selected_products = [p for p in aps if p['id'] in selected_ids]
    
    # Comparison Grid
    cols = st.columns(len(selected_products))
    
    # Common keys for detail comparison make sure all exist
    detail_keys = set()
    for p in selected_products:
        detail_keys.update(p.get('details', {}).keys())
    detail_keys = sorted(list(detail_keys))

    for idx, product in enumerate(selected_products):
        with cols[idx]:
            # Use container for visual grouping
            with st.container(border=True):
                st.image(product['image'], use_container_width=True)
                st.subheader(product['model'])
                
                # Main specs
                st.markdown("**Throughput**")
                st.write(product['throughput'])
                st.markdown("**Radios**")
                st.write(product['radios'])
                st.markdown("**Ports**")
                st.write(product['ports'])
                
                st.divider()
                st.markdown("#### Detailed Specs")
                
                for key in detail_keys:
                    val = product['details'].get(key, "-")
                    st.markdown(f"**{key}**")
                    st.write(val)
                    st.write("") # spacer

def show_details(product_id):
    product = next((p for p in aps if str(p['id']) == str(product_id)), None)
    
    if not product:
        st.error("Product not found.")
        st.button("Back to Dashboard", on_click=back_to_dashboard)
        return

    st.button("← Back to Dashboard", on_click=back_to_dashboard)

    # Header Section
    c_img, c_info = st.columns([1, 2])
    with c_img:
        st.image(product['image'], use_container_width=True)
    with c_info:
        st.caption(product['vendor'])
        st.title(product['model'])
        
        # Badge
        badge_class = "badge-wifi6"
        if product['standard'] == 'Wi-Fi 7':
            badge_class = "badge-wifi7"
        elif product['standard'] == 'Wi-Fi 6E':
            badge_class = "badge-wifi6e"
            
        st.markdown(f'<span class="badge {badge_class}">{product["standard"]}</span>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background-color: #1e293b; padding: 1.5rem; border-radius: 12px; border: 1px solid #334155; margin-top: 2rem;">
            <div style="font-size: 1.1rem; margin-bottom: 0.5rem;">⚡ <strong>Throughput:</strong> {product['throughput']}</div>
            <div style="font-size: 1.1rem; margin-bottom: 0.5rem;">📶 <strong>Radios:</strong> {product['radios']}</div>
            <div style="font-size: 1.1rem;">🔌 <strong>Ports:</strong> {product['ports']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    
    st.subheader("Technical Specifications")
    
    # Grid for details
    detail_items = list(product.get('details', {}).items())
    # Display in rows of 2
    for i in range(0, len(detail_items), 2):
        col1, col2 = st.columns(2)
        k1, v1 = detail_items[i]
        with col1:
             st.markdown(f"""
            <div style="padding: 1rem; border-bottom: 1px solid #334155;">
                <span style="color: #94a3b8; font-weight: 600;">{k1}</span>
                <div style="color: white; font-size: 1.05rem; margin-top: 4px;">{v1}</div>
            </div>
            """, unsafe_allow_html=True)
            
        if i + 1 < len(detail_items):
            k2, v2 = detail_items[i+1]
            with col2:
                st.markdown(f"""
                <div style="padding: 1rem; border-bottom: 1px solid #334155;">
                    <span style="color: #94a3b8; font-weight: 600;">{k2}</span>
                    <div style="color: white; font-size: 1.05rem; margin-top: 4px;">{v2}</div>
                </div>
                """, unsafe_allow_html=True)


def show_dashboard():
    # Sidebar
    with st.sidebar:
        st.title("Filters")
        
        if st.button("Reset Filters"):
            st.session_state.filters_vendor = []
            st.session_state.filters_standard = []
            st.rerun()

        st.subheader("VENDOR")
        vendors_list = sorted(list(set(df['vendor'])))
        selected_vendors = st.multiselect(
            "Select Vendor",
            vendors_list,
            default=st.session_state.filters_vendor,
            key="filters_vendor",
            label_visibility="collapsed"
        )

        st.subheader("WI-FI STANDARD")
        standards_list = sorted(list(set(df['standard'])))
        selected_standards = st.multiselect(
            "Select Standard",
            standards_list,
            default=st.session_state.filters_standard,
            key="filters_standard",
            label_visibility="collapsed"
        )
        
        # Compare Button in Sidebar
        if st.session_state.selected_products:
            st.divider()
            st.write(f"selected: {len(st.session_state.selected_products)}")
            st.button("Compare Selected", type="primary", on_click=view_comparison_page)

    # Main Content
    st.title("NetCompare")
    
    search_term = st.text_input("Search", placeholder="Search models, brands, or specs...", label_visibility="collapsed")
    st.markdown("---")

    # Filtering
    filtered_df = df.copy()
    if selected_vendors:
        filtered_df = filtered_df[filtered_df['vendor'].isin(selected_vendors)]
    if selected_standards:
        filtered_df = filtered_df[filtered_df['standard'].isin(selected_standards)]
    if search_term:
        search_lower = search_term.lower()
        filtered_df = filtered_df[
            filtered_df['model'].str.lower().str.contains(search_lower) | 
            filtered_df['vendor'].str.lower().str.contains(search_lower)
        ]

    st.subheader(f"Access Points ({len(filtered_df)})")
    
    # Grid Layout
    cols = st.columns(4)

    for idx, row in enumerate(filtered_df.to_dict('records')):
        col = cols[idx % 4]
        with col:
            with st.container(border=True):
                # 1. Top Row: Checkbox only (Right aligned)
                # Using columns to push checkbox to right
                c_spacer, c_chk = st.columns([5, 1])
                with c_chk:
                    is_selected = row['id'] in st.session_state.selected_products
                    st.checkbox(
                        "Select", 
                        key=f"chk_{row['id']}", 
                        value=is_selected,
                        on_change=toggle_product_selection,
                        args=(row['id'],),
                        label_visibility="collapsed"
                    )

                # 2. Image Area (Centered)
                st.image(row['image'], use_container_width=True)

                # 3. Content Area (Badge, Vendor, Title, Specs)
                # Badge logic
                badge_class = "badge-wifi6"
                if row['standard'] == 'Wi-Fi 7':
                    badge_class = "badge-wifi7"
                elif row['standard'] == 'Wi-Fi 6E':
                    badge_class = "badge-wifi6e"
                
                # Render content block
                st.markdown(f"""
                <div style="margin-top: 0.5rem; text-align: left;">
                    <span class="badge {badge_class}">{row["standard"]}</span>
                    <div class="card-label" style="text-align: left; margin-top: 0.5rem;">{row["vendor"]}</div>
                    <div class="card-title" style="text-align: left;">{row["model"]}</div>
                </div>
                
                <div class="specs-grid">
                    <div class="spec-row">
                        <span class="spec-icon">⚡</span>
                        <span>{row['throughput']}</span>
                    </div>
                    <div class="spec-row">
                        <span class="spec-icon">🔌</span>
                        <span>{row['ports']}</span>
                    </div>
                    <div class="spec-row">
                        <span class="spec-icon">📶</span>
                        <span>{row['radios']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # 4. Action Button
                st.button(
                    "View Details", 
                    key=f"btn_{row['id']}", 
                    use_container_width=True,
                    on_click=view_details_page,
                    args=(row['id'],)
                )

# --- AUTHENTICATION & USER MANAGEMENT ---
import json
import os

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {
            "admin": {
                "password": "password123", # Default
                "role": "admin",
                "force_change": True
            }
        }
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users_data):
    with open(USERS_FILE, "w") as f:
        json.dump(users_data, f, indent=4)

def init_user_store():
    # Always load fresh from disk on init or if not in session
    if "users" not in st.session_state:
        st.session_state["users"] = load_users()

def check_credentials():
    init_user_store()
    username = st.session_state.get("username")
    password = st.session_state.get("password")
    
    # Reload to ensure we have latest data
    users = load_users()
    st.session_state["users"] = users 
    
    if username in users and users[username]["password"] == password:
        st.session_state["authenticated"] = True
        st.session_state["current_user"] = username
        st.session_state["user_role"] = users[username]["role"]
        st.session_state["force_change"] = users[username].get("force_change", False)
        return True
    else:
        st.session_state["authenticated"] = False
        st.error("Invalid Username or Password")
        return False

def change_password(username, new_password):
    users = load_users()
    if username in users:
        users[username]["password"] = new_password
        users[username]["force_change"] = False
        save_users(users)
        
        # Update session immediately
        st.session_state["users"] = users
        st.session_state["force_change"] = False 
        return True
    return False

def add_user(username, password, role="user"):
    users = load_users()
    if username in users:
        return False
    users[username] = {
        "password": password,
        "role": role,
        "force_change": True
    }
    save_users(users)
    st.session_state["users"] = users
    return True

def delete_user(username):
    if username == "admin":
        return False 
    
    users = load_users()
    if username in users:
        del users[username]
        save_users(users)
        st.session_state["users"] = users
        return True
    return False

# --- VIEWS: AUTH ---

def show_login_page():
    # Login Page styling
    st.markdown("""
    <style>
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 2rem;
            background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid #334155;
            border-radius: 16px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
            text-align: center;
        }
        .login-title {
            color: white;
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">NetCompare Login</div>', unsafe_allow_html=True)
        st.write("Please sign in to continue")
        
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        
        if st.button("Sign In", type="primary", use_container_width=True):
            if check_credentials():
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)
        st.caption("Default: admin / password123")

def show_change_password_page():
    st.title("Change Password")
    st.warning("You must change your password to continue.")
    
    with st.form("change_pass_form"):
        new_pass = st.text_input("New Password", type="password")
        confirm_pass = st.text_input("Confirm Password", type="password")
        
        if st.form_submit_button("Update Password"):
            if new_pass != confirm_pass:
                st.error("Passwords do not match.")
            elif len(new_pass) < 4:
                st.error("Password is too short.")
            else:
                user = st.session_state["current_user"]
                change_password(user, new_pass)
                st.success("Password updated! Redirecting...")
                st.rerun()

def show_admin_page():
    st.title("Admin: User Management")
    st.write("Manage users and their access.")
    st.divider()
    
    # 1. List Users
    st.subheader("Current Users")
    users = st.session_state["users"]
    
    # Simple table display
    user_data = []
    for u, data in users.items():
        user_data.append({
            "Username": u,
            "Role": data["role"],
            "Need Password Change": "Yes" if data.get("force_change") else "No"
        })
    st.table(user_data)
    
    st.divider()
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Add New User")
        with st.form("add_user_form"):
            new_u = st.text_input("Username")
            new_p = st.text_input("Temporary Password", type="password")
            role = st.selectbox("Role", ["user", "admin"])
            
            if st.form_submit_button("Create User"):
                if add_user(new_u, new_p, role):
                    st.success(f"User {new_u} created.")
                    st.rerun()
                else:
                    st.error("User already exists.")
                    
    with c2:
        st.subheader("Delete User")
        with st.form("del_user_form"):
            del_u = st.selectbox("Select User", [u for u in users.keys() if u != "admin"])
            
            if st.form_submit_button("Delete"):
                if delete_user(del_u):
                    st.success(f"User {del_u} deleted.")
                    st.rerun()
                else:
                    st.error("Failed to delete user.")


def logout():
    st.session_state["authenticated"] = False
    st.session_state["current_user"] = None
    st.rerun()

# --- MAIN APP ROUTER ---
def main_app():
    # Show logout in sidebar
    with st.sidebar:
        st.write(f"Logged in as: **{st.session_state['current_user']}**")
        st.divider()
        
        # Navigation
        current_view = st.query_params.get("view", "dashboard")
        
        if st.button("Dashboard", use_container_width=True):
             st.query_params["view"] = "dashboard"
             st.rerun()
             
        if st.session_state["user_role"] == "admin":
             if st.button("User Management", use_container_width=True):
                  st.query_params["view"] = "admin"
                  st.rerun()
        
        st.divider()
        st.button("Logout", on_click=logout, use_container_width=True)

    # Middleware: Check Force Change
    if st.session_state.get("force_change", False):
        show_change_password_page()
        return

    # Router Logic
    view = st.query_params.get("view", "dashboard")

    if view == "compare":
        show_comparison()
    elif view == "details":
        pid = st.query_params.get("product_id")
        show_details(pid)
    elif view == "admin":
        if st.session_state["user_role"] == "admin":
            show_admin_page()
        else:
            st.error("Access Denied")
    else:
        show_dashboard()

if __name__ == "__main__":
    init_user_store()
    
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        main_app()
    else:
        show_login_page()

