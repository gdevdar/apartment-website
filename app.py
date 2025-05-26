# streamlit run app.py
# source .venv/scripts/activate

import streamlit as st
import numpy as np
import pandas as pd
from sklearn.neighbors import BallTree

# pip install streamlit, numpy, pandas, scikit-learn, xgboost

st.title("Custom Apartment Prediction")
st.write("Input your specifications below")

urbans = ["Saburtalo","Didi Dighomi","Vake","Isani","Krtsanisi","Didube","Samgori",
          "Gldani","Nadzaladevi","Mtatsminda","Chughureti","Vashlijvari"]

conditions = ["unspecified","ახალი გარემონტებული","ძველი გარემონტებული",
              "მწვანე კარკასი","შავი კარკასი","სარემონტო","მიმდინარე რემონტი",
              "თეთრი პლიუსი","თეთრი კარკასი"]
estate_status_types = ["ახალი აშენებული","ძველი აშენებული","მშენებარე"]

bathroom_types = ["unspecified","1","2","3+","საერთო"]

room_types = ["1","2","3","4","5","6","7","8","9","10+"]
# id 6 doesn't exist. id 7 is actually 6
bedroom_types = ["unspecified","1","2","3","4","5","6","7","8","9","10+"]


st.subheader("Main Characteristics")

lat_col, lng_col = st.columns(2)
with lat_col:
    latitude = st.number_input(
    label="Latitude",
    min_value=41.61,
    max_value=41.84,
    step=0.000001,              # Step size of 1 means only integers
    format="%.6f"          # Optional: ensures it's displayed as an integer
    )

with lng_col:
    longitude = st.number_input(
    label="longitude",
    min_value=44.7,
    max_value=44.95,
    step=0.000001,              # Step size of 1 means only integers
    format="%.6f"          # Optional: ensures it's displayed as an integer
    )


col1, col2, col3 = st.columns(3)

with col1:
    urban = st.selectbox("Urban", urbans, key="urban")
    bathroom_type = st.selectbox("Bathroom", bathroom_types, key="bathroom")
    area = st.number_input(
    label="Area (square meters)",
    min_value=20,
    max_value=1000,
    step=1,              # Step size of 1 means only integers
    format="%d"          # Optional: ensures it's displayed as an integer
    )

with col2:
    condition = st.selectbox("Condition", conditions, key="condition")
    room_num = st.selectbox("Rooms", room_types, key="rooms")
    floor = st.number_input(
    label="Floor",
    min_value=0,
    max_value=2000,
    step=1,              # Step size of 1 means only integers
    format="%d"          # Optional: ensures it's displayed as an integer
    )

with col3:
    estate_status = st.selectbox("Estate Status", estate_status_types, key="estate_status")
    bedroom_type = st.selectbox("Bedrooms", bedroom_types, key="bedrooms")
    total_floors = st.number_input(
    label="Total floors in the building",
    min_value=0,
    max_value=2000,
    step=1,              # Step size of 1 means only integers
    format="%d"          # Optional: ensures it's displayed as an integer
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
            "sewage",
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
selected_features = st.multiselect("Select available features:", features)


if "storage room" in selected_features:
    storeroom_type = st.selectbox("storage room type",storeroom_types,key="storeroom_type")
else:
    storeroom_type = "unspecified"
if "swimming pool" in selected_features:
    swimming_pool_type = st.selectbox("swimming pool type",swimming_pool_types,key="swimming_pool_type")
else:
    swimming_pool_type = "unspecified"
if "living room" in selected_features:
    living_room_type = st.selectbox("living room type",living_room_types,key="living_room_type")
else:
    living_room_type = "unspecified"

col4, col5, col6 = st.columns(3)

with col4:
    build_year = st.selectbox("Build year",build_years,key="build_year")
    height = st.number_input(
        label="Enter height (in meters)",
        min_value=0.0,
        max_value=500.0,
        step=0.01,
        format="%.2f"  # Optional: display 2 decimal places
    )
    balconies = st.number_input(
        label="Number of balconies",
        min_value=0,
        max_value=300,
        step=1,
        format="%d"
    )
    parking_type = st.selectbox("Parking type",parking_types,key="parking_type")

with col5:
    for_special_people = st.selectbox("Is it for special people?",["no","yes"],key="for_special_people")
    for_investment = st.selectbox("Is it for investment?",["no","yes"],key="for_investment")
    heating_type =  st.selectbox("Heating type",heating_types,key="heating_type")

with col6:
    project_type = st.selectbox("Project type",project_types,key="project_type")
    hot_water_type = st.selectbox("Hot water type",hot_water_types,key="hot_water_type")
    material_type = st.selectbox("Building material type",material_types,key="material_type")


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
               "Cheap"]

other_features = st.multiselect("Does any of these describe your apartment?", other_words)


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
has_sewage = 1 if "sewage" in selected_features else 0
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

def dist_to_center():
    cent_lat = 41.697007
    cent_lng = 44.799183
    return haversine(latitude, longitude,cent_lat,cent_lng)

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

city_center_dist = dist_to_center()
nearest_metro_dist = dist_to_places('for_location/metro_stations.csv', coords)
nearest_bus_stop_dist = dist_to_places('for_location/tbilisi_bus_stops.csv', coords)
nearest_gym_dist = dist_to_places('for_location/tbilisi_gyms.csv', coords)
nearest_kindergarten_dist = dist_to_places('for_location/tbilisi_kindergartens.csv', coords)
nearest_park_dist = dist_to_places('for_location/tbilisi_parks.csv', coords)
nearest_pharmacy_dist = dist_to_places('for_location/tbilisi_pharmacies.csv', coords)
nearest_school_dist = dist_to_places('for_location/tbilisi_schools.csv', coords)
nearest_supermarket_dist = dist_to_places('for_location/tbilisi_supermarkets.csv', coords)
nearest_university_dist = dist_to_places('for_location/tbilisi_universities.csv', coords)

metro_stations_nearby = count_within_radius('for_location/metro_stations.csv',coords,1)
bus_stops_nearby = count_within_radius('for_location/tbilisi_bus_stops.csv', coords, 1)
gyms_nearby = count_within_radius('for_location/tbilisi_gyms.csv',coords, 1)
kindergartens_nearby = count_within_radius('for_location/tbilisi_kindergartens.csv', coords, 1)
parks_nearby = count_within_radius('for_location/tbilisi_parks.csv',coords, 1)
pharmacies_nearby = count_within_radius('for_location/tbilisi_pharmacies.csv',coords, 1)
schools_nearby = count_within_radius('for_location/tbilisi_schools.csv', coords, 1)
supermarkets_nearby = count_within_radius('for_location/tbilisi_supermarkets.csv', coords, 1)
universities_nearby = count_within_radius('for_location/tbilisi_universities.csv', coords, 1)

# True ratio
for_special_people = 1 if for_special_people == "yes" else 0
for_investment = 1 if for_investment == "yes" else 0

sum_of_true = is_old+can_exchanged+for_special_people+has_color+has_gas+has_internet\
+has_TV+has_air_conditioner+has_alarms+has_elevator+has_ventilation+has_freight_elevator\
+has_chimney+has_furniture+has_telephone+has_protection+has_Jacuzzi+has_swimming_pool\
+has_sauna+has_fridge+has_washing_machine+has_dishwasher+has_stove+has_oven+has_living_room\
+has_loggia+has_veranda+has_water+has_sewage+has_electricity+has_spa+has_bar+has_gym+has_coded_door\
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
    has_sewage,
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
    for_investment,
    city_center_dist,
    nearest_metro_dist,
    nearest_bus_stop_dist,
    nearest_gym_dist,
    nearest_kindergarten_dist,
    nearest_park_dist,
    nearest_pharmacy_dist,
    nearest_school_dist,
    nearest_supermarket_dist,
    nearest_university_dist,
    metro_stations_nearby,
    bus_stops_nearby,
    gyms_nearby,
    kindergartens_nearby,
    parks_nearby,
    pharmacies_nearby,
    schools_nearby,
    supermarkets_nearby,
    universities_nearby,
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
]+estate_status_types_val+bathroom_types_val+proj_types_vals+heating_types_val+parking_types_val\
+storeroom_types_val+material_types_val+swimming_pool_types_val+hot_water_types_val+conditions_val\
+living_room_types_val+build_years_val+user_types_val+urbans_val
#st.write("You selected:", input_array)



import joblib
model = joblib.load("xgboost_model.pkl")

feature_vector = np.array(input_array).reshape(1,-1)

prediction = model.predict(feature_vector)

# Show prediction
st.subheader("Predicted Price:")
st.write(f"Price per square is {prediction[0]:,.2f} ₾ and the total {prediction[0]*area:,.2f} ₾")