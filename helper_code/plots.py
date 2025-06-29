import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import shap
import pandas as pd

def get_feature_names(
        estate_status_types_col,
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
        urbans_col,
        ):
    feature_names = [
        "room_num",
        "bedroom_type",
        "height",
        "balconies",
        "area",
        "floor",
        "total_floors",
        "views",
        "is_old",
        "can_exchanged",
        "for_special_people",
        "user_statements_count",
        "has_color",
        "has_gas",
        "has_internet",
        "has_TV",
        "has_air_conditioner",
        "has_alarms",
        "has_elevator",
        "has_ventilation",
        "has_freight_elevator",
        "has_chimney",
        "has_furniture",
        "has_telephone",
        "has_protection",
        "has_Jacuzzi",
        "has_swimming_pool",
        "has_sauna",
        "has_fridge",
        "has_washing_machine",
        "has_dishwasher",
        "has_stove",
        "has_oven",
        "has_living_room",
        "has_loggia",
        "has_veranda",
        "has_water",
        #has_sewage,
        "has_electricity",
        "has_spa",
        "has_bar",
        "has_gym",
        "has_coded_door",
        "has_grill",
        "has_bed",
        "has_sofa",
        "has_table",
        "has_chair",
        "has_kitchen_with_technology",
        "has_storage_room",
        "for_investment",

        "city_center_dist",
        "lisi_lake_dist",
        "ku_lake_dist",
        "dinamo_dist",
        "meskhi_dist",
        "public_service_hall_dist",
        "nearest_metro_dist",
        "nearest_bus_stop_dist",
        "nearest_gym_dist",
        "nearest_kindergarten_dist",
        "nearest_park_dist",
        "nearest_pharmacy_dist",
        "nearest_school_dist",
        "nearest_supermarket_dist",
        "nearest_university_dist",
        "nearest_atms_dist",
        "nearest_banks_dist",
        "nearest_gas_dist",
        "nearest_hospitals_dist",
        "nearest_malls_dist",
        "nearest_big_swimming_sites_dist",
        "nearest_courts_dist",
        "nearest_embassies_dist",
        "nearest_entertainment_dist",
        "nearest_fast_food_dist",
        "nearest_police_stations_dist",
        "nearest_swimming_pools_dist",
        "nearest_fast_food_chain_dist",
        "metro_stations_nearby_1km",
        "bus_stops_nearby_1km",
        "gyms_nearby_1km",
        "kindergartens_nearby_1km",
        "parks_nearby_1km",
        "pharmacies_nearby_1km",
        "schools_nearby_1km",
        "supermarkets_nearby_1km",
        "universities_nearby_1km",
        "atms_nearby_1km",
        "banks_nearby_1km",
        "gas_stations_nearby_1km",
        "hospitals_nearby_1km",
        "malls_nearby_1km",
        "big_swimming_sites_nearby_1km",
        "courts_nearby_1km",
        "embassies_nearby_1km",
        "entertainment_nearby_1km",
        "fast_food_nearby_1km",
        "police_stations_nearby_1km",
        "swimming_pools_nearby_1km",
        "fast_food_chain_nearby_1km",
        "metro_stations_nearby_500m",
        "bus_stops_nearby_500m",
        "gyms_nearby_500m",
        "kindergartens_nearby_500m",
        "parks_nearby_500m",
        "pharmacies_nearby_500m",
        "schools_nearby_500m",
        "supermarkets_nearby_500m",
        "universities_nearby_500m",
        "atms_nearby_500m",
        "banks_nearby_500m",
        "gas_stations_nearby_500m",
        "hospitals_nearby_500m",
        "malls_nearby_500m",
        "big_swimming_sites_nearby_500m",
        "courts_nearby_500m",
        "embassies_nearby_500m",
        "entertainment_nearby_500m",
        "fast_food_nearby_500m",
        "police_stations_nearby_500m",
        "swimming_pools_nearby_500m",
        "fast_food_chain_nearby_500m",
        "metro_stations_nearby_200m",
        "bus_stops_nearby_200m",
        "gyms_nearby_200m",
        "kindergartens_nearby_200m",
        "parks_nearby_200m",
        "pharmacies_nearby_200m",
        "schools_nearby_200m",
        "supermarkets_nearby_200m",
        "universities_nearby_200m",
        "atms_nearby_200m",
        "banks_nearby_200m",
        "gas_stations_nearby_200m",
        "hospitals_nearby_200m",
        "malls_nearby_200m",
        "big_swimming_sites_nearby_200m",
        "courts_nearby_200m",
        "embassies_nearby_200m",
        "entertainment_nearby_200m",
        "fast_food_nearby_200m",
        "police_stations_nearby_200m",
        "swimming_pools_nearby_200m",
        "fast_food_chain_nearby_200m",
        "metro_stations_nearby_100m",
        "bus_stops_nearby_100m",
        "gyms_nearby_100m",
        "kindergartens_nearby_100m",
        "parks_nearby_100m",
        "pharmacies_nearby_100m",
        "schools_nearby_100m",
        "supermarkets_nearby_100m",
        "universities_nearby_100m",
        "atms_nearby_100m",
        "banks_nearby_100m",
        "gas_stations_nearby_100m",
        "hospitals_nearby_100m",
        "malls_nearby_100m",
        "big_swimming_sites_nearby_100m",
        "courts_nearby_100m",
        "embassies_nearby_100m",
        "entertainment_nearby_100m",
        "fast_food_nearby_100m",
        "police_stations_nearby_100m",
        "swimming_pools_nearby_100m",
        "fast_food_chain_nearby_100m",

        "created_days_ago",
        "updated_days_ago",
        "true_ratio",
        "word_axis",
        "word_Bagebi",
        "word_Urgent",
        "word_Unlived",
        "word_Secondary",
        "word_with_renovation",
        "word_prestigeous",
        "word_complex",
        "word_cheap",
        "word_smart",
        "word_paved",
        "word_european",
        "word_has_view"
    ]



    prefixed_estate_status_types = [f"estate_status_type_{x}" for x in estate_status_types_col]
    prefixed_bathroom_types = [f"bathroom_type_{x}" for x in bathroom_types_col]
    prefixed_project_types = [f"project_type_{x}" for x in project_types_col]
    prefixed_heating_tyoes = [f"heating_type_{x}" for x in heating_types_col]
    prefixed_parking_types = [f"parking_type_{x}" for x in parking_types_col]
    prefixed_storeroom_types = [f"storeroom_type_{x}" for x in storeroom_types_col]
    prefixed_material_types = [f"material_type_{x}" for x in material_types_col]
    prefixed_swimming_pool_types = [f"swimming_pool_type_{x}" for x in swimming_pool_types_col]
    prefixed_hot_water_types = [f"hot_water_type_{x}" for x in hot_water_types_col]
    prefixed_condition_types = [f"condition_{x}" for x in conditions_col]
    prefixed_living_room_types = [f"living_toom_type_{x}" for x in living_room_types_col]
    prefixed_build_years = [f"build_year_{x}" for x in build_years_col]
    prefixed_user_types = [f"user_type_{x}" for x in user_types_col]
    prefixed_urbans = [f"urban_{x}" for x in urbans_col]


    feature_names = feature_names+prefixed_estate_status_types+prefixed_bathroom_types+\
    prefixed_project_types+prefixed_heating_tyoes+prefixed_parking_types+prefixed_storeroom_types+\
    prefixed_material_types+prefixed_swimming_pool_types+prefixed_hot_water_types+prefixed_condition_types+\
    prefixed_living_room_types+prefixed_build_years+prefixed_user_types+prefixed_urbans


    def clean_name(name):
        for ch in ['[', ']', '<', '>']:
            name = name.replace(ch, '_')
        return name

    feature_names = [clean_name(str(n)) for n in feature_names]

    return feature_names

def shap_value_waterplot(input_array, feature_names, model):
    feature_df   = pd.DataFrame([input_array], columns=feature_names)

    explainer   = shap.TreeExplainer(model)
    shap_values = explainer(feature_df)  


    fig, ax = plt.subplots()
    shap.plots.waterfall(shap_values[0], show=False)  # show=False prevents automatic plot display
    return fig

def price_interval_plot(
        lower, upper, prediction,
        true_value=None, *, area=1, total_price=False,
        interval_label="90% Prediction Interval",
        pred_label="Point Prediction",
        true_label="True Value",
        offset_pt=5,  # text shift in points
    ):
    """
    Horizontal interval + point (+ optional true point) plot.

    Parameters
    ----------
    lower, upper : float
        Bounds of the prediction interval (per‑sqm units).
    prediction : float or length‑1 array
        Point prediction (per‑sqm units).
    true_value : float, optional
        True target value (per‑sqm units).  If None, only the prediction is shown.
    area : float, default 1
        Multiplier to switch to total‑price units.
    total_price : bool, default False
        If True, x‑axis label switches to "Total Price ($)" and all values are area‑scaled.
    """

    # ---------- scale -----------------
    lower *= area
    upper *= area
    pred   = (prediction[0] if hasattr(prediction, "__iter__") else prediction) * area
    true   = None if true_value is None else true_value * area

    # ---------- plot ------------------
    fig, ax = plt.subplots(figsize=(6, 1.5))

    ax.hlines(0, lower, upper, color="skyblue", linewidth=8, label=interval_label)
    ax.plot(pred, 0, "o", color="red",  label=pred_label)

    if true is not None:
        ax.plot(true, 0, "o", color="green", label=true_label)

    # 5‑point offset converter
    d2p = transforms.ScaledTranslation(0, offset_pt / 72, fig.dpi_scale_trans)
    d2p_2 = transforms.ScaledTranslation(0, offset_pt*3 / 72, fig.dpi_scale_trans)

    # labels
    ax.text(pred, 0, f"{pred:,.2f} $",
            ha="center", va="bottom",
            transform=ax.transData + d2p,
            color="#8B0000", fontweight="bold", fontsize=10)

    if true is not None:
        ax.text(true, 0, f"{true:,.2f} $",
                ha="center", va="top",
                transform=ax.transData - d2p_2,
                color="green", fontweight="bold", fontsize=10)

    # ---------- formatting ------------
    xmin = min(lower, pred, true if true is not None else pred) * 0.95
    xmax = max(upper, pred, true if true is not None else pred) * 1.05
    ax.set_xlim(xmin, xmax)
    ax.set_yticks([])

    ax.set_xlabel("Total Price ($)" if total_price else "Price per square meter ($)")

    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15),
              ncol=3 if true is not None else 2)

    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)

    return fig
