import numpy as np
import pandas as pd
import re

def expanding_car_name_col(col):
     """
     (Function need to be used after level 1 cleaning)
     Function that accept a car_name col and expands to dataframe
     
     returns a DataFrame with colunms - model_year,Brand_name,model_name
     """
     return (       col
                    .str.strip()
                    .str.split(' ',n=2,expand=True)
                    .set_axis(['model_year','Brand_name','model_name'],axis=1)
            )

def MPG_mean_calculation(col):
    """
    (Function need to be used after level 1 cleaning)
    Function that accept the mpg column and calculate mean of hyphened mpg values 
    else the number itself
    e.g. -> 10-15 converted to 12.5

    returns a column
    """
    return (
        col
        .str.strip()
        .str.split('\n',n=1)
        .str.get(0)
        .str.split('–',expand=True)
        .set_axis(['lower_mpg','higher_mpg'],axis=1)
        .fillna('0')
        .replace('','0')
        .assign(
            lower_mpg = lambda df_ : (
                df_
                .lower_mpg
                .astype(float)
            ),

            higher_mpg = lambda df_ : (
                df_
                .higher_mpg
                .astype(float)
            )
        )
    ).mean(axis=1)

# drivetrain_map is useful to put each messy drivetrain column's value to a specific category, insuring consistency.
# it can be edited according to future need
drivetrain_map = {
    # Four-wheel drive variations
    "Four-wheel Drive": "4WD",
    "Four Wheel Drive": "4WD",
    "4WD": "4WD",

    # All-wheel drive variations
    "All-wheel Drive": "AWD",
    "All Wheel Drive": "AWD",
    "AWD": "AWD",

    # Front-wheel drive variations
    "Front-wheel Drive": "FWD",
    "Front Wheel Drive": "FWD",
    "FWD": "FWD",

    # Rear-wheel drive variations
    "Rear-wheel Drive": "RWD",
    "RWD": "RWD",

    # Invalid / unknown values
    "-": np.nan,
    "–": np.nan, 
    "Unknown": np.nan
}

# fuel_map is helpful to pair each messy value of fuel_type col to a relevent category, insuring data consistency.
# it can be updated, if I encounter more category
fuel_map = {
    # Gasoline / Petrol
    "Gasoline": "Gasoline",
    "Gasoline / Petrol": "Gasoline",
    "Gasoline fuel type": "Gasoline",
    "Gasoline Fuel": "Gasoline",
    "Regular Unleaded": "Gasoline",
    'Gas': 'Gasoline',
    'Gas Regular Unleaded': 'Gasoline',
    

    # Diesel
    "Diesel": "Diesel",
    "Diesel (B20 capable)": "Diesel",
    "Diesel fuel type": "Diesel",

    # Hybrid
    "Hybrid": "Hybrid",
    "Hybrid Fuel": "Hybrid",
    "Full Hybrid Electric (FHEV)": "Hybrid",
    "Gasoline/Mild Electric Hybrid": "Hybrid",
    "Gasoline/Mild Electric Hy": "Hybrid",
    "MHEV (mild hybrid electric vehicle)": "Hybrid",
    "Gasoline/Mild Electr": "Hybrid",     
    "Hybrid fuel": "Hybrid",            
    "MH": "Hybrid",     
    "Gas Hybrid" : "Hybrid",
    "PHEV (plug-in hybrid electric vehicle)" : "Hybrid",                 

    # Plug-in Hybrid
    "Plug-In Hybrid": "Plug-in Hybrid",
    "Plug-in Gas/Electric Hybrid": "Plug-in Hybrid",
    "Plug-in Hybrid": "Plug-in Hybrid",   
    "hybrid_plug_in": "Plug-in Hybrid",  

    # Flex Fuel / Ethanol
    "E85 Flex Fuel": "Flex Fuel",
    "Flexible Fuel": "Flex Fuel",
    "Flex Fuel": "Flex Fuel", 
    "flex_fuel" : "Flex Fuel",         
    "Ethanol": "Flex Fuel",               

    # Gaseous Fuels
    "Gaseous": "CNG/LPG",
    "Compressed Natural Gas": "CNG/LPG",
    "Gas/CNG": "CNG/LPG",
    "Gasoline / Natural Gas": "CNG/LPG",
    "Natural Gas": "CNG/LPG",             
    "CNG/LPG": "CNG/LPG", 

    "Electric fuel type" : "Electric",                

    # Other/Unknown
    "Other": "Other",
    "Unknown": np.nan,                   
    "Unspecified": np.nan,
    "–": np.nan,
    None: np.nan                          
}


def speeds_in_transmission(col):
    """
    (Function need to be used after level 1 cleaning)
    This function takes the transmission col as input and extract the speed-detail using regex

    returns a column containing gear-specs
    """
    pattern = r'\b(?:\d+|ten|single|one|two|three|four|five|six|seven|eight|nine)-?\s*(?:speed|spd)\b|\b\d+A[T]?\b'
    return (
            col
            .str.strip()
            .str.lower()
            .str.extract(f'({pattern})',flags=re.IGNORECASE)
        )

# transmission_mapping dict is helpful to map messy value of Transmission to its corresponding cleaned value.
transmission_mapping = {
    'manual': 'Manual',
    'm/t': 'Manual',
    'automatic': 'Automatic',
    'auto': 'Automatic',
    'a/t': 'Automatic',
    'at': 'Automatic',
    'cvt': 'CVT',
    'variable': 'CVT',
    'ect': 'Automatic',
    'shiftable': 'Automatic',
    'dual shift': 'Automatic',
    'double clutch': 'DCT',
    'double clutc': 'DCT',
    'dual clutch': 'DCT',
    'quattroa': 'Automatic',
    'tronica': 'DCT',
    '–': np.nan,
    '8-speed porsche doppelkupplung (pdk)': 'DCT',
    'single-speed transmission': 'Automatic',
    'a': 'Automatic',
    'hev 10-speed transmission': 'Automatic',
    '10-speed transmission': 'Automatic',
    'not specified': np.nan,
    '10 speed allison': 'Automatic',
    '7-speed porsche doppelkupplung (pdk)': 'DCT',
    '2-speed': 'Automatic',
    's tronic': 'DCT',
    'dft': np.nan,
    '10a': 'Automatic',
    '10 speed': 'Automatic',
    '265/': np.nan,
    'null': np.nan,
    'unknown': np.nan,
    '7a': 'Automatic',
    'single-speed fixed gear': 'Automatic',
    '.10-speed transmission': 'Automatic',
    'front/rear offset 1 spd gearbox': 'Automatic',
    '6a': 'Automatic',
    'allison': 'Automatic',
    'unknown other': np.nan,
    'm-21 4-speed': 'Manual',
    '8-speed pdk': 'DCT',
    'single speed reducer': 'Automatic',
    '255f': np.nan,
    '904 3 speed': 'Automatic',
    '8 spd zf sport trans w/paddles': 'Automatic',
    '6 speed allison': 'Automatic',
    'pdk': 'DCT',
    'quattro s tronic': 'DCT',
    'unknown/ other': np.nan,
    'aod': 'Automatic',
    '5a': 'Automatic',
    '1a': 'Automatic',
    '4at': 'Automatic',
    'transmission overdrive switch': np.nan,
    'ivt': 'CVT',
    '44t': np.nan,
    '7-speed pdk': 'DCT',
    '3at': 'Automatic',
    '62 kwh battery': np.nan,
    'single speed': 'Automatic',
    'standard': np.nan,
    '5 speed': 'Manual',
    '5-speed': 'Manual',
    '6-speed': 'Manual',
    '7-speed': 'Manual'
}

def extracting_transmission(val):
    """
    This function takes transmission col (after level-1 cleaning) as input

    return correct Transmission value using transmission_mapping dict
    """
    for key,value in transmission_mapping.items():
        if key in val:
            return value
    return np.nan

def expending_convenience(col):
    """
    (Function need to be used after level 1 cleaning)
    This function takes Convenience column as input

    returns a dataframe with 13 columns includes - 
    1. adaptive_cruise_control 2. cooled_seats 3. heated_seats. 4. heated_steering_wheels 5. keyless_entry
    6. keyless_start 7. navigation_system 8. remote_start 9. power_liftgate 10.automatic_parking 11. wheel_chair_accessible
    12. autopilot
    """
    adaptive_cruise_control = []
    cooled_seats = []
    heated_seats = []
    heated_steering_wheels = []
    keyless_entry = []
    keyless_start = []
    navigation_system = []
    remote_start = []
    power_liftgate = []
    automatic_parking = []
    power_folding_mirror = []
    wheel_chair_accessible = []
    autopilot = []

    for i in (col.str.strip().str.split('\n')).values:
        if i is None:
            adaptive_cruise_control.append(np.nan)
            cooled_seats.append(np.nan)
            heated_seats.append(np.nan)
            heated_steering_wheels.append(np.nan)
            keyless_entry.append(np.nan)
            keyless_start.append(np.nan)
            navigation_system.append(np.nan)
            remote_start.append(np.nan)
            power_liftgate.append(np.nan)
            automatic_parking.append(np.nan)
            power_folding_mirror.append(np.nan)
            wheel_chair_accessible.append(np.nan)
            autopilot.append(np.nan)
        
        else:
            if 'Adaptive Cruise Control' in i:
                adaptive_cruise_control.append('yes')
            else:
                adaptive_cruise_control.append(np.nan)
            
            if 'Cooled Seats' in i:
                cooled_seats.append('yes')
            else:
                cooled_seats.append(np.nan)
            
            if 'Heated Seats' in i:
                heated_seats.append('yes')
            else:
                heated_seats.append(np.nan)
            
            if 'Heated Steering Wheel' in i:
                heated_steering_wheels.append('yes')
            else:
                heated_steering_wheels.append(np.nan)
            
            if 'Keyless Entry' in i:
                keyless_entry.append('yes')
            else:
                keyless_entry.append(np.nan)
            
            if 'Keyless Start' in i:
                keyless_start.append('yes')
            else:
                keyless_start.append(np.nan)
            
            if 'Navigation System' in i:
                navigation_system.append('yes')
            else:
                navigation_system.append(np.nan)
            
            if 'Remote Start' in i:
                remote_start.append('yes')
            else:
                remote_start.append(np.nan)
            
            if 'Power Liftgate' in i:
                power_liftgate.append('yes')
            else:
                power_liftgate.append(np.nan)
            
            if 'Automatic Parking' in i:
                automatic_parking.append('yes')
            else:
                automatic_parking.append(np.nan)
            
            if 'Power Folding Mirrors' in i:
                power_folding_mirror.append('yes')
            else:
                power_folding_mirror.append(np.nan)
            
            if 'Wheelchair Accessible' in i:
                wheel_chair_accessible.append('yes')
            else:
                wheel_chair_accessible.append(np.nan)
            
            if 'Autopilot' in i:
                autopilot.append('yes')
            else:
                autopilot.append(np.nan)

    return pd.DataFrame({'adaptive_cruise_control':adaptive_cruise_control,'cooled_seats':cooled_seats,'heated_seats':heated_seats,'heated_steering_wheels':heated_steering_wheels,'keyless_entry':keyless_entry,'keyless_start':keyless_start,'navigation_system':navigation_system,'remote_start':remote_start,'power_liftgate':power_liftgate,'automatic_parking':automatic_parking,'power_folding_mirror':power_folding_mirror,'wheel_chair_accessible':wheel_chair_accessible,'autopilot':autopilot})


def expanding_entertainment(col):
    """
    (Function need to be used after level 1 cleaning)
    This function takes Entertainment col 
    
    returns a dataframe containing 12 cols, which includes - 
    1. android_auto 2. apple_carplay 3. bluetooth 4. premium_sound_system
    5. usb_port 6. wifi_hotspot 7. satelite_radio 8. cd_player 
    9. homelink 10. rear_seat_entertainment 11. dvd_player
    """
    android_auto =[]
    apple_carplay = []
    bluetooth = []
    premium_sound_system = []
    usb_port = []
    wifi_hotspot = []
    satellite_radio = []
    cd_player = []
    homelink = []
    rear_seat_entertainment = []
    dvd_player = []

    for i in (col.str.strip().str.split('\n')).values:
        if i is None:
            android_auto.append(np.nan)
            apple_carplay.append(np.nan)
            bluetooth.append(np.nan)
            premium_sound_system.append(np.nan)
            usb_port.append(np.nan)
            wifi_hotspot.append(np.nan)
            satellite_radio.append(np.nan)
            cd_player.append(np.nan)
            homelink.append(np.nan)
            rear_seat_entertainment.append(np.nan)
            dvd_player.append(np.nan)
        else:
            if ('Android Auto®' in i) or ('Apple CarPlay/Android Auto' in i) or ('Apple CarPlay®/Android Auto®' in i):
                android_auto.append('yes')
            else:
                android_auto.append(np.nan)
            
            if ('Apple CarPlay®' in i) or ('Apple CarPlay/Android Auto' in i) or ('Apple CarPlay®/Android Auto®' in i):
                apple_carplay.append('yes')
            else:
                apple_carplay.append(np.nan)
            

            if ('Bluetooth®' in i) or ('Bluetooth' in i):
                bluetooth.append('yes')
            else:
                bluetooth.append(np.nan)
            
            if 'Premium Sound System' in i:
                premium_sound_system.append('yes')
            else:
                premium_sound_system.append(np.nan)
            
            if 'USB Port' in i:
                usb_port.append('yes')
            else:
                usb_port.append(np.nan)
            
            if 'WiFi Hotspot' in i:
                wifi_hotspot.append('yes')
            else:
                wifi_hotspot.append(np.nan)
            
            if 'Satellite Radio' in i:
                satellite_radio.append('yes')
            else:
                satellite_radio.append(np.nan)
            
            if 'CD Player' in i:
                cd_player.append('yes')
            else:
                cd_player.append(np.nan)
            
            if 'HomeLink' in i:
                homelink.append('yes')
            else:
                homelink.append(np.nan)
            
            if 'Rear Seat Entertainment' in i:
                rear_seat_entertainment.append('yes')
            else:
                rear_seat_entertainment.append(np.nan)
            
            if 'DVD Player' in i:
                dvd_player.append('yes')
            else:
                dvd_player.append(np.nan)
    return pd.DataFrame({'android_auto':android_auto,'apple_carplay':apple_carplay,'bluetooth':bluetooth,'premium_sound_system':premium_sound_system,'usb_port':usb_port,'wifi_hotspot':wifi_hotspot,'satellite_radio':satellite_radio,'cd_player':cd_player,'homelink':homelink,'rear_seat_entertainment':rear_seat_entertainment,'dvd_player':dvd_player})


def expanding_exterior(col):
    """
    (Function need to be used after level 1 cleaning)
    This function takes exterior column as input 

    returns a dataframe with 5 col, that includes - 
    1. alloy_wheels 2. sunroof_moonroof 
    3. tow_hitch 4. tow_hooks
    5. roof_rack
    """
    alloy_wheels = []
    sunroof_moonroof = []
    tow_hitch = []
    tow_hooks = []
    roof_rack = []

    for i in (col.str.strip().str.split('\n')).values:
        if i is None:
            alloy_wheels.append(np.nan)
            sunroof_moonroof.append(np.nan)
            tow_hitch.append(np.nan)
            tow_hooks.append(np.nan)
            roof_rack.append(np.nan)
        else:
            if 'Alloy Wheels' in i:
                alloy_wheels.append('yes')
            else:
                alloy_wheels.append(np.nan)
            
            if ('Sunroof/Moonroof' in i) or ('Moonroof' in i):
                sunroof_moonroof.append('yes')
            else:
                sunroof_moonroof.append(np.nan)
            
            if 'Tow Hitch' in i:
                tow_hitch.append('yes')
            else:
                tow_hitch.append(np.nan)
            
            if 'Tow Hooks' in i:
                tow_hooks.append('yes')
            else:
                tow_hooks.append(np.nan)
            
            if 'Roof Rack' in i:
                roof_rack.append('yes')
            else:
                roof_rack.append(np.nan)

    return pd.DataFrame({'alloy_wheels':alloy_wheels,'sunroof_moonroof':sunroof_moonroof,'tow_hitch':tow_hitch,'tow_hooks':tow_hooks,'roof_rack':roof_rack})

def expanding_safety(col):
    """
    (Function need to be used after level 1 cleaning)
    Function takes safety col as input 

    returns dataframe with 9 cols, that includes - 
    1. automatic_emergency_braking 2. backup_camera 3. blind_spot_monitor
    4. brake_assist 5. led_headlights 6. lane_departre_warning 7. rear_cross_traffic_alert
    8. stability_control 9. rain_sensing_wipers
    """
    automatic_emergency_braking = []
    backup_camera = []
    blind_spot_monitor = []
    brake_assist = []
    led_headlights = []
    lane_departure_warning = []
    rear_cross_traffic_alert = []
    stability_control = []
    rain_sensing_wipers = []

    for i in (col.str.strip().str.split('\n')).values:
        if i is None:
            automatic_emergency_braking.append(np.nan)
            backup_camera.append(np.nan)
            blind_spot_monitor.append(np.nan)
            brake_assist.append(np.nan)
            led_headlights.append(np.nan)
            lane_departure_warning.append(np.nan)
            rear_cross_traffic_alert.append(np.nan)
            stability_control.append(np.nan)
            rain_sensing_wipers.append(np.nan)
        else:
            if 'Automatic Emergency Braking' in i:
                automatic_emergency_braking.append('yes')
            else:
                automatic_emergency_braking.append(np.nan)
            
            if 'Backup Camera' in i:
                backup_camera.append('yes')
            else:
                backup_camera.append(np.nan)
            
            if 'Blind Spot Monitor' in i:
                blind_spot_monitor.append('yes')
            else:
                blind_spot_monitor.append(np.nan)
            
            if 'Brake Assist' in i:
                brake_assist.append('yes')
            else:
                brake_assist.append(np.nan)
            
            if 'LED Headlights' in i:
                led_headlights.append('yes')
            else:
                led_headlights.append(np.nan)
            
            if 'Lane Departure Warning' in i:
                lane_departure_warning.append('yes')
            else:
                lane_departure_warning.append(np.nan)
            
            if 'Rear Cross Traffic Alert' in i:
                rear_cross_traffic_alert.append('yes')
            else:
                rear_cross_traffic_alert.append(np.nan)
            
            if 'Stability Control' in i:
                stability_control.append('yes')
            else:
                stability_control.append(np.nan)
            
            if 'Rain Sensing Wipers' in i:
                rain_sensing_wipers.append('yes')
            else:
                rain_sensing_wipers.append(np.nan)

    return pd.DataFrame({'automatic_emergency_braking':automatic_emergency_braking,'backup_camera':backup_camera,'blind_spot_monitor':blind_spot_monitor,
                         'brake_assist':brake_assist,'led_headlights':led_headlights,'lane_departure_warning':lane_departure_warning,
                         'rear_cross_traffic_alert':rear_cross_traffic_alert,'stability_control':stability_control,'rain_sensing_wipers':rain_sensing_wipers
                         })

def expanding_seating(col):
    """
    (Function need to be used after level 1 cleaning)
    Function takes seating col as input

    returns a dataframe with 3 cols
    1. leather_seats 
    2. memory_seat
    3. third_row_seating
    """
    leather_seats = []
    memory_seat = []
    third_row_seating = []

    for i in (col.str.strip().str.split('\n')).values:
        if i is None:
            leather_seats.append(np.nan)
            memory_seat.append(np.nan)
            third_row_seating.append(np.nan)
        else:
            if 'Leather Seats' in i:
                leather_seats.append('yes')
            else:
                leather_seats.append(np.nan)
            
            if 'Memory Seat' in i:
                memory_seat.append('yes')
            else:
                memory_seat.append(np.nan)
            
            if 'Third Row Seating' in i:
                third_row_seating.append('yes')
            else:
                third_row_seating.append(np.nan)

    return pd.DataFrame({'leather_seats':leather_seats,'memory_seat':memory_seat,'third_row_seating':third_row_seating}) 

def expanding_seller_address(col):
    """
    (Function need to be used after level 1 cleaning)
    Function takes seller address as input 

    Returns dataframe with 4 cols that are - 
    1. street_address 2. city 
    3. state 4. postal code
    """
    return (
        col
        .str.replace(',,',',')
        .str.split(',',expand=True,n=1)
        .set_axis(['street_address','city_state'],axis=1)
        .assign(
            city = lambda df_ : (
                df_
                .city_state
                .str.rsplit(',',n=1)
                .str.get(0)
            ),

            state = lambda df_ : (
                df_
                .city_state
                .str.rsplit(',',n=1)
                .str.get(1)
            )
        )
        .assign(
            postal_code = lambda df_ : (
                df_
                .state
                .str.strip()
                .str.split(' ',n=1)
                .str.get(-1)
            ),

            state = lambda df_ : (
                df_
                .state
                .str.strip()
                .str.split(' ',n=1)
                .str.get(0)
            )
        )
        .drop(columns='city_state')
    )

def expanding_mpge(col):
        """

        (Function need to be used after level 1 cleaning)
        Functions takes mpge col as input

        Returns dataframe with 2 cols 
        1. mpge_city
        2. mpge_hwy

        """
        return   (    col
                    .str.split('/',expand=True)
                    .set_axis(['mpge_city','mpge_hwy'],axis=1)
                    .assign(
                        mpge_city = lambda df_ : (
                            df_
                            .mpge_city
                            .str.strip()
                            .str.replace('\ncity','')
                        ),
                        mpge_hwy = lambda df_ : (
                            df_
                            .mpge_hwy
                            .str.strip()
                            .str.replace('\nhwy.','')
                        )
                    ))

def expanding_battery_range_score(col):
    """

    (Function need to be used after level 1 cleaning)
    Function takes battery_range_score col as input 

    Returns dataframe with 2 columns
    1. Battery_range_score_cleaned 
    2. Battery_range_score_category

    """
    return (
                    col
                    .dropna()
                    .str.split('|',expand=True)
                    .set_axis(['battery_range_score_cleaned','battery_range_score_category'],axis=1)
                    .assign(
                        battery_range_score_cleaned = lambda df_ : (
                            df_
                            .battery_range_score_cleaned
                            .str.strip()
                        ),

                        battery_range_score_category = lambda df_ : (
                            df_
                            .battery_range_score_category
                            .str.strip()
                        )
                    )
    )


# This dict will be used with extracting_color function, to extract perticular category from messy interior and exterior color col
color_keywords = {
    # Whites
    'white': 'white',
    'pearl': 'white',
    'ivory': 'white',
    'snow': 'white',
    'ice': 'white',
    'frost': 'white',
    'powder': 'white',
    'chalk': 'white',
    'cap': 'white',       # Ice Cap
    'blizzard': 'white',
    'moon dust': 'white',
    'fresh powder': 'white',

    # Blacks / dark
    'black': 'black',
    'ebony': 'black',
    'onyx': 'black',
    'midnight': 'black',
    'caviar': 'black',
    'shadow': 'black',
    'underground': 'black',
    'crystal bl': 'black',  # paint code variation

    # Gray / Silver
    'gray': 'gray',
    'grey': 'gray',
    'gun': 'gray',
    'graphite': 'gray',
    'charcoal': 'gray',
    'slate': 'gray',
    'ash': 'gray',
    'cement': 'gray',
    'pewter': 'gray',
    'metal': 'gray',        # Heavy Metal, Polished Metal, Panthera Metal
    'tungsten': 'gray',
    'meteorite': 'gray',
    'maximum steel': 'gray',
    'steel': 'gray',
    'modern steel': 'gray',
    'smoke': 'gray',

    'silver': 'silver',
    'platinum': 'silver',
    'sterling': 'silver',
    'billet': 'silver',
    'satin': 'silver',
    'nickel': 'silver',
    'iridium': 'silver',
    'rhodoium': 'silver',
    'polished': 'silver',
    'moonbeam': 'silver',

    # Red
    'red': 'red',
    'ruby': 'red',
    'scarlet': 'red',
    'ember': 'red',
    'crimson': 'red',
    'burgundy': 'red',
    'velvet': 'red',
    'rouge': 'red',
    'magma': 'red',
    'molten': 'red',
    'sinamon': 'red',
    'pr6': 'red',

    # Blue
    'blue': 'blue',
    'navy': 'blue',
    'aqua': 'blue',
    'teal': 'blue',
    'indigo': 'blue',
    'sky': 'blue',
    'ocean': 'blue',
    'lake': 'blue',
    'canyon': 'blue',
    'downpour': 'blue',
    'frostbite': 'blue',
    'velocity': 'blue',

    # Green
    'green': 'green',
    'cypress': 'green',
    'cactus': 'green',
    'mojito': 'green',
    'emerald': 'green',
    'olive': 'green',

    # Yellow / Orange / Gold
    'yellow': 'yellow',
    'gold': 'yellow',
    'champagne': 'yellow',
    'sand': 'yellow',
    'desert': 'yellow',
    'dune': 'yellow',
    'tan': 'yellow',
    'beige': 'yellow',
    'terra': 'yellow',
    'high velocity': 'yellow',
    'mango': 'orange',
    'yella': 'yellow',   # Hellayella

    # Purple
    'purple': 'purple',
    'magenta': 'purple',
    'hellraisin': 'purple',
    'raisin': 'purple',
    'pr6': 'red',

    "anvil clearcoat": "Gray",
    "avalanche": "White",
    "lunar rock": "Gray",
    "brown": "Brown",
    "cutting edge": "Gray",
    "magnetic": "Gray",
    "joose": "Green",
    "orange": "Orange",
    "celestite": "Blue",
    "maroon": "Red",
    "area 51": "Blue",
    "bronze": "Brown",
    "mars orange": "Orange",
    "lunar": "Gray",
    "bronze oxide": "Brown",
    "crystal": "White",
    "diamond": "White",
    "granite crystal": "Gray",
    "anvil clear coat": "Gray",
    "nightfall mica": "Blue",
    "rhino clearcoat": "Gray",
    "granite": "Gray",
    "earl clearcoat": "Green",
    "pear": "White",
    "rhodium": "Gray",
    "anvil": "Gray",
    "obsidian": "Black",
    "bluprint": "Blue",
    "sebring orange tintcoat": "Orange",
    "inferno": "Orange",
    "opulent amber": "Brown",
    "magnetite": "Gray",
    "azure": "Blue",
    "limited edition gobi clearcoat": "Beige",
    "wind chill prl": "White",
    "amplify orange tintcoat": "Orange",
    "lime rush": "Green",
    "alien ii": "Green",
    "lime": "Green",
    "maroon": "Red",
    "cyber orange met tri-coat": "Orange",
    "shock": "Yellow",
    "m7": "Gray",
    "magnetic": "Gray",
    "wild cherry tintcoat": "Red",
    "lead foot": "Gray",
    "everest": "Gray",
    "avalanche": "White",
    "competition orange": "Orange",
    "creme brulee mica": "Beige",
    "gobi clearcoat": "Beige",
    "baja storm": "Brown",
    "after dark": "Black",
    "gator clearcoat": "Green",
    "sunset": "Orange",
    "stardust": "Gray",
    "nacho clearcoat": "Orange",
    "fusion orange": "Orange",
    "crush": "Orange",
    "anvil clear-coat exterior paint": "Gray",
    "chief clearcoat": "Blue",
    "celestite": "Blue",
    "blk": "Black",
    "gry": "Gray",
    "verde": "Green",

    "creme brulee mica": "Beige",
    "gator clearcoat": "Green",
    "still night": "Blue",
    "wh": "White",
    "blu": "Blue",
    "brilliant": "Silver",
    "iridescent prl": "White",
    "amber": "Orange",
    "alpine": "White",
    "wht": "White",
    "pure": "White",
    "tambora flame": "Orange",
    "cream": "Beige",
    "limited edition gecko clearcoat": "Green",
    "titainium": "Gray",
    "tide": "Blue",
    "rock lobster clearcoat": "Red",
    "bl": "Black",
    "aluminum": "Silver",
    "quartz": "Gray",
    "truffle mica": "Brown",
    "jet blk mica": "Black",
    "burgandy": "Red",
    "merlot": "Red",
    "autumn": "Orange",
    "agate": "Gray",
    "smokin asphalt": "Gray",
    "pyrite mica": "Brown",
    "wind chill": "White",


    "creme brulee mica": "beige",
    "gator clearcoat": "green",
    "still night": "blue",
    "wh": "white",
    "blu": "blue",
    "brilliant": "silver",
    "iridescent prl": "white",
    "amber": "orange",
    "alpine": "white",
    "wht": "white",
    "pure": "white",
    "tambora flame": "orange",
    "cream": "beige",
    "limited edition gecko clearcoat": "green",
    "titainium": "gray",
    "tide": "blue",
    "rock lobster clearcoat": "red",
    "bl": "black",
    "aluminum": "silver",
    "quartz": "gray",
    "truffle mica": "brown",
    "jet blk mica": "black",
    "burgandy": "red",
    "merlot": "red",
    "autumn": "orange",
    "agate": "gray",
    "smokin asphalt": "gray",
    "pyrite mica": "brown",
    "wind chill": "white",
    "storm": "gray",
    "walnut": "brown",
    "leather": "brown",
    "dozer clearcoat": "yellow",
    "mars orang": "orange",

    "creme brulee mica": "beige",
    "gator clearcoat": "green",
    "still night": "blue",
    "wh": "white",
    "blu": "blue",
    "brilliant": "silver",
    "iridescent prl": "white",
    "amber": "orange",
    "alpine": "white",
    "wht": "white",
    "pure": "white",
    "tambora flame": "orange",
    "cream": "beige",
    "limited edition gecko clearcoat": "green",
    "titainium": "gray",
    "tide": "blue",
    "rock lobster clearcoat": "red",
    "bl": "black",
    "aluminum": "silver",
    "quartz": "gray",
    "truffle mica": "brown",
    "jet blk mica": "black",
    "burgandy": "red",
    "merlot": "red",
    "autumn": "orange",
    "agate": "gray",
    "smokin asphalt": "gray",
    "pyrite mica": "brown",
    "wind chill": "white",
    "storm": "gray",
    "walnut": "brown",
    "leather": "brown",
    "dozer clearcoat": "yellow",
    "mars orang": "orange",

    "creme brulee mica": "beige",
    "gator clearcoat": "green",
    "truffle mica": "brown",
    "titainium": "gray",
    "aluminum": "silver",
    "autumn": "orange",
    "pyrite mica": "brown",
    "burgandy": "red",
    "agate": "gray",
    "jet blk mica": "black",
    "saharan sun": "orange",
    "azzuro thetys": "blue",

    "burgan": "brown",
    "saharan stone": "beige",
    "claret mica": "red",
    "imperial jade mica": "green",
    "moon shell mica": "beige",

    "carbon": "gray",
    "cool vanilla": "white",
    "laurel": "green",
    "carmine": "red",
    "windchill": "white",
    "creme brulee": "beige",
    "saharan sun": "orange",
    "beach": "beige",
    "turquoise": "blue",
    "argon": "gray",
    "solar": "yellow",
    "oxford": "blue",
    "liquid carbon m": "gray",
    "mystic": "purple",
    "mountain air": "blue",
    "river 51t": "blue",
    "cutting_edge": "silver",
    "mudbath": "brown",
    "dozer": "yellow",
    "chief": "red",
    "ultraviolet": "purple",
    "night": "black",
    "sonic": "blue",
    "bright_dusk": "orange",
    "limited edition gecko clear": "green",
    "hot lava": "orange",
    "bkack": "black",   # (likely typo of black)
    "sil": "silver",
    "slvery zynith": "silver",
    "mountain air meta": "blue",
    "still_night_pea": "blue",
    "river rock": "gray",
    "mineral": "gray",
    "guard": "green",
    "limited edition reign": "purple",
    "dolomite sil": "silver",
    "arctic": "white",
    "moon": "gray",
    "celistite": "blue",
    "copper": "brown",
    "coppa florio": "brown",
    "parisian night pe": "blue",
    "wjite": "white",   # typo of white
    "camouflage": "green",
    "amethyst": "purple",
    "zircon": "gray",
    "alien": "green",
    "rhino": "gray",
    "brnz": "brown",
    "stone": "gray",
    "tectonic": "gray",
    "mist": "gray",

    "mauve": "purple",
    "radiant re": "red",
    "sea": "blue",
    "urban bamboozle": "green",  
    "brn me": "brown",

    "boulder": "gray",
    "cognac": "brown",
    "parchment": "beige",
    "java": "brown",
    "taupe": "brown",
    "truffle": "brown",
    "coffee": "brown",
    "dark palazzo": "brown",
    "almond": "beige",
    "mocha": "brown",
    "macadamia": "beige",
    "bk": "black",
    "espresso": "brown",
    "baja": "beige",
    "bisque": "beige",
    "nutmeg": "brown",
    "atmosphere": "gray",
    "palomino": "beige",
    "tartufo": "brown",
    "dark atmosphere": "gray",
    "neutral": "beige",
    "umber": "brown",
    "saddle": "brown",
    "natural": "beige",
    "glazed caramel": "beige",
    "ceramic": "beige",
    "kalahari": "beige",
    "acorn": "brown",
    "chateau": "beige",
    "dark galvanized": "gray",
    "roast": "brown",
    "tuscan umber": "brown",
    "flaxen": "beige",
    "camel": "beige",
    "oyster": "beige",
    "light oak": "beige",
    "hickory": "brown",
    "macadamia nulux": "beige",
    "nutmeg fabric": "brown",
    "toffee/cognac/alloy": "brown",
    "macchiato": "beige",
    "cognac sensafin": "brown",
    "dark saddle": "brown",
    "giga amido": "beige",
    "shale": "gray",
    "cocoa": "brown",
    "adobe": "brown",
    "terracotta": "brown",
    "tupelo": "brown",
    "oak": "beige",
    "murillo bwn lth": "brown",
    "greige": "gray",
    "alloy": "gray",
    "chestnut": "brown",
    "caramel": "beige",
    "cocoa/mahogany": "brown",
    "sienna": "brown",
    "medium parchment": "beige",
    "dark palazzo gr": "brown",
    "dark marsala": "brown",
    "parchment mb-tex": "beige",
    "atelier european dark": "brown",

    "amarone": "red",
    "boulder softex-trimmed": "gray",
    "nutmeg softex": "brown",
    "toffee": "brown",
    "orchid": "purple",
    "boulder fa": "gray",
    "boulder fabric": "gray",
    "vk dark palazzo": "brown",
    "palomino semi": "beige",
    "ceramic activex trm sts w/p": "beige",
    "bwn perforated lth": "brown",
    "espresso bwn veganza perf": "brown",
    "cognac/alloy": "brown",
    "pecan": "brown",
    "mojave": "beige",
    "palomino nuluxe with open": "beige",
    "fawn": "beige",
    "cognac w/contrast stitching": "brown",
    "kjb parchment": "beige",
    "boulder softex": "gray",
    "coffee sensafin": "brown",
    "marsala": "red",
    "espresso/cognac": "brown",
    "palomino nuluxe": "beige",
    "sepia": "brown",
    "boulder fabric (fa)": "gray",
    "baja activex": "beige",
    "deep mocha": "brown",
    "boulder": "gray",
    "portobello": "brown",
    "medium flint": "gray",
    "khaki": "beige",
    "tucsan umber": "brown",
    "boulder w sporty b": "gray",
    "cinnamon": "brown",
    "prl bge lth": "beige",
    "oyster": "beige",
    "spicy mocha": "brown",
    "camelback": "beige",
    "parchment lth": "beige",
    "kalahari": "beige",
    "saddle": "brown",
    "taupe": "brown",
    "perf plaid ltr-trm brwn sts": "brown",
    "graph": "gray",
    "cloth": "gray",
    "java int w/norias/mesa lthr": "brown",
    "medium / dark flint": "gray",
    "almond mb-tex": "beige",
    "boulder cloth": "gray",
    "palomino quilted &perfora": "beige",
    "tobacco": "brown",
    "tpb/taupe": "brown",
    "boulder fabric (ff)": "gray",

    "cardamom": "green",
    "eboney": "black",
    "beige": "beige",
    "flint": "gray",
    "birch": "beige",
    "medium earth": "brown",
    "medium dark": "brown",
    "medium dark sla": "brown",
    "smkd trfl lthr": "brown",
    "tuscan umbe": "brown",
    "aspen": "beige",
    "jet balck": "black",
    "harvest": "brown",
    "gy": "gray",

    "gideon": "brown",
    "beige": "beige",
    "teracotta": "brown",
    "biege": "beige",
    "gn": "green",
    "ebny lth-trm sts/miko insrt": "brown",
    "med dk sla": "brown",
    "drk palazzo gre": "gray",
    "sport interior": "gray",

    # White
    "pw7": "white",
    "wz": "white",
    "wy": "white",
    "wy gr": "white",
    "+wy": "white",
    "w1h": "white",
    "glacier": "white",
    "cloud": "white",

    # Black
    "pxj": "black",
    "pxj": "black",
    "pj5 41": "black",
    "41 exterior paint": "black",
    "01u": "black",
    "01u/undergroun": "black",
    "01l7": "black",
    "01l7/undergroun": "black",
    "01l7 undergroun": "black",
    "gxd": "black",
    "gxd": "black",
    "g": "black",
    "um": "black",
    "um": "black",
    "ga": "black",
    "+ga": "black",
    "bm": "black",
    "bm": "black",

    # Gray / Silver
    "slver": "silver",
    "selver": "silver",
    "silver": "silver",
    "ilv": "silver",
    "mgn": "gray",
    "dark matter gra": "gray",
    "gray": "gray",
    "01g3": "gray",
    "01g3/": "gray",
    "01l0": "gray",

    # Blue
    "bule": "blue",
    "lue": "blue",
    "blue": "blue",
    "b": "blue",
    "b-640m": "blue",
    "b-593m": "blue",
    "b-575p": "blue",
    "stratosphere mica": "blue",

    # Red / Maroon
    "r7": "red",
    "r7/b": "red",
    "dr": "red",
    "dr": "red",
    "rn": "red",
    "rn": "red",
    "rurm": "red",
    "dark cherry": "red",
    "plum crazy": "red",
    "plum c": "red",
    "berry": "red",

    # Green
    "jade": "green",
    "spruce mica": "green",
    "gecko clearcoat": "green",

    # Purple
    "murasaki": "purple",

    # Pink
    "pink": "pink",

    # Brown / Beige
    "timberland mica": "brown",
    "dolomite": "brown",
    "earl": "brown",

    # Gray / Black shades
    "anthracite": "gray",
    "med dark slt": "gray",

    # Brown
    "hazel": "brown",
    "russet": "brown",
    "earth": "brown",

    # Green
    "eucalyptus": "green",

    # White / Cream
    "porcelain": "white",
    "creme": "white",
    "rich creme": "white",


    "vanilla": "white",
    "linen": "white",

    # Gray / Silver
    "sliver": "silver",
    "slv": "silver",
    "exterior, sharkskin met-1 (130h)": "gray",
    "iridescent": "gray",
    "vapor": "gray",

    # Blue
    "south pacific pea": "blue",
    "wave maker": "blue",
    "celestial": "blue",
    "provence": "blue",
    "daytona": "blue",

    # Red / Brown
    "marroon": "red",
    "tuscan sun": "red",
    "district": "red",
    "majestic": "red",
    "meteor": "red",

    # Purple / Violet
    "ultra violet": "purple",


    # Brown / Wood tones
    "rustic cedar": "brown",
    "savanna": "brown",

    # Red
    "salsa": "red",

    # Yellow
    "manufaktur pastel yello": "yellow",

    # Gray
    "sharkskin met-1": "gray",


    # Gray / Black shades
    "charco": "gray",
    "dark cosmos": "gray",
    "mood dust": "gray",
    "chrome": "gray",
    
    # Blue
    "denim": "blue",
    "chill": "blue",
    "florett": "blue",

    # Red / Orange
    "punkn": "orange",
    "rock": "red",

    "citrus": "green",

    # Violet
    "violet chromaflair": "violet",

    # Brown / Neutral
    "mythos": "brown",

    "char clth": "black",       # charcoal cloth
    "char lth-appointed": "black", 
    "latte": "beige",
    "parch nv": "beige",
    "parch lthette trim sts": "beige",
    "carmelo trim": "brown",
    "chaparral": "brown",
    "pal": "beige",
    "suede": "grey",            # usually light/neutral suede
    "schottenkaro": "grey", 

    "az": "blue",         # usually Azure / Azul
    "mar": "red",         # often shorthand for Maroon
    "marsh": "green",     # Marsh → earthy green
    "radiant": "red",     # Radiant often used for red finishes
    "celeste": "blue",    # Celeste = sky blue
    "viridian joule": "green",
    "prosecco": "beige",  # champagne/beige tone
    "madeira": "brown",   # deep brown woodlike
    "haz": "brown",       # Hazel
    "avlanache": "white", # Avalanche → white/pearl
    "amp'd": "orange",    # Jeep’s “Amp’d” color
    "eruption": "green",

    "houndstooth": "black",     # interior pattern, usually black/white check  
    "parchm": "beige",          # short for parchment  
    "char lth": "black",        # charcoal leather  
    "ecru": "beige",            # light cream/beige  
    "saffron nappa": "brown",   # saffron leather = warm brown/tan  
    "truff": "brown",           # truffle = dark brown  
    "sun": "yellow",            # sun = yellow/golden tone  
    "ray": "grey", 
}

def extracting_color(col):
    """
    (Function need to be used after the LEVEL-2 cleaning)
    Function takes either Exterior_color and Interior_color col as input and does transformation with help of color_keywords dict

    Returns color category.
    """
    if col is None:
        return np.nan
    else:
        for key,value in color_keywords.items():
            if key in col:
                return value.lower()
        return np.nan

def is_clean_title(row):
    """
    (Function need to be used after the LEVEL-2 cleaning)
    This function checks multiple condition to determine whether title is clean

    Returns True False or np.nan (in case of -> as of now no clean indication of clean_title)
    """
    if row['Clean_title'] == 'Yes':
        return True
    elif row['Clean_title'] == 'No':
        return False
    elif (row['new_used'] == 'New') | (row['new_used'] == 'Certified'): # new car are by default clean_titled and car get certified only if they have clean_title
        return True
    else:
        return np.nan

def is_one_owner(row):
    """
    (Function need to be used after the LEVEL-2 cleaning)
    Function checks whether a car is one_owner,more than one owner or not_owned_yet (new)

    Returns One of the category after checking the conditions
    """
    if row['one_owner_vehicle'] == 'Yes':
        return 'one'
    elif row['one_owner_vehicle'] == 'No':
        return 'more'
    elif row['new_used'] == 'New':
        return 'not_owned_yet'
    else:
        return np.nan

def is_personal_use_only(row):
    """
    (Function need to be used after the LEVEL-2 cleaning)
    Function checks whether a car is personal use only, not_in_use_yet(new) or not personal use only car.

    returns one of category after checking conditions
    """
    if row['Personal_use_only'] == 'Yes':
        return 'yes'
    elif row['Personal_use_only'] == 'No':
        return 'no'
    elif row['new_used'] == 'New':
        return 'not_in_use_yet'
    else:
        return np.nan
    
def has_open_recall(row):
    """
    (Function need to be used after the LEVEL-2 cleaning)
    Function checks whether car have any open recall(s)
    
    returns yes is any else no and np.nan in case of no proper info
    """
    if row['Open_recall'] == 'At least 1 open recall reported':
        return 'yes'
    elif row['new_used'] == 'New':
        return 'not_in_use_yet'
    else:
        return np.nan

word_map = {
    "single": 1,
    "one": 1,
    "double": 2,
    "two": 2,
    "triple": 3,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12
}

def gear_spec_extract(val):
    """
    (Function need to be used after the LEVEL-2 cleaning)
    Function change the number written in words (ten,six, etc) into number
    with help of word_map dict

    returns nan if value is none, returns value from dict if present 
    else simply return the input as it is.

    """
    if val is None:
        return np.nan
    else:
        for key,value in word_map.items():
            if key in val:
                return value
        return val