# streamlit run app.py
# source .venv/scripts/activate

import streamlit as st
import numpy as np
import pandas as pd
from sklearn.neighbors import BallTree
import re

# pip install streamlit, numpy, pandas, scikit-learn, xgboost

st.title("Custom Apartment Prediction")
st.write("Input your specifications below")

# Initialize session state for all inputs if they don't exist
if 'latitude' not in st.session_state:
    st.session_state.latitude = 41.697007
if 'longitude' not in st.session_state:
    st.session_state.longitude = 44.799183
if 'urban' not in st.session_state:
    st.session_state.urban = "Saburtalo"
if 'bathroom_type' not in st.session_state:
    st.session_state.bathroom_type = "unspecified"
if 'area' not in st.session_state:
    st.session_state.area = 50
if 'condition' not in st.session_state:
    st.session_state.condition = "unspecified"
if 'room_num' not in st.session_state:
    st.session_state.room_num = "1"
if 'floor' not in st.session_state:
    st.session_state.floor = 1
if 'estate_status' not in st.session_state:
    st.session_state.estate_status = "ახალი აშენებული"
if 'bedroom_type' not in st.session_state:
    st.session_state.bedroom_type = "1"
if 'total_floors' not in st.session_state:
    st.session_state.total_floors = 5
if 'selected_features' not in st.session_state:
    st.session_state.selected_features = []
if 'storeroom_type' not in st.session_state:
    st.session_state.storeroom_type = "unspecified"
if 'swimming_pool_type' not in st.session_state:
    st.session_state.swimming_pool_type = "unspecified"
if 'living_room_type' not in st.session_state:
    st.session_state.living_room_type = "unspecified"
if 'build_year' not in st.session_state:
    st.session_state.build_year = "unspecified"
if 'height' not in st.session_state:
    st.session_state.height = 2.7
if 'balconies' not in st.session_state:
    st.session_state.balconies = 1
if 'parking_type' not in st.session_state:
    st.session_state.parking_type = "unspecified"
if 'for_special_people' not in st.session_state:
    st.session_state.for_special_people = "no"
if 'for_investment' not in st.session_state:
    st.session_state.for_investment = "no"
if 'heating_type' not in st.session_state:
    st.session_state.heating_type = "unspecified"
if 'project_type' not in st.session_state:
    st.session_state.project_type = "unspecified"
if 'hot_water_type' not in st.session_state:
    st.session_state.hot_water_type = "unspecified"
if 'material_type' not in st.session_state:
    st.session_state.material_type = "unspecified"
if 'other_features' not in st.session_state:
    st.session_state.other_features = []

# Define all the lists first
urbans = ["Saburtalo","Didi Dighomi","Vake","Isani","Krtsanisi","Didube","Samgori",
          "Gldani","Nadzaladevi","Mtatsminda","Chughureti","Vashlijvari"]

conditions = ["unspecified","ახალი გარემონტებული","ძველი გარემონტებული",
              "მწვანე კარკასი","შავი კარკასი","სარემონტო","მიმდინარე რემონტი",
              "თეთრი პლიუსი","თეთრი კარკასი"]
estate_status_types = ["ახალი აშენებული","ძველი აშენებული","მშენებარე"]

bathroom_types = ["unspecified","1","2","3+","საერთო"]

room_types = ["1","2","3","4","5","6","7","8","9","10+"]
bedroom_types = ["unspecified","1","2","3","4","5","6","7","8","9","10+"]

# Callback functions to update session state
#def update_latitude():
#    st.session_state.latitude = st.session_state.latitude_input

def update_longitude():
    st.session_state.longitude = st.session_state.longitude_input

def update_urban():
    st.session_state.urban = st.session_state.urban_input

def update_bathroom():
    st.session_state.bathroom_type = st.session_state.bathroom_input

def update_area():
    st.session_state.area = st.session_state.area_input

def update_condition():
    st.session_state.condition = st.session_state.condition_input

def update_room_num():
    st.session_state.room_num = st.session_state.room_num_input

def update_floor():
    st.session_state.floor = st.session_state.floor_input

def update_estate_status():
    st.session_state.estate_status = st.session_state.estate_status_input

def update_bedroom():
    st.session_state.bedroom_type = st.session_state.bedroom_input

def update_total_floors():
    st.session_state.total_floors = st.session_state.total_floors_input

def update_selected_features():
    st.session_state.selected_features = st.session_state.selected_features_input

def update_storeroom():
    st.session_state.storeroom_type = st.session_state.storeroom_type_input

def update_swimming_pool():
    st.session_state.swimming_pool_type = st.session_state.swimming_pool_type_input

def update_living_room():
    st.session_state.living_room_type = st.session_state.living_room_type_input

def update_build_year():
    st.session_state.build_year = st.session_state.build_year_input

def update_height():
    st.session_state.height = st.session_state.height_input

def update_balconies():
    st.session_state.balconies = st.session_state.balconies_input

def update_parking():
    st.session_state.parking_type = st.session_state.parking_type_input

def update_special_people():
    st.session_state.for_special_people = st.session_state.special_people_input

def update_investment():
    st.session_state.for_investment = st.session_state.investment_input

def update_heating():
    st.session_state.heating_type = st.session_state.heating_type_input

def update_project():
    st.session_state.project_type = st.session_state.project_type_input

def update_hot_water():
    st.session_state.hot_water_type = st.session_state.hot_water_type_input

def update_material():
    st.session_state.material_type = st.session_state.material_type_input

def update_other_features():
    st.session_state.other_features = st.session_state.other_features_input

st.subheader("Main Characteristics")


def dms_to_decimal(dms_str):
    # Regex to extract degrees, minutes, seconds, and direction
    match = re.match(r"(\d+)°(\d+)'(\d+(?:\.\d+)?)\"?([NSEW])", dms_str.strip())
    if not match:
        return None
    
    degrees, minutes, seconds, direction = match.groups()
    decimal = float(degrees) + float(minutes) / 60 + float(seconds) / 3600
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

def parse_latitude(input_str):
    try:
        # Try to convert directly to float (decimal degrees)
        return float(input_str)
    except ValueError:
        # Try DMS parsing
        decimal = dms_to_decimal(input_str)
        if decimal is not None:
            return decimal
        else:
            st.error("Invalid latitude format. Use decimal (e.g., 41.699444) or DMS (e.g., 41°41'58.0\"N)")
            return None

# -- Update function --
def update_latitude(new_latitude):
    st.session_state.latitude = new_latitude

# -- Ensure session state is initialized --
if "latitude" not in st.session_state:
    st.session_state.latitude = 41.699444  # or any default value in range



lat_col, lng_col = st.columns(2)
with lat_col:
    lat_input_str = st.text_input("Enter Latitude", value=str(st.session_state.latitude))

    # latitude = st.number_input(
    # label="Latitude",
    # min_value=41.61,
    # max_value=41.84,
    # step=0.000001,
    # format="%.6f",
    # value=st.session_state.latitude,
    # key="latitude_input",
    # on_change=update_latitude
    # )
latitude = parse_latitude(lat_input_str)

if latitude is not None:
    # Optional: check bounds
    if 41.61 <= latitude <= 41.84:
        st.session_state.latitude = latitude
        update_latitude(latitude)
    else:
        st.warning("Latitude out of range (41.61 to 41.84)")


def parse_longitude(input_str):
    try:
        return float(input_str)
    except ValueError:
        decimal = dms_to_decimal(input_str)
        if decimal is not None:
            return decimal
        else:
            st.error("Invalid longitude format. Use decimal (e.g., 44.807182) or DMS (e.g., 44°48'25.9\"E)")
            return None

def update_longitude(new_longitude):
    st.session_state.longitude = new_longitude

if "longitude" not in st.session_state:
    st.session_state.longitude = 44.807182  # or your default

with lng_col:
    lng_input_str = st.text_input("Enter Longitude", value=str(st.session_state.longitude))
    longitude = parse_longitude(lng_input_str)
    if longitude is not None:
        if 44.70 <= longitude <= 44.95:
            update_longitude(longitude)
        else:
            st.warning("Longitude out of range (44.70 to 44.85)")


# with lng_col:
#     longitude = st.number_input(
#     label="longitude",
#     min_value=44.7,
#     max_value=44.95,
#     step=0.000001,
#     format="%.6f",
#     value=st.session_state.longitude,
#     key="longitude_input",
#     on_change=update_longitude
#     )


col1, col2, col3 = st.columns(3)

with col1:
    urban = st.selectbox("Urban", urbans, key="urban_input", index=urbans.index(st.session_state.urban), on_change=update_urban)
    bathroom_type = st.selectbox("Bathroom", bathroom_types, key="bathroom_input", index=bathroom_types.index(st.session_state.bathroom_type), on_change=update_bathroom)
    area = st.number_input(
    label="Area (square meters)",
    min_value=20,
    max_value=1000,
    step=1,
    format="%d",
    value=st.session_state.area,
    key="area_input",
    on_change=update_area
    )

with col2:
    condition = st.selectbox("Condition", conditions, key="condition_input", index=conditions.index(st.session_state.condition), on_change=update_condition)
    room_num = st.selectbox("Rooms", room_types, key="room_num_input", index=room_types.index(st.session_state.room_num), on_change=update_room_num)
    floor = st.number_input(
    label="Floor",
    min_value=0,
    max_value=2000,
    step=1,
    format="%d",
    value=st.session_state.floor,
    key="floor_input",
    on_change=update_floor
    )

with col3:
    estate_status = st.selectbox("Estate Status", estate_status_types, key="estate_status_input", index=estate_status_types.index(st.session_state.estate_status), on_change=update_estate_status)
    bedroom_type = st.selectbox("Bedrooms", bedroom_types, key="bedroom_input", index=bedroom_types.index(st.session_state.bedroom_type), on_change=update_bedroom)
    total_floors = st.number_input(
    label="Total floors in the building",
    min_value=0,
    max_value=2000,
    step=1,
    format="%d",
    value=st.session_state.total_floors,
    key="total_floors_input",
    on_change=update_total_floors
    )

st.subheader("More Features")

build_years = ["unspecified","<1955","1955-2000",">2000"]

project_types = ["unspecified","არასტანდარტული","ქალაქური","ჩეხური","იტალიური ეზო","ყავლაშვილის",
                "მოსკოვის","ხრუშოვის","ლვოვის","თუხარელის","მ2 დეველოპმენტი","დუპლექსი",
                "ლენინგრადის","OPTIMA m2-ისგან","მეტრა პარკი","საერთო საცხოვრებელი","ტრიპლექსი"]

heating_types = ["unspecified","ცენტრალური გათბობა","გაზის გამაცხელებელი","ცენტრალური + იატაკის გათბობა",
                "ელექტრო გამაცხელებელი","გათბობის გარეშე","ინდივიდუალური","იატაკის გათბობა"]

hot_water_types = ["unspecified","ცენტრალური ცხელი წყალი","გაზის გამაცხელებელი","დენის გამაცხელებელი",
                  "ბუნებრივი ცხელი წყალი","ინდივიდუალური","ცხელი წყლის გარეშე","ავზი","მზის გამათბობელი"]

parking_types = ["unspecified","ეზოს პარკინგი","პარკინგის ადგილი","მიწისქვეშა პარკინგი","ავტოფარეხი",
                "პარკინგის გარეშე","ფასიანი ავტოსადგომი"]

material_types = ["unspecified","ბლოკი","კომბინირებული","რკინა-ბეტონი","აგური","ხის მასალა"]

storeroom_types = ["unspecified","გარე სათავსო","საკუჭნაო","სარდაფი","სარდაფი + სხვენი",
                  "სხვენი","საერთო სათავსო"]

living_room_types = ["unspecified","სტუდიო","გამოყოფილი"]

swimming_pool_types = ["unspecified","ღია","დახურული"]

# List of available utilities/features
features = ["storage room",
            "color",
            "gas",
            "internet",
            "TV",
            "sauna",
            "fridge",
            "swimming pool",
            "Jacuzzi",
            "protection",
            "telephone",
            "furniture",
            "chimney",
            "freight elevator",
            "ventilation",
            "elevator",
            "alarms",
            "air conditioner",
            "kitchen with technology",
            "oven",
            "stove",
            "dishwasher",
            "washing machine",
            "electricity",
            #"sewage",
            "water",
            "veranda",
            "loggia",
            "living room",
            "bed",
            "grill",
            "coded door",
            "gym",
            "bar",
            "spa",
            "chair",
            "table",
            "sofa"
            ]

# Multi-select field
selected_features = st.multiselect("Select available features:", features, default=st.session_state.selected_features, key="selected_features_input", on_change=update_selected_features)


if "storage room" in selected_features:
    storeroom_type = st.selectbox("storage room type", storeroom_types, key="storeroom_type_input", index=storeroom_types.index(st.session_state.storeroom_type), on_change=update_storeroom)
else:
    storeroom_type = "unspecified"
if "swimming pool" in selected_features:
    swimming_pool_type = st.selectbox("swimming pool type", swimming_pool_types, key="swimming_pool_type_input", index=swimming_pool_types.index(st.session_state.swimming_pool_type), on_change=update_swimming_pool)
else:
    swimming_pool_type = "unspecified"
if "living room" in selected_features:
    living_room_type = st.selectbox("living room type", living_room_types, key="living_room_type_input", index=living_room_types.index(st.session_state.living_room_type), on_change=update_living_room)
else:
    living_room_type = "unspecified"

col4, col5, col6 = st.columns(3)

with col4:
    build_year = st.selectbox("Build year", build_years, key="build_year_input", index=build_years.index(st.session_state.build_year), on_change=update_build_year)
    height = st.number_input(
        label="Enter height (in meters)",
        min_value=0.0,
        max_value=500.0,
        step=0.01,
        format="%.2f",
        value=st.session_state.height,
        key="height_input",
        on_change=update_height
    )
    balconies = st.number_input(
        label="Number of balconies",
        min_value=0,
        max_value=300,
        step=1,
        format="%d",
        value=st.session_state.balconies,
        key="balconies_input",
        on_change=update_balconies
    )
    parking_type = st.selectbox("Parking type", parking_types, key="parking_type_input", index=parking_types.index(st.session_state.parking_type), on_change=update_parking)

with col5:
    for_special_people = st.selectbox("Is it for special people?", ["no","yes"], key="special_people_input", index=["no","yes"].index(st.session_state.for_special_people), on_change=update_special_people)
    for_investment = st.selectbox("Is it for investment?", ["no","yes"], key="investment_input", index=["no","yes"].index(st.session_state.for_investment), on_change=update_investment)
    heating_type = st.selectbox("Heating type", heating_types, key="heating_type_input", index=heating_types.index(st.session_state.heating_type), on_change=update_heating)

with col6:
    project_type = st.selectbox("Project type", project_types, key="project_type_input", index=project_types.index(st.session_state.project_type), on_change=update_project)
    hot_water_type = st.selectbox("Hot water type", hot_water_types, key="hot_water_type_input", index=hot_water_types.index(st.session_state.hot_water_type), on_change=update_hot_water)
    material_type = st.selectbox("Building material type", material_types, key="material_type_input", index=material_types.index(st.session_state.material_type), on_change=update_material)


other_words = ["Axis",
               "Smart",
               "Urgent",
               "Prestigeous",
               "With Renovation",
               "Complex",
               "Bagebi",
               "European",
               "Paved",
               "Unlived",
               "Secondary",
               "Cheap",
               "Good view"]

other_features = st.multiselect("Does any of these describe your apartment?", other_words, default=st.session_state.other_features, key="other_features_input", on_change=update_other_features)

# Add a button to trigger prediction
if st.button("Predict Price", type="primary"):
    # Show what the user selected
    #st.write("You selected:", selected_features)

    # Permanent variables
    views = 21 # median views
    is_old = 0 # Most are not old
    can_exchanged = 0 # Most don't post to exchange
    user_statements_count = 153 # Median number of user statements count
    created_days_ago = 30 # Median
    updated_days_ago = 14 # Median

    # True False variables
    has_color = 1 if "color" in selected_features else 0
    has_gas = 1 if "gas" in selected_features else 0
    has_internet = 1 if "internet" in selected_features else 0
    has_TV = 1 if "TV" in selected_features else 0
    has_air_conditioner = 1 if "air conditioner" in selected_features else 0
    has_alarms = 1 if "alarms" in selected_features else 0
    has_elevator = 1 if "elevator" in selected_features else 0
    has_ventilation = 1 if "ventilation" in selected_features else 0
    has_freight_elevator = 1 if "freight elevator" in selected_features else 0
    has_chimney = 1 if "chimney" in selected_features else 0
    has_furniture = 1 if "furniture" in selected_features else 0
    has_telephone = 1 if "telephone" in selected_features else 0
    has_protection = 1 if "protection" in selected_features else 0
    has_Jacuzzi = 1 if "Jacuzzi" in selected_features else 0
    has_swimming_pool = 1 if "swimming pool"in selected_features else 0
    has_sauna = 1 if "sauna" in selected_features else 0
    has_fridge = 1 if "fridge" in selected_features else 0
    has_washing_machine = 1 if "washing machine"in selected_features else 0
    has_dishwasher = 1 if "dishwasher" in selected_features else 0
    has_stove = 1 if "stove" in selected_features else 0
    has_oven = 1 if "oven"in selected_features else 0
    has_living_room = 1 if "living room" in selected_features else 0
    has_loggia = 1 if "loggia" in selected_features else 0
    has_veranda = 1 if "veranda" in selected_features else 0
    has_water = 1 if "water" in selected_features else 0
    #has_sewage = 1 if "sewage" in selected_features else 0
    has_electricity = 1 if "electricity" in selected_features else 0
    has_spa = 1 if "spa" in selected_features else 0
    has_bar = 1 if "bar" in selected_features else 0
    has_gym = 1 if "gym" in selected_features else 0
    has_coded_door = 1 if "coded door" in selected_features else 0
    has_grill = 1 if "grill" in selected_features else 0
    has_bed = 1 if "bed" in selected_features else 0
    has_sofa = 1 if "sofa" in selected_features else 0
    has_table = 1 if "table" in selected_features else 0
    has_chair = 1 if "chair" in selected_features else 0
    has_kitchen_with_technology = 1 if "kitchen with technology" in selected_features else 0
    has_storage_room = 1 if "storage room" in selected_features else 0

    # Location based variables
    def haversine(lat1, lon1, lat2, lon2):
        # Radius of the Earth in kilometers
        R = 6371.0

        # Convert degrees to radians
        phi1 = np.radians(lat1)
        phi2 = np.radians(lat2)
        delta_phi = np.radians(lat2 - lat1)
        delta_lambda = np.radians(lon2 - lon1)

        # Haversine formula
        a = np.sin(delta_phi / 2.0) ** 2 + \
            np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2.0) ** 2
        c = 2 * np.arcsin(np.sqrt(a))

        return R * c  # distance in kilometers

    def dist_to_specific():
        cent_lat = 41.697007
        cent_lng = 44.799183
        city_center_dist = haversine(latitude, longitude,cent_lat,cent_lng)
        lisi_lat = 41.742885
        lisi_lng = 44.733691
        lisi_lake_dist = haversine(latitude, longitude,lisi_lat,lisi_lng)
        ku_lat = 41.700945
        ku_lng = 44.754591
        ku_lake_dist = haversine(latitude, longitude,ku_lat,ku_lng)
        dinamo_lat = 41.722849
        dinamo_lng = 44.789828
        dinamo_dist = haversine(latitude, longitude,dinamo_lat,dinamo_lng)
        meskhi_lat = 41.710134
        meskhi_lng = 44.746094
        meskhi_dist = haversine(latitude, longitude,meskhi_lat,meskhi_lng)
        public_service_hall_lat = 41.699147
        public_service_hall_lng = 44.806558
        public_service_hall_dist = haversine(latitude, longitude,public_service_hall_lat,public_service_hall_lng)
        return city_center_dist,lisi_lake_dist,ku_lake_dist,dinamo_dist,meskhi_dist,public_service_hall_dist

    def dist_to_places(path,coords):
        # Read metro station coordinates
        helper_table = pd.read_csv(path)
        metro_coords = np.radians(helper_table[['latitude', 'longitude']].values)

        # Create BallTree with metro coordinates
        tree = BallTree(metro_coords, metric='haversine')

        # Convert input coordinate to radians and reshape
        input_coord = np.radians(np.array(coords).reshape(1, -1))

        # Query the nearest metro
        distance, _ = tree.query(input_coord, k=1)

        # Convert from radians to kilometers (Earth radius ≈ 6371 km)
        return distance[0][0] * 6371

    def count_within_radius(path, coords, radius_km):
        input_coord = np.radians(np.array(coords).reshape(1, -1))
        est_df = pd.read_csv(path)
        est_coords = np.radians(est_df[['latitude','longitude']].values)
        earth_radius_km = 6371.0
        tree = BallTree(est_coords, metric='haversine')
        radius_rad = radius_km / earth_radius_km
        counts = tree.query_radius(input_coord, r=radius_rad, count_only=True)
        return int(counts[0])

    coords = [latitude, longitude]

    # Dist to specific
    city_center_dist\
        ,lisi_lake_dist\
            ,ku_lake_dist\
                ,dinamo_dist\
                     ,meskhi_dist\
                         ,public_service_hall_dist = dist_to_specific()

    # Nearest distances
    nearest_metro_dist = dist_to_places('for_location/metro_stations.csv',coords)
    nearest_bus_stop_dist = dist_to_places('for_location/tbilisi_bus_stops.csv',coords)
    nearest_gym_dist = dist_to_places( 'for_location/tbilisi_gyms.csv',  coords)
    nearest_kindergarten_dist = dist_to_places( 'for_location/tbilisi_kindergartens.csv',  coords)
    nearest_park_dist = dist_to_places( 'for_location/tbilisi_parks.csv', coords)
    nearest_pharmacy_dist = dist_to_places( 'for_location/tbilisi_pharmacies.csv',  coords)
    nearest_school_dist = dist_to_places( 'for_location/tbilisi_schools.csv',  coords)
    nearest_supermarket_dist = dist_to_places( 'for_location/tbilisi_supermarkets.csv',  coords)
    nearest_university_dist = dist_to_places( 'for_location/tbilisi_universities.csv',  coords)
    nearest_atms_dist = dist_to_places( 'for_location/tbilisi_atms.csv',  coords)
    nearest_banks_dist = dist_to_places( 'for_location/tbilisi_banks.csv',  coords)
    nearest_gas_dist = dist_to_places( 'for_location/tbilisi_gas_stations.csv',  coords)
    nearest_hospitals_dist = dist_to_places( 'for_location/tbilisi_hospitals.csv',  coords)
    nearest_malls_dist = dist_to_places( 'for_location/tbilisi_malls.csv',  coords)
    nearest_big_swimming_sites_dist = dist_to_places( 'for_location/big_swimming_sites.csv',  coords)
    nearest_courts_dist = dist_to_places( 'for_location/tbilisi_courts.csv',  coords)
    nearest_embassies_dist = dist_to_places( 'for_location/tbilisi_embassies.csv',  coords)
    nearest_entertainment_dist = dist_to_places( 'for_location/tbilisi_entertainment_venues.csv',  coords)
    nearest_fast_food_dist = dist_to_places( 'for_location/tbilisi_fast_food_expanded.csv',  coords)
    nearest_police_stations_dist = dist_to_places( 'for_location/tbilisi_police_stations.csv',  coords)
    nearest_swimming_pools_dist = dist_to_places( 'for_location/tbilisi_swimming_pools.csv',  coords)
    nearest_fast_food_chain_dist = dist_to_places( 'for_location/tbilisi_fast_food_chain.csv',  coords)

    # Nearby distances 1 km
    metro_stations_nearby_1km = count_within_radius( 'for_location/metro_stations.csv',  coords, 1)
    bus_stops_nearby_1km = count_within_radius( 'for_location/tbilisi_bus_stops.csv',  coords, 1)
    gyms_nearby_1km = count_within_radius( 'for_location/tbilisi_gyms.csv',  coords, 1)
    kindergartens_nearby_1km = count_within_radius( 'for_location/tbilisi_kindergartens.csv',  coords, 1)
    parks_nearby_1km = count_within_radius( 'for_location/tbilisi_parks.csv',  coords, 1)
    pharmacies_nearby_1km = count_within_radius( 'for_location/tbilisi_pharmacies.csv',  coords, 1)
    schools_nearby_1km = count_within_radius( 'for_location/tbilisi_schools.csv',  coords, 1)
    supermarkets_nearby_1km = count_within_radius( 'for_location/tbilisi_supermarkets.csv',  coords, 1)
    universities_nearby_1km = count_within_radius( 'for_location/tbilisi_universities.csv',  coords, 1)
    atms_nearby_1km = count_within_radius( 'for_location/tbilisi_atms.csv',  coords, 1)
    banks_nearby_1km = count_within_radius( 'for_location/tbilisi_banks.csv',  coords, 1)
    gas_stations_nearby_1km = count_within_radius( 'for_location/tbilisi_gas_stations.csv',  coords, 1)
    hospitals_nearby_1km = count_within_radius( 'for_location/tbilisi_hospitals.csv',  coords, 1)
    malls_nearby_1km = count_within_radius( 'for_location/tbilisi_malls.csv',  coords, 1)
    big_swimming_sites_nearby_1km = count_within_radius( 'for_location/big_swimming_sites.csv',  coords,1)
    courts_nearby_1km = count_within_radius( 'for_location/tbilisi_courts.csv',  coords, 1)
    embassies_nearby_1km = count_within_radius( 'for_location/tbilisi_embassies.csv',  coords,1)
    entertainment_nearby_1km = count_within_radius( 'for_location/tbilisi_entertainment_venues.csv',  coords,1)
    fast_food_nearby_1km = count_within_radius( 'for_location/tbilisi_fast_food_expanded.csv',  coords,1)
    police_stations_nearby_1km = count_within_radius( 'for_location/tbilisi_police_stations.csv',  coords,1)
    swimming_pools_nearby_1km = count_within_radius( 'for_location/tbilisi_swimming_pools.csv',  coords,1)
    fast_food_chain_nearby_1km = count_within_radius( 'for_location/tbilisi_fast_food_chain.csv',  coords, 1)

    # Nearby distances 500 m
    metro_stations_nearby_500m = count_within_radius( 'for_location/metro_stations.csv',  coords, 0.5)
    bus_stops_nearby_500m = count_within_radius( 'for_location/tbilisi_bus_stops.csv',  coords, 0.5)
    gyms_nearby_500m = count_within_radius( 'for_location/tbilisi_gyms.csv',  coords, 0.5)
    kindergartens_nearby_500m = count_within_radius( 'for_location/tbilisi_kindergartens.csv',  coords, 0.5)
    parks_nearby_500m = count_within_radius( 'for_location/tbilisi_parks.csv',  coords, 0.5)
    pharmacies_nearby_500m = count_within_radius( 'for_location/tbilisi_pharmacies.csv',  coords, 0.5)
    schools_nearby_500m = count_within_radius( 'for_location/tbilisi_schools.csv',  coords, 0.5)
    supermarkets_nearby_500m = count_within_radius( 'for_location/tbilisi_supermarkets.csv',  coords, 0.5)
    universities_nearby_500m = count_within_radius( 'for_location/tbilisi_universities.csv',  coords, 0.5)
    atms_nearby_500m = count_within_radius( 'for_location/tbilisi_atms.csv',  coords, 0.5)
    banks_nearby_500m = count_within_radius( 'for_location/tbilisi_banks.csv',  coords, 0.5)
    gas_stations_nearby_500m = count_within_radius( 'for_location/tbilisi_gas_stations.csv',  coords, 0.5)
    hospitals_nearby_500m = count_within_radius( 'for_location/tbilisi_hospitals.csv',  coords, 0.5)
    malls_nearby_500m = count_within_radius( 'for_location/tbilisi_malls.csv',  coords, 0.5)
    big_swimming_sites_nearby_500m = count_within_radius( 'for_location/big_swimming_sites.csv',  coords,0.5)
    courts_nearby_500m = count_within_radius( 'for_location/tbilisi_courts.csv',  coords, 0.5)
    embassies_nearby_500m = count_within_radius( 'for_location/tbilisi_embassies.csv',  coords,0.5)
    entertainment_nearby_500m = count_within_radius( 'for_location/tbilisi_entertainment_venues.csv',  coords,0.5)
    fast_food_nearby_500m = count_within_radius( 'for_location/tbilisi_fast_food_expanded.csv',  coords,0.5)
    police_stations_nearby_500m = count_within_radius( 'for_location/tbilisi_police_stations.csv',  coords,0.5)
    swimming_pools_nearby_500m = count_within_radius( 'for_location/tbilisi_swimming_pools.csv',  coords,0.5)
    fast_food_chain_nearby_500m = count_within_radius( 'for_location/tbilisi_fast_food_chain.csv',  coords, 0.5)
    # Nearby distances 200 m

    metro_stations_nearby_200m = count_within_radius( 'for_location/metro_stations.csv',  coords, 0.2)
    bus_stops_nearby_200m = count_within_radius( 'for_location/tbilisi_bus_stops.csv',  coords, 0.2)
    gyms_nearby_200m = count_within_radius( 'for_location/tbilisi_gyms.csv',  coords, 0.2)
    kindergartens_nearby_200m = count_within_radius( 'for_location/tbilisi_kindergartens.csv',  coords, 0.2)
    parks_nearby_200m = count_within_radius( 'for_location/tbilisi_parks.csv',  coords, 0.2)
    pharmacies_nearby_200m = count_within_radius( 'for_location/tbilisi_pharmacies.csv',  coords, 0.2)
    schools_nearby_200m = count_within_radius( 'for_location/tbilisi_schools.csv',  coords, 0.2)
    supermarkets_nearby_200m = count_within_radius( 'for_location/tbilisi_supermarkets.csv',  coords, 0.2)
    universities_nearby_200m = count_within_radius( 'for_location/tbilisi_universities.csv',  coords, 0.2)
    atms_nearby_200m = count_within_radius( 'for_location/tbilisi_atms.csv',  coords, 0.2)
    banks_nearby_200m = count_within_radius( 'for_location/tbilisi_banks.csv',  coords, 0.2)
    gas_stations_nearby_200m = count_within_radius( 'for_location/tbilisi_gas_stations.csv',  coords, 0.2)
    hospitals_nearby_200m = count_within_radius( 'for_location/tbilisi_hospitals.csv',  coords, 0.2)
    malls_nearby_200m = count_within_radius( 'for_location/tbilisi_malls.csv',  coords, 0.2)
    big_swimming_sites_nearby_200m = count_within_radius( 'for_location/big_swimming_sites.csv',  coords,0.2)
    courts_nearby_200m = count_within_radius( 'for_location/tbilisi_courts.csv',  coords, 0.2)
    embassies_nearby_200m = count_within_radius( 'for_location/tbilisi_embassies.csv',  coords,0.2)
    entertainment_nearby_200m = count_within_radius( 'for_location/tbilisi_entertainment_venues.csv',  coords,0.2)
    fast_food_nearby_200m = count_within_radius( 'for_location/tbilisi_fast_food_expanded.csv',  coords,0.2)
    police_stations_nearby_200m = count_within_radius( 'for_location/tbilisi_police_stations.csv',  coords,0.2)
    swimming_pools_nearby_200m = count_within_radius( 'for_location/tbilisi_swimming_pools.csv',  coords,0.2)
    fast_food_chain_nearby_200m = count_within_radius( 'for_location/tbilisi_fast_food_chain.csv',  coords, 0.2)
    # Nearby distances 100 m

    metro_stations_nearby_100m = count_within_radius( 'for_location/metro_stations.csv',  coords, 0.1)
    bus_stops_nearby_100m = count_within_radius( 'for_location/tbilisi_bus_stops.csv',  coords, 0.1)
    gyms_nearby_100m = count_within_radius( 'for_location/tbilisi_gyms.csv',  coords, 0.1)
    kindergartens_nearby_100m = count_within_radius( 'for_location/tbilisi_kindergartens.csv',  coords, 0.1)
    parks_nearby_100m = count_within_radius( 'for_location/tbilisi_parks.csv',  coords, 0.1)
    pharmacies_nearby_100m = count_within_radius( 'for_location/tbilisi_pharmacies.csv',  coords, 0.1)
    schools_nearby_100m = count_within_radius( 'for_location/tbilisi_schools.csv',  coords, 0.1)
    supermarkets_nearby_100m = count_within_radius( 'for_location/tbilisi_supermarkets.csv',  coords, 0.1)
    universities_nearby_100m = count_within_radius( 'for_location/tbilisi_universities.csv',  coords, 0.1)
    atms_nearby_100m = count_within_radius( 'for_location/tbilisi_atms.csv',  coords, 0.1)
    banks_nearby_100m = count_within_radius( 'for_location/tbilisi_banks.csv',  coords, 0.1)
    gas_stations_nearby_100m = count_within_radius( 'for_location/tbilisi_gas_stations.csv',  coords, 0.1)
    hospitals_nearby_100m = count_within_radius( 'for_location/tbilisi_hospitals.csv',  coords, 0.1)
    malls_nearby_100m = count_within_radius( 'for_location/tbilisi_malls.csv',  coords, 0.1)
    big_swimming_sites_nearby_100m = count_within_radius( 'for_location/big_swimming_sites.csv',  coords,0.1)
    courts_nearby_100m = count_within_radius( 'for_location/tbilisi_courts.csv',  coords, 0.1)
    embassies_nearby_100m = count_within_radius( 'for_location/tbilisi_embassies.csv',  coords,0.1)
    entertainment_nearby_100m = count_within_radius( 'for_location/tbilisi_entertainment_venues.csv',  coords,0.1)
    fast_food_nearby_100m = count_within_radius( 'for_location/tbilisi_fast_food_expanded.csv',  coords,0.1)
    police_stations_nearby_100m = count_within_radius( 'for_location/tbilisi_police_stations.csv',  coords,0.1)
    swimming_pools_nearby_100m = count_within_radius( 'for_location/tbilisi_swimming_pools.csv',  coords,0.1)
    fast_food_chain_nearby_100m = count_within_radius( 'for_location/tbilisi_fast_food_chain.csv',  coords, 0.1)

    distance_variables = [
        city_center_dist,
        lisi_lake_dist,
        ku_lake_dist,
        dinamo_dist,
        meskhi_dist,
        public_service_hall_dist,
        nearest_metro_dist,
        nearest_bus_stop_dist,
        nearest_gym_dist,
        nearest_kindergarten_dist,
        nearest_park_dist,
        nearest_pharmacy_dist,
        nearest_school_dist,
        nearest_supermarket_dist,
        nearest_university_dist,
        nearest_atms_dist,
        nearest_banks_dist,
        nearest_gas_dist,
        nearest_hospitals_dist,
        nearest_malls_dist,
        nearest_big_swimming_sites_dist,
        nearest_courts_dist,
        nearest_embassies_dist,
        nearest_entertainment_dist,
        nearest_fast_food_dist,
        nearest_police_stations_dist,
        nearest_swimming_pools_dist,
        nearest_fast_food_chain_dist,
        metro_stations_nearby_1km,
        bus_stops_nearby_1km,
        gyms_nearby_1km,
        kindergartens_nearby_1km,
        parks_nearby_1km,
        pharmacies_nearby_1km,
        schools_nearby_1km,
        supermarkets_nearby_1km,
        universities_nearby_1km,
        atms_nearby_1km,
        banks_nearby_1km,
        gas_stations_nearby_1km,
        hospitals_nearby_1km,
        malls_nearby_1km,
        big_swimming_sites_nearby_1km,
        courts_nearby_1km,
        embassies_nearby_1km,
        entertainment_nearby_1km,
        fast_food_nearby_1km,
        police_stations_nearby_1km,
        swimming_pools_nearby_1km,
        fast_food_chain_nearby_1km,
        metro_stations_nearby_500m,
        bus_stops_nearby_500m,
        gyms_nearby_500m,
        kindergartens_nearby_500m,
        parks_nearby_500m,
        pharmacies_nearby_500m,
        schools_nearby_500m,
        supermarkets_nearby_500m,
        universities_nearby_500m,
        atms_nearby_500m,
        banks_nearby_500m,
        gas_stations_nearby_500m,
        hospitals_nearby_500m,
        malls_nearby_500m,
        big_swimming_sites_nearby_500m,
        courts_nearby_500m,
        embassies_nearby_500m,
        entertainment_nearby_500m,
        fast_food_nearby_500m,
        police_stations_nearby_500m,
        swimming_pools_nearby_500m,
        fast_food_chain_nearby_500m,
        metro_stations_nearby_200m,
        bus_stops_nearby_200m,
        gyms_nearby_200m,
        kindergartens_nearby_200m,
        parks_nearby_200m,
        pharmacies_nearby_200m,
        schools_nearby_200m,
        supermarkets_nearby_200m,
        universities_nearby_200m,
        atms_nearby_200m,
        banks_nearby_200m,
        gas_stations_nearby_200m,
        hospitals_nearby_200m,
        malls_nearby_200m,
        big_swimming_sites_nearby_200m,
        courts_nearby_200m,
        embassies_nearby_200m,
        entertainment_nearby_200m,
        fast_food_nearby_200m,
        police_stations_nearby_200m,
        swimming_pools_nearby_200m,
        fast_food_chain_nearby_200m,
        metro_stations_nearby_100m,
        bus_stops_nearby_100m,
        gyms_nearby_100m,
        kindergartens_nearby_100m,
        parks_nearby_100m,
        pharmacies_nearby_100m,
        schools_nearby_100m,
        supermarkets_nearby_100m,
        universities_nearby_100m,
        atms_nearby_100m,
        banks_nearby_100m,
        gas_stations_nearby_100m,
        hospitals_nearby_100m,
        malls_nearby_100m,
        big_swimming_sites_nearby_100m,
        courts_nearby_100m,
        embassies_nearby_100m,
        entertainment_nearby_100m,
        fast_food_nearby_100m,
        police_stations_nearby_100m,
        swimming_pools_nearby_100m,
        fast_food_chain_nearby_100m,
    ]
    # True ratio
    for_special_people = 1 if for_special_people == "yes" else 0
    for_investment = 1 if for_investment == "yes" else 0

    sum_of_true = is_old+can_exchanged+for_special_people+has_color+has_gas+has_internet\
    +has_TV+has_air_conditioner+has_alarms+has_elevator+has_ventilation+has_freight_elevator\
    +has_chimney+has_furniture+has_telephone+has_protection+has_Jacuzzi+has_swimming_pool\
    +has_sauna+has_fridge+has_washing_machine+has_dishwasher+has_stove+has_oven+has_living_room\
    +has_loggia+has_veranda+has_water+0.3168+has_electricity+has_spa+has_bar+has_gym+has_coded_door\
    +has_grill+has_spa+has_bed+has_sofa+has_table+has_chair+has_kitchen_with_technology+has_storage_room\
    +for_investment
    total_boolean = 42.0
    true_ratio = sum_of_true/total_boolean

    # Word based variables
    word_axis = 1 if "Axis" in other_features else 0
    word_Bagebi = 1 if "Bagebi" in other_features else 0
    word_Urgent = 1 if "Urgent" in other_features else 0
    word_Unlived = 1 if "Unlived" in other_features else 0
    word_Secondary = 1 if "Secondary" in other_features else 0
    word_with_renovation = 1 if "With Renovation" in other_features else 0
    word_prestigeous = 1 if "Prestigeous" in other_features else 0
    word_complex = 1 if "Complex" in other_features else 0
    word_cheap = 1 if "Cheap" in other_features else 0
    word_smart = 1 if "Smart" in other_features else 0
    word_paved = 1 if "Paved" in other_features else 0
    word_european = 1 if "European" in other_features else 0
    word_has_view = 1 if "Good view" in other_features else 0
    # estate_status_types

    estate_status_types_col = ["ახალი აშენებული","მშენებარე","ძველი აშენებული"]
    estate_status_types_val = []
    for type in estate_status_types_col:
        estate_status_types_val.append(1 if estate_status == type else 0)

    # bathroom_type
    bathroom_types_col = ["unspecified","1","2","3+","საერთო"]
    bathroom_types_val = []
    for type in bathroom_types_col:
        bathroom_types_val.append(1 if bathroom_type == type else 0)
    # project_type
    project_types_col = ["unspecified","OPTIMA m2-ისგან","არასტანდარტული","დუპლექსი","თუხარელის",
                     "იტალიური ეზო","ლენინგრადის","ლვოვის","მ2 დეველოპმენტი","მეტრა პარკი",
                     "მოსკოვის","საერთო საცხოვრებელი","ტრიპლექსი","ქალაქური","ყავლაშვილის",
                     "ჩეხური","ხრუშოვის",]
    proj_types_vals = []
    for type in project_types_col:
        proj_types_vals.append(1 if project_type == type else 0)

    # heating type
    heating_types_col = ["unspecified","გაზის გამაცხელებელი","გათბობის გარეშე","ელექტრო გამაცხელებელი",
                         "იატაკის გათბობა","ინდივიდუალური","ცენტრალური + იატაკის გათბობა","ცენტრალური გათბობა",
                        ]
    heating_types_val = []
    for type in heating_types_col:
        heating_types_val.append(1 if heating_type == type else 0)

    # parking type
    parking_types_col = ["unspecified","ავტოფარეხი","ეზოს პარკინგი","მიწისქვეშა პარკინგი","პარკინგის ადგილი",
                    "პარკინგის გარეშე","ფასიანი ავტოსადგომი"]
    parking_types_val = []
    for type in parking_types_col:
        parking_types_val.append(1 if parking_type == type else 0)

    # storeroom type

    storeroom_types_col = ["unspecified","გარე სათავსო","საერთო სათავსო","საკუჭნაო"
                       ,"სარდაფი","სარდაფი + სხვენი","სხვენი",]
    storeroom_types_val = []
    for type in storeroom_types_col:
        storeroom_types_val.append(1 if storeroom_type == type else 0)

    # material type
    material_types_col = ["unspecified","აგური","ბლოკი","კომბინირებული","რკინა-ბეტონი","ხის მასალა"]
    material_types_val = []
    for type in material_types_col:
        material_types_val.append(1 if material_type == type else 0)
    # Swimming pool type
    swimming_pool_types_col = ["unspecified","დახურული","ღია"]
    swimming_pool_types_val = []
    for type in swimming_pool_types_col:
        swimming_pool_types_val.append(1 if swimming_pool_type == type else 0)

    #  hot water type
    hot_water_types_col = ["unspecified","ავზი","ბუნებრივი ცხელი წყალი","გაზის გამაცხელებელი",
                       "დენის გამაცხელებელი","ინდივიდუალური","მზის გამათბობელი",
                       "ცენტრალური ცხელი წყალი","ცხელი წყლის გარეშე",]
    hot_water_types_val = []
    for type in hot_water_types_col:
        hot_water_types_val.append(1 if hot_water_type == type else 0)

    # condition

    conditions_col = ["unspecified","ახალი გარემონტებული","თეთრი კარკასი",
                  "თეთრი პლიუსი","მიმდინარე რემონტი","მწვანე კარკასი",
                  "სარემონტო","შავი კარკასი","ძველი გარემონტებული",
                  ]
    conditions_val = []
    for type in conditions_col:
        conditions_val.append(1 if condition == type else 0)

    # living room type
    living_room_types_col = ["unspecified","გამოყოფილი","სტუდიო"]
    living_room_types_val = []
    for type in living_room_types_col:
        living_room_types_val.append(1 if living_room_type == type else 0)
    # build year
    build_years_col = ["unspecified",">2000","<1955","1955-2000"]
    build_years_val = []
    for type in build_years_col:
        build_years_val.append(1 if build_year == type else 0)
    # user type
    # Here choose default values for each type
    user_types_col = ["-1","agent","developer","physical"]
    user_types_val = [0,1,0,0] # Agent is the most common type and will be used in the model as default

    # urban
    urbans_col = ["Chughureti","Didi Dighomi","Didube","Gldani","Isani","Krtsanisi",
              "Mtatsminda","Nadzaladevi","Saburtalo","Samgori","Vake",
              "Vashlijvari"]
    urbans_val = []
    for type in urbans_col:
        urbans_val.append(1 if urban == type else 0)

    input_array = [
        10 if room_num == "10+" else int(room_num), #room_type_id
        -1 if bedroom_type == "unspecified" else (11 if bedroom_type == "10+" else int(bedroom_type)), #bedroom_type_id
        # bedroom type skips 6 for some reason and 10+'s id is 11
        height,
        balconies,
        area,
        floor,
        total_floors,
        views,
        is_old,
        can_exchanged,
        for_special_people,
        user_statements_count,
        has_color,
        has_gas,
        has_internet,
        has_TV,
        has_air_conditioner,
        has_alarms,
        has_elevator,
        has_ventilation,
        has_freight_elevator,
        has_chimney,
        has_furniture,
        has_telephone,
        has_protection,
        has_Jacuzzi,
        has_swimming_pool,
        has_sauna,
        has_fridge,
        has_washing_machine,
        has_dishwasher,
        has_stove,
        has_oven,
        has_living_room,
        has_loggia,
        has_veranda,
        has_water,
        #has_sewage,
        has_electricity,
        has_spa,
        has_bar,
        has_gym,
        has_coded_door,
        has_grill,
        has_bed,
        has_sofa,
        has_table,
        has_chair,
        has_kitchen_with_technology,
        has_storage_room,
        for_investment,]\
        +distance_variables\
        +[
        created_days_ago,
        updated_days_ago,
        true_ratio,
        word_axis,
        word_Bagebi,
        word_Urgent,
        word_Unlived,
        word_Secondary,
        word_with_renovation,
        word_prestigeous,
        word_complex,
        word_cheap,
        word_smart,
        word_paved,
        word_european,
        word_has_view
    ]+estate_status_types_val+bathroom_types_val+proj_types_vals+heating_types_val+parking_types_val\
    +storeroom_types_val+material_types_val+swimming_pool_types_val+hot_water_types_val+conditions_val\
    +living_room_types_val+build_years_val+user_types_val+urbans_val
    #st.write("You selected:", input_array)

    import joblib
    model = joblib.load("xgboost_model18june.pkl")
    loforest = joblib.load("loforest_full_model.pkl")

    feature_vector = np.array(input_array).reshape(1,-1)

    prediction = model.predict(feature_vector)
    # Show prediction
    # st.write(f"Price per square is {prediction[0]:,.2f} \$ and the total {prediction[0]*area:,.2f} \$")

    #q_hat = pd.read_csv('conformal/q_hat.csv')['q_hat'].iloc[0]

    bounds = loforest.predict(feature_vector)
    lower = bounds[:,0][0]
    upper = bounds[:,1][0]
    #lower, upper = prediction[0] - q_hat, prediction[0] + q_hat
    # st.write(f"The prediction interval with 90% probability is: {lower:,.2f} \$ - {upper:,.2f} \$")
    # st.write(f"With the total price being: {lower*area:,.2f} \$ - {upper*area:,.2f} \$")

    import matplotlib.pyplot as plt
    import matplotlib.transforms as transforms

    from helper_code.plots import get_feature_names
    from helper_code.plots import shap_value_waterplot
    from helper_code.plots import price_interval_plot

    feature_names = get_feature_names(estate_status_types_col,
                                        bathroom_types_col,
                                        project_types_col,
                                        heating_types_col,
                                        parking_types_col,
                                        storeroom_types_col,
                                        material_types_col,
                                        swimming_pool_types_col,
                                        hot_water_types_col,
                                        conditions_col,
                                        living_room_types_col,
                                        build_years_col,
                                        user_types_col,
                                        urbans_col,)

    st.subheader("Prediction and intervals")
    per_square_fig = price_interval_plot(lower,upper,prediction)
    st.pyplot(per_square_fig)


    total_price_fig = price_interval_plot(lower,upper,prediction,total_price=True,area=area)
    st.pyplot(total_price_fig)
    st.subheader("SHAP Waterfall Plot")
    shap_fig = shap_value_waterplot(input_array, feature_names, model)
    st.pyplot(shap_fig)