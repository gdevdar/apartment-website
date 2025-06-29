import streamlit as st

st.set_page_config(
    page_title="Apartment Price Checker",
    page_icon="🏠",
    layout="centered"
)

st.title("Apartment Price Checker")
st.write("Enter a MyHome.ge apartment listing URL to check its estimated price.")

# URL input field
url = st.text_input(
    "Enter MyHome.ge URL",
    placeholder="https://www.myhome.ge/pr/..."
)

from helper_code.link_scrape import data_collector
from helper_code.data_extract import row_creator
from helper_code.data_extract import data_load
import pandas as pd
from helper_code.procedure import procedure

# Submit button
if st.button("Check Price"):
    if url:
        if "myhome.ge" in url.lower():
            st.write("Processing URL...")
            data = data_collector(url)
            mapping = data_load("mapping.json")
            row = row_creator(data,mapping)
            df = pd.DataFrame([row])
            from datetime import date
            today = date.today().isoformat()
            df = procedure(df,today)
            st.session_state['result_df'] = df
            # Your scraper code will go here
            # For now, just showing a placeholder
            st.dataframe(df, use_container_width=True)
            st.info("URL received and ready for processing!")
        else:
            st.error("Please enter a valid MyHome.ge URL")
    else:
        st.warning("Please enter a URL first")

if 'result_df' in st.session_state:
    import numpy as np
    df = st.session_state['result_df']
    # Display the original price per square, price and the id of the apartment
    apartment_id = df['id'].iloc[0]
    total_price = df['price_2_price_total'].iloc[0]
    price_per_sqm = df['price_2_price_square'].iloc[0]

    df = df.drop(columns = ['id','price_2_price_total','price_2_price_square'])
    estate_status = df['estate_status_types'].iloc[0]
    bathroom_type = df['bathroom_type'].iloc[0]
    project_type = df['project_type'].iloc[0]
    heating_type = df['heating_type'].iloc[0]
    parking_type = df['parking_type'].iloc[0]
    storeroom_type = df['storeroom_type'].iloc[0]
    material_type = df['material_type'].iloc[0]
    swimming_pool_type = df['swimming_pool_type'].iloc[0]
    hot_water_type = df['hot_water_type'].iloc[0]
    condition = df['condition'].iloc[0]
    living_room_type = df['living_room_type'].iloc[0]
    build_year = df['build_year'].iloc[0]
    user_type = df['user_type'].iloc[0]
    urban = df['urban'].iloc[0]

    df = df.drop(columns = ['estate_status_types','bathroom_type','project_type','heating_type',
                            'parking_type','storeroom_type','material_type','swimming_pool_type',
                            'hot_water_type','condition','living_room_type','build_year',
                            'user_type','urban'])

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
    user_types_val = []
    for type in build_years_col:
        user_types_val.append(1 if user_type == type else 0)
   
    # urban
    urbans_col = ["Chughureti","Didi Dighomi","Didube","Gldani","Isani","Krtsanisi",
            "Mtatsminda","Nadzaladevi","Saburtalo","Samgori","Vake",
            "Vashlijvari"]
    urbans_val = []
    for type in urbans_col:
        urbans_val.append(1 if urban == type else 0)

    categoricals = estate_status_types_val+bathroom_types_val+proj_types_vals+heating_types_val+parking_types_val\
    +storeroom_types_val+material_types_val+swimming_pool_types_val+hot_water_types_val+conditions_val\
    +living_room_types_val+build_years_val+user_types_val+urbans_val

    # Convering booleans into integers
    bool_cols = df.select_dtypes(include='bool').columns
    df[bool_cols] = df[bool_cols].astype(int)
    lst = df.iloc[0].tolist()

    input_array = lst+categoricals
    #st.write(input_array)
    import joblib
    model = joblib.load("xgboost_model18june.pkl")

    feature_vector = np.array(input_array).reshape(1,-1)

    prediction = model.predict(feature_vector)
    predicted_value = prediction[0]
    total_price_pred = predicted_value * df['area'].iloc[0]

    diff_per_sqm = price_per_sqm - predicted_value
    diff_total = total_price - total_price_pred

    per_sqm_label = "overvalued" if diff_per_sqm > 0 else "undervalued"
    total_label = "overvalued" if diff_total > 0 else "undervalued"

    st.markdown(
        f"🏠 **Apartment ID:** `{apartment_id}`\n\n💵 **Price:** `${total_price:,.0f}`\n\n📐 **Price per square meter:** `${price_per_sqm:,.0f}`"
    )
    st.markdown(
    f"🔍 This apartment is **{per_sqm_label}** by `${abs(diff_per_sqm):,.0f}` per square meter.\n\n"
    f"🔍 The total price is **{total_label}** by `${abs(diff_total):,.0f}` in total."
    )
    #q_hat = pd.read_csv('conformal/q_hat.csv')['q_hat'].iloc[0]
    loforest = joblib.load("loforest_full_model.pkl")
    bounds = loforest.predict(feature_vector)
    lower = bounds[:,0][0]
    upper = bounds[:,1][0]

    #lower, upper = prediction[0] - q_hat, prediction[0] + q_hat

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
    per_square_fig = price_interval_plot(lower,upper,prediction,true_value=price_per_sqm)
    st.pyplot(per_square_fig)

    total_price_fig = price_interval_plot(lower,upper,prediction,true_value=price_per_sqm,total_price=True,area=df['area'][0])
    st.pyplot(total_price_fig)
    st.subheader("SHAP Waterfall Plot")
    shap_fig = shap_value_waterplot(input_array, feature_names, model)
    st.pyplot(shap_fig)