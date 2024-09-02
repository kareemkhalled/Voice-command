import os
import sys
import json
import uvicorn
import logging
from datetime import datetime
from dotenv import load_dotenv
from line_profiler import profile
from logging.handlers import RotatingFileHandler
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # To resolve the imports

import ems_zeta_voice.db as db
from langchain_openai import ChatOpenAI
from ems_zeta_voice.voice import VoiceHandler
from ems_zeta_voice.aichains import ChainClassifier
from ems_zeta_voice.aichains import DateExtractionChain
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Response, Form
from ems_zeta_voice.config import StationTwoConfigurator, StationFourConfigurator, StationInvConfigurator, StationFiveConfigurator, SuezMedicalComplexConfigurator, CommonConfigurator
    

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = RotatingFileHandler('app.log', maxBytes=1024*1024, backupCount=10)
file_handler.setFormatter(log_formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

db_name = 'stations'
db_uri = "mongodb://root:ZZ4P6ePRfmmL8Z()3aFk@154.176.111.41:27017/"  
station_two_collection = db.connect_to_mongodb(db_uri, db_name, '2')
station_three_collection = db.connect_to_mongodb(db_uri, db_name, '3')
station_four_collection = db.connect_to_mongodb(db_uri, db_name, '4')
station_five_collection = db.connect_to_mongodb(db_uri, db_name, '5')
station_inv_collection = db.connect_to_mongodb(db_uri, db_name, 'sewage-station-investors-ext')
suez_medical_complex_collection = db.connect_to_mongodb(db_uri, db_name,'smc')

voice_handler = VoiceHandler(language="ar")

date_classifier = ChainClassifier(classes=['date', 'no_date'], descriptions="If the input contains date of\
                                            indication to any day ratherthan today return 'date'.\
                                            If date isn't mentioned or asked about today's data return 'no_date'",
                                            llm=ChatOpenAI, llm_kwds={}).init_chain()

date_extraction = DateExtractionChain(date=str(datetime.now().strftime("%Y-%m-%d")), day=str(datetime.now().strftime("%A"))
                                       ,llm=ChatOpenAI, llm_kwds={}).init_chain()

station_classifier = ChainClassifier(classes=['2', '3', '4', '5', 'sewage-station-investors-ext','smc'], 
                                     descriptions="""Return '2' when asking about station two of water station two.
                                     Return '3' when asking about station two of water station three.
                                     Return '4' when asking about station two of water station four.
                                     REturn 'smc' when asking about suez medical complex.
                                     Return '5' when asking about station two of water station five.
                                     Return 'sewage-station-investors-ext' when asking about station
                                     'الامتداد' or 'المستثمرين' of sewage 'الصرف' station two. 
                                     Return 'current' if the station number is not determined in the input""",
                                     llm=ChatOpenAI, llm_kwds={}).init_chain()

station_two_data_mapper = {
    'transformers': StationTwoConfigurator.Home.return_transformers_info,
    'working_transformers': StationTwoConfigurator.Home.return_working_transformers_info,
    'not_working_transformers': StationTwoConfigurator.Home.return_not_working_transformers_info,
    'generator': StationTwoConfigurator.Home.return_generators_info,
    'working_generator': StationTwoConfigurator.Home.return_working_generators_info,
    'not_working_generator': StationTwoConfigurator.Home.return_not_working_generators_info,
    'electrical': StationTwoConfigurator.Home.return_electrical_info,
    'working_electrical': StationTwoConfigurator.Home.return_working_electrical_info,
    'not_working_electrical': StationTwoConfigurator.Home.return_not_working_electrical_info,
    'warnings_status': StationTwoConfigurator.Home.return_system_status_info,
    'working_pumps': StationTwoConfigurator.Home.return_working_pumps_info,
    'pumps': StationTwoConfigurator.Home.return_working_pumps_info,
    'not_working_pumps': StationTwoConfigurator.Home.return_not_working_pumps_info,
    'group_a_pumps': StationTwoConfigurator.Home.return_group_a_pumps_info,
    'group_b_pumps': StationTwoConfigurator.Home.return_group_b_pumps_info,
    'pressure': StationTwoConfigurator.Home.return_pressure_info,
    'flow': StationTwoConfigurator.Home.return_station_flow,
    'flow_l1400_a': StationTwoConfigurator.Home.flow_l1400_a,
    'flow_l1400_b': StationTwoConfigurator.Home.flow_l1400_b,
    'flow_l1000': StationTwoConfigurator.Home.flow_l1000,
    'pressure_l1400_a': StationTwoConfigurator.Home.pressure_l1400_a,
    'pressure_l1400_b': StationTwoConfigurator.Home.pressure_l1400_b,
    'pressure_l1000': StationTwoConfigurator.Home.pressure_l1000,
    'tanks': StationTwoConfigurator.Home.return_tanks_info,
    'tank_1': StationTwoConfigurator.Home.return_tank1_info,
    'tank_2': StationTwoConfigurator.Home.return_tank2_info,
    'sump': StationTwoConfigurator.Home.return_sump_info,
    'report': StationTwoConfigurator.Home.return_station_report,
    'zeeta': CommonConfigurator.zeeta_info,
    'other': CommonConfigurator.return_other_message
}

station_two_classifier = ChainClassifier(
    classes=[
        'transformers', 'working_transformers', 'not_working_transformers',
        'generator', 'working_generator', 'not_working_generator', 'electrical',
        'working_electrical', 'not_working_electrical', 'warnings_status', 
        'working_pumps', 'pumps', 'not_working_pumps', 'group_a_pumps', 
        'group_b_pumps', 'pressure', 'flow', 'flow_l1400_a', 'flow_l1400_b', 
        'flow_l1000', 'pressure_l1400_a', 'pressure_l1400_b', 'pressure_l1000', 
        'tanks', 'tank_1', 'tank_2', 'sump', 'report', 'zeeta', 'other'
    ],
    descriptions="""When asked generally about transformers, return 'transformers'.
                    When asked only about the working or functioning transformers in the station,
                    return 'working_transformers'. Likewise, when asked only about transformers that
                    are not functioning or working, return 'not_working_transformers'.
                    For generators, return 'generator' when asked generally, 'working_generator' when
                    inquiring about working generators, and 'not_working_generator' when specifically 
                    asked about generators that are not working. Similarly, for electrical panels, 
                    return 'electrical' for general inquiries, 'working_electrical' for working panels, 
                    and 'not_working_electrical' for panels that are not working. 
                    When asked about pumps generally return 'pumps'. Return 'working_pumps' for working pumps, 
                    'not_working_pumps' for pumps that are not working, 'group_a_pumps' for pumps in 
                    group A or (ا), and 'group_b_pumps' for pumps in group B or (ب).
                    When asked about tanks generally return 'tanks'. Return 'tank_1' 
                    when asked about the first tank or tank number one, return 'tank_2' 
                    when asked about the second tank or tank number two.
                    Return 'flow' when asked about the water flow rate of the station (معدل التدفق)
                    Return 'flow_l1400_a' when asked about the flow in line 1400a and return 'flow_l1400_b' when asked about 
                    flow in line 1400b, return 'flow_l1000' when asked about flow in line 1000.
                    Return 'sump' when asked about water accumulator (مجمع المياه).
                    Return 'pressure' when asked about the pressure values in general. Return 'pressure_l1400_a'
                    when asked about the pressure in line 1400a, return 'pressure_l1400_b' when asked about 
                    pressure in line 1400b, return 'pressure_l1000' when asked about pressure in line 1000.
                    Return 'warnings_status' when asked about station warnings. Return 'report' when asked about 
                    a report about the station or all station information.
                    Return 'zeeta' when asked about the ems platform or who we are or any details about the system.
                    Return 'other' if you couldn't understand the voice.
                    """,
    llm=ChatOpenAI,
    llm_kwds={}
).init_chain()

station_four_data_mapper = {
    'transformers': StationFourConfigurator.Home.return_transformers_info,
    'working_transformers': StationFourConfigurator.Home.return_working_transformers_info,
    'not_working_transformers': StationFourConfigurator.Home.return_not_working_transformers_info,
    'generator': StationFourConfigurator.Home.return_generators_info,
    'working_generator': StationFourConfigurator.Home.return_working_generators_info,
    'not_working_generator': StationFourConfigurator.Home.return_not_working_generators_info,
    'electrical': StationFourConfigurator.Home.return_electrical_info,
    'working_electrical': StationFourConfigurator.Home.return_working_electrical_info,
    'not_working_electrical': StationFourConfigurator.Home.return_not_working_electrical_info,
    'warnings_status': StationFourConfigurator.Home.return_system_status_info,
    'working_pumps': StationFourConfigurator.Home.return_working_pumps_info,
    'pumps': StationFourConfigurator.Home.return_working_pumps_info,
    'not_working_pumps': StationFourConfigurator.Home.return_not_working_pumps_info,
    'group_a_pumps': StationFourConfigurator.Home.return_group_a_pumps_info,
    'group_b_pumps': StationFourConfigurator.Home.return_group_b_pumps_info,
    'pressure': StationFourConfigurator.Home.return_pressure_info,
    'pressure_1200': StationFourConfigurator.Home.pressure_1200,
    'pressure_1000': StationFourConfigurator.Home.pressure_1000,
    'tanks': StationFourConfigurator.Home.return_tanks_info,
    'tank_1': StationFourConfigurator.Home.return_tank1_info,
    'tank_2': StationFourConfigurator.Home.return_tank2_info,
    'tank_3': StationFourConfigurator.Home.return_tank3_info,
    'hammer2_lvl': StationFourConfigurator.Home.return_hammer2_level_info,
    'flow': StationFourConfigurator.Home.return_station_flow,
    'flow_1200': StationFourConfigurator.Home.flow_1200,
    'flow_1000': StationFourConfigurator.Home.flow_1000,
    'zeeta': CommonConfigurator.zeeta_info,  
    'other': CommonConfigurator.return_other_message
}

station_four_classifier = ChainClassifier(
    classes=[
        'transformers', 'working_transformers', 'not_working_transformers',
        'generator', 'working_generator', 'not_working_generator', 'electrical',
        'working_electrical', 'not_working_electrical', 'warnings_status', 
        'working_pumps', 'pumps', 'not_working_pumps', 'group_a_pumps', 
        'group_b_pumps', 'pressure', 'flow', 'flow_1200', 'flow_1000', 'pressure_1200', 
        'pressure_1000', 'tanks', 'tank_1', 'tank_2', 
        'tank_3', 'hammer1', 'hammer2', 'report', 'zeeta', 'other'
    ],
    descriptions="""When asked generally about transformers, return 'transformers'.
                    When asked only about the working or functioning transformers in the station,
                    return 'working_transformers'. Likewise, when asked only about transformers that
                    are not functioning or working, return 'not_working_transformers'.
                    For generators, return 'generator' when asked generally, 'working_generator' when
                    inquiring about working generators, and 'not_working_generator' when specifically 
                    asked about generators that are not working. Similarly, for electrical panels, 
                    return 'electrical' for general inquiries, 'working_electrical' for working panels, 
                    and 'not_working_electrical' for panels that are not working. 
                    When asked about pumps generally return 'pumps'. Return 'working_pumps' for working pumps, 
                    'not_working_pumps' for pumps that are not working, 'group_a_pumps' for pumps in 
                    group A or (ا), and 'group_b_pumps' for pumps in group B or (ب).
                    When asked about tanks generally return 'tanks'. Return 'tank_1' 
                    when asked about the first tank or tank number one, return 'tank_2' 
                    when asked about the second tank or tank number two and return 'tank_3' 
                    when asked about the third tank or tank number three.
                    Return 'flow' when asked about the water flow rate of the station (معدل التدفق)
                    Return 'flow_1200' when asked about the flow in line 1200 
                    , return 'flow_1000' when asked about flow in line 1000, 
                    Return 'hammer1' when asked about first hammer, return 'hammer2' when asked about the second hammer.
                    Return 'pressure' when asked about the pressure values in general. Return 'pressure_1200'
                    when asked about the pressure in line 1200, return 'pressure_1000' when asked about pressure in line 1000, 
                    Return 'warnings_status' when asked about station warnings. Return 'report' when asked about 
                    a report about the station or all station information.
                    Return 'zeeta' when asked about the ems platform or who we are or any details about the system.
                    Return 'other' if you couldn't understand the voice.
                    """,
    llm=ChatOpenAI,
    llm_kwds={}
).init_chain()

station_five_data_mapper = {'transformers': StationFiveConfigurator.Home.return_transformers_info,
    'working_transformers': StationFiveConfigurator.Home.return_working_transformers_info,
    'not_working_transformers': StationFiveConfigurator.Home.return_not_working_transformers_info,
    'generator': StationFiveConfigurator.Home.return_generators_info,
    'working_generator': StationFiveConfigurator.Home.return_working_generators_info,
    'flow': StationFiveConfigurator.Home.return_station_flow,
    'flow_1200': StationFiveConfigurator.Home.flow_1200,
    'flow_800': StationFiveConfigurator.Home.flow_800,
    'flow_900': StationFiveConfigurator.Home.flow_900,
    'flow_military': StationFiveConfigurator.Home.flow_military,
    'not_working_generator': StationFiveConfigurator.Home.return_not_working_generators_info,
    'electrical': StationFiveConfigurator.Home.return_electrical_info,
    'working_electrical': StationFiveConfigurator.Home.return_working_electrical_info,
    'not_working_electrical': StationFiveConfigurator.Home.return_not_working_electrical_info,
    'warnings_status': StationFiveConfigurator.Home.return_system_status_info,
    'working_pumps': StationFiveConfigurator.Home.return_working_pumps_info,
    'pumps': StationFiveConfigurator.Home.return_working_pumps_info,
    'not_working_pumps': StationFiveConfigurator.Home.return_not_working_pumps_info,
    'group_a_pumps': StationFiveConfigurator.Home.return_group_a_pumps_info,
    'group_b_pumps': StationFiveConfigurator.Home.return_group_b_pumps_info,
    'pressure': StationFiveConfigurator.Home.return_pressure_info,
    'pressure_1200': StationFiveConfigurator.Home.pressure_1200,
    'pressure_900': StationFiveConfigurator.Home.pressure_900,
    'pressure_800': StationFiveConfigurator.Home.pressure_800,
    'tanks': StationFiveConfigurator.Home.return_tanks_info,
    'tank_1': StationFiveConfigurator.Home.return_tank1_info,
    'tank_2': StationFiveConfigurator.Home.return_tank2_info,
    'tank_3': StationFiveConfigurator.Home.return_tank3_info,
    'sump': StationFiveConfigurator.Home.return_sump_info,
    'flow_per_day': StationFiveConfigurator.Home.return_flow_per_day,
    'report': StationFiveConfigurator.Home.return_station_report,
    'zeeta': CommonConfigurator.zeeta_info,  
    'other': CommonConfigurator.return_other_message
}

station_five_classifier = ChainClassifier(classes=['transformers', 'working_transformers', 'not_working_transformers'
                                           , 'generator', 'working_generator', 'not_working_generator', 'electrical'
                                           , 'working_electrical', 'not_working_electrical', 'warnings_status', 'working_pumps', 'pumps'
                                           , 'not_working_pumps', 'group_a_pumps', 'group_b_pumps', 'pressure', 'flow', 'flow_1200', 'flow_800', 'flow_900', 'flow_military'
                                           , 'pressure_1200', 'pressure_900', 'pressure_800', 'tanks', 'tank_1'
                                           , 'tank_2', 'tank_3', 'sump', 'flow_per_day', 'report', 'zeeta', 'other']

                                           , descriptions="""When asked generally about transformers, return 'transformers'.
                                             When asked only about the working or functioning transformers in the station,
                                             return 'working_transformers'. Likewise, when asked only about transformers that
                                             are not functioning or working, return 'not_working_transformers'.
                                             For generators, return 'generator' when asked generally, 'working_generator' when
                                             inquiring about working generators, and 'not_working_generator' when specifically 
                                             asked about generators that are not working. Similarly, for electrical panels, 
                                             return 'electrical' for general inquiries, 'working_electrical' for working panels, 
                                             and 'not_working_electrical' for panels that are not working. 
                                             When asked about pumps generally return 'pumps'. Return 'working_pumps' for working pumps, 
                                             'not_working_pumps' for pumps that are not working, 'group_a_pumps' for pumps in 
                                             group A or (ا), and 'group_b_pumps' for pumps in group B or (ب).
                                             When asked about tanks generally return 'tanks'. Return 'tank_1' 
                                             when asked about the first tank or tank number one, return 'tank_2' 
                                             when asked about the second tank or tank number two and return 'tank_3' 
                                             when asked about the third tank or tank number three.
                                             Return 'flow_per_day' when asked about the quantity of water out of the station in a specific
                                             Return 'flow' when asked about the water flow rate of the station (معدل التدفق)
                                             Return 'flow_1200'when asked about the flow in line 1200 and return 'flow_800' when asked about 
                                             flow in line 800 and return 'flow_900' when asked about flow in line 900.
                                             Return 'sump' when asked about water accumulator (مجمع المياه).
                                             Return 'pressure' when asked about the pressure values in general. Return 'pressure_1200'
                                             when asked about the pressure in line 1200 and return 'pressure_800' when asked about 
                                             pressure in line 800 and return 'pressure_900' when asked about pressure in line 900. 
                                             Return 'warnings_status' when asked about station warnings. Return 'report' when asked about 
                                             a report about the station or all station information.
                                             Return 'zeeta' when asked about the ems platform or who we are or any details about the system.
                                             Return 'other' if you couldn't understand the voice.
                                             """
                                           , llm=ChatOpenAI, llm_kwds={}).init_chain()

station_inv_data_mapper = {
    'transformers': StationInvConfigurator.Home.return_transformers_info,
    'working_transformers': StationInvConfigurator.Home.return_working_transformers_info,
    'not_working_transformers': StationInvConfigurator.Home.return_not_working_transformers_info,
    'generator': StationInvConfigurator.Home.return_generators_info,
    'working_generator': StationInvConfigurator.Home.return_working_generators_info,
    'not_working_generator': StationInvConfigurator.Home.return_not_working_generators_info,
    'electrical': StationInvConfigurator.Home.return_electrical_info,
    'working_electrical': StationInvConfigurator.Home.return_working_electrical_info,
    'not_working_electrical': StationInvConfigurator.Home.return_not_working_electrical_info,
    'warnings_status': StationInvConfigurator.Home.return_system_status_info,
    'working_pumps': StationInvConfigurator.Home.return_working_pumps_info,
    'pumps': StationInvConfigurator.Home.return_pump_info,
    'not_working_pumps': StationInvConfigurator.Home.return_not_working_pumps_info,
    'group_a_pumps': StationInvConfigurator.Home.return_group_a_pumps_info,
    'group_b_pumps': StationInvConfigurator.Home.return_group_b_pumps_info,
    'flow_rate1': StationInvConfigurator.Home.flow_L1,
    'flow_rate2': StationInvConfigurator.Home.flow_L2,
    'pressure1': StationInvConfigurator.Home.pressure_L1,
    'pressure2': StationInvConfigurator.Home.pressure_L2,
    'station_flow_rate': StationInvConfigurator.Home.return_station_flow,
    'sump_a': StationInvConfigurator.Home.return_group_a_sumps_info,
    'sump_b': StationInvConfigurator.Home.return_group_b_sumps_info,
    'report': StationInvConfigurator.Home.return_station_report,
    'zeeta': CommonConfigurator.zeeta_info, 
    'other': CommonConfigurator.return_other_message
}
station_inv_classifier = ChainClassifier(classes=['transformers', 'working_transformers', 'not_working_transformers'
                                , 'generator', 'working_generator', 'not_working_generator', 'electrical'
                                , 'working_electrical', 'not_working_electrical', 'warnings_status', 'working_pumps', 'pumps'
                                , 'not_working_pumps', 'group_a_pumps', 'group_b_pumps', 'flow_rate1', 'flow_rate2', 'pressure1'
                                , 'pressure2', 'station_flow_rate', 'sump_a', 'sump_b', 'report', 'zeeta', 'other']

                                , descriptions="""When asked generally about transformers, return 'transformers'.
                                    When asked only about the working or functioning transformers in the station,
                                    return 'working_transformers'. Likewise, when asked only about transformers that
                                    are not functioning or working, return 'not_working_transformers'.
                                    For generators, return 'generator' when asked generally, 'working_generator' when
                                    inquiring about working generators, and 'not_working_generator' when specifically 
                                    asked about generators that are not working. Similarly, for electrical panels, 
                                    return 'electrical' for general inquiries, 'working_electrical' for working panels, 
                                    and 'not_working_electrical' for panels that are not working. 
                                    When asked about pumps generally return 'pumps'. Return 'working_pumps' for working pumps, 
                                    'not_working_pumps' for pumps that are not working, 'group_a_pumps' for pumps in 
                                    group A or (ا), and 'group_b_pumps' for pumps in group B or (ب).
                                    Return 'station_flow_rate' when asked about the water flow rate of the station (معدل التدفق)
                                    Return 'flow_rate1'when asked about the flow in line 1 and return 'flow_rate2' when asked about 
                                    flow in line 2. Return 'pressure1'when asked about the pressure in line 1 and return 'pressure2' 
                                    when asked about pressure in line 2.
                                    Return 'sump_a' when asked about water accumulator A (مجمع المياه ا), and return
                                    'sump_b' when asked about water accumulator B (مجمع المياه ب)
                                    Return 'warnings_status' when asked about station warnings. Return 'report' when asked about 
                                    a report about the station or all station information.
                                    Return 'zeeta' when asked about the ems platform or who we are or any details about the system.
                                    Return 'other' if you couldn't understand the voice.
                                    """
                                    , llm=ChatOpenAI, llm_kwds={}).init_chain()


suez_medical_complex_classifier = ChainClassifier(
    classes=[
        "date", "Beds_Occupancy_Rate", "Inpatient_Beds_used", "Inpatient_Beds_unused", "ICU_CCU_Beds_used",
          "ICU_CCU_Beds_unused", "Emergency_Beds_used", "Emergency_Beds_Unused", "Incubators_Beds_used", 
          "Incubators_Beds_unused", "Total_Hospital_Beds_used", "Total_Hospital_Beds_unused", "monthlycost_sg", 
          "monthly_water_cost", "monthly_oxygen_cost", "Hospital_Occupancy_Rate", "Clinic_Occupancy_Rate", 
          #update 2
          "Mask_Policy_Violations","Social_Distance_Violations","NuOF_Detected_Falls",
          "transformer_on","transformer_Off","generator_on","generator_off",
          "Elevator_on","Elevator_off","monthly_total_cost","HVAC_alarm","medical_gas_alarm","fire_fighting_alarm",
          "transformer_alarm","elevator_alarm","F_AHU_ON","F_AHU_OFF","chiller_on","chiller_off",
          "monthlyenergy_MVSG","vaccum_press","air_4bar_press","air_7bar_press","oxygen_press",
          "dailyenergy_MVSG","dailyenergy_MVSG_incoming2_energy",
          "dailyenergy_MVSG_incoming3_energy","dailyenergy_Hospital",
          "dailyenergy_Clinics","dailyenergy_Utilities",
          "dailyenergy_ele","dailyenergy_chillers","dailyenergy_AHU",
          "dailyenergy_Boilers","monthlyenergy_MVSG_incoming2_energy",
          "monthlyenergy_MVSG_incoming3_energy",
          "monthlyenergy_Hospital","monthlyenergy_Clinics",
          "monthlyenergy_Utilities","monthlyenergy_ele",
          "monthlyenergy_chillers","monthlyenergy_AHU","monthlyenergy_Boilers",
          "dailycost_sg","yearlyenergy_MVSG",
          "yearlycost_sg","monthlycost_g","monthlycost_f","monthlycost_s",
          "monthlycost_th","monthlycost_roof","monthlycost_Hospital","monthlycost_clinic",
          "monthlycost_Utilities","daily_water_consumption","monthly_water_consumption",
          "daily_water_cost","yearly_water_consumption","yearly_water_cost",
          "daily_oxygen_consumption","monthly_oxygen_consumption","daily_oxygen_cost",
          "yearly_oxygen_consumption","yearly_oxygen_cost","gen1_status",
          "gen1_engine_runtime","gen1_solar","gen1_last_op","gen1_bv","gen1_volt","gen1_curr","gen1_energy",
          "gen1_object_feed1","gen1_object_feed2","gen1_object_feed3","gen1_rated_feed","gen1_estimated_feed_time",
          "chiller1_status","chiller1_supply_temp","chiller1_return_temp","chiller2_status","chiller2_supply_temp",
          "chiller2_return_temp","chiller3_status","chiller3_supply_temp","chiller3_return_temp","chiller4_status",
          "chiller4_supply_temp","chiller4_return_temp","chillers_op_hours","chiller1_op_hours","chiller2_op_hours",
          "chiller3_op_hours","chiller4_op_hours","monthlyenergy_chiller1","monthlyenergy_chiller2","monthlyenergy_chiller3",
          "monthlyenergy_chiller4","in-Patients","out-Patients","chillers_sys_operation_cost","main_return_temp",
          "main_supply_temp","chiller1_maintenance_hours","chiller2_maintenance_hours","chiller3_maintenance_hours","chiller4_maintenance_hours",
          #Update 3
          "daily_index", "yearly_index","monthly_index","random_MVSG_2_energy","random_MVSG_3_energy","updated_at",  "gen2_status", 
          "gen2_engine_runtime", "gen2_solar", "gen2_last_op",  "index","gen2_bv","gen2_volt","gen2_curr","gen2_energy",
           "gen2_object_feed1", "gen2_object_feed2", "gen2_object_feed3","gen2_estimated_feed_time","air_4bar_percentage","air_7bar_percentage"
           "vaccum_percentage","oxygen_percentage", "no_of_surgry_month","no_of_dialysis_month", "no_of_xrays_month","Inpatient_Beds_used_monthly","Inpatient_Beds_unused_monthly",
           "ICU_CCU_Beds_used_monthly","ICU_CCU_Beds_unused_monthly","Emergency_Beds_used_monthly","Emergency_Beds_unused_monthly",
           "Incubators_Beds_unused_monthly", "Incubators_Beds_used_monthly", "no_of_pepole_cam1","no_of_pepole_cam2", "no_of_pepole_cam3", "no_of_pepole_cam4",
           "daily_carbon_foot_print","monthly_carbon_foot_print",
           #ubdate_4 
           "invoices_information"
           'report', 'zeeta', 'other'
          
    ],
    descriptions="""When asked generally about the bed occupancy rate, return 'Beds_Occupancy_Rate'.
                    When asked about the non-Patients usage of beds or Inpatient beds used,
                    return 'Inpatient_Beds_used'. Likewise, when asked about Inpatient beds that are not used, return 'Inpatient_Beds_unused'.
                    When asked about Intensive care unit and Cardiac care unit beds that are used, return 'ICU_CCU_Beds_used' 
                    when asked about Intensive care unit and Cardiac care unit beds that are unused and available, return 'ICU_CCU_Beds_unused' when
                    When asked about Emergency beds that are used or unavailable, return 'Emergency_Beds_used'
                    When asked about Emergency beds that are unsed or available, return 'Emergency_Beds_Unused'
                    When asked about Incubator beds that are used or unavailable, return 'Incubators_Beds_used'
                    When asked about Incubator beds that are unused or available, return 'Incubators_Beds_Unused'
                    When asked generally  about all Hospital beds that are used and unavailable, return 'Total_Hospital_Beds_used'
                    When asked generally  about all Hospital beds that are unused and available, return 'Total_Hospital_Beds_Unused'
                    When asked about the Switch gear monthly costs , return 'monthlycost_sg'. Return 'monthly_water_cost' for Monthly Water Costs, 
                    'monthly_oxygen_cost' for Monthly oxygen costs,
                    When asked about hospital Occupancy rate, return 'Hospital_Occupancy_Rate'. Return 'Clinic_Occupancy_Rate' for Clinic occupancy Rate
                    
                    When asked about the violation of mask wearing policy in the hosbital , return 'Mask_Policy_Violations'
                    When asked about the social distance policy ,return 'Social_Distance_Violations'
                    When asked about the number of falls detecteed in the hospital ,return 'NuOF_Detected_Falls'
                    When asked about  how many transformer is currently switched on ,return 'transformer_on'
                    When asked about  how many transformer is currently switched of ,return 'transformer_Off'
                    When asked about how many the generator is currently on or switched  ,return 'generator_on'
                    When asked about  how many generator is currently not on switched off ,return 'generator_off'
                    When asked about how many  Elevator is currently in opertaion ,return 'Elevator_on'
                    When asked about how manyElevator is currently not in opertaion ,return 'Elevator_of'
                    When asked about the total cost of the whole complex for the month ,return 'monthly_total_cost'
                    When asked about if there is alarm on hvac system ,return 'HVAC_alarm'
                    When asked about if there is alarm on alarms related to medical gass system system  ,return 'medical_gas_alarm'
                    When asked about alarms if there is alarm on related to fire fighting system ,return 'fire_fighting_alarm'
                    When asked about alarms if there is alarm on related to the transformer  ,return 'transformer_alarm'
                    When asked about alarms if there is alarm on related to the elevator ,return 'elevator_alarm'
                    When asked about how many air handling unit switched on ,return 'F_AHU_ON'
                    When asked about the air handling unit switched off ,return 'F_AHU_OFF'
                    When asked about  how many chiller in operation  ,return 'chiller_on'
                    When asked about how many chiller not in operation  ,return 'chiller_off'
                    When asked about the total energy consumption for Medium Voltage switch gear or the whole complex , return 'monthlyenergy_MVSG'
                    When asked about vaccum pressure measurment, return'vaccum_press'
                    When asked about the pressure of 4bar, return 'air_4bar_press'
                    When asked about the pressure of 7bar ,return 'air_7bar_press'
                    When asked about the pressure of oxygen in the system, return 'oxygen_press'
                    When asked about the daily energy consumption for MVSG or the whole complex  return, 'dailyenergy_MVSG'
                    When asked about the incoming 2 daily energy consumption for MVSG return, 'dailyenergy_MVSG_incoming2_energy'
                    When asked about the incoming 3 daily energy consumption for MVSG  return, 'dailyenergy_MVSG_incoming3_energy'
                    When asked about daily energy for the hospital , return 'dailyenergy_Hospital'
                    When asked about the daily energy consumption for the clinc, return 'dailyenergy_Clinics'
                    When asked about the daily energy consumption for the utilities, return 'dailyenergy_Utilities'
                    When asked about the daily energy consumption for electrical system, return 'dailyenergy_ele'
                    When asked about the daily energy consumption for chillers, return 'dailyenergy_chillers'
                    When asked about the daily energy consumption for the Air handling units, return 'dailyenergy_AHU'
                    When asked about the daily energy consumption for  boilers, return 'dailyenergy_Boilers'
                    When asked about the monthly energy consumption from incoming source 2 for MVSG, return 'monthlyenergy_MVSG_incoming2_energy'
                    When asked about the monthly energy consumption from incoming source 3 for MVSG ,return 'monthlyenergy_MVSG_incoming3_energy'
                    When asked about the monthly energy consumption for the hospital, return 'monthlyenergy_Hospital'
                    When asked about the monthly energy consumption for the clinics, return 'monthlyenergy_Clinics'
                    When asked about the monthly energy consumption for  utilities ,return 'monthlyenergy_Utilities'
                    When asked about the monthly energy consumption for electrical system, return 'monthlyenergy_ele'
                    When asked about the monthly energy consumption for chillers , return return 'monthlyenergy_chillers'
                    When asked about the monthly energy consumption for the Air handling units, return 'monthlyenergy_AHU'
                    When asked about the monthly energy consumption for  boilers, return 'monthlyenergy_Boilers'
                    When asked about the daily cost for switch gear or the whole complex ,return 'dailycost_sg'
                    When asked about the yearly energy consumption for MVSG, return 'yearlyenergy_MVSG'
                    When asked about the yearly cost for switch gear, return 'yearlycost_sg'
                    When asked about the monthly cost in the ground floor ,return 'monthlycost_g'
                    When asked about the monthly cost in the first floor, return 'monthlycost_f'
                    When asked about the monthly cost in the second floor, return 'monthlycost_s'
                    When asked about the monthly cost in the third floor, return 'monthlycost_th'
                    When asked about the monthly cost in the roof, return 'monthlycost_roof'
                    When asked about the the monthly cost for the Hospital, return 'monthlycost_Hospital'
                    When asked about the monthly cost for the clinic, return 'monthlycost_clinic'
                    When asked about the monthly cost for the utilities, return 'monthlycost_Utilities'
                    When asked about the daily water consumption, return 'daily_water_consumption'
                    When asked about the monthly water consumption, return 'monthly_water_consumption'
                    When asked about the daily cost of water, return 'daily_water_cost'
                    When asked about the yearly water consumption, return 'yearly_water_consumption'
                    When asked about the yearly cost of water, return 'yearly_water_cost'
                    When asked about the daily oxygen consumption, return 'daily_oxygen_consumption'
                    When asked about the monthly oxygen consumption, return 'monthly_oxygen_consumption'
                    When asked about the daily cost of oxygen, return 'daily_oxygen_cost'
                    When asked about the yearly oxygen consumption ,return 'yearly_oxygen_consumption'
                    When asked about the yearly cost of oxygen ,return 'yearly_oxygen_cost'
                    When asked about the status of generator 1 is on or of ,return 'gen1_status'
                    When asked about the runtime of generator 1 engine,  return 'gen1_engine_runtime'
                    When asked about the solar power input  of generator 1, return 'gen1_solar'
                    When asked about the last opreator time  of generator 1, return 'gen1_last_op'
                    When asked about if generator is ready or not ready of  , return 'gen1_bv'
                    When asked about the voltage of generator 1, return 'gen1_volt'
                    When asked about the current of generator 1 ,return 'gen1_curr'
                    When asked about the energy output of generator 1, return 'gen1_energy'
                    When asked about the object feed of generator 1, return 'gen1_object_feed1'and'gen1_object_feed2'and'gen1_object_feed3'
                    When asked about the rated feed of generator 1, return 'gen1_rated_feed'
                    When asked about the feed time of generator 1,  return 'gen1_estimated_feed_time'
                    When asked about the status of chiller 1,  return 'chiller1_status'
                    When asked about the supply temperature of chiller 1,  return 'chiller1_supply_temp'
                    When asked about the return temperature of chiller 1, return 'chiller1_return_temp'
                    When asked about the status of chiller 2 , return 'chiller2_status'
                    When asked about the supply temperature of chiller 2 ,return 'chiller2_supply_temp'
                    When asked about the return temperature of chiller 2  ,return 'chiller2_return_temp'
                    When asked about the status of chiller 3, return 'chiller3_status'
                    When asked about the supply temperature of chiller 3, return 'chiller3_supply_temp'
                    When asked about the return temperature of chiller 3, return 'chiller3_return_temp'
                    When asked about the status of chiller 4 , return 'chiller4_status'
                    When asked about the supply temperature of chiller 4, return 'chiller4_supply_temp'
                    When asked about the return temperature of chiller 4, return 'chiller4_return_temp'
                    When asked about the operational hours of chillers, return 'chillers_op_hours'
                    When asked about the operational hours of chiller 1, return 'chiller1_op_hours'
                    When asked about the operational hours of chiller 2,  return 'chiller2_op_hours'
                    When asked about the operational hours of chiller 3, return 'chiller3_op_hours'
                    When asked about the operational hours of chiller 4, return 'chiller4_op_hours'
                    When asked about the monthly energy consumption of chiller 1, return 'monthlyenergy_chiller1'
                    When asked about the monthly energy consumption of chiller 2, return 'monthlyenergy_chiller2'
                    When asked about the monthly energy consumption of chiller 3, return 'monthlyenergy_chiller3'
                    When asked about the monthly energy consumption of chiller 4, return 'monthlyenergy_chiller4'
                    When asked about the number of patients that will stay over the night , return 'in-Patients'
                    When asked about the number of number of patients that will leave and not stay over the night, return 'out-Patients'
                    When asked about the operation cost of the chiller system, return 'chillers_sys_operation_cost'
                    When asked about the main return temperature return 'main_return_temp'
                    When asked about the supply temperature, return  'main_supply_temp'
                    When asked about the maintenance hours for chiller 1, return 'chiller1_maintenance_hours'
                    When asked about the maintenance hours for chiller 2, return 'chiller2_maintenance_hours'
                    When asked about the maintenance hours for chiller 3, return 'chiller3_maintenance_hours'
                    When asked about the maintenance hours for chiller 4, return 'chiller4_maintenance_hours'

                    When asked about the Status of generator 2, return 'gen2_status'
                    When asked about the Runtime of generator 2, return 'gen2_engine_runtime'
                    When asked about the solar power input  of generator 2, return 'gen2_solar'
                    When asked about the last opreator time  of generator 2, return 'gen2_last_op'
                    When asked about the  battery voltage if its ready or not ready of generator 2 , return 'gen2_bv'
                    When asked about the voltage of generator 2, return 'gen2_volt'
                    When asked about the current of generator 2 ,return 'gen2_curr'
                    When asked about the energy output of generator 2, return 'gen2_energy'
                    When asked about the object feed of generator 2, return 'gen2_object_feed1' and 'gen2_object_feed2'and gen2_object_feed3'
                    When asked about the feed time of generator 1,  return 'gen1_estimated_feed_time'
                    When asked about the 4 bar air pressure percentage , return air_4bar_percentage'
                    When asked about the 7 bar air pressure percentage , return air_7bar_percentage'
                    When asked about the vaccum pressure percentage , return 'vaccum_percentage'   
                    When asked about the Oxygen pressure percentage , return 'oxygen_percentage'   
                    When asked about the number off surgeries preformed in a month , return 'no_of_surgry_month'  
                    When asked about the number off dialysis operaions preformed in a month , return 'no_of_surgry_month'  
                    When asked about the number of x rays taken in a month, return 'no_of_xrays_month'
                    When asked about the non-Patients usage of beds or Inpatient beds used in a month,
                    return 'Inpatient_Beds_used_monthly'. Likewise, when asked about Inpatient beds that are not used in a month, return 'Inpatient_Beds_unused_monthly'.
                    When asked about Intensive care unit and Cardiac care unit beds that are used in a month, return 'ICU_CCU_Beds_used_monthly' 
                    when asked about Intensive care unit and Cardiac care unit beds that are unused and available in a month, return 'ICU_CCU_Beds_unused_monthly' when
                    When asked about Emergency beds that are used or unavailable in a month, return 'Emergency_Beds_used_monthly'
                    When asked about Emergency beds that are unsed or available in a month, return 'Emergency_Beds_Unused_monthly'
                    When asked about Incubator beds that are used or unavailable in a monh, return 'Incubators_Beds_used_monthly'
                    When asked about Incubator beds that are unused or available in a month, return 'Incubators_Beds_Unused_monthly'                    
                    When asked about number of people seen by camera 1, return 'no_of_pepole_cam1'
                    When asked about number of people seen by camera 2, return 'no_of_pepole_cam2'
                    When asked about number of people seen by camera 3, return 'no_of_pepole_cam3'
                    When asked about number of people seen by camera 4, return 'no_of_pepole_cam4'
                    When asked about daily carbon footprint across the whole complex, return'daily_carbon_foot_print'
                    When asked about Monthly carbon footprint across the whole complex, return'monthly_carbon_foot_print'


                    when asked about invoices information,return 'invoices_information'







                    Return 'report' when asked about a report about the The complex information.
                    """,
    llm=ChatOpenAI,
    llm_kwds={}
).init_chain()

suez_medical_complex_mapper = {
    'Beds_Occupancy_Rate': SuezMedicalComplexConfigurator.Home.return_Beds_occupancy_rate_info,
    'Inpatient_Beds_used': SuezMedicalComplexConfigurator.Home.return_Inpatient_Beds_used_info,
    'Inpatient_Beds_Unused': SuezMedicalComplexConfigurator.Home.return_Inpatient_Beds_Unused_info,
    'ICU_CCU_Beds_used': SuezMedicalComplexConfigurator.Home.return_ICU_CCU_Beds_used_info,
    'ICU_CCU_Beds_Unused': SuezMedicalComplexConfigurator.Home.return_ICU_CCU_Beds_Unused_info,
    'Emergency_Beds_used': SuezMedicalComplexConfigurator.Home.return_Emergency_Beds_used_info,
    'Emergency_Beds_Unused': SuezMedicalComplexConfigurator.Home.return_Emergency_Beds_Unused_info,
    'Incubators_Beds_used': SuezMedicalComplexConfigurator.Home.return_Incubators_Beds_used_info,
    'Incubators_Beds_unused': SuezMedicalComplexConfigurator.Home.return_Incubators_Beds_unused_info,
    'Total_Hospital_Beds_used': SuezMedicalComplexConfigurator.Home.return_Total_Hospital_Beds_used_info,
    'Total_Hospital_Beds_unused': SuezMedicalComplexConfigurator.Home.return_Total_Hospital_Beds_unused_info,
    'monthlycost_sg': SuezMedicalComplexConfigurator.Home.return_monthlycost_sg_info,
    'monthly_water_cost': SuezMedicalComplexConfigurator.Home.return_monthly_water_cost_info,
    'monthly_oxygen_cost': SuezMedicalComplexConfigurator.Home.return_monthly_oxygen_cost_info,
    'Hospital_Occupancy_Rate': SuezMedicalComplexConfigurator.Home.return_Hospital_Occupancy_Rate_info,
    'Clinic_Occupancy_Rate': SuezMedicalComplexConfigurator.Home.return_Clinic_Occupancy_Rate_info,
    #update 2
    'Mask_Policy_Violations': SuezMedicalComplexConfigurator.Home.Mask_Policy_Violations_info,
    'Social_Distance_Violations': SuezMedicalComplexConfigurator.Home.Social_Distance_Violations_info,
    'NuOF_Detected_Falls': SuezMedicalComplexConfigurator.Home.NuOF_Detected_Falls_info,
    'transformer_on': SuezMedicalComplexConfigurator.Home.transformer_on_info,
    'transformer_Off': SuezMedicalComplexConfigurator.Home.transformer_Off_info,
    'generator_on': SuezMedicalComplexConfigurator.Home.generator_on_info,
    'generator_off': SuezMedicalComplexConfigurator.Home.generator_off_info,
    'Elevator_on': SuezMedicalComplexConfigurator.Home.Elevator_on_info,
    'Elevator_off': SuezMedicalComplexConfigurator.Home.Elevator_off_info,
    'monthly_total_cost': SuezMedicalComplexConfigurator.Home.monthly_total_cost_info,
    'HVAC_alarm': SuezMedicalComplexConfigurator.Home.HVAC_alarm_info,
    'medical_gas_alarm': SuezMedicalComplexConfigurator.Home.medical_gas_alarm_info,
    'fire_fighting_alarm': SuezMedicalComplexConfigurator.Home.fire_fighting_alarm_info,
    'transformer_alarm': SuezMedicalComplexConfigurator.Home.transformer_alarm_info,
    'elevator_alarm': SuezMedicalComplexConfigurator.Home.elevator_alarm_info,
    'F_AHU_ON': SuezMedicalComplexConfigurator.Home.F_AHU_ON_info,
    'F_AHU_OFF': SuezMedicalComplexConfigurator.Home.F_AHU_OFF_info,
    'chiller_on': SuezMedicalComplexConfigurator.Home.chiller_on_info,
    'chiller_off': SuezMedicalComplexConfigurator.Home.chiller_off_info,
    'monthlyenergy_MVSG': SuezMedicalComplexConfigurator.Home.monthlyenergy_MVSG_info,
    'vaccum_press': SuezMedicalComplexConfigurator.Home.vaccum_press_info,
    'air_4bar_press': SuezMedicalComplexConfigurator.Home.air_4bar_press_info,
    'air_7bar_press': SuezMedicalComplexConfigurator.Home.air_7bar_press_info,
    'oxygen_press': SuezMedicalComplexConfigurator.Home.oxygen_press_info,
    'dailyenergy_MVSG': SuezMedicalComplexConfigurator.Home.dailyenergy_MVSG_info,
    'dailyenergy_MVSG_incoming2_energy': SuezMedicalComplexConfigurator.Home.dailyenergy_MVSG_incoming2_energy_info,
    'dailyenergy_MVSG_incoming3_energy': SuezMedicalComplexConfigurator.Home.dailyenergy_MVSG_incoming3_energy_info,
    'dailyenergy_Hospital': SuezMedicalComplexConfigurator.Home.dailyenergy_Hospital_info,
    'dailyenergy_Clinics': SuezMedicalComplexConfigurator.Home.dailyenergy_Clinics_info,
    'dailyenergy_Utilities': SuezMedicalComplexConfigurator.Home.dailyenergy_Utilities_info,
    'dailyenergy_ele': SuezMedicalComplexConfigurator.Home.dailyenergy_ele_info,
    'dailyenergy_chillers': SuezMedicalComplexConfigurator.Home.dailyenergy_chillers_info,
    'dailyenergy_AHU': SuezMedicalComplexConfigurator.Home.dailyenergy_AHU_info,
    'dailyenergy_Boilers': SuezMedicalComplexConfigurator.Home.dailyenergy_Boilers_info,
    'monthlyenergy_MVSG_incoming2_energy': SuezMedicalComplexConfigurator.Home.monthlyenergy_MVSG_incoming2_energy_info,
    'monthlyenergy_MVSG_incoming3_energy': SuezMedicalComplexConfigurator.Home.monthlyenergy_MVSG_incoming3_energy_info,
    'monthlyenergy_Hospital': SuezMedicalComplexConfigurator.Home.monthlyenergy_Hospital_info,
    'monthlyenergy_Clinics': SuezMedicalComplexConfigurator.Home.monthlyenergy_Clinics_info,
    'monthlyenergy_Utilities': SuezMedicalComplexConfigurator.Home.monthlyenergy_Utilities_info,
    'monthlyenergy_ele': SuezMedicalComplexConfigurator.Home.monthlyenergy_ele_info,
    'monthlyenergy_chillers': SuezMedicalComplexConfigurator.Home.monthlyenergy_chillers_info,
    'monthlyenergy_AHU': SuezMedicalComplexConfigurator.Home.monthlyenergy_AHU_info,
    'monthlyenergy_Boilers': SuezMedicalComplexConfigurator.Home.monthlyenergy_Boilers_info,
    'dailycost_sg': SuezMedicalComplexConfigurator.Home.dailycost_sg_info,
    'yearlyenergy_MVSG': SuezMedicalComplexConfigurator.Home.yearlyenergy_MVSG_info,
    'yearlycost_sg': SuezMedicalComplexConfigurator.Home.yearlycost_sg_info,
    'monthlycost_g': SuezMedicalComplexConfigurator.Home.monthlycost_g_info,
    'monthlycost_f': SuezMedicalComplexConfigurator.Home.monthlycost_f_info,
    'monthlycost_s': SuezMedicalComplexConfigurator.Home.monthlycost_s_info,
    'monthlycost_th': SuezMedicalComplexConfigurator.Home.monthlycost_th_info,
    'monthlycost_roof': SuezMedicalComplexConfigurator.Home.monthlycost_roof_info,
    'monthlycost_Hospital': SuezMedicalComplexConfigurator.Home.monthlycost_Hospital_info,
    'monthlycost_clinic': SuezMedicalComplexConfigurator.Home.monthlycost_clinic_info,
    'monthlycost_Utilities': SuezMedicalComplexConfigurator.Home.monthlycost_Utilities_info,
    'daily_water_consumption': SuezMedicalComplexConfigurator.Home.daily_water_consumption_info,
    'monthly_water_consumption': SuezMedicalComplexConfigurator.Home.monthly_water_consumption_info,
    'daily_water_cost': SuezMedicalComplexConfigurator.Home.daily_water_cost_info,
    'yearly_water_consumption': SuezMedicalComplexConfigurator.Home.yearly_water_consumption_info,
    'yearly_water_cost': SuezMedicalComplexConfigurator.Home.yearly_water_cost_info,
    'daily_oxygen_consumption': SuezMedicalComplexConfigurator.Home.daily_oxygen_consumption_info,
    'monthly_oxygen_consumption': SuezMedicalComplexConfigurator.Home.monthly_oxygen_consumption_info,
    'daily_oxygen_cost': SuezMedicalComplexConfigurator.Home.daily_oxygen_cost_info,
    'yearly_oxygen_consumption': SuezMedicalComplexConfigurator.Home.yearly_oxygen_consumption_info,
    'yearly_oxygen_cost': SuezMedicalComplexConfigurator.Home.yearly_oxygen_cost_info,
    'gen1_status': SuezMedicalComplexConfigurator.Home.gen1_status_info,
    'gen1_engine_runtime': SuezMedicalComplexConfigurator.Home.gen1_engine_runtime_info,
    'gen1_solar': SuezMedicalComplexConfigurator.Home.gen1_solar_info,
    'gen1_last_op': SuezMedicalComplexConfigurator.Home.gen1_last_op_info,
    'gen1_bv': SuezMedicalComplexConfigurator.Home.gen1_bv_info,
    'gen1_volt': SuezMedicalComplexConfigurator.Home.gen1_volt_info,
    'gen1_curr': SuezMedicalComplexConfigurator.Home.gen1_curr_info,
    'gen1_energy': SuezMedicalComplexConfigurator.Home.gen1_energy_info,
    'gen1_object_feed1': SuezMedicalComplexConfigurator.Home.gen1_object_feed1_info,
    'gen1_object_feed2': SuezMedicalComplexConfigurator.Home.gen1_object_feed2_info,
    'gen1_object_feed3': SuezMedicalComplexConfigurator.Home.gen1_object_feed3_info,
    'gen1_rated_feed': SuezMedicalComplexConfigurator.Home.gen1_rated_feed_info,
    'gen1_estimated_feed_time': SuezMedicalComplexConfigurator.Home.gen1_estimated_feed_time_info,
    'chiller1_status': SuezMedicalComplexConfigurator.Home.chiller1_status_info,
    'chiller1_supply_temp': SuezMedicalComplexConfigurator.Home.chiller1_supply_temp_info,
    # 'chiller1_temp': SuezMedicalComplexConfigurator.Home.chiller1_temp_info,
    'chiller2_status': SuezMedicalComplexConfigurator.Home.chiller2_status_info,
    'chiller2_supply_temp': SuezMedicalComplexConfigurator.Home.chiller2_supply_temp_info,
    # 'chiller2_temp': SuezMedicalComplexConfigurator.Home.chiller2_temp_info,
    'chiller3_status': SuezMedicalComplexConfigurator.Home.chiller3_status_info,
    'chiller3_supply_temp': SuezMedicalComplexConfigurator.Home.chiller3_supply_temp_info,
    # 'chiller3_temp': SuezMedicalComplexConfigurator.Home.chiller3_temp_info,
    'chiller4_status': SuezMedicalComplexConfigurator.Home.chiller4_status_info,
    'chiller4_supply_temp': SuezMedicalComplexConfigurator.Home.chiller4_supply_temp_info,
    # 'chiller4_temp': SuezMedicalComplexConfigurator.Home.chiller4_temp_info,
    'chillers_op_hours': SuezMedicalComplexConfigurator.Home.chillers_op_hours_info,
    'chiller1_op_hours': SuezMedicalComplexConfigurator.Home.chiller1_op_hours_info,
    'chiller2_op_hours': SuezMedicalComplexConfigurator.Home.chiller2_op_hours_info,
    'chiller3_op_hours': SuezMedicalComplexConfigurator.Home.chiller3_op_hours_info,
    'chiller4_op_hours': SuezMedicalComplexConfigurator.Home.chiller4_op_hours_info,
    'monthlyenergy_chiller1': SuezMedicalComplexConfigurator.Home.monthlyenergy_chiller1_info,
    'monthlyenergy_chiller2': SuezMedicalComplexConfigurator.Home.monthlyenergy_chiller2_info,
    'monthlyenergy_chiller3': SuezMedicalComplexConfigurator.Home.monthlyenergy_chiller3_info,
    'monthlyenergy_chiller4': SuezMedicalComplexConfigurator.Home.monthlyenergy_chiller4_info,
    'in-Patients': SuezMedicalComplexConfigurator.Home.in_Patients_info,
    'out-Patients': SuezMedicalComplexConfigurator.Home.out_Patients_info,
    'chillers_sys_operation_cost': SuezMedicalComplexConfigurator.Home.chillers_sys_operation_cost_info,
    'main_temp': SuezMedicalComplexConfigurator.Home.main_temp_info,
    'main_supply_temp': SuezMedicalComplexConfigurator.Home.main_supply_temp_info,
    'chiller1_maintenance_hours': SuezMedicalComplexConfigurator.Home.chiller1_maintenance_hours_info,
    'chiller2_maintenance_hours': SuezMedicalComplexConfigurator.Home.chiller2_maintenance_hours_info,
    'chiller3_maintenance_hours': SuezMedicalComplexConfigurator.Home.chiller3_maintenance_hours_info,
    'chiller4_maintenance_hours': SuezMedicalComplexConfigurator.Home.chiller4_maintenance_hours_info,
    #Update 3
    'daily_index': SuezMedicalComplexConfigurator.Home.daily_index_info,
    'yearly_index': SuezMedicalComplexConfigurator.Home.yearly_index_info,
    'monthly_index': SuezMedicalComplexConfigurator.Home.monthly_index_info,
    'random_MVSG_2_energy': SuezMedicalComplexConfigurator.Home.random_MVSG_2_energy_info,
    'random_MVSG_3_energy': SuezMedicalComplexConfigurator.Home.chiller4_maintenance_hours_info,
    'updated_at': SuezMedicalComplexConfigurator.Home.updated_at_info,
    'gen2_status': SuezMedicalComplexConfigurator.Home.gen2_status_info,
    'gen2_engine_runtime': SuezMedicalComplexConfigurator.Home.gen2_engine_runtime_info,
    'gen2_solar': SuezMedicalComplexConfigurator.Home.gen2_solar_info,
    'gen2_last_op': SuezMedicalComplexConfigurator.Home.gen2_last_op_info,
    # 'index': SuezMedicalComplexConfigurator.Home.index_info,
    'gen2_bv': SuezMedicalComplexConfigurator.Home.gen2_bv_info,
    'gen2_volt': SuezMedicalComplexConfigurator.Home.gen2_volt_info,
    'gen2_curr': SuezMedicalComplexConfigurator.Home.gen2_curr_info,
    'gen2_energy': SuezMedicalComplexConfigurator.Home.gen2_energy_info,
    'gen2_object_feed1': SuezMedicalComplexConfigurator.Home.gen2_object_feed1_info,
    'gen2_object_feed2': SuezMedicalComplexConfigurator.Home.gen2_object_feed2_info,
    'gen2_object_feed3': SuezMedicalComplexConfigurator.Home.gen2_object_feed3_info,
    'gen2_estimated_feed_time': SuezMedicalComplexConfigurator.Home.gen2_estimated_feed_time_info,
    'air_4bar_percentage': SuezMedicalComplexConfigurator.Home.air_4bar_percentage_info,
    'air_7bar_percentage': SuezMedicalComplexConfigurator.Home.air_7bar_percentage_info,
    'vaccum_percentage': SuezMedicalComplexConfigurator.Home.vaccum_percentage_info,
    'oxygen_percentage': SuezMedicalComplexConfigurator.Home.oxygen_percentage_info,
    'no_of_surgry_month': SuezMedicalComplexConfigurator.Home.no_of_surgry_month_info,
    'no_of_dialysis_month': SuezMedicalComplexConfigurator.Home.no_of_dialysis_month_info,
    'no_of_xrays_month': SuezMedicalComplexConfigurator.Home.no_of_xrays_month_info,
    'Inpatient_Beds_used_monthly': SuezMedicalComplexConfigurator.Home.Inpatient_Beds_used_monthly_info,
    'Inpatient_Beds_unused_monthly': SuezMedicalComplexConfigurator.Home.Inpatient_Beds_unused_monthly_info,
    'ICU_CCU_Beds_used_monthly': SuezMedicalComplexConfigurator.Home.ICU_CCU_Beds_used_monthly_info,
    'ICU_CCU_Beds_unused_monthly': SuezMedicalComplexConfigurator.Home.ICU_CCU_Beds_unused_monthly_info,
    'Emergency_Beds_used_monthly': SuezMedicalComplexConfigurator.Home.Emergency_Beds_used_monthly_info,
    'Emergency_Beds_unused_monthly': SuezMedicalComplexConfigurator.Home.Emergency_Beds_unused_monthly_info,
    'Incubators_Beds_unused_monthly': SuezMedicalComplexConfigurator.Home.Incubators_Beds_unused_monthly_info,
    'Incubators_Beds_used_monthly': SuezMedicalComplexConfigurator.Home.Incubators_Beds_used_monthly_info,
    'no_of_pepole_cam1': SuezMedicalComplexConfigurator.Home.no_of_pepole_cam1_info,
    'no_of_pepole_cam2': SuezMedicalComplexConfigurator.Home.no_of_pepole_cam2_info,
    'no_of_pepole_cam3': SuezMedicalComplexConfigurator.Home.no_of_pepole_cam3_info,
    'no_of_pepole_cam4': SuezMedicalComplexConfigurator.Home.no_of_pepole_cam4_info,
    'daily_carbon_foot_print': SuezMedicalComplexConfigurator.Home.daily_carbon_foot_print_info,
    'monthly_carbon_foot_print': SuezMedicalComplexConfigurator.Home.monthly_carbon_foot_print_info,

    
    'invoices_information' :SuezMedicalComplexConfigurator.Home.invoices_information_info,
    


    'report': SuezMedicalComplexConfigurator.Home.return_complex_report_info,
    'zeeta': CommonConfigurator.zeeta_info, 
    'other': CommonConfigurator.return_other_message

}

id_classifiers_mapper = {
    'smc': [suez_medical_complex_mapper, suez_medical_complex_classifier],
    '2': [station_two_data_mapper, station_two_classifier],
    '4': [station_four_data_mapper, station_four_classifier],
    '5': [station_five_data_mapper, station_five_classifier],
    'sewage-station-investors-ext': [station_inv_data_mapper, station_inv_classifier]
}

id_collections_mapper = {
    'smc': suez_medical_complex_collection,
    '2': station_two_collection,
    '4': station_four_collection,
    '5': station_five_collection,
    'sewage-station-investors-ext': station_inv_collection
}

@profile
async def suez_request_handler(complex_data, voice_file):
    complex_data = json.loads(complex_data)
    transcript = await voice_handler.speech_to_text(audio_file=voice_file.file)
    print(transcript)
    dated_request = await date_classifier.ainvoke({'input': transcript})
    dated_request = ''.join(e for e in dated_request if e.isalnum() or e == '_')    
    if dated_request == 'date':
        dates = await date_extraction.ainvoke({'input': transcript})
        print(dates)
        start_date = dates.get('start_date', str(datetime.now().strftime("%Y-%m-%d")))
        collection = suez_medical_complex_collection
        if dates.get('end_date') == None:
            end_date = start_date
        else:
            end_date = dates.get('end_date')
        print("Data collection is: ", collection)
        complex_data = db.calculate_sums(db.get_documents_between_dates(collection, start_date, end_date))
    else:
        complex_data = complex_data
    
    classifier = suez_medical_complex_classifier
    selected_data = await classifier.ainvoke({'input': transcript})
    selected_data = ''.join(e for e in selected_data if e.isalnum() or e == '_')
    print(selected_data)
    output_text = suez_medical_complex_mapper[selected_data](complex_data)
    print(output_text)
    if dated_request == 'date':
        _, audio_data = await voice_handler.text_to_speech(text_data = "المعلومات التالية في الفترة الزمنية المطلوبة " + output_text + "\n شكرا لاستخدامك منصة زِيتَا \n")
    else:
        _, audio_data = await voice_handler.text_to_speech(text_data = output_text + "\n شكرا لاستخدامك منصة زِيتَا \n")
    os.remove(_)
    return audio_data

@profile
async def request_handler(stations_data, voice_file):
    payload = json.loads(stations_data)
    current_station_id = payload.get("current_index")
    stations_data = payload.get("stations_data", {})
    transcript = await voice_handler.speech_to_text(audio_file=voice_file.file)
    print(transcript)
    station_id = await station_classifier.ainvoke({'input': transcript})
    station_id = ''.join(e for e in station_id if e.isalnum() or e == '-')
    if station_id == 'current':
        station_id = current_station_id

    print("STATION IS: ", station_id)
    dated_request = await date_classifier.ainvoke({'input': transcript})
    dated_request = ''.join(e for e in dated_request if e.isalnum() or e == '_')    
    if dated_request == 'date':
        dates = await date_extraction.ainvoke({'input': transcript})
        print(dates)
        start_date = dates.get('start_date', str(datetime.now().strftime("%Y-%m-%d")))
        collection = id_collections_mapper[station_id]
        if dates.get('end_date') == None:
            end_date = start_date
        else:
            end_date = dates.get('end_date')
        print("Data collection is: ", collection)
        station_data = db.get_last_document_for_date(collection, start_date)
    else:
        station_data = stations_data.get(station_id, None)
    print(station_data)
    
    mapper = id_classifiers_mapper[station_id][0]
    classifier = id_classifiers_mapper[station_id][1]
    selected_data = await classifier.ainvoke({'input': transcript})
    selected_data = ''.join(e for e in selected_data if e.isalnum() or e == '_')
    print(selected_data)
    output_text = mapper[selected_data](station_data)
    if dated_request == 'date':
        _, audio_data = await voice_handler.text_to_speech(text_data = "المعلومات التالية في الفترة الزمنية المطلوبة " + output_text + "\n شكرا لاستخدامك منصة زِيتَا \n")
    else:
        _, audio_data = await voice_handler.text_to_speech(text_data = output_text + "\n شكرا لاستخدامك منصة زِيتَا \n")
    os.remove(_)
    return audio_data


@app.post("/voice/main")
async def voice_endpoint(upload_file: UploadFile = File(...), stations_data: str = Form(...)):
    audio_data = await request_handler(stations_data, upload_file) 
    return Response(content=audio_data, media_type="audio/mp3")

@app.post("/voice/suez")
async def voice_endpoint(upload_file: UploadFile = File(...), complex_data: str = Form(...)):
    audio_data = await suez_request_handler(complex_data, upload_file) 
    return Response(content=audio_data, media_type="audio/mp3")

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
    