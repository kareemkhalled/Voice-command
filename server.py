import os
import sys
import json
import uvicorn
import logging
import argparse
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
# Parse command-line arguments for mode
parser = argparse.ArgumentParser(description="Run the voice handler service with specified mode.")
parser.add_argument("--mode", type=str, default="original", choices=["original", "openai"], help="Select the mode to use: original or openai")
args = parser.parse_args()

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

db_name = 'stations'
db_uri = "mongodb://root:ZZ4P6ePRfmmL8Z()3aFk@localhost:27017/"  
station_two_collection = db.connect_to_mongodb(db_uri, db_name, '2')
station_three_collection = db.connect_to_mongodb(db_uri, db_name, '3')
station_four_collection = db.connect_to_mongodb(db_uri, db_name, '4')
station_five_collection = db.connect_to_mongodb(db_uri, db_name, '5')
station_inv_collection = db.connect_to_mongodb(db_uri, db_name, 'sewage-station-investors-ext')
suez_medical_complex_collection = db.connect_to_mongodb(db_uri,db_name, 'smc')

voice_handler = VoiceHandler(language="ar", mode=args.mode)

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
         "any_alarm","date", "complex_Occupancy_Rate", "Inpatient_Beds_used", "Inpatient_Beds_unused", "ICU_CCU_Beds_used",
          "ICU_CCU_Beds_unused", "Emergency_Beds_used", "Emergency_Beds_Unused", "Incubators_Beds_used", 
          "Incubators_Beds_unused", "Total_Hospital_Beds_used", "Total_Hospital_Beds_unused", "monthlycost_sg", 
          "monthly_water_cost","daily_water_cost_hospital", "monthly_oxygen_cost", "Hospital_Occupancy_Rate", "Clinic_Occupancy_Rate", "monthly_gas_system", "carbon_foot_Hospital", "carbon_foot_Clinics", "carbon_foot_Utilites",
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
          "monthlyenergy_chiller4","in_Patients","out_Patients","chillers_sys_operation_cost","main_return_temp",
          "main_supply_temp","chiller1_maintenance_hours","chiller2_maintenance_hours","chiller3_maintenance_hours","chiller4_maintenance_hours",
          #Update 3
          "daily_index", "yearly_index","monthly_index","random_MVSG_2_energy","random_MVSG_3_energy","updated_at",  "gen2_status", 
          "gen2_engine_runtime", "gen2_solar", "gen2_last_op",  "index","gen2_bv","gen2_volt","gen2_curr","gen2_energy",
           "gen2_object_feed1", "gen2_object_feed2", "gen2_object_feed3","gen2_estimated_feed_time","air_4bar_percentage","air_7bar_percentage"
           "vaccum_percentage","oxygen_percentage", "no_of_surgry_month","no_of_dialysis_month", "no_of_xrays_month","Inpatient_Beds_used_monthly","Inpatient_Beds_unused_monthly",
           "ICU_CCU_Beds_used_monthly","ICU_CCU_Beds_unused_monthly","Emergency_Beds_used_monthly","Emergency_Beds_unused_monthly",
           "Incubators_Beds_unused_monthly", "Incubators_Beds_used_monthly", "no_of_pepole_cam1","no_of_pepole_cam2", "no_of_pepole_cam3", "no_of_pepole_cam4",
           "daily_carbon_foot_print","out_Patients_hospital","monthlyenergy_cost_hospital","monthlyenergy_Hospital_GF","monthly_water_cost_hospital","monthly_water_consumption_hospital","monthly_oxygen_cost_hospital",
           "monthly_oxygen_consumption_hospital","in_Patients_hospital","dailyenergy_Hospital_GF","dailyenergy_Hospital_cost","daily_water_consumption_hospital","monthly_carbon_foot_print","daily_oxygen_cost_hospital",
           "daily_oxygen_consumption_hospital" ,"invoices_information" ,"temp_outside","temp_inside","total_complex_doctor","total_complex_staff","total_complex_nurse",
           #groundfloor ubdate
           "in_patients_GF","out_patients_GF","monthlyenergy_g","energy_dental_xray","cost_dental_xray","energy_radiology_lab","cost_radiology_lab",
           "energy_bio_tanks","cost_bio_tanks","energy_triage","cost_triage","energy_administration","cost_administration","carbon_foot_print_GF",

           #boilers ubdate
           "Hospital_Boiler_1_Status","Hospital_Boiler_1_Alarm","Hospital_Boiler_1_Hot_Water_Temperature","Hospital_Boiler_1_BC_Sequence_Time",
           ,"Hospital_Boiler_1_Operation_Time","Hospital_Boiler_1_Hot_Water_Volume",
           "Hospital_Boiler_1_Gas_Consumption_Month","Hospital_Boiler_1_Gas_Invoice_Month",
           "Hospital_Boiler_2_Status","Hospital_Boiler_2_Alarm","Hospital_Boiler_2_Hot_Water_Temperature"
           ,"Hospital_Boiler_2_BC_Sequence_Time","Hospital_Boiler_2_Operation_Time","Hospital_Boiler_2_Hot_Water_Volume",
           "Hospital_Boiler_2_Gas_Consumption_Month","Hospital_Boiler_2_Gas_Invoice_Month",
           "Primary_Pump_1_Status","Primary_Pump_2_Status","Primary_Pump_3_Status",
           "secondry_Pump_1_Status","secondry_Pump_2_Status","secondry_Pump_3_Status",

           
           
           ,'report', 'zeeta', 'other'

          


    ],
    descriptions="""عند السؤال بشكل عام عن نسبة الاشغال الشهري في المجمع او  نِسْبَةِ الاشْغَالِ الشَّهْرِي فِي الْمُجَمَّعِ ، ارجع 'complex_Occupancy_Rate'.  
            عند السؤال هل يوجود إنذار او تنبيه في اي نظام في المجمع او  هَلْ يُوجَدُ إِنْذَارٌ أَوْ تَنْبِيهٌ فِي أَيِّ نِظَامٍ فِي الْمُجَمَّعِ ، ارجع 'any_alarm'.  
            عند السؤال عن البصمه الكربونيه اليوميه للمستشفي او  الْبَصْمَةِ الْكَرْبُونِيَّةِ الْيَوْمِيَّةِ لِلْمُسْتَشْفَى ، ارجع 'carbon_foot_Hospital'.  
            عند السؤال عن البصمه الكربونيه اليوميه للطابق الارضي للمستشفي او  الْبَصْمَةِ الْكَرْبُونِيَّةِ الْيَوْمِيَّةِ للطابق الارضي للمستشفي ، ارجع 'carbon_foot_print_GF'.  
            عند السؤال عن البصمه الكربونيه اليوميه للاماكن الخدميه او  الْبَصْمَةِ الْكَرْبُونِيَّةِ الْيَوْمِيَّةِ لِلْأَمَاكِنِ الْخِدْمِيَّةِ ، ارجع 'carbon_foot_Utilites'.  
            عند السؤال عن البصمه الكربونيه اليوميه للعيادات او  الْبَصْمَةِ الْكَرْبُونِيَّةِ الْيَوْمِيَّةِ لِلْعِيَادَاتِ ، ارجع 'carbon_foot_Clinics'.  
            عند السؤال عن عدد المرضي المقيمين الشهري في المجمع او  عَدَدِ الْمَرْضَى الْمُقِيمِينَ الشَّهْرِي فِي الْمُجَمَّعِ ، ارجع 'in_Patients'. 
            عند السؤال بشكل عام عن جميع الأسرة غير المستخدمة والمتاحة في المستشفى شهريا او جميع الاسره الغير مستخدمه في المستشفي شهريا او  جَمِيعِ الْأَسِرَّةِ غَيْرِ الْمُسْتَخْدَمَةِ وَالْمُتَاحَةِ فِي الْمُسْتَشْفَى ، ارجع 'Total_Hospital_Beds_unused_monthly'.  
            عند السؤال عن تكلفةاستهلاك الكهرباء الشهرية في المجمع او  تَكْلِفَةِ اسْتِهْلَاكِ الْكَهْرَبَاءِ الشَّهْرِيَّةِ فِي الْمُجَمَّعِ ، ارجع 'monthlycost_sg'.  
            عند السؤال عن تكلفةاستهلاك المياه الشهرية في المجمع او  تَكْلِفَةِ اسْتِهْلَاكِ الْمِيَاهِ الشَّهْرِيَّةِ فِي الْمُجَمَّعِ ، ارجع 'monthly_water_cost'.  
            عند السؤال عن تكلفةاستهلاك الاكسجين الشهرية في المجمع او  تَكْلِفَةِ اسْتِهْلَاكِ الْأُكْسِجِينِ الشَّهْرِيَّةِ فِي الْمُجَمَّعِ ، ارجع 'monthly_oxygen_cost'.  
            عند السؤال عن معلومات نظام الغازات في المجمع او  مَعْلُومَاتِ نِظَامِ الْغَازَاتِ فِي الْمُجَمَّعِ ، ارجع 'monthly_gas_system'.  
            عند السؤال عن نسبة إشغال المستشفى او معدل الاشغال في المستفش او  نِسْبَةِ إِشْغَالِ الْمُسْتَشْفَى أَوْ مُعَدَّلِ الْإِشْغَالِ فِي الْمُسْتَشْفَى ، ارجع 'Hospital_Occupancy_Rate'.  
            ارجع 'Clinic_Occupancy_Rate' نسبة إشغال العيادة او معدل الاشغال في العياده او  نِسْبَةَ إِشْغَالِ الْعِيَادَةِ أَوْ مُعَدَّلَ الْإِشْغَالِ فِي الْعِيَادَةِ .
            عند السؤال عن تكلفه الطاقة الشهريه للمستشفى او تكلفه الكهرباء الشهرية للمستفي، ارجع 'monthlyenergy_cost_hospital'.  
            عند السؤال عن استهلاك الطاقة الشهري للطابق الارضي في المستشفى او استهلاك الكهرباء الشهري للطابق الارضي في  المستفي، ارجع 'monthlyenergy_Hospital_GF'.
            عند السؤال عن تكلفةاستهلاك المياه الشهرية في المستشفي او  تَكْلِفَةِ اسْتِهْلَاكِ الْمِيَاهِ الشَّهْرِيَّةِ فِي الْمُسْتَشْفَى ، ارجع 'monthly_water_cost_hospital'. 
            عند السؤال عن استهلاك المياه الشهري في المستشفي ، ارجع 'monthly_water_consumption_hospital'. 
            عند السؤال عن تَكْلِفَةِ الأكسجين الشَّهْرِيَّةِ في الْمُسْتَشْفَى او التكلفه الشهريه للاكسجين بالمستشفي، ارجع 'monthly_oxygen_cost_hospital'. 
            عند السؤال عن استهلاك الأكسجين الشهري في المستشفي، ارجع 'monthly_oxygen_consumption_hospital'.   
            عند السؤال عن استهلاك الطاقة اليومي للطابق الارضي بالمستشفي  او استهلاك الكهرباء اليومي بالطابق الارضي للمستفي، ارجع 'dailyenergy_Hospital_GF'.  
            عند السؤال عن التكلفه اليومي للمستشفى او تكلفه الكهرباء اليوميه للمستفي، ارجع 'dailyenergy_Hospital_cost'. 
            عند السؤال عن استهلاك المياه اليومي في المستشفي، ارجع 'daily_water_consumption_hospital'.  
            عند السؤال عن تكلفة الأكسجين اليومية في المستشفي، ارجع 'daily_oxygen_cost_hospital'.  
            عند السؤال عن استهلاك الأكسجين اليومي في المستشفي، ارجع 'daily_oxygen_consumption_hospital'. 
            عند السؤال عن درجه الحراره داخل  الْمُجَمَّعِ ، ارجع 'temp_inside'. 
            عند السؤال عن  درجه الحراره خارج  الْمُجَمَّعِ ، ارجع 'temp_outside'.
            عند السؤال عن عدد الاطباء والممرضين المتواجدين في  المستشفي ، ارجع 'total_complex_staff'. 
            عند السؤال عن الاطباء المتواجدين في  المستشفي او عدد الدكاتره او عَدَدُ الأَطِبَّاءِالمتَوَاجِدِينَ في المَسْتَشْفَى ، ارجع 'total_complex_doctor'. 
            عند السؤال عن عدد الممرضين المتواجدين في  الْمُجَمَّعِ او عدد الممرضين او عَدَدُ المُمَرِّضِينَ المتَوَاجِدَاتِين في الْمُجَمَّعِ  ، ارجع 'total_complex_nurse'.

            #groundfloor ubdate

            عند السؤال عن عدد المرضي المقيمين في الطابق الارضي للمستشفي  او عَدَدُ المرضي المقيمين في الطابق الارضي للمُسْتَشْفَى  ، ارجع 'in_patients_GF'. 
            عند السؤال عن عدد المرضي الغير مقيمين في الطابق الارضي للمستشفي  او عَدَدُ المرضي الغير مقيمين في الطابق الارضي للمُسْتَشْفَى  ، ارجع 'out_patients_GF'. 
            عند السؤال عن استهلاك الكهرباء الشهري في الطابق الارضي للمستشفي  ، ارجع 'monthlyenergy_g'. 
            عند السؤال عن استهلاك الكهرباء الشهري في قسم الاشعه السينيه   ، ارجع 'energy_dental_xray'. 
            عند السؤال عن تكلفه الكهرباء الشهريه في قسم الاشعه السينيه   ، ارجع 'cost_dental_xray'. 
            عند السؤال عن استهلاك الكهرباء الشهري في قسم الاشعه و المختبر   ، ارجع 'energy_radiology_lab'. 
            عند السؤال عن تكلفه الكهرباء الشهريه في قسم الاشعه و المختبر   ، ارجع 'cost_radiology_lab'. 
            عند السؤال عن استهلاك الكهرباء الشهري في قسم الخزانات والمعدات   ، ارجع 'energy_bio_tanks'. 
            عند السؤال عن تكلفه الكهرباء الشهريه في قسم الخزانات والمعدات   ، ارجع 'cost_bio_tanks'. 
            عند السؤال عن استهلاك الكهرباء الشهري في قسم الطوارئ والانعاش   ، ارجع 'energy_triage'. 
            عند السؤال عن تكلفه الكهرباء الشهريه في قسم الطوارئ والانعاش    ، ارجع 'cost_triage'. 
            عند السؤال عن استهلاك الكهرباء الشهري في قسم الاداره    ، ارجع 'energy_administration'. 
            عند السؤال عن تكلفه الكهرباء الشهريه في قسم الاداره    ، ارجع 'cost_administration'. 

            #boilers ubdate

                                            
            عند السؤال عن حاله الغلايه الاولي او حاله الغلايه رقم 1 ، ارجع 'Hospital_Boiler_1_Status'.  
            عند السؤال عن وجود انزار في الغلايه الاولي او وجود انزار في الغلايه رقم 1 ، ارجع 'Hospital_Boiler_1_Alarm'.  
            عند السؤال عن درجه حراره المياه في الغلايه الاولي او درجه حراره المياه في الغلايه رقم 1 ، ارجع 'Hospital_Boiler_1_Hot_Water_Temperature'.  
            عند السؤال عن عدد ساعات تشغيل الغلايه الاولي في الشهر او عدد ساعات تشغيل الغلايه رقم 1 في الشهر ، ارجع 'Hospital_Boiler_1_Operation_Time'.  
            عند السؤال عن حجم المياه او سعه المياه في الغلايه  الاولي او حجم او سعه المياه في الغلايه رقم 1 ، ارجع 'Hospital_Boiler_1_Hot_Water_Volume'.  
            عند السؤال عن الغاز المستهلك للغلايه الاولي شهريا او الغاز المستهلك للغلايه رقم 1 شهريا ، ارجع 'Hospital_Boiler_1_Gas_Consumption_Month'.  
            عند السؤال عن تكلفه الغاز المستهلك للغلايه الاولي شهريا او تكلفه الغاز المستهلك للغلايه رقم 1 شهريا ، ارجع 'Hospital_Boiler_1_Gas_Invoice_Month'.  
            عند السؤال عن حاله الغلايه الثانيه او حاله الغلايه رقم 2  ، ارجع 'Hospital_Boiler_2_Status'.  
            عند السؤال عن وجود انزار في الغلايه الثانيه او وجود انزار في الغلايه رقم 2 ، ارجع 'Hospital_Boiler_2_Alarm'.  
            عند السؤال عن درجه حراره المياه في الغلايه الثانيه او درجه حراره المياه في الغلايه رقم 2، ارجع 'Hospital_Boiler_2_Hot_Water_Temperature'.  
            عند السؤال عن عدد ساعات تشغيل الغلايه الثانيه في الشهر او عدد ساعات تشغيل الغلايه رقم2  في الشهر ، ارجع 'Hospital_Boiler_2_Operation_Time'.  
            عند السؤال عن حجم المياه او سعه المياه في الغلايه  الثانيه او حجم او سعه المياه في الغلايه رقم 2 ، ارجع 'Hospital_Boiler_2_Hot_Water_Volume'.  
            عند السؤال عن الغاز المستهلك للغلايه الثانيه شهريا او الغاز المستهلك للغلايه رقم 2 شهريا ، ارجع 'Hospital_Boiler_2_Gas_Consumption_Month'.  
            عند السؤال عن تكلفه الغاز المستهلك للغلايه الثانيه شهريا او تكلفه الغاز المستهلك للغلايه رقم 2 شهريا ، ارجع 'Hospital_Boiler_2_Gas_Invoice_Month'.

            #pumps ubdate

            عند السؤال عن حاله المضخه الاولي في المجموعه الاولي ، ارجع 'Primary_Pump_1_Status'.
            عند السؤال عن عن حاله المضخه الثانيه في المجموعه الاولي ، ارجع 'Primary_Pump_2_Status'.
            عند السؤال عن عن حاله المضخه الثالثه في المجموعه الاولي ، ارجع 'Primary_Pump_3_Status'.
            عند السؤال عن عن حاله المضخه الاولي في المجموعه الثانيه ، ارجع 'secondry_Pump_1_Status'.
            عند السؤال عن عن حاله المضخه الثانيه في المجموعه الثانيه ، ارجع 'secondry_Pump_2_Status'.
            عند السؤال عن عن حاله المضخه الثالثه في المجموعه الثالثه ، ارجع 'secondry_Pump_3_Status'.






            عند السؤال عن انتهاك سياسة ارتداء الكمامات في المستشفى او السؤال عن الكمامات ، ارجع 'Mask_Policy_Violations'.  
            عند السؤال عن سياسة التباعد الاجتماعي او السؤال عن المسافات الامنه بين المرضي، ارجع 'Social_Distance_Violations'.  
            عند السؤال عن عدد السقطات المكتشفة في المستشفى او السؤال عن الاشخاص الملقون علي الارض، ارجع 'NuOF_Detected_Falls'.  
            عند السؤال عن عدد المحولات العامله حاليًا، ارجع 'transformer_on'.  
            عند السؤال عن عدد المحولات الغير عامله حاليًا، ارجع 'transformer_Off'.  
            عند السؤال عن عدد المولدات العامله حاليا، ارجع 'generator_on'.  
            عند السؤال عن عدد المولدات الغير العامله حاليًا، ارجع 'generator_off'.  
            عند السؤال عن عدد المصاعد العامله حاليًا، ارجع 'Elevator_on'.  
            عند السؤال عن عدد المصاعد الغير عامله حاليًا، ارجع 'Elevator_of'.  
            عند السؤال عن التكلفة الإجمالية للمجمع بالكامل للشهر او التكلفه الشهريه الاجماليه للمجمع كاملا، ارجع 'monthly_total_cost'.  
            عند السؤال عن وجود إنذار في نظام التدفئة والتهوية وتكييف الهواء (HVAC)، ارجع 'HVAC_alarm'.  
            عند السؤال عن وجود إنذار يتعلق بنظام الغاز الطبي، ارجع 'medical_gas_alarm'.  
            عند السؤال عن وجود إنذار يتعلق بنظام مكافحة الحرائق، ارجع 'fire_fighting_alarm'.  
            عند السؤال عن وجود إنذار يتعلق بالمحول الكهربائي، ارجع 'transformer_alarm'.  
            عند السؤال عن وجود إنذار يتعلق بالمصعد، ارجع 'elevator_alarm'.  
            عند السؤال عن عدد وحدات معالجة الهواء التي تم تشغيلها، ارجع 'F_AHU_ON'.  
            عند السؤال عن وحدات معالجة الهواء التي تم إيقاف تشغيلها، ارجع 'F_AHU_OFF'.  
            عند السؤال عن عدد المبردات التي تعمل، ارجع 'chiller_on'.  
            عند السؤال عن عدد المبردات التي لا تعمل، ارجع 'chiller_off'.  
            عند السؤال عن استهلاك الكهرباء الشهري في المجمع، ارجع 'monthlyenergy_MVSG'.  
            عند السؤال عن قياس ضغط الفراغ، ارجع 'vaccum_press'.  
            عند السؤال عن ضغط 4 بار، ارجع 'air_4bar_press'.  
            عند السؤال عن ضغط 7 بار، ارجع 'air_7bar_press'.  
            عند السؤال عن ضغط الأكسجين في النظا م، ارجع 'oxygen_press'.  
            عند السؤال عن استهلاك الطاقة اليومي لمعدات التحويل ذات الجهد المتوسط أو المجمع بالكامل، ارجع 'dailyenergy_MVSG'.  
            عند السؤال عن استهلاك الطاقة اليومي للمصدر الثاني لمعدات التحويل ذات الجهد المتوسط، ارجع 'dailyenergy_MVSG_incoming2_energy'.  
            عند السؤال عن استهلاك الطاقة اليومي للمصدر الثالث لمعدات التحويل ذات الجهد المتوسط، ارجع 'dailyenergy_MVSG_incoming3_energy'.  
            عند السؤال عن استهلاك الطاقة اليومي للمستشفى او استهلاك الكهرباء اليومي للمستفي، ارجع 'dailyenergy_Hospital'.  
            عند السؤال عن استهلاك الطاقة اليومي للعيادة او استهلاك الكهرباء اليومي للعيادات، ارجع 'dailyenergy_Clinics'.  
            عند السؤال عن استهلاك الطاقة اليومي للمرافق او استهلاك الكهرباء اليومي للمرافق، ارجع 'dailyenergy_Utilities'.  
            عند السؤال عن استهلاك الطاقة اليومي للنظام الكهربائي، ارجع 'dailyenergy_ele'.  
            عند السؤال عن استهلاك الطاقة اليومي للمبردات، ارجع 'dailyenergy_chillers'.  
            عند السؤال عن استهلاك الطاقة اليومي لوحدات معالجة الهواء، ارجع 'dailyenergy_AHU'.  
            عند السؤال عن استهلاك الطاقة اليومي للغلايات، ارجع 'dailyenergy_Boilers'.  
            عند السؤال عن استهلاك الطاقة الشهري للمصدر الثاني لمعدات التحويل ذات الجهد المتوسط، ارجع 'monthlyenergy_MVSG_incoming2_energy'.  
            عند السؤال عن استهلاك الطاقة الشهري للمصدر الثالث لمعدات التحويل ذات الجهد المتوسط، ارجع 'monthlyenergy_MVSG_incoming3_energy'.  
            عند السؤال عن استهلاك الطاقة الشهري للمستشفى او استهلاك الكهرباء الشهري للمستفي، ارجع 'monthlyenergy_Hospital'.  
            عند السؤال عن استهلاك الطاقة الشهري للعيادات او استهلاك الكهرباء الشهري للعيادات ،ارجع 'monthlyenergy_Clinics'.  
            عند السؤال عن استهلاك الطاقة الشهري للمرافق او استهلاك الكهرباء الشهري للمرافق، ارجع 'monthlyenergy_Utilities'.  
            عند السؤال عن استهلاك الطاقة الشهري للنظام الكهربائي، ارجع 'monthlyenergy_ele'.  
            عند السؤال عن استهلاك الطاقة الشهري للمبردات، ارجع 'monthlyenergy_chillers'.  
            عند السؤال عن استهلاك الطاقة الشهري لوحدات معالجة الهواء، ارجع 'monthlyenergy_AHU'.  
            عند السؤال عن استهلاك الطاقة الشهري للغلايات، ارجع 'monthlyenergy_Boilers'.  
            عند السؤال عن تكلفة معدات التحويل اليومية أو المجمع بالكامل، ارجع 'dailycost_sg'.  
            عند السؤال عن استهلاك الطاقة السنوي لمعدات التحويل ذات الجهد المتوسط، ارجع 'yearlyenergy_MVSG'.  
            عند السؤال عن تكلفة معدات التحويل السنوية، ارجع 'yearlycost_sg'.  
            عند السؤال عن التكلفة الشهرية للكهرباء في الطابق الأرضي او التكلفه الشهريه في الدور الارضي، ارجع 'monthlycost_g'.  
            عند السؤال عن التكلفة الشهرية في الطابق الأول اوالتكلفه الشهريه في الدور الاول، ارجع 'monthlycost_f'.  
            عند السؤال عن التكلفة الشهرية في الطابق الثاني او التكلفه الشهريه في الدور الثاني، ارجع 'monthlycost_s'.  
            عند السؤال عن التكلفة الشهرية في الطابق الثالث او التكلفه الشهريه في الدور الثالث، ارجع 'monthlycost_th'.  
            عند السؤال عن التكلفة الشهرية على السطح او التكلفه الشهريه علي السطح، ارجع 'monthlycost_roof'.  
            عند السؤال عن التكلفة الشهرية للمستشفى، ارجع 'monthlycost_Hospital'.  
            عند السؤال عن التكلفة الشهرية للعيادة، ارجع 'monthlycost_clinic'.  
            عند السؤال عن التكلفة الشهرية للمرافق، ارجع 'monthlycost_Utilities'.  
            عند السؤال عن استهلاك المياه اليومي، ارجع 'daily_water_consumption'.  
            عند السؤال عن استهلاك المياه الشهري في المجمع، ارجع 'monthly_water_consumption'.  
            عند السؤال عن تكلفة المياه اليومية، ارجع 'daily_water_cost'.  
            عند السؤال عن استهلاك المياه السنوي، ارجع 'yearly_water_consumption'.  
            عند السؤال عن تكلفة المياه السنوية، ارجع 'yearly_water_cost'.  
            عند السؤال عن استهلاك الأكسجين اليومي، ارجع 'daily_oxygen_consumption'.  
            عند السؤال عن استهلاك الأكسجين الشهري في المجمع، ارجع 'monthly_oxygen_consumption'.  
            عند السؤال عن تكلفة الأكسجين اليومية، ارجع 'daily_oxygen_cost'.  
            عند السؤال عن تكلفة المياه اليومية في المستشفي، ارجع 'daily_water_cost_hospital'.  
            عند السؤال عن استهلاك الأكسجين السنوي، ارجع 'yearly_oxygen_consumption'.  
            عند السؤال عن تكلفة الأكسجين السنوية، ارجع 'yearly_oxygen_cost'.  
            عند السؤال عن حالة المولد 1، ارجع 'gen1_status'.  
            عند السؤال عن وقت تشغيل محرك المولد 1، ارجع 'gen1_engine_runtime'.  
            عند السؤال عن مدخل الطاقة الشمسية للمولد 1، ارجع 'gen1_solar'.  
            عند السؤال عن آخر وقت تشغيل للمشغل للمولد 1، ارجع 'gen1_last_op'.  
            عند السؤال عن ما إذا كان المولد جاهزًا أم لا، ارجع 'gen1_bv'.  
            عند السؤال عن جهد المولد 1، ارجع 'gen1_volt'.  
            عند السؤال عن تيار المولد 1، ارجع 'gen1_curr'.
            عند السؤال عن قدرة المولد 1، ارجع 'gen1_kw'.  
            عند السؤال عن حالة الوقود للمولد 1، ارجع 'gen1_fuel'.  
            عند السؤال عن حالة الزيت للمولد 1، ارجع 'gen1_oil'.  
            عند السؤال عن حالة المياه للمولد 1، ارجع 'gen1_water'.  
            عند السؤال عن وضع الشاحن للمولد 1، ارجع 'gen1_charge'.  
            عند السؤال عن حالة المولد 2، ارجع 'gen2_status'.  
            عند السؤال عن وقت تشغيل محرك المولد 2، ارجع 'gen2_engine_runtime'.  
            عند السؤال عن مدخل الطاقة الشمسية للمولد 2، ارجع 'gen2_solar'.  
            عند السؤال عن آخر وقت تشغيل للمشغل للمولد 2، ارجع 'gen2_last_op'.  
            عند السؤال عن ما إذا كان المولد جاهزًا أم لا، ارجع 'gen2_bv'.  
            عند السؤال عن جهد المولد 2، ارجع 'gen2_volt'.  
            عند السؤال عن تيار المولد 2، ارجع 'gen2_curr'.  
            عند السؤال عن قدرة المولد 2، ارجع 'gen2_kw'.  
            عند السؤال عن حالة الوقود للمولد 2، ارجع 'gen2_fuel'.  
            عند السؤال عن حالة الزيت للمولد 2، ارجع 'gen2_oil'.  
            عند السؤال عن حالة المياه للمولد 2، ارجع 'gen2_water'.  
            عند السؤال عن وضع الشاحن للمولد 2، ارجع 'gen2_charge'.
            عند السؤال عن الفواتير الشهريه للمستشفي او الفواتير الشهريه او الاستهلاك الشهري للمستشفي او تفاصيل الفواتير الشهريه او تكلفه الفواتير الشهريه 2، ارجع 'invoices_information'.
                    """,
    llm=ChatOpenAI,
    llm_kwds={}
).init_chain()

suez_medical_complex_mapper = {

#boilers and pump ubdate

    'Hospital_Boiler_1_Status': SuezMedicalComplexConfigurator.Home.Hospital_Boiler_1_Status_info,
    'Hospital_Boiler_1_Alarm': SuezMedicalComplexConfigurator.Home.Hospital_Boiler_1_Alarm_info,
    'Hospital_Boiler_1_Hot_Water_Temperature': SuezMedicalComplexConfigurator.Home.Hospital_Boiler_1_Hot_Water_Temperature_info,
    'Hospital_Boiler_1_Operation_Time': SuezMedicalComplexConfigurator.Home.Hospital_Boiler_1_Operation_Time_info,
    'Hospital_Boiler_1_Hot_Water_Volume': SuezMedicalComplexConfigurator.Home.Hospital_Boiler_1_Hot_Water_Volume_info,
    'Hospital_Boiler_1_Gas_Consumption_Month': SuezMedicalComplexConfigurator.Home.Hospital_Boiler_1_Gas_Consumption_Month_info,
    'Hospital_Boiler_1_Gas_Invoice_Month': SuezMedicalComplexConfigurator.Home.Hospital_Boiler_1_Gas_Invoice_Month_info,
    'Hospital_Boiler_2_Status': SuezMedicalComplexConfigurator.Home.Hospital_Boiler_2_Status_info,
    'Hospital_Boiler_2_Alarm': SuezMedicalComplexConfigurator.Home.Hospital_Boiler_2_Alarm_info,
    'Hospital_Boiler_2_Hot_Water_Temperature': SuezMedicalComplexConfigurator.Home.Hospital_Boiler_2_Hot_Water_Temperature_info,
    'Hospital_Boiler_2_Operation_Time': SuezMedicalComplexConfigurator.Home.Hospital_Boiler_2_Operation_Time_info,
    'Hospital_Boiler_2_Hot_Water_Volume': SuezMedicalComplexConfigurator.Home.Hospital_Boiler_2_Hot_Water_Volume_info,
    'Hospital_Boiler_2_Gas_Consumption_Month': SuezMedicalComplexConfigurator.Home.Hospital_Boiler_2_Gas_Consumption_Month_info,
    'Hospital_Boiler_2_Gas_Invoice_Month': SuezMedicalComplexConfigurator.Home.Hospital_Boiler_2_Gas_Invoice_Month_info,
    'Primary_Pump_1_Status': SuezMedicalComplexConfigurator.Home.Primary_Pump_1_Status_info,
    'Primary_Pump_2_Status': SuezMedicalComplexConfigurator.Home.Primary_Pump_2_Status_info,
    'Primary_Pump_3_Status': SuezMedicalComplexConfigurator.Home.Primary_Pump_3_Status_info,
    'secondry_Pump_1_Status': SuezMedicalComplexConfigurator.Home.secondry_Pump_1_Status_info,
    'secondry_Pump_2_Status': SuezMedicalComplexConfigurator.Home.secondry_Pump_2_Status_info,
    'secondry_Pump_3_Status': SuezMedicalComplexConfigurator.Home.secondry_Pump_3_Status_info,


#home and hospital and gf ubdates

    'in_patients_GF': SuezMedicalComplexConfigurator.Home.in_patients_GF_info,
    'out_patients_GF': SuezMedicalComplexConfigurator.Home.out_patients_GF_info,
    'monthlyenergy_g': SuezMedicalComplexConfigurator.Home.monthlyenergy_g_info,
    'energy_dental_xray': SuezMedicalComplexConfigurator.Home.energy_dental_xray_info,
    'cost_dental_xray': SuezMedicalComplexConfigurator.Home.cost_dental_xray_info,
    'energy_radiology_lab': SuezMedicalComplexConfigurator.Home.energy_radiology_lab_info,
    'cost_radiology_lab': SuezMedicalComplexConfigurator.Home.cost_radiology_lab_info,
    'energy_bio_tanks': SuezMedicalComplexConfigurator.Home.energy_bio_tanks_info,
    'cost_bio_tanks': SuezMedicalComplexConfigurator.Home.cost_bio_tanks_info,
    'energy_triage': SuezMedicalComplexConfigurator.Home.energy_triage_info,
    'cost_triage': SuezMedicalComplexConfigurator.Home.cost_triage_info,
    'energy_administration': SuezMedicalComplexConfigurator.Home.energy_administration_info,
    'cost_administration': SuezMedicalComplexConfigurator.Home.cost_administration_info,
    'daily_water_consumption_hospital': SuezMedicalComplexConfigurator.Home.daily_water_consumption_hospital_info,
    'daily_oxygen_cost_hospital': SuezMedicalComplexConfigurator.Home.daily_oxygen_cost_hospital_info,
    'daily_water_cost_hospital': SuezMedicalComplexConfigurator.Home.daily_oxygen_cost_hospital_info,
    'daily_oxygen_consumption_hospital': SuezMedicalComplexConfigurator.Home.daily_oxygen_consumption_hospital_info,
    'temp_inside': SuezMedicalComplexConfigurator.Home.temp_inside_info,
    'temp_outside': SuezMedicalComplexConfigurator.Home.temp_outside_info,
    'total_complex_staff': SuezMedicalComplexConfigurator.Home.total_complex_staff_info,
    'total_complex_doctor': SuezMedicalComplexConfigurator.Home.total_complex_doctor_info,
    'total_complex_nurse': SuezMedicalComplexConfigurator.Home.total_complex_nurse_info,
    'any_alarm': SuezMedicalComplexConfigurator.Home.any_alarm_info,

    
    'complex_Occupancy_Rate': SuezMedicalComplexConfigurator.Home.return_Beds_occupancy_rate_info,
    'Inpatient_Beds_used_monthly': SuezMedicalComplexConfigurator.Home.return_Inpatient_Beds_used_info,
    'Inpatient_Beds_Unused': SuezMedicalComplexConfigurator.Home.return_Inpatient_Beds_Unused_info,
    'ICU_CCU_Beds_used_monthly': SuezMedicalComplexConfigurator.Home.return_ICU_CCU_Beds_used_info,
    'ICU_CCU_Beds_Unused': SuezMedicalComplexConfigurator.Home.return_ICU_CCU_Beds_Unused_info,
    'Emergency_Beds_used_monthly': SuezMedicalComplexConfigurator.Home.return_Emergency_Beds_used_info,
    'Emergency_Beds_unused_monthly': SuezMedicalComplexConfigurator.Home.return_Emergency_Beds_Unused_info,
    'Incubators_Beds_used_monthly': SuezMedicalComplexConfigurator.Home.return_Incubators_Beds_used_info,
    'Incubators_Beds_unused_monthly': SuezMedicalComplexConfigurator.Home.return_Incubators_Beds_unused_info,
    'Total_Hospital_Beds_used_monthly': SuezMedicalComplexConfigurator.Home.return_Total_Hospital_Beds_used_info,
    'Total_Hospital_Beds_unused_monthly': SuezMedicalComplexConfigurator.Home.return_Total_Hospital_Beds_unused_info,
    'monthlycost_sg': SuezMedicalComplexConfigurator.Home.return_monthlycost_sg_info,
    'monthly_water_cost': SuezMedicalComplexConfigurator.Home.return_monthly_water_cost_info,
    'monthly_water_cost_hospital': SuezMedicalComplexConfigurator.Home.return_monthly_water_cost_info,
    'monthly_oxygen_cost': SuezMedicalComplexConfigurator.Home.return_monthly_water_cost_hospital_info,
    'monthly_oxygen_cost_hospital': SuezMedicalComplexConfigurator.Home.monthly_oxygen_cost_hospital_info,
    'monthly_gas_system': SuezMedicalComplexConfigurator.Home.return_monthly_gas_system_info,
    'carbon_foot_Hospital': SuezMedicalComplexConfigurator.Home.return_carbon_foot_Hospital,
    'carbon_foot_Utilites': SuezMedicalComplexConfigurator.Home.return_carbon_foot_Utilites,
    'carbon_foot_Clinics': SuezMedicalComplexConfigurator.Home.return_carbon_foot_Clinics,
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
    'dailyenergy_Hospital_GF': SuezMedicalComplexConfigurator.Home.dailyenergy_Hospital_GF_info,
    'dailyenergy_Hospital_cost': SuezMedicalComplexConfigurator.Home.dailyenergy_Hospital_cost_info,
    'dailyenergy_Clinics': SuezMedicalComplexConfigurator.Home.dailyenergy_Clinics_info,
    'dailyenergy_Utilities': SuezMedicalComplexConfigurator.Home.dailyenergy_Utilities_info,
    'dailyenergy_ele': SuezMedicalComplexConfigurator.Home.dailyenergy_ele_info,
    'dailyenergy_chillers': SuezMedicalComplexConfigurator.Home.dailyenergy_chillers_info,
    'dailyenergy_AHU': SuezMedicalComplexConfigurator.Home.dailyenergy_AHU_info,
    'dailyenergy_Boilers': SuezMedicalComplexConfigurator.Home.dailyenergy_Boilers_info,
    'monthlyenergy_MVSG_incoming2_energy': SuezMedicalComplexConfigurator.Home.monthlyenergy_MVSG_incoming2_energy_info,
    'monthlyenergy_MVSG_incoming3_energy': SuezMedicalComplexConfigurator.Home.monthlyenergy_MVSG_incoming3_energy_info,
    'monthlyenergy_Hospital': SuezMedicalComplexConfigurator.Home.monthlyenergy_Hospital_info,
    'monthlyenergy_Hospital_GF': SuezMedicalComplexConfigurator.Home.monthlyenergy_Hospital_GF_info,
    'monthlyenergy_cost_hospital': SuezMedicalComplexConfigurator.Home.monthlyenergy_cost_hospital_info,
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
    'monthly_water_consumption_hospital': SuezMedicalComplexConfigurator.Home.monthly_water_consumption_hospital_info,
    'daily_water_cost': SuezMedicalComplexConfigurator.Home.daily_water_cost_info,
    'yearly_water_consumption': SuezMedicalComplexConfigurator.Home.yearly_water_consumption_info,
    'yearly_water_cost': SuezMedicalComplexConfigurator.Home.yearly_water_cost_info,
    'daily_oxygen_consumption': SuezMedicalComplexConfigurator.Home.daily_oxygen_consumption_info,
    'monthly_oxygen_consumption': SuezMedicalComplexConfigurator.Home.monthly_oxygen_consumption_info,
    'monthly_oxygen_consumption_hospital': SuezMedicalComplexConfigurator.Home.monthly_oxygen_consumption_hospital_info,
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
    'in_Patients': SuezMedicalComplexConfigurator.Home.in_Patients_info,
    'in_Patients_hospital': SuezMedicalComplexConfigurator.Home.in_Patients_hospital_info,
    'out_Patients': SuezMedicalComplexConfigurator.Home.out_Patients_info,
    'out_Patients_hospital': SuezMedicalComplexConfigurator.Home.out_Patients_hospital_info,
    'every_department': SuezMedicalComplexConfigurator.Home.every_department_info,
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
    'carbon_foot_print_GF': SuezMedicalComplexConfigurator.Home.carbon_foot_print_GF_info,
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

import asyncio
import json
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)

@profile
async def suez_request_handler(complex_data, voice_file):
    try:
        complex_data = json.loads(complex_data)

        # Asynchronously perform speech-to-text and classify the request in parallel
        transcript = await voice_handler.speech_to_text(audio_file=voice_file.file)
        dated_request = await date_classifier.ainvoke({'input': transcript})
        
        logger.info(f'Transcription is: {transcript}')
        dated_request = ''.join(e for e in dated_request if e.isalnum() or e == '_')

        if dated_request == 'date':
            dates = await date_extraction.ainvoke({'input': transcript})
            date = dates.get('date', str(datetime.now().strftime("%Y-%m-%d")))
            logger.info(f'The request date is: {date}')
            collection = suez_medical_complex_collection
            logger.info(f'Data collection is: {collection}')
            complex_data = db.get_last_document_for_date(collection, date)
        else:
            complex_data = complex_data
        
        selected_data = await suez_medical_complex_classifier.ainvoke({'input': transcript})
        
        selected_data = ''.join(e for e in selected_data if e.isalnum() or e == '_')

        # Map the selected data to the appropriate output
        output_text = suez_medical_complex_mapper.get(selected_data, lambda x: "لم يتم العثور على البيانات المطلوبة")(complex_data)
        logger.info(f'Final output is: {output_text}')

        # Add prefix for date requests and generate audio output
        if dated_request == 'date':
            _, audio_data = await voice_handler.text_to_speech(
                text_data="المعلومات التالية في الفترة الزمنية المطلوبة " + output_text + "\n شكرا لاستخدامك منصة زِيتَا \n"
            )
        else:
            _, audio_data = await voice_handler.text_to_speech(
                text_data=output_text + "\n شكرا لاستخدامك منصة زِيتَا \n"
            )

        # Cleanup temporary file
        os.remove(_)
        return audio_data
    except Exception as e:
        logger.error(f'Error in suez_request_handler: {e}')
        return await voice_handler.text_to_speech(text_data="حدث خطأ أثناء معالجة الطلب")

@profile
async def station_request_handler(stations_data, voice_file):
    try:
        payload = json.loads(stations_data)
        current_station_id = payload.get("current_index")
        stations_data = payload.get("stations_data", {})
        # Asynchronously fetch both transcript and station ID in parallel
        transcript = await voice_handler.speech_to_text(audio_file=voice_file.file)
        station_id = await station_classifier.ainvoke({'input': transcript})
        print(transcript)
        station_id = ''.join(e for e in station_id if e.isalnum() or e == '-')
        logger.info(f'Station ID: {station_id}, Transcription: {transcript}')

        if station_id == 'current':
            station_id = current_station_id

        # Process date extraction concurrently with previous tasks
        dated_request = await date_classifier.ainvoke({'input': transcript})
        dated_request = ''.join(e for e in dated_request if e.isalnum() or e == '_')

        if dated_request == 'date':
            dates = await date_extraction.ainvoke({'input': transcript})
            date = dates.get('date', str(datetime.now().strftime("%Y-%m-%d")))
            collection = id_collections_mapper.get(station_id)
            station_data = db.get_last_document_for_date(collection, date)
            logger.info(f'Request date: {date}, Data collection: {collection}')
        else:
            station_data = stations_data.get(station_id)

        if station_data is None:
            logger.warning(f'No data found for station ID: {station_id}')
            return await voice_handler.text_to_speech(
                text_data="لم يتم العثور على البيانات المطلوبة"
            )

        # Classify the request type and fetch the output
        selected_data = await id_classifiers_mapper.get(station_id, [None, None])[1].ainvoke({'input': transcript})
        
        selected_data = ''.join(e for e in selected_data if e.isalnum() or e == '_')

        mapper = id_classifiers_mapper.get(station_id, [None, None])[0]
        output_text = mapper.get(selected_data, lambda x: "لم يتم العثور على البيانات المطلوبة")(station_data)
        logger.info(f'Final output for station ID {station_id}: {output_text}')

        # Add prefix for date requests
        if dated_request == 'date':
            output_text = "المعلومات التالية في الفترة الزمنية المطلوبة " + output_text

        # Generate the audio output
        _, audio_data = await voice_handler.text_to_speech(
            text_data=output_text + "\n شكرا لاستخدامك منصة زِيتَا \n"
        )

        # Cleanup temporary file
        print(output_text)
        os.remove(_)
        return audio_data
    except Exception as e:
        logger.error(f'Error in station_request_handler: {e}')
        return await voice_handler.text_to_speech(text_data="حدث خطأ أثناء معالجة الطلب")



@app.post("/voice/main")
async def voice_endpoint(upload_file: UploadFile = File(...), stations_data: str = Form(...)):
    audio_data = await station_request_handler(stations_data, upload_file) 
    return Response(content=audio_data, media_type="audio/mp3")

@app.post("/voice/suez")
async def voice_endpoint(upload_file: UploadFile = File(...), complex_data: str = Form(...)):
    audio_data = await suez_request_handler(complex_data, upload_file) 
    return Response(content=audio_data, media_type="audio/mp3")

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)