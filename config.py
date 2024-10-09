import json
import string
import random
import requests

class SuezMedicalComplexConfigurator(object):
    class Home:
        @staticmethod
        def return_carbon_foot_Hospital(parsed_data: dict) -> str:
            return (
                f"البَصْمَةُ الكَرْبُونِيَّةُ اليَوْمِيَّةُ للمستشفي: {float(parsed_data['carbon_foot_Hospital'])} كِيلُوجرام/مِتْر مُرَبَّع\n"
            )        
        @staticmethod
        def return_carbon_foot_Utilites(parsed_data: dict) -> str:
            return (
                f"البَصْمَةُ الكَرْبُونِيَّةُ اليَوْمِيَّةُ لِلْأَمَاكِنِ الخِدْمِيَّةِ في المُجَمَّعِ {float(parsed_data['carbon_foot_Utilites'])} كِيلُوجرام/مِتْر مُرَبَّع\n"
            )        
        @staticmethod
        def return_carbon_foot_Clinics(parsed_data: dict) -> str:
            return (
                f"البَصْمَةُ الكَرْبُونِيَّةُ اليَوْمِيَّةُ لِلْعِيَادَاتِ: {float(parsed_data['carbon_foot_Clinics'])} كِيلُوجرام/مِتْر مُرَبَّع\n"
            )        
        @staticmethod
        def return_Beds_occupancy_rate_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ إِشْغَالِ الأَسِرَّةِ فِي المُجَمَّعِ: {int(float(parsed_data['complex_Occupancy_Rate']))} فِي المِئَةِ\n"
            )

        @staticmethod
        def return_Inpatient_Beds_used_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ الأَسِرَّةِ المُسْتَخْدَمَةِ لِغَيْرِ المَرْضَى: {int(float(parsed_data['Inpatient_Beds_used']))} سَرِيرٍ\n"
            )

        @staticmethod
        def return_Inpatient_Beds_Unused_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ الأَسِرَّةِ غَيْرِ المُسْتَخْدَمَةِ لِغَيْرِ المَرْضَى: {int(float(parsed_data['Inpatient_Beds_unused']))} سَرِيرٍ\n"
            )

        @staticmethod
        def return_ICU_CCU_Beds_used_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ الأَسِرَّةِ المُسْتَخْدَمَةِ فِي العِنَايَةِ المَرْكَزِيَّةِ لِمَرْضَى القَلْبِ: {int(float(parsed_data['ICU_CCU_Beds_used_monthly']))} سَرِيرٍ\n"
            )

        @staticmethod
        def return_ICU_CCU_Beds_Unused_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ الأَسِرَّةِ غَيْرِ المُسْتَخْدَمَةِ فِي العِنَايَةِ المَرْكَزِيَّةِ لِمَرْضَى القَلْبِ: {int(float(parsed_data['ICU_CCU_Beds_unused']))} سَرِيرٍ\n"
            )

        @staticmethod
        def return_Emergency_Beds_used_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ أَسِرَّةِ الطَّوَارِئِ الشهري المُسْتَخْدَمَةِ: {int(float(parsed_data['Emergency_Beds_used_monthly']))} سَرِيرٍ\n"
            )

        @staticmethod
        def return_Emergency_Beds_Unused_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ أَسِرَّةِ الطَّوَارِئِ الشهري غَيْرِ المُسْتَخْدَمَةِ: {int(float(parsed_data['Emergency_Beds_unused_monthly']))} سَرِيرٍ\n"
            )

        @staticmethod
        def return_Incubators_Beds_used_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ أَسِرَّةِ الحَضَّانَاتِ الشهري المُسْتَخْدَمَةِ: {int(float(parsed_data['Incubators_Beds_used_monthly']))} سَرِيرٍ\n"
            )

        @staticmethod
        def return_Incubators_Beds_unused_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ أَسِرَّةِ الحَضَّانَاتِ الشهري غَيْرِ المُسْتَخْدَمَةِ: {int(float(parsed_data['Incubators_Beds_unused_monthly']))} سَرِيرٍ\n"
            )

        @staticmethod
        def return_Total_Hospital_Beds_used_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ جَمِيعِ الأَسِرَّةِ الشهري المُسْتَخْدَمَةِ فِي المُسْتَشْفَى: {int(float(parsed_data['Total_Hospital_Beds_used_monthly']))} سَرِيرٍ\n"
            )

        @staticmethod
        def return_Total_Hospital_Beds_unused_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ جَمِيعِ الأَسِرَّةِ الشهري الغَيْرِ المُسْتَخْدَمَةِ فِي المُسْتَشْفَى: {int(float(parsed_data['Total_Hospital_Beds_unused_monthly']))} سَرِيرٍ\n"
            )

        @staticmethod
        def return_monthlycost_sg_info(parsed_data: dict) -> str:
            return (
                f"التَّكْلِفَةُ الشَّهْرِيَّةُ لاستهلاك الكرباء الكُلَى في المُجَمَّعِ: {int(float(parsed_data['monthlycost_sg']))} جُنَيْهًا\n"
            )

        @staticmethod
        def return_monthly_water_cost_info(parsed_data: dict) -> str:
            return (
                f"التَّكْلِفَةُ الشَّهْرِيَّةُ لِاِسْتِهْلَاكِ المِيَاهِ الكُلَى في المُجَمَّعِ: {int(float(parsed_data['monthly_water_cost']))} جُنَيْهًا\n"
            )
        @staticmethod
        def return_monthly_water_cost_hospital_info(parsed_data: dict) -> str:
            return (
                f"التَّكْلِفَةُ الشَّهْرِيَّةُ لِاِسْتِهْلَاكِ المِيَاهِ الكُلَى في المُسْتَشْفَى: {int(float(parsed_data['monthly_water_cost_hospital']))} جُنَيْهًا\n"
            )

        @staticmethod
        def return_monthly_oxygen_cost_info(parsed_data: dict) -> str:
            return (
                f" التَّكْلِفَةُ الشَّهْرِيَّةُ لِاِسْتِهْلَاكِ الأُكْسُجِينِ الكُلَى في المُجَمَّعِ: {int(float(parsed_data['monthly_oxygen_cost']))} جُنَيْهًا\n"
            )
        @staticmethod
        def return_monthly_oxygen_cost_hospital_info(parsed_data: dict) -> str:
            return (
                f" التَّكْلِفَةُ الشَّهْرِيَّةُ لِاِسْتِهْلَاكِ الأُكْسُجِينِ الكُلَى في المُسْتَشْفَى: {int(float(parsed_data['monthly_oxygen_cost_hospital']))} جُنَيْهًا\n"
            )

        @staticmethod
        def return_Hospital_Occupancy_Rate_info(parsed_data: dict) -> str:
            return (
                f"نِسْبَةُ مُعَدَّلِ الإِشْغَالِ فِي المُسْتَشْفَى: {int(float(parsed_data['Hospital_Occupancy_Rate']))} فِي المِئَةِ\n"
            )

        @staticmethod
        def return_Clinic_Occupancy_Rate_info(parsed_data: dict) -> str:
            return (
                f"نِسْبَةُ مُعَدَّلِ الإِشْغَالِ فِي العِيَادَاتِ: {int(float(parsed_data['Clinic_Occupancy_Rate']))} فِي المِئَةِ\n"
            )

        @staticmethod
        def Mask_Policy_Violations_info(parsed_data: dict) -> str:
            return (
                f"اِنْتِهَاكَاتُ سِيَاسَةِ اِرْتِدَاءِ الكِمَامَاتِ: {int(float(parsed_data['Mask_Policy_Violations']))} \n"
            )

        @staticmethod
        def Social_Distance_Violations_info(parsed_data: dict) -> str:
            return (
                f"اِنْتِهَاكَاتُ التَّبَاعُدِ الاِجْتِمَاعِيِّ: {int(float(parsed_data['Social_Distance_Violations']))} \n"
            )

        @staticmethod
        def NuOF_Detected_Falls_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ مَرَّاتِ السُّقُوطِ المُكْتَشَفَةِ: {int(float(parsed_data['NuOF_Detected_Falls']))}\n"
            )

        @staticmethod
        def transformer_on_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ المُحَوِّلَاتِ الحاليه العَامِلَةِ: {int(float(parsed_data['transformer_on']))}\n"
            )

        @staticmethod
        def transformer_Off_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ المُحَوِّلَاتِ الحاليه الغير العَامِلَةِ: {int(float(parsed_data['transformer_Off']))}\n"
            )

        @staticmethod
        def generator_on_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ المُوَلِّدَاتِ الحاليه العَامِلَةِ: {int(float(parsed_data['generator_on']))}\n"
            )

        @staticmethod
        def generator_off_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ المُوَلِّدَاتِ الحالي الغَيْرِ العَامِلَةِ: {int(float(parsed_data['generator_off']))} \n"
            )

        @staticmethod
        def Elevator_on_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ المَصَاعِدِ الحالي العَامِلَةِ: {int(float(parsed_data['Elevator_on']))} \n"
            )

        @staticmethod
        def Elevator_off_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ المَصَاعِدِ الحالي غَيْرِ العَامِلَةِ: {int(float(parsed_data['Elevator_off']))} \n"
            )

        @staticmethod
        def monthly_total_cost_info(parsed_data: dict) -> str:
            return (
                f"التَّكْلِفَةُ الشَّهْرِيَّةُ الإِجْمَالِيَّةُ: {float(parsed_data['monthly_total_cost'])} جُنَيْهٍ\n"
            )
        @staticmethod
        def any_alarm_info(parsed_data: dict) -> str:
            if int((parsed_data['HVAC_alarm'])) == 1:
                return "يوُجُودِ انظار فِي نِظَامِ التَّكْيِيفِ المَرْكَزِيِّ\n"
            
            elif int((parsed_data['medical_gas_alarm'])) == 1:
                return "يوُجُودِ انظار فِي نظام الغَازِات الطِّبِّيِّ\n"
            
            elif int((parsed_data['fire_fighting_alarm'])) == 1:
                return "يوُجُودِ انظار فِي نِظَامِ الحَرِيقِ\n"
            
            elif int((parsed_data['transformer_alarm'])) == 1:
                return "يوُجُودِ انظار فِي المُحَوِّلَاتِ\n"
            
            elif int((parsed_data['elevator_alarm'])) == 1:
                return "يوُجُودِ انظار فِي المَصَاعِدِ\n"
            
            else:
                return "No alarms in the critical systems."
                
        @staticmethod
        def temp_outside_info(parsed_data: dict) -> str:
            return (
                f"دَرَجةُ الحَرَارةِ خارِجَ المُجَمَّعِ.: {int(float(parsed_data['temp_outside']))} \n"
            )
        @staticmethod
        def  temp_inside_info(parsed_data: dict) -> str:
            return (
                f"دَرَجةُ الحَرَارةِ داخِلَ المُجَمَّعِ: {int(float(parsed_data['temp_inside']))} \n"
            )
       
        @staticmethod
        def total_complex_staff_info(parsed_data: dict) -> str:
            return (
                f" عَدَدُ الأَطِبَّاءِ وَالمُمَرِّضِينَ المتَوَاجِدِينَ في المَسْتَشْفَى: {int(float(parsed_data['total_complex_staff']))}  شخص\n"
            )
        @staticmethod
        def total_complex_doctor_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ الأَطِبَّاءِالمتَوَاجِدِينَ في المَسْتَشْفَى: {int(float(parsed_data['total_complex_doctor']))}طبيب \n"
            )
        @staticmethod
        def total_complex_nurse_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ المُمَرِّضِينَ المتَوَاجِدَاتِين في المُسْتَشْفَى: {int(float(parsed_data['total_complex_nurse']))}مُمَرِّضٌ \n"
            )
        
        @staticmethod
        def HVAC_alarm_info(parsed_data: dict) -> str:
            return (
                f"الكَشْفُ عَنْ وُجُودِ تَنْبِيهٍ فِي نِظَامِ التَّكْيِيفِ المَرْكَزِيِّ: {int(float(parsed_data['HVAC_alarm']))} \n"
            )

        @staticmethod
        def medical_gas_alarm_info(parsed_data: dict) -> str:
            return (
                f"الكَشْفُ عَنْ وُجُودِ تَنْبِيهٍ فِي الغَازِ الطِّبِّيِّ: {int(float(parsed_data['medical_gas_alarm']))} \n"
            )

        @staticmethod
        def fire_fighting_alarm_info(parsed_data: dict) -> str:
            return (
                f"الكَشْفُ عَنْ وُجُودِ تَنْبِيهٍ فِي نِظَامِ الحَرِيقِ: {int(float(parsed_data['fire_fighting_alarm']))} \n"
            )

        @staticmethod
        def transformer_alarm_info(parsed_data: dict) -> str:
            return (
                f"الكَشْفُ عَنْ وُجُودِ تَنْبِيهٍ فِي المُحَوِّلَاتِ: {int(float(parsed_data['transformer_alarm']))} \n"
            )

        @staticmethod
        def elevator_alarm_info(parsed_data: dict) -> str:
            return (
                f"الكَشْفُ عَنْ وُجُودِ تَنْبِيهٍ فِي المَصَاعِدِ: {int(float(parsed_data['elevator_alarm']))} \n"
            )

        @staticmethod
        def F_AHU_ON_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ وَحْدَاتِ مُنَاوَلَةِ الهَوَاءِ العَامِلَةِ: {int(float(parsed_data['F_AHU_ON']))} \n"
            )

        @staticmethod
        def F_AHU_OFF_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ وَحْدَاتِ مُنَاوَلَةِ الهَوَاءِ غَيْرِ العَامِلَةِ: {int(float(parsed_data['F_AHU_OFF']))} \n"
            )

        @staticmethod
        def chiller_on_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ المُبَرِّدَاتِ المَرْكَزِيَّةِ العَامِلَةِ: {int(float(parsed_data['chiller_on']))} \n"
            )

        @staticmethod
        def chiller_off_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ المُبَرِّدَاتِ المَرْكَزِيَّةِ غَيْرِ العَامِلَةِ: {int(float(parsed_data['chiller_off']))} \n"
            )

        @staticmethod
        def monthlyenergy_MVSG_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ اِسْتِهْلَاكِ الطَّاقَةِ الشَّهْرِيِّ المُجَمَّعِ: {float(parsed_data['monthlyenergy_MVSG'])} كِيلُو وَاتِّ سَاعَةٍ\n"
            )

        @staticmethod
        def vaccum_press_info(parsed_data: dict) -> str:
            return (
                f" الضَّغْطِ شَّفْطِ: {float(parsed_data['vaccum_press'])} بَارٍ\n"
            )

        @staticmethod
        def air_4bar_press_info(parsed_data: dict) -> str:
            return (
                f"ضَغْطُ الهَوَاءِ 4 بَارٍ: {float(parsed_data['air_4bar_press'])} بَارٍ\n"
            )

        @staticmethod
        def air_7bar_press_info(parsed_data: dict) -> str:
            return (
                f"ضَغْطُ الهَوَاءِ 7 بَارٍ: {float(parsed_data['air_7bar_press'])} بَارٍ\n"
            )

        @staticmethod
        def oxygen_press_info(parsed_data: dict) -> str:
            return (
                f"ضَغْطُ الأُكْسُجِينِ: {float(parsed_data['oxygen_press'])} بَارٍ\n"
            )

        @staticmethod
        def dailyenergy_MVSG_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ اِسْتِهْلَاكِ الطَّاقَةِ اليَوْمِيِّ لِلْقِيمَةِ الرَّئِيسِيَّةِ لِلْمَصْدَرِ الكَهْرَبَائِيِّ: {float(parsed_data['dailyenergy_MVSG'])} كِيلُو وَاتِّ سَاعَةٍ\n"
            )

        @staticmethod
        def dailyenergy_MVSG_incoming2_energy_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ اِسْتِهْلَاكِ الطَّاقَةِ اليَوْمِيِّ الدَّاخِلَةِ لِلْمَصْدَرِ الكَهْرَبَائِيِّ الثَّانِي: {float(parsed_data['dailyenergy_MVSG_incoming2_energy'])} كِيلُو وَاتِّ سَاعَةٍ\n"
            )

        @staticmethod
        def dailyenergy_MVSG_incoming3_energy_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ اِسْتِهْلَاكِ الطَّاقَةِ اليَوْمِيِّ الدَّاخِلَةِ لِلْمَصْدَرِ الكَهْرَبَائِيِّ الثَّالِثِ: {float(parsed_data['dailyenergy_MVSG_incoming3_energy'])} كِيلُو وَاتِّ سَاعَةٍ\n"
            )

        @staticmethod
        def dailyenergy_Hospital_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ اِسْتِهْلَاكِ الطَّاقَةِ اليَوْمِيِّ لِلْمُسْتَشْفَى: {float(parsed_data['dailyenergy_Hospital'])} كِيلُو وَاتِّ سَاعَةٍ\n"
            )
        @staticmethod
        def dailyenergy_Hospital_GF_info(parsed_data: dict) -> str:
            return (
                f"  مُعَدَّلُ اِسْتِهْلَاكِ الطَّاقَةِ اليَوْمِيِّ للطابق الارضي لْلمُسْتَشْفَى: {float(parsed_data['dailyenergy_Hospital_GF'])} كِيلُو وَاتِّ سَاعَةٍ\n"
            )
        @staticmethod
        def dailyenergy_Hospital_cost_info(parsed_data: dict) -> str:
            return (
                f"  تَّكْلِفَةُ الطَّاقَةِ اليوميه  لْلمُسْتَشْفَى: {float(parsed_data['dailyenergy_Hospital_cost'])} كِيلُو وَاتِّ سَاعَةٍ\n"
            )

        @staticmethod
        def dailyenergy_Clinics_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ اِسْتِهْلَاكِ الطَّاقَةِ اليَوْمِيِّ لِلْعِيَادَاتِ: {float(parsed_data['dailyenergy_Clinics'])} كِيلُو وَاتِّ سَاعَةٍ\n"
            )

        @staticmethod
        def dailyenergy_Utilities_info(parsed_data: dict) -> str:
            return (
                f"اِسْتِهْلَاكُ الطَّاقَةِ اليَوْمِيُّ لِلْمَرَافِقِ: {float(parsed_data['dailyenergy_Utilities'])} كِيلُو وَاتِّ سَاعَةٍ\n"
            )

        @staticmethod
        def dailyenergy_ele_info(parsed_data: dict) -> str:
            return (
                f"اِسْتِهْلَاكُ الطَّاقَةِ اليَوْمِيُّ لِلْكَهْرَبَاءِ: {float(parsed_data['dailyenergy_ele'])} كِيلُو وَاتِّ سَاعَةٍ\n"
            )

        @staticmethod
        def dailyenergy_chillers_info(parsed_data: dict) -> str:
            return (
                f"اِسْتِهْلَاكُ الطَّاقَةِ اليَوْمِيُّ لِلْمُبَرِّدَاتِ: {float(parsed_data['dailyenergy_chillers'])} كِيلُو وَاتِّ سَاعَةٍ\n"
            )

        @staticmethod
        def dailyenergy_AHU_info(parsed_data: dict) -> str:
            return (
                f"اِسْتِهْلَاكُ الطَّاقَةِ اليَوْمِيُّ لِوَحْدَاتِ مُنَاوَلَةِ الهَوَاءِ: {float(parsed_data['dailyenergy_AHU'])} كِيلُو وَاتِّ سَاعَةٍ\n"
            )

        @staticmethod
        def dailyenergy_Boilers_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ اِسْتِهْلَاكِ الطَّاقَةِ اليَوْمِيِّ لِلْغَلَّايَاتِ: {float(parsed_data['dailyenergy_Boilers'])} كِيلُو وَاتِّ سَاعَةٍ\n"
            )

        @staticmethod
        def monthlyenergy_MVSG_incoming2_energy_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ اِسْتِهْلَاكِ الطَّاقَةِ الشَّهْرِيِّ الدَّاخِلَةِ لِلْمَصْدَرِ الكَهْرَبَائِيِّ الثَّانِي: {float(parsed_data['monthlyenergy_MVSG_incoming2_energy'])} كِيلُو وَاتِّ سَاعَةٍ\n"
            )

        @staticmethod
        def monthlyenergy_MVSG_incoming3_energy_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ اِسْتِهْلَاكِ الطَّاقَةِ الشَّهْرِيِّ الدَّاخِلَةِ لِلْمَصْدَرِ الكَهْرَبَائِيِّ الثَّالِثِ: {float(parsed_data['monthlyenergy_MVSG_incoming3_energy'])} كِيلُو وَاتِّ سَاعَةٍ\n"
            )

        @staticmethod
        def monthlyenergy_Hospital_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ اِسْتِهْلَاكِ الطَّاقَةِ الشَّهْرِيِّ لِلْمُسْتَشْفَى: {float(parsed_data['monthlyenergy_Hospital'])} كِيلُو وَاتِّ سَاعَةٍ\n"
            )
        @staticmethod
        def monthlyenergy_Hospital_GF_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ اِسْتِهْلَاكِ الطَّاقَةِ الشَّهْرِيِّ  للطابق الارضي في الْمُسْتَشْفَى: {float(parsed_data['monthlyenergy_Hospital_GF'])} كِيلُو وَاتِّ سَاعَةٍ\n"
            )

        @staticmethod
        def monthlyenergy_Clinics_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ اِسْتِهْلَاكِ الطَّاقَةِ الشَّهْرِيِّ لِلْعِيَادَاتِ: {float(parsed_data['monthlyenergy_Clinics'])} كِيلُو وَاتِّ سَاعَةٍ\n"
            )
        @staticmethod
        def monthlyenergy_cost_hospital_info(parsed_data: dict) -> str:
            return (
                f"تَّكْلِفَةُ الطَّاقَةِ الشَّهْرِيِّة لِلْمُسْتَشْفَى: {float(parsed_data['monthlyenergy_cost_hospital'])} كِيلُو وَاتِّ سَاعَةٍ\n"
            )

        @staticmethod
        def monthlyenergy_Utilities_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ اِسْتِهْلَاكِ الطَّاقَةِ الشَّهْرِيِّ لِلْمَرَافِقِ: {float(parsed_data['monthlyenergy_Utilities'])} كِيلُو وَاتِّ سَاعَةٍ\n"
            )

        @staticmethod
        def monthlyenergy_ele_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ اِسْتِهْلَاكِ الطَّاقَةِ الشَّهْرِيِّ لِلْكَهْرَبَاءِ: {float(parsed_data['monthlyenergy_ele'])} كِيلُو وَاتِّ سَاعَةٍ\n"
            )

        @staticmethod
        def monthlyenergy_chillers_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ اِسْتِهْلَاكِ الطَّاقَةِ الشَّهْرِيِّ لِلْمُبَرِّدَاتِ: {float(parsed_data['monthlyenergy_chillers'])} كِيلُو وَاتِّ سَاعَةٍ\n"
            )

        @staticmethod
        def monthlyenergy_AHU_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ اِسْتِهْلَاكِ الطَّاقَةِ الشَّهْرِيِّ لِوَحْدَاتِ مُنَاوَلَةِ الهَوَاءِ: {float(parsed_data['monthlyenergy_AHU'])} كِيلُو وَاتِّ سَاعَةٍ\n"
            )

        @staticmethod
        def monthlyenergy_Boilers_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ اِسْتِهْلَاكِ الطَّاقَةِ الشَّهْرِيِّ لِلْغَلَّايَاتِ: {float(parsed_data['monthlyenergy_Boilers'])} كِيلُو وَاتِّ سَاعَةٍ\n"
            )

        @staticmethod
        def dailycost_sg_info(parsed_data: dict) -> str:
            return (
                f"التَّكْلِفَةُ اليَوْمِيَّةُ لِلْمَصْدَرِ الكَهْرَبَائِيِّ: {float(parsed_data['dailycost_sg'])} جُنَيْهٍ\n"
            )

        @staticmethod
        def yearlyenergy_MVSG_info(parsed_data: dict) -> str:
            return (
                f"اِسْتِهْلَاكُ الطَّاقَةِ السَّنَوِيُّ لِلْمَصْدَرِ الكَهْرَبَائِيِّ: {float(parsed_data['yearlyenergy_MVSG'])} كِيلُو وَاتِّ سَاعَةٍ\n"
            )

        @staticmethod
        def yearlycost_sg_info(parsed_data: dict) -> str:
            return (
                f"التَّكْلِفَةُ السَّنَوِيَّةُ لِلْمَصْدَرِ الكَهْرَبَائِيِّ: {float(parsed_data['yearlycost_sg'])} جُنَيْهٍ\n"
            )

        @staticmethod
        def monthlycost_g_info(parsed_data: dict) -> str:
            return (
                f"التَّكْلِفَةُ الشَّهْرِيَّةُ لِلطَّابِقِ الأَرْضِيِّ: {float(parsed_data['monthlycost_g'])} جُنَيْهٍ\n"
            )

        @staticmethod
        def monthlycost_f_info(parsed_data: dict) -> str:
            return (
                f"التَّكْلِفَةُ الشَّهْرِيَّةُ لِلطَّابِقِ الأَوَّلِ: {float(parsed_data['monthlycost_f'])} جُنَيْهٍ\n"
            )

        @staticmethod
        def monthlycost_s_info(parsed_data: dict) -> str:
            return (
                f"التَّكْلِفَةُ الشَّهْرِيَّةُ لِلطَّابِقِ الثَّانِي: {float(parsed_data['monthlycost_s'])} جُنَيْهٍ\n"
            )

        @staticmethod
        def monthlycost_th_info(parsed_data: dict) -> str:
            return (
                f"التَّكْلِفَةُ الشَّهْرِيَّةُ لِلطَّابِقِ الثَّالِثِ: {float(parsed_data['monthlycost_th'])} جُنَيْهٍ\n"
            )

        @staticmethod
        def monthlycost_roof_info(parsed_data: dict) -> str:
            return (
                f"التَّكْلِفَةُ الشَّهْرِيَّةُ لِلسُّطُوحِ: {float(parsed_data['monthlycost_roof'])} جُنَيْهٍ\n"
            )

        @staticmethod
        def monthlycost_Hospital_info(parsed_data: dict) -> str:
            return (
                f"التَّكْلِفَةُ الشَّهْرِيَّةُ لِلْمُسْتَشْفَى: {float(parsed_data['monthlycost_Hospital'])} جُنَيْهٍ\n"
            )

        @staticmethod
        def monthlycost_clinic_info(parsed_data: dict) -> str:
            return (
                f"التَّكْلِفَةُ الشَّهْرِيَّةُ لِلْعِيَادَةِ: {float(parsed_data['monthlycost_clinic'])} جُنَيْهٍ\n"
            )

        @staticmethod
        def monthlycost_Utilities_info(parsed_data: dict) -> str:
            return (
                f"التَّكْلِفَةُ الشَّهْرِيَّةُ لِلْمَرَافِقِ: {float(parsed_data['monthlycost_Utilities'])} جُنَيْهٍ\n"
            )

        @staticmethod
        def daily_water_consumption_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ اِسْتِهْلَاكِ المِيَاهِ اليَوْمِيِّ: {float(parsed_data['daily_water_consumption'])} مِتْرٍ مُكَعَّبٍ\n"
            )

        @staticmethod
        def monthly_water_consumption_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ اِسْتِهْلَاكِ المِيَاهِ الشَّهْرِيِّ في المُجَمَّعِ: {float(parsed_data['monthly_water_consumption'])} مِتْرٍ مُكَعَّبٍ\n"
            )
        @staticmethod
        def monthly_water_consumption_hospital_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ اِسْتِهْلَاكِ المِيَاهِ الشَّهْرِيِّ في المُسْتَشْفَى: {float(parsed_data['monthly_water_consumption_hospital'])} مِتْرٍ مُكَعَّبٍ\n"
            )

        @staticmethod
        def daily_water_cost_info(parsed_data: dict) -> str:
            return (
                f"التَّكْلِفَةُ اليَوْمِيَّةُ لِلْمِيَاهِ: {float(parsed_data['daily_water_cost'])} جُنَيْهٍ\n"
            )

        @staticmethod
        def yearly_water_consumption_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ اِسْتِهْلَاكِ المِيَاهِ السَّنَوِيِّ: {float(parsed_data['yearly_water_consumption'])} مِتْرٍ مُكَعَّبٍ\n"
            )

        @staticmethod
        def yearly_water_cost_info(parsed_data: dict) -> str:
            return (
                f"التَّكْلِفَةُ السَّنَوِيَّةُ لِلْمِيَاهِ: {float(parsed_data['yearly_water_cost'])} جُنَيْهٍ\n"
            )

        @staticmethod
        def daily_oxygen_consumption_info(parsed_data: dict) -> str:
            return (
                f"مُعدَّل اسْتِهْلَاكِ الْأُكْسِجِينِ اليومي: {float(parsed_data['daily_oxygen_consumption'])} متر مكعب\n"
            )
       
        @staticmethod
        def daily_oxygen_cost_hospital_info(parsed_data: dict) -> str:
            return (
                f"   تَّكْلِفَةُ الْأُكْسِجِينِ اليومي لِلْمُسْتَشْفَى: {float(parsed_data['daily_oxygen_cost_hospital'])} جُنَيْهٍ \n"
            )
        @staticmethod
        def daily_water_cost_hospital_info(parsed_data: dict) -> str:
            return (
                f"   تَّكْلِفَةُ المِيَاهِ اليوميه لِلْمُسْتَشْفَى: {float(parsed_data['daily_water_cost_hospital'])} جُنَيْهٍ \n"
            )
        @staticmethod
        def daily_water_consumption_hospital_info(parsed_data: dict) -> str:
            return (
                f"   مُعدَّل اسْتِهْلَاكِ  المِيَاهِ اليومي لِلْمُسْتَشْفَى: {float(parsed_data['daily_water_consumption_hospital'])} متر مكعب\n"
            )
        @staticmethod
        def daily_oxygen_consumption_hospital_info(parsed_data: dict) -> str:
            return (
                f" مُعدَّل اسْتِهْلَاكِ الْأُكْسِجِينِ اليومي لِلْمُسْتَشْفَى: {float(parsed_data['daily_oxygen_consumption_hospital'])} متر مكعب\n"
            )
        @staticmethod
        def monthly_oxygen_consumption_hospital_info(parsed_data: dict) -> str:
            return (
                f"مُعدَّل اسْتِهْلَاكِ الْأُكْسِجِينِ الشَّهْرِيَّ في الْمُسْتَشْفَى: {float(parsed_data['monthly_oxygen_consumption_hospital'])} متر مكعب\n"
            )


        @staticmethod
        def monthly_oxygen_consumption_info(parsed_data: dict) -> str:
            return (
                f"مُعدَّل اسْتِهْلَاكِ الْأُكْسِجِينِ الشَّهْرِيَّ في الْمُجَمَّعِ: {float(parsed_data['monthly_oxygen_consumption'])} متر مكعب\n"
            )
       
        @staticmethod
        def daily_oxygen_cost_info(parsed_data: dict) -> str:
            return (
                f"التَّكْلِفَةُ اليومية للْأُكْسِجِينِ: {float(parsed_data['daily_oxygen_cost'])} جنيه\n"
            )

        @staticmethod
        def yearly_oxygen_consumption_info(parsed_data: dict) -> str:
            return (
                f"مُعدَّل اسْتِهْلَاكِ الْأُكْسِجِينِ السنوي: {float(parsed_data['yearly_oxygen_consumption'])} متر مكعب\n"
            )

        @staticmethod
        def yearly_oxygen_cost_info(parsed_data: dict) -> str:
            return (
                f"التَّكْلِفَةُ السَّنَوِيَّةُ للْأُكْسِجِينِ: {float(parsed_data['yearly_oxygen_cost'])} جنيه\n"
            )

        @staticmethod
        def gen1_status_info(parsed_data: dict) -> str:
            return (
                f"حالة المولِّد رقم 1: {parsed_data['gen1_status']}\n"
            )

        @staticmethod
        def gen1_engine_runtime_info(parsed_data: dict) -> str:
            return (
                f"وقت تشغيل محرك المولِّد رقم 1: {float(parsed_data['gen1_engine_runtime'])} ساعات\n"
            )

        @staticmethod
        def gen1_solar_info(parsed_data: dict) -> str:
            return (
                f"مخزون السولار للمولِّد رقم 1: {float(parsed_data['gen1_solar'])} كيلووات\n"
            )

        @staticmethod
        def gen1_last_op_info(parsed_data: dict) -> str:
            return (
                f"آخر عملية تشغيل للمولِّد رقم 1: {parsed_data['gen1_last_op']}\n"
            )

        @staticmethod
        def gen1_bv_info(parsed_data: dict) -> str:
            return (
                f"معدل جهد البطارية للمولِّد رقم 1: {float(parsed_data['gen1_bv'])} فولت\n"
            )

        @staticmethod
        def gen1_volt_info(parsed_data: dict) -> str:
            return (
                f"معدل جهد المولِّد رقم 1: {float(parsed_data['gen1_volt'])} فولت\n"
            )

        @staticmethod
        def gen1_curr_info(parsed_data: dict) -> str:
            return (
                f"تيار المولِّد رقم 1: {float(parsed_data['gen1_curr'])} أمبير\n"
            )

        @staticmethod
        def gen1_energy_info(parsed_data: dict) -> str:
            return (
                f"طاقة المولِّد رقم 1: {float(parsed_data['gen1_energy'])} كيلووات ساعة\n"
            )

        @staticmethod
        def gen1_object_feed1_info(parsed_data: dict) -> str:
            return (
                f"التغذية الْكَهْرَبَائيه للمولِّد رقم 1 للطابق الأول: {parsed_data['gen1_object_feed1']} كيلووات ساعة\n"
            )

        @staticmethod
        def gen1_object_feed2_info(parsed_data: dict) -> str:
            return (
                f"التغذية الْكَهْرَبَائيه للمولِّد رقم 1 للطابق الثاني: {parsed_data['gen1_object_feed2']} كيلووات ساعة\n"
            )

        @staticmethod
        def gen1_object_feed3_info(parsed_data: dict) -> str:
            return (
                f"التغذية الْكَهْرَبَائيه للمولِّد رقم 1 للطابق الثالث: {parsed_data['gen1_object_feed3']} كيلووات ساعة\n"
            )

        @staticmethod
        def gen1_rated_feed_info(parsed_data: dict) -> str:
            return (
                f"التغذية المقدَّرة للمولِّد رقم 1: {parsed_data['gen1_rated_feed']} كيلووات ساعة\n"
            )

        @staticmethod
        def gen1_estimated_feed_time_info(parsed_data: dict) -> str:
            return (
                f"وقت التغذية المتوقع للمولِّد رقم 1: {parsed_data['gen1_estimated_feed_time']} ساعات\n"
            )

        @staticmethod
        def chiller1_status_info(parsed_data: dict) -> str:
            return (
                f"حالة المبرد رقم 1: {parsed_data['chiller1_status']}\n"
            )

        @staticmethod
        def chiller1_supply_temp_info(parsed_data: dict) -> str:
            return (
                f"درجة حرارة الإمداد من المبرد رقم 1: {float(parsed_data['chiller1_supply_temp'])} درجة مئوية\n"
            )

        @staticmethod
        def chiller1_return_temp_info(parsed_data: dict) -> str:
            return (
                f"درجة حرارة العائد من المبرد رقم 1: {float(parsed_data['chiller1_return_temp'])} درجة مئوية\n"
            )

        @staticmethod
        def chiller2_status_info(parsed_data: dict) -> str:
            return (
                f"حالة المبرد رقم 2: {parsed_data['chiller2_status']}\n"
            )

        @staticmethod
        def chiller2_supply_temp_info(parsed_data: dict) -> str:
            return (
                f"درجة حرارة الإمداد من المبرد رقم 2: {float(parsed_data['chiller2_supply_temp'])} درجة مئوية\n"
            )

        @staticmethod
        def chiller2_return_temp_info(parsed_data: dict) -> str:
            return (
                f"درجة حرارة العائد من المبرد رقم 2: {float(parsed_data['chiller2_return_temp'])} درجة مئوية\n"
            )

        @staticmethod
        def chiller3_status_info(parsed_data: dict) -> str:
            return (
                f"حالة المبرد رقم 3: {parsed_data['chiller3_status']}\n"
            )

        @staticmethod
        def chiller3_supply_temp_info(parsed_data: dict) -> str:
            return (
                f"درجة حرارة الإمداد من المبرد رقم 3: {float(parsed_data['chiller3_supply_temp'])} درجة مئوية\n"
            )

        @staticmethod
        def chiller3_return_temp_info(parsed_data: dict) -> str:
            return (
                f"درجة حرارة العائد من المبرد رقم 3: {float(parsed_data['chiller3_return_temp'])} درجة مئوية\n"
            )


        @staticmethod
        def chiller3_supply_temp_info(parsed_data: dict) -> str:
            return (
                f"دَرَجَةُ حَرَارَةِ الإِمْدَادِ مِنَ المُبَرِّدِ رَقْمَ 3: {float(parsed_data['chiller3_supply_temp'])} دَرَجَةٌ مِئَوِيَّة\n"
            )

        @staticmethod
        def chiller3_return_temp_info(parsed_data: dict) -> str:
            return (
                f"دَرَجَةُ حَرَارَةِ العَائِدِ مِنَ المُبَرِّدِ رَقْمَ 3: {float(parsed_data['chiller3_return_temp'])} دَرَجَةٌ مِئَوِيَّة\n"
            )

        @staticmethod
        def chiller4_status_info(parsed_data: dict) -> str:
            return (
                f"حَالَةُ المُبَرِّدِ رَقْمَ 4: {parsed_data['chiller4_status']}\n"
            )

        @staticmethod
        def chiller4_supply_temp_info(parsed_data: dict) -> str:
            return (
                f"دَرَجَةُ حَرَارَةِ الإِمْدَادِ مِنَ المُبَرِّدِ رَقْمَ 4: {float(parsed_data['chiller4_supply_temp'])} دَرَجَةٌ مِئَوِيَّة\n"
            )

        @staticmethod
        def chiller4_return_temp_info(parsed_data: dict) -> str:
            return (
                f"دَرَجَةُ حَرَارَةِ العَائِدِ مِنَ المُبَرِّدِ رَقْمَ 4: {float(parsed_data['chiller4_return_temp'])} دَرَجَةٌ مِئَوِيَّة\n"
            )

        @staticmethod
        def chillers_op_hours_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ سَاعَاتِ تَشْغِيلِ جَمِيعِ المُبَرِّدَاتِ: {float(parsed_data['chillers_op_hours'])} سَاعَة\n"
            )

        @staticmethod
        def chiller1_op_hours_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ سَاعَاتِ تَشْغِيلِ المُبَرِّدِ رَقْمَ 1: {float(parsed_data['chiller1_op_hours'])} سَاعَة\n"
            )

        @staticmethod
        def chiller2_op_hours_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ سَاعَاتِ تَشْغِيلِ المُبَرِّدِ رَقْمَ 2: {float(parsed_data['chiller2_op_hours'])} سَاعَة\n"
            )

        @staticmethod
        def chiller3_op_hours_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ سَاعَاتِ تَشْغِيلِ المُبَرِّدِ رَقْمَ 3: {float(parsed_data['chiller3_op_hours'])} سَاعَة\n"
            )

        @staticmethod
        def chiller4_op_hours_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ سَاعَاتِ تَشْغِيلِ المُبَرِّدِ رَقْمَ 4: {float(parsed_data['chiller4_op_hours'])} سَاعَة\n"
            )

        @staticmethod
        def monthlyenergy_chiller1_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ استِهْلاكِ الطَّاقَةِ الشَّهْرِيِّ لِلْمُبَرِّدِ رَقْمَ 1: {float(parsed_data['monthlyenergy_chiller1'])} كِيلُووات سَاعَة\n"
            )

        @staticmethod
        def monthlyenergy_chiller2_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ استِهْلاكِ الطَّاقَةِ الشَّهْرِيِّ لِلْمُبَرِّدِ رَقْمَ 2: {float(parsed_data['monthlyenergy_chiller2'])} كِيلُووات سَاعَة\n"
            )

        @staticmethod
        def monthlyenergy_chiller3_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ استِهْلاكِ الطَّاقَةِ الشَّهْرِيِّ لِلْمُبَرِّدِ رَقْمَ 3: {float(parsed_data['monthlyenergy_chiller3'])} كِيلُووات سَاعَة\n"
            )

        @staticmethod
        def monthlyenergy_chiller4_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ استِهْلاكِ الطَّاقَةِ الشَّهْرِيِّ لِلْمُبَرِّدِ رَقْمَ 4: {float(parsed_data['monthlyenergy_chiller4'])} كِيلُووات سَاعَة\n"
            )

        @staticmethod
        def in_Patients_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ المَرْضَى المقيمين الشهري  فِي المجمع: {int(parsed_data['in_Patients'])} مَرِيض\n"
            )
        @staticmethod
        def in_Patients_hospital_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ المَرْضَى المقيمين الشهري  فِي الْمُسْتَشْفَى: {int(parsed_data['in_Patients_hospital'])} مَرِيض\n"
            )

        @staticmethod
        def out_Patients_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ المَرْضَى الشهري الغير مقيمين في المُجَمَّعِ: {int(parsed_data['out_Patients'])} مَرِيض\n"
            )
        @staticmethod
        def out_Patients_hospital_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ المَرْضَى الشهري الغير مقيمين في الْمُسْتَشْفَى: {int(parsed_data['out_Patients_hospital'])} مَرِيض\n"
            )
        @staticmethod
        def every_department_info(parsed_data: dict) -> str:
            return (
                f"مَعْلُومَاتُ عن عدد المرضي الشهري في كل قسم في المُجَمَّعِ:\n"
                f"عَدَدُ الأَسِرَّةِ الشهري المُسْتَخْدَمَةِ لِغَيْرِ المَرْضَى: {int(float(parsed_data['Inpatient_Beds_used_monthly']))} سَرِيرٍ\n"
                f"عَدَدُ الأَسِرَّةِ الشهري المُسْتَخْدَمَةِ فِي العِنَايَةِ المَرْكَزِيَّةِ لِمَرْضَى القَلْبِ: {int(float(parsed_data['ICU_CCU_Beds_used_monthly']))} سَرِيرٍ\n"
                f"عَدَدُ أَسِرَّةِ الطَّوَارِئِ الشهري المُسْتَخْدَمَةِ: {int(float(parsed_data['Emergency_Beds_used_monthly']))} سَرِيرٍ\n"
                f"عَدَدُ أَسِرَّةِ الحَضَّانَاتِ الشهري المُسْتَخْدَمَةِ: {int(float(parsed_data['Incubators_Beds_used_monthly']))} سَرِيرٍ\n"
            )
        def return_monthly_gas_system_info(parsed_data: dict) -> str:
            return (
                f"مَعْلُومَاتُ عن  نظام الغازات في المُجَمَّعِال:\n"
                f"ضَغْطُ الأُكْسُجِينِ: {float(parsed_data['oxygen_press'])} بَارٍ\n"
                f"ضَغْطُ الهَوَاءِ 7 بَارٍ: {float(parsed_data['air_7bar_press'])} بَارٍ\n"
                f"ضَغْطُ الهَوَاءِ 4 بَارٍ: {float(parsed_data['air_4bar_press'])} بَارٍ\n"
                f" ضَغْطُ هَوَاءِالشَّفْطِ: {float(parsed_data['vaccum_press'])} بَارٍ\n"
            )
        @staticmethod
        def chillers_sys_operation_cost_info(parsed_data: dict) -> str:
            return (
                f"تَكْلِفَةُ تَشْغِيلِ نِظَامِ المُبَرِّدَاتِ: {float(parsed_data['chillers_sys_operation_cost'])} جُنَيْه\n"
            )

        @staticmethod
        def main_temp_info(parsed_data: dict) -> str:
            return (
                f"دَرَجَةُ حَرَارَةِ العَائِدِ الرَّئِيسِيَّةِ مِنَ المُبَرِّدِ: {float(parsed_data['main_return_temp'])} دَرَجَةٌ مِئَوِيَّة\n"
            )

        @staticmethod
        def main_supply_temp_info(parsed_data: dict) -> str:
            return (
                f"دَرَجَةُ حَرَارَةِ الإِمْدَادِ الرَّئِيسِيَّةِ مِنَ المُبَرِّدِ: {float(parsed_data['main_supply_temp'])} دَرَجَةٌ مِئَوِيَّة\n"
            )

        @staticmethod
        def chiller1_maintenance_hours_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ سَاعَاتِ صِيَانَةِ المُبَرِّدِ رَقْمَ 1: {float(parsed_data['chiller1_maintenance_hours'])} سَاعَة\n"
            )

        @staticmethod
        def chiller2_maintenance_hours_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ سَاعَاتِ صِيَانَةِ المُبَرِّدِ رَقْمَ 2: {float(parsed_data['chiller2_maintenance_hours'])} سَاعَة\n"
            )

        @staticmethod
        def chiller3_maintenance_hours_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ سَاعَاتِ صِيَانَةِ المُبَرِّدِ رَقْمَ 3: {float(parsed_data['chiller3_maintenance_hours'])} سَاعَة\n"
            )

        @staticmethod
        def chiller4_maintenance_hours_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ سَاعَاتِ صِيَانَةِ المُبَرِّدِ رَقْمَ 4: {float(parsed_data['chiller4_maintenance_hours'])} سَاعَة\n"
            )

        @staticmethod
        def daily_index_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ المُؤَشِّرِ اليَوْمِيِّ: {float(parsed_data['daily_index'])}\n"
            )

        @staticmethod
        def yearly_index_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ المُؤَشِّرِ السَّنَوِيِّ: {float(parsed_data['yearly_index'])}\n"
            )

        @staticmethod
        def monthly_index_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ المُؤَشِّرِ الشَّهْرِيِّ: {float(parsed_data['monthly_index'])}\n"
            )

        @staticmethod
        def random_MVSG_2_energy_info(parsed_data: dict) -> str:
            return (
                f"طَاقَةُ المَصْدَرِ الكَهْرَبَائِيِّ الثَّانِيِّ العَشْوَائِيَّةُ: {float(parsed_data['random_MVSG_2_energy'])} كِيلُووات سَاعَة\n"
            )

        @staticmethod
        def random_MVSG_3_energy(parsed_data: dict) -> str:
            return (
                f"طَاقَةُ المَصْدَرِ الكَهْرَبَائِيِّ الثَّالِثِ العَشْوَائِيَّةُ: {float(parsed_data['random_MVSG_3_energy'])} كِيلُووات سَاعَة\n"
            )

        @staticmethod
        def updated_at_info(parsed_data: dict) -> str:
            return (
                f"تَارِيخُ التَّحْدِيثِ: {parsed_data['updated_at']}\n"
            )

        @staticmethod
        def gen2_status_info(parsed_data: dict) -> str:
            return (
                f"حَالَةُ المُوَلِّدِ رَقْمَ 2: {parsed_data['gen2_status']}\n"
            )

        @staticmethod
        def gen2_engine_runtime_info(parsed_data: dict) -> str:
            return (
                f"وَقْتُ تَشْغِيلِ مُحَرِّكِ المُوَلِّدِ رَقْمَ 2: {float(parsed_data['gen2_engine_runtime'])} سَاعَة\n"
            )

        @staticmethod
        def gen2_solar_info(parsed_data: dict) -> str:
            return (
                f"مَخْزُونُ الطَّاقَةِ الشَّمْسِيَّةِ لِلْمُوَلِّدِ رَقْمَ 2: {float(parsed_data['gen2_solar'])} كِيلُووات\n"
            )

        @staticmethod
        def gen2_last_op_info(parsed_data: dict) -> str:
            return (
                f"آخِرُ عَمَلِيَّةِ تَشْغِيلٍ لِلْمُوَلِّدِ رَقْمَ 2: {parsed_data['gen2_last_op']}\n"
            )

        @staticmethod
        def gen2_bv_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ جُهْدِ البَطَّارِيَّةِ لِلْمُوَلِّدِ رَقْمَ 2: {float(parsed_data['gen2_bv'])} فُولْت\n"
            )

        @staticmethod
        def gen2_volt_info(parsed_data: dict) -> str:
            return (
                f"مُعَدَّلُ جُهْدِ المُوَلِّدِ رَقْمَ 2: {float(parsed_data['gen2_volt'])} فُولْت\n"
            )

        @staticmethod
        def gen2_curr_info(parsed_data: dict) -> str:
            return (
                f"تِيَّارُ المُوَلِّدِ رَقْمَ 2: {float(parsed_data['gen2_curr'])} أَمْبِير\n"
            )

        @staticmethod
        def gen2_energy_info(parsed_data: dict) -> str:
            return (
                f"طَاقَةُ المُوَلِّدِ رَقْمَ 2: {float(parsed_data['gen2_energy'])} كِيلُووات سَاعَة\n"
            )

        @staticmethod
        def gen2_object_feed1_info(parsed_data: dict) -> str:
            return (
                f"التَّغْذِيَةُ الكَهْرَبَائِيَّةُ لِلْطَابِقِ الأَوَّلِ لِلْمُوَلِّدِ رَقْمَ 2: {parsed_data['gen2_object_feed1']} كِيلُووات سَاعَة\n"
            )

        @staticmethod
        def gen2_object_feed2_info(parsed_data: dict) -> str:
            return (
                f"التَّغْذِيَةُ الكَهْرَبَائِيَّةُ لِلْطَابِقِ الثَّانِيِّ لِلْمُوَلِّدِ رَقْمَ 2: {parsed_data['gen2_object_feed2']} كِيلُووات سَاعَة\n"
            )

        @staticmethod
        def gen2_object_feed3_info(parsed_data: dict) -> str:
            return (
                f"التَّغْذِيَةُ الكَهْرَبَائِيَّةُ لِلْطَابِقِ الثَّالِثِ لِلْمُوَلِّدِ رَقْمَ 2: {parsed_data['gen2_object_feed3']} كِيلُووات سَاعَة\n"
            )

        @staticmethod
        def gen2_rated_feedv(parsed_data: dict) -> str:
            return (
                f"التَّغْذِيَةُ المُقَدَّرَةُ لِلْمُوَلِّدِ رَقْمَ 2: {parsed_data['gen2_rated_feed']} كِيلُووات سَاعَة\n"
            )

        @staticmethod
        def gen2_estimated_feed_time_info(parsed_data: dict) -> str:
            return (
                f"وَقْتُ التَّغْذِيَةِ المُتَوَقَّعُ لِلْمُوَلِّدِ رَقْمَ 2: {parsed_data['gen2_estimated_feed_time']} سَاعَة\n"
            )

        @staticmethod
        def air_4bar_percentage_info(parsed_data: dict) -> str:
            return (
                f"نِسْبَةُ ضَغْطِ الهَوَاءِ 4 بَار: {float(parsed_data['air_4bar_percentage'])} %\n"
            )

        @staticmethod
        def air_7bar_percentage_info(parsed_data: dict) -> str:
            return (
                f"نِسْبَةُ ضَغْطِ الهَوَاءِ 7 بَار: {float(parsed_data['air_7bar_percentage'])} %\n"
            )

        @staticmethod
        def vaccum_percentage_info(parsed_data: dict) -> str:
            return (
                f"نِسْبَةُ ضَغْطِ السَّحْبِ: {float(parsed_data['vaccum_percentage'])} %\n"
            )

        @staticmethod
        def oxygen_percentage_info(parsed_data: dict) -> str:
            return (
                f"نِسْبَةُ ضَغْطِ الأُكْسِيجِينِ: {float(parsed_data['oxygen_percentage'])} %\n"
            )

        @staticmethod
        def no_of_surgry_month_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ العَمَلِيَّاتِ الجِرَاحِيَّةِ فِي الشَّهْرِ: {int(parsed_data['no_of_surgry_month'])} عَمَلِيَّة\n"
            )

        @staticmethod
        def no_of_dialysis_month_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ عَمَلِيَّاتِ غَسِيلِ الكُلَى فِي الشَّهْرِ: {int(parsed_data['no_of_dialysis_month'])} عَمَلِيَّة\n"
            )

        @staticmethod
        def no_of_xrays_month_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ الأَشِعَّةِ السِّينِيَّةِ فِي الشَّهْرِ: {int(parsed_data['no_of_xrays_month'])} أَشِعَّة\n"
            )

        @staticmethod
        def Inpatient_Beds_used_monthly_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ الأَسِرَّةِ المُسْتَخْدَمَةِ لِلْمَرْضَى المُقِيمِينَ شَهْرِيًّا: {int(parsed_data['Inpatient_Beds_used_monthly'])} سَرِير\n"
            )

        @staticmethod
        def Inpatient_Beds_unused_monthly_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ الأَسِرَّةِ غَيْرِ المُسْتَخْدَمَةِ لِلْمَرْضَى المُقِيمِينَ شَهْرِيًّا: {int(parsed_data['Inpatient_Beds_unused_monthly'])} سَرِير\n"
            )

        @staticmethod
        def ICU_CCU_Beds_used_monthly_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ الأَسِرَّةِ المُسْتَخْدَمَةِ فِي العِنَايَةِ المُرَكَّزَةِ لِمَرْضَى القَلْبِ شَهْرِيًّا: {int(parsed_data['ICU_CCU_Beds_used_monthly'])} سَرِير\n"
            )

        @staticmethod
        def ICU_CCU_Beds_unused_monthly_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ الأَسِرَّةِ غَيْرِ المُسْتَخْدَمَةِ فِي العِنَايَةِ المُرَكَّزَةِ لِمَرْضَى القَلْبِ شَهْرِيًّا: {int(parsed_data['ICU_CCU_Beds_unused_monthly'])} سَرِير\n"
            )

        @staticmethod
        def Emergency_Beds_used_monthly_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ الأَسِرَّةِ المُسْتَخْدَمَةِ فِي الطَّوَارِئِ شَهْرِيًّا: {int(parsed_data['Emergency_Beds_used_monthly'])} سَرِير\n"
            )

        @staticmethod
        def Emergency_Beds_unused_monthly_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ الأَسِرَّةِ غَيْرِ المُسْتَخْدَمَةِ فِي الطَّوَارِئِ شَهْرِيًّا: {int(parsed_data['Emergency_Beds_unused_monthly'])} سَرِير\n"
            )

        @staticmethod
        def Incubators_Beds_unused_monthly_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ الأَسِرَّةِ غَيْرِ المُسْتَخْدَمَةِ فِي الحَاضِنَاتِ شَهْرِيًّا: {int(parsed_data['Incubators_Beds_unused_monthly'])} سَرِير\n"
            )

        @staticmethod
        def Incubators_Beds_used_monthly_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ الأَسِرَّةِ المُسْتَخْدَمَةِ فِي الحَاضِنَاتِ شَهْرِيًّا: {int(parsed_data['Incubators_Beds_used_monthly'])} سَرِير\n"
            )

        @staticmethod
        def no_of_pepole_cam1_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ الأَشْخَاصِ الظَّاهِرِينَ فِي الكَامِيرَا رَقْمَ 1: {int(parsed_data['no_of_pepole_cam1'])} شَخْص\n"
            )

        @staticmethod
        def no_of_pepole_cam2_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ الأَشْخَاصِ الظَّاهِرِينَ فِي الكَامِيرَا رَقْمَ 2: {int(parsed_data['no_of_pepole_cam2'])} شَخْص\n"
            )

        @staticmethod
        def no_of_pepole_cam3_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ الأَشْخَاصِ الظَّاهِرِينَ فِي الكَامِيرَا رَقْمَ 3: {int(parsed_data['no_of_pepole_cam3'])} شَخْص\n"
            )

        @staticmethod
        def no_of_pepole_cam4_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ الأَشْخَاصِ الظَّاهِرِينَ فِي الكَامِيرَا رَقْمَ 4: {int(parsed_data['no_of_pepole_cam4'])} شَخْص\n"
            )

        @staticmethod
        def daily_carbon_foot_print_info(parsed_data: dict) -> str:
            return (
                f"البَصْمَةُ الكَرْبُونِيَّةُ اليَوْمِيَّةُ: {float(parsed_data['daily_carbon_foot_print'])} كِيلُوجرام/مِتْر مُرَبَّع\n"
            )

        @staticmethod
        def monthly_carbon_foot_print_info(parsed_data: dict) -> str:
            return (
                f"البَصْمَةُ الكَرْبُونِيَّةُ الشَّهْرِيَّةُ: {float(parsed_data['monthly_carbon_foot_print'])} كِيلُوجرام/مِتْر مُرَبَّع\n"
            )
        @staticmethod
        def in_patients_GF_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ المَرْضَى المُقِيمِينَ في الطَّابِقِ الأَرْضِيِّ لِلْمُسْتَشْفَى: {float(parsed_data['in_patients_GF'])} مريض \n"
            )
        @staticmethod
        def out_patients_GF_info(parsed_data: dict) -> str:
            return (
                f"عَدَدُ المَرْضَى غَيْرِ المُقِيمِينَ في الطَّابِقِ الأَرْضِيِّ لِلْمُسْتَشْفَى: {float(parsed_data['out_patients_GF'])} مريض\n"
            )
        @staticmethod
        def monthlyenergy_g_info(parsed_data: dict) -> str:
            return (
                f"اِسْتِهْلَاكُ الكَهْرَبَاءِ الشَّهْرِي بِالطَّابِقِ الأَرْضِيِّ لِلْمُسْتَشْفَى : {float(parsed_data['monthlyenergy_g'])} كِيلُووات سَاعَة\n"
            )
        @staticmethod
        def energy_dental_xray_info(parsed_data: dict) -> str:
            return (
                f"اِسْتِهْلَاكُ الكَهْرَبَاءِ الشَّهْرِيُّ في قِسْمِ الأَشِعَّةِ السِّينِيَّةِ بِالطَّابِقِ الأَرْضِيِّ: {float(parsed_data['energy_dental_xray'])} كِيلُووات سَاعَة\n"
            )
        @staticmethod
        def cost_dental_xray_info(parsed_data: dict) -> str:
            return (
                f"التَّكْلِفَةُ الشَّهْرِيَّةُ لِلْكَهْرَبَاءِ في قِسْمِ الأَشِعَّةِ السِّينِيَّةِ بِالطَّابِقِ الأَرْضِيِّ: {float(parsed_data['cost_dental_xray'])} جُنَيْه\n"
            )
        @staticmethod
        def energy_radiology_lab_info(parsed_data: dict) -> str:
            return (
                f"اِسْتِهْلَاكُ الكَهْرَبَاءِ الشَّهْرِيُّ في قِسْمِ الأَشِعَّةِ وَالمُخْتَبَرِ بِالطَّابِقِ الأَرْضِيِّ: {float(parsed_data['energy_radiology_lab'])} كِيلُووات سَاعَة\n"
            )
        @staticmethod
        def cost_radiology_lab_info(parsed_data: dict) -> str:
            return (
                f"لتَّكْلِفَةُ الشَّهْرِيَّةُ لِلْكَهْرَبَاءِ في قِسْمِ الأَشِعَّةِ وَالمُخْتَبَرِ بِالطَّابِقِ الأَرْضِيِّ: {float(parsed_data['cost_radiology_lab'])} جُنَيْه\n"
            )
        @staticmethod
        def energy_bio_tanks_info(parsed_data: dict) -> str:
            return (
                f"اِسْتِهْلَاكُ الكَهْرَبَاءِ الشَّهْرِيُّ في قِسْمِ الخَزَّانَاتِ وَالمُعِدَّاتِ بِالطَّابِقِ الأَرْضِيِّ: {float(parsed_data['energy_bio_tanks'])}كِيلُووات سَاعَة\n"
            )
        @staticmethod
        def cost_bio_tanks_info(parsed_data: dict) -> str:
            return (
                f"التَّكْلِفَةُ الشَّهْرِيَّةُ لِلْكَهْرَبَاءِ في قِسْمِ الخَزَّانَاتِ وَالمُعِدَّاتِ بِالطَّابِقِ الأَرْضِيِّ: {float(parsed_data['cost_bio_tanks'])} جُنَيْه\n"
            )
        @staticmethod
        def energy_triage_info(parsed_data: dict) -> str:
            return (
                f"اِسْتِهْلَاكُ الكَهْرَبَاءِ الشَّهْرِيُّ في قِسْمِ الطَّوَارِئِ وَالإِنْعَاشِ بِالطَّابِقِ الأَرْضِيِّ: {float(parsed_data['energy_triage'])} كِيلُووات سَاعَة\n"
            )
        @staticmethod
        def cost_triage_info(parsed_data: dict) -> str:
            return (
                f"التَّكْلِفَةُ الشَّهْرِيَّةُ لِلْكَهْرَبَاءِ في قِسْمِ الطَّوَارِئِ وَالإِنْعَاشِ بِالطَّابِقِ الأَرْضِيِّ: {float(parsed_data['cost_triage'])} جُنَيْه\n"
            )
        @staticmethod
        def energy_administration_info(parsed_data: dict) -> str:
            return (
                f"اِسْتِهْلَاكُ الكَهْرَبَاءِ الشَّهْرِيُّ في قِسْمِ الإِدَارَةِ بِالطَّابِقِ الأَرْضِيِّ: {float(parsed_data['energy_administration'])} كِيلُووات سَاعَة\n"
            )
        @staticmethod
        def cost_administration_info(parsed_data: dict) -> str:
            return (
                f"التَّكْلِفَةُ الشَّهْرِيَّةُ لِلْكَهْرَبَاءِ في قِسْمِ الإِدَارَةِ التَّكْلِفَةُ الشَّهْرِيَّةُ لِلْكَهْرَبَاءِ في قِسْمِ الإِدَارَةِ بِالطَّابِقِ الأَرْضِيِّ: {float(parsed_data['cost_administration'])} جُنَيْه\n"
            )
        @staticmethod
        def carbon_foot_print_GF_info(parsed_data: dict) -> str:
            return (
                f" البَصْمَةُ الكَرْبُونِيَّةُ الشَّهْرِيَّة  بِالطَّابِقِ الأَرْضِيِّ: {float(parsed_data['carbon_foot_print_GF'])} كِيلُوجرام/مِتْر مُرَبَّع\n"
            )

        @staticmethod
        def invoices_information_info(parsed_data: dict) -> str:
            return (
                f"مَعْلُومَاتُ الفَوَاتِيرِ الشَّهْرِيَّةِ:\n"
                f"تَكْلِفَةُ المِيَاهِ الشَّهْرِيَّةِ: {int(float(parsed_data['monthly_water_cost']))} جُنَيْه\n"
                f"تَكْلِفَةُ الأُكْسِيجِينِ الشَّهْرِيَّةِ: {int(float(parsed_data['monthly_oxygen_cost']))} جُنَيْه\n\n"
                f"تَكْلِفَةُ الكَهْرَبَاءِ الشَّهْرِيَّةِ: {int(float(parsed_data['monthlycost_sg']))} جُنَيْه\n\n"
            )

                
        @staticmethod
        def return_complex_report_info(parsed_data: dict) -> str:
            
            """
            Generate and return station report based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about the station.

            Returns:
            str: A string containing the station report.
            """
            report = ""

            report += SuezMedicalComplexConfigurator.Home.return_Beds_occupancy_rate_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.return_Inpatient_Beds_used_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.return_Inpatient_Beds_Unused_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.return_ICU_CCU_Beds_used_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.return_ICU_CCU_Beds_Unused_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.return_Emergency_Beds_used_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.return_Emergency_Beds_Unused_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.return_Incubators_Beds_used_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.return_Incubators_Beds_unused_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.return_Total_Hospital_Beds_used_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.return_Total_Hospital_Beds_unused_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.return_monthlycost_sg_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.return_monthly_water_cost_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.return_monthly_water_cost_hospital_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.return_monthly_oxygen_cost_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.return_monthly_oxygen_cost_hospital_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.return_Hospital_Occupancy_Rate_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.return_Clinic_Occupancy_Rate_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.Mask_Policy_Violations_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.Social_Distance_Violations_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.NuOF_Detected_Falls_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.transformer_on_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.transformer_Off_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.generator_on_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.generator_off_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.Elevator_on_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthly_total_cost_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.any_alarm_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.HVAC_alarm_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.medical_gas_alarm_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.fire_fighting_alarm_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.transformer_alarm_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.elevator_alarm_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.F_AHU_ON_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.F_AHU_OFF_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.chiller_on_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.chiller_off_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthlyenergy_MVSG_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.vaccum_press_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.air_4bar_press_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.air_7bar_press_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.oxygen_press_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.dailyenergy_MVSG_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.dailyenergy_MVSG_incoming2_energy_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.dailyenergy_MVSG_incoming3_energy_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.dailyenergy_Hospital_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.dailyenergy_Hospital_GF_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.dailyenergy_Hospital_cost_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.dailyenergy_Clinics_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.dailyenergy_Utilities_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.dailyenergy_ele_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.dailyenergy_chillers_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.dailyenergy_AHU_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.dailyenergy_Boilers_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthlyenergy_MVSG_incoming2_energy_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthlyenergy_MVSG_incoming3_energy_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthlyenergy_Hospital_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthlyenergy_Hospital_GF_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthlyenergy_cost_hospital_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthlyenergy_Clinics_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthlyenergy_Utilities_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthlyenergy_ele_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthlyenergy_chillers_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthlyenergy_AHU_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthlyenergy_Boilers_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.dailycost_sg_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.yearlyenergy_MVSG_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.yearlycost_sg_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthlycost_g_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthlycost_f_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthlycost_s_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthlycost_th_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthlycost_roof_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthlycost_Hospital_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthlycost_clinic_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthlycost_Utilities_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.daily_water_consumption_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthly_water_consumption_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthly_water_consumption_hospital_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.daily_water_cost_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.yearly_water_consumption_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.yearly_water_cost_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.daily_oxygen_consumption_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.daily_oxygen_consumption_hospital_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.daily_water_consumption_hospital_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.daily_oxygen_cost_hospital_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.daily_water_cost_hospital_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthly_oxygen_consumption_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthly_oxygen_consumption_hospital_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.daily_oxygen_cost_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.yearly_oxygen_consumption_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.yearly_oxygen_cost_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.gen1_status_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.gen1_engine_runtime_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.gen1_solar_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.gen1_last_op_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.gen1_bv_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.gen1_volt_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.gen1_curr_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.gen1_energy_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.gen1_object_feed1_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.gen1_object_feed2_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.gen1_object_feed3_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.gen1_rated_feed_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.gen1_estimated_feed_time_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.chiller1_status_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.chiller1_supply_temp_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.chiller1_temp_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.chiller2_status_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.chiller2_supply_temp_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.chiller2_temp_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.chiller3_status_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.chiller3_supply_temp_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.chiller3_temp_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.chiller4_status_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.chiller4_supply_temp_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.chiller4_temp_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.chillers_op_hours_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.chiller1_op_hours_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.chiller2_op_hours_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.chiller3_op_hours_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.chiller4_op_hours_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthlyenergy_chiller1_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthlyenergy_chiller2_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthlyenergy_chiller3_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthlyenergy_chiller4_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.in_Patients_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.in_Patients_hospital_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.out_Patients_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.out_Patients_hospital_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.chillers_sys_operation_cost_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.main_temp_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.main_supply_temp_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.chiller1_maintenance_hours_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.chiller2_maintenance_hours_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.chiller3_maintenance_hours_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.chiller4_maintenance_hours_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.daily_index_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.yearly_index_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthly_index_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.random_MVSG_2_energy_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.random_MVSG_3_energy_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.updated_at_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.gen2_status_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.gen2_curr_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.gen2_energy_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.gen2_object_feed1_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.gen2_object_feed2_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.gen2_object_feed3_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.gen2_estimated_feed_time_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.air_4bar_percentage_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.air_7bar_percentage_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.vaccum_percentage_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.oxygen_percentage_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.no_of_surgry_month_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.no_of_dialysis_month_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.no_of_xrays_month_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.Inpatient_Beds_used_monthly_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.Inpatient_Beds_unused_monthly_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.ICU_CCU_Beds_used_monthly_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.ICU_CCU_Beds_unused_monthly_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.Emergency_Beds_used_monthly_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.Emergency_Beds_unused_monthly_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.Incubators_Beds_unused_monthly_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.Incubators_Beds_used_monthly_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.no_of_pepole_cam1_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.no_of_pepole_cam2_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.no_of_pepole_cam3_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.no_of_pepole_cam4_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.daily_carbon_foot_print_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthly_carbon_foot_print_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.invoices_information_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.every_department_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.return_carbon_foot_Hospital(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.return_monthly_gas_system_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.return_carbon_foot_Utilites(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.return_carbon_foot_Clinics(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.temp_inside_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.temp_outside_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.total_complex_staff_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.in_patients_GF_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.out_patients_GF_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.monthlyenergy_g_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.cost_dental_xray_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.energy_dental_xray_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.energy_radiology_lab_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.cost_radiology_lab_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.energy_bio_tanks_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.cost_bio_tanks_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.energy_triage_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.cost_triage_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.energy_administration_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.cost_administration_info(parsed_data)
            report += SuezMedicalComplexConfigurator.Home.carbon_foot_print_GF_info(parsed_data)
            


            return report
        
       



class CommonConfigurator(object):

    @staticmethod
    def return_welcome_message(parsed_data: dict, station_name:str) -> str:
        """
        Return the welcome message when asked about irrelevant topic.

        Args:
        None
        Returns:
        str: A string containing the message.
        """
        return "أَهْلاً بِكَ فِي نِظَامِ زيتًا " + station_name
    
    @staticmethod
    def fetch_station_data(station_url:str) -> dict:
        """
        Fetches data from a given station URL.

        Args:
            station_url (str): The URL of the station to fetch data from.

        Returns:
            dict: The parsed data obtained from the station.

        Raises:
            Exception: If there is an error while fetching data from the station.
        """
        response = requests.get(station_url, verify=False)
        if response.status_code == 200:
            parsed_data = json.loads(response.text)
            return parsed_data
        else:
            raise Exception(f"Error: Unable to fetch data. Status code: {response.status_code}")
        
    @staticmethod
    def generate_random_name(length=6):
        """
        Generate a random name for a file.

        Args:
        - length (int): Length of the random name. Default is 10.

        Returns:
        - str: Random name for the file.
        """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))
    
    @staticmethod
    def return_other_message(parsed_data: dict) -> str:
        """
        Generate and return the message when asked about irrelevant topic.

        Args:
        None
        Returns:
        str: A string containing the message.
        """
        return "الرجاء توجيه الأسئلة ذات الصلة إلى منصة زِيتَا. في حال عدم الفهم، يُرجى إعادة صياغة السؤال."
        
    @staticmethod
    def zeeta_info(parsed_data: dict) -> str:
        """
        Generate and return the message giving general info about zeeta
        
        Args:
        None
        Returns:
        str: A string containing the message.
        """
        return "زيتا هو نظام الذكاء الصناعي الاول الذي يعمل للمساعدة في اتخاذ القرارات المتعلقة بالبنيط التحتية"

class StationTwoConfigurator(object):
    class Home:
        @staticmethod
        def return_transformers_info(parsed_data: dict) -> str:
            return (
                f"معلومات المحولات:\n"
                f"عدد المحولات التي تعمل : {int(float(parsed_data['transformer_on']))} محولات\n"
                f"عدد المحولات التي لا تعمل : {int(float(parsed_data['transformer_off']))} محولات\n\n"
            )
        
        @staticmethod
        def return_working_transformers_info(parsed_data: dict) -> str:
            return (
                f"معلومات المحولات:\n"
                f"عدد المحولات التي تعمل : {int(float(parsed_data['transformer_on']))} محولات\n\n"
            )
        
        @staticmethod
        def return_not_working_transformers_info(parsed_data: dict) -> str:
            return (
                f"معلومات المحولات:\n"
                f"عدد المحولات التي لا تعمل : {int(float(parsed_data['transformer_off']))} محولات\n\n"
            )

        @staticmethod
        def return_generators_info(parsed_data: dict) -> str:
            return (
                f"معلومات المولدات:\n"
                f"عدد المولدات التي تعمل : {int(float(parsed_data['generator_on']))} مولدات\n"
                f"عدد المولدات التي لا تعمل : {int(float(parsed_data['generator_off']))} مولدات\n\n"
            )
        
        @staticmethod
        def return_working_generators_info(parsed_data: dict) -> str:
            return (
                f"عدد المولدات التي تعمل : {int(float(parsed_data['generator_on']))} مولدات\n\n"
            )

        @staticmethod
        def return_not_working_generators_info(parsed_data: dict) -> str:
            return (
                f"عدد المولدات التي لا تعمل : {int(float(parsed_data['generator_off']))} مولدات\n\n"
            )

        @staticmethod
        def return_electrical_info(parsed_data: dict) -> str:
            return (
                f"معلومات لوحات الكهرباء:\n"
                f"عدد لوحات الكهرباء التي تعمل : {int(float(parsed_data['ele_on']))} لوحات\n"
                f"عدد لوحات الكهرباء التي لا تعمل : {int(float(parsed_data['ele_off']))} لوحات\n\n"
            )
        
        @staticmethod
        def return_working_electrical_info(parsed_data: dict) -> str:
            return (
                f"عدد لوحات الكهرباء التي تعمل : {int(float(parsed_data['ele_on']))} لوحات\n\n"
            )

        @staticmethod
        def return_not_working_electrical_info(parsed_data: dict) -> str:
            return (
                f"عدد لوحات الكهرباء التي لا تعمل : {int(float(parsed_data['ele_off']))} لوحات\n\n"
            )

        @staticmethod
        def return_system_status_info(parsed_data: dict) -> str:
            return (
                f"معلومات الانذارت:\n"
                f"{'يوجد' if int(float(parsed_data['ele_alarms'])) else 'لا يوجد'} إنذار كهربائي\n\n"
                f"{'يوجد' if int(float(parsed_data['pumps_alarms'])) else 'لا يوجد'} إنذار مضخات\n\n"
                f"{'يوجد' if int(float(parsed_data['valves_alarms'])) else 'لا يوجد'} إنذار محابس\n\n"
                f"{'يوجد' if int(float(parsed_data['hammer_alarms'])) else 'لا يوجد'} إنذار في المطرقة\n\n"
                f"{'يوجد' if int(float(parsed_data['generator_alarms'])) else 'لا يوجد'} إنذار مولدات\n\n"
            )

        @staticmethod
        def return_working_pumps_info(parsed_data: dict) -> str:
            TOTAL_WORKING_GROUP_A = int(float(parsed_data['group_a_on']))
            TOTAL_WORKING_GROUP_B = int(float(parsed_data['group_b_on']))
            TOTAL_WORKING_ALL_GROUPS = TOTAL_WORKING_GROUP_A + TOTAL_WORKING_GROUP_B

            return (
                f"معلومات المضخات:\n"
                f"إجمالي عدد المضخات العاملة في محطة رقم 2 : {TOTAL_WORKING_ALL_GROUPS} مضخات\n"
                f"عدد المضخات العاملة في مجموعة ا: {TOTAL_WORKING_GROUP_A} مضخة\n"
                f"عدد المضخات العاملة في مجموعة ب: {TOTAL_WORKING_GROUP_B} مضخة\n"
            )
        
        @staticmethod
        def return_not_working_pumps_info(parsed_data: dict) -> str:
            TOTAL_NOT_WORKING_GROUP_A = int(float(parsed_data['group_a_off']))
            TOTAL_NOT_WORKING_GROUP_B = int(float(parsed_data['group_b_off']))
            TOTAL_NOT_WORKING_ALL_GROUPS = TOTAL_NOT_WORKING_GROUP_A + TOTAL_NOT_WORKING_GROUP_B

            return (
                f"معلومات المضخات:\n"
                f"إجمالي عدد المضخات الغير عاملة في محطة رقم 2 : {TOTAL_NOT_WORKING_ALL_GROUPS} مضخات\n"
                f"عدد المضخات الغير عاملة في مجموعة ا: {TOTAL_NOT_WORKING_GROUP_A} مضخة\n"
                f"عدد المضخات الغير عاملة في مجموعة ب: {TOTAL_NOT_WORKING_GROUP_B} مضخة\n"
            )
        
        @staticmethod
        def return_group_a_pumps_info(parsed_data: dict) -> str:
            TOTAL_WORKING_GROUP_A = int(float(parsed_data['group_a_on']))
            TOTAL_NOT_WORKING_GROUP_A = int(float(parsed_data['group_a_off']))

            return (
                f"معلومات المضخات في مجموعة ا:\n"
                f"إجمالي عدد المضخات العاملة في مجموعة ا: {TOTAL_WORKING_GROUP_A} مضخة\n"
                f"عدد المضخات الغير عاملة في مجموعة ا: {TOTAL_NOT_WORKING_GROUP_A} مضخة\n"
            )
        
        @staticmethod
        def return_group_b_pumps_info(parsed_data: dict) -> str:
            TOTAL_WORKING_GROUP_B = int(float(parsed_data['group_b_on']))
            TOTAL_NOT_WORKING_GROUP_B = int(float(parsed_data['group_b_off']))

            return (
                f"معلومات المضخات في مجموعة ب:\n"
                f"إجمالي عدد المضخات العاملة في مجموعة ب: {TOTAL_WORKING_GROUP_B} مضخة\n"
                f"عدد المضخات الغير عاملة في مجموعة ب: {TOTAL_NOT_WORKING_GROUP_B} مضخة\n"
            )

        @staticmethod
        def return_pressure_info(parsed_data: dict) -> str:
            return (
                f"معلومات الضغط:\n"
                f"قيمة الضغط في الخط L1400 A هي : {round(float(parsed_data['press_l1400_a']), 1)} بَارْ\n"
                f"قيمة الضغط في الخط L1400 B هي : {round(float(parsed_data['press_l1400_b']), 1)} بَارْ\n"
                f"قيمة الضغط في الخط L1000 هي: {round(float(parsed_data['pressure_l1000']), 1)} بَارْ\n\n"
            )
        
        @staticmethod
        def pressure_l1400_a(parsed_data: dict) -> str:
            return f"قيمة الضغط في الخط L1400 A هي : {round(float(parsed_data['press_l1400_a']), 1)} بَارْ"

        @staticmethod
        def pressure_l1400_b(parsed_data: dict) -> str:
            return f"قيمة الضغط في الخط L1400 B هي : {round(float(parsed_data['press_l1400_b']), 1)} بَارْ"

        @staticmethod
        def pressure_l1000(parsed_data: dict) -> str:
            return f"قيمة الضغط في الخط L1000 هي: {round(float(parsed_data['press_l1000']), 1)} بَارْ"

        @staticmethod
        def return_tanks_info(parsed_data: dict) -> str:
            return (
                f"معلومات الخزانات: \n"
                f"مستوى الخزان 1: {round(float(parsed_data['tank_1']), 1)} امتار\n"
                f"نسبة الخزان 1: {int(float(parsed_data['tank_1_percent']))} % \n"
                f"مستوى الخزان 2: {round(float(parsed_data['tank_2']), 1)} امتار\n"
                f"نسبة الخزان 2: {int(float(parsed_data['tank_2_percent']))} % \n"
            )
        
        @staticmethod
        def return_tank1_info(parsed_data: dict) -> str:
            return (
                f"معلومات الخزان 1:\n"
                f"مستوى الخزان 1: {round(float(parsed_data['tank_1']), 1)} امتار\n"
                f"نسبة الخزان 1: {round(float(parsed_data['tank_1_percent']), 1)} % \n"
            )

        @staticmethod
        def return_tank2_info(parsed_data: dict) -> str:
            return (
                f"معلومات الخزان 2:\n"
                f"مستوى الخزان 2: {round(float(parsed_data['tank_2']), 1)} امتار\n"
                f"نسبة الخزان 2: {round(float(parsed_data['tank_2_percent']), 1)} % \n"
            )
        
        @staticmethod
        def return_station_flow(parsed_data: dict) -> str:
            return f"التدفق في المحطة: {round(float(parsed_data['station_flow']), 1)} لتر/ثانية"

        @staticmethod
        def flow_l1400_a(parsed_data: dict) -> str:
            return f"التدفق في الخط L1400 A: {round(float(parsed_data['flow_l1400_a']), 1)} لتر/ثانية"

        @staticmethod
        def flow_l1400_b(parsed_data: dict) -> str:
            return f"التدفق في الخط L1400 B: {round(float(parsed_data['flow_l1400_b']), 1)} لتر/ثانية"

        @staticmethod
        def flow_l1000(parsed_data: dict) -> str:
            return f"التدفق في الخط L1000: {round(float(parsed_data['flow_l1000']), 1)} لتر/ثانية"
        @staticmethod
        def return_sump_info(parsed_data: dict) -> str:
            return (
                f"معلومات المجمع للمياه:\n"
                f"مستوى مجمع المياه: {round(float(parsed_data['sump_level']), 1)} امتار\n"
                f"نسبة مجمع المياه: {int(float(parsed_data['sump_level_percent']))} % \n"
            )
        
        @staticmethod
        def return_station_report(parsed_data: dict) -> str:
            report = (
                StationTwoConfigurator.Home.return_transformers_info(parsed_data) +
                StationTwoConfigurator.Home.return_generators_info(parsed_data) +
                StationTwoConfigurator.Home.return_electrical_info(parsed_data) +
                StationTwoConfigurator.Home.return_system_status_info(parsed_data) +
                StationTwoConfigurator.Home.return_working_pumps_info(parsed_data) +
                StationTwoConfigurator.Home.return_not_working_pumps_info(parsed_data) +
                StationTwoConfigurator.Home.return_group_a_pumps_info(parsed_data) +
                StationTwoConfigurator.Home.return_group_b_pumps_info(parsed_data) +
                StationTwoConfigurator.Home.return_pressure_info(parsed_data) +
                StationTwoConfigurator.Home.return_tanks_info(parsed_data) +
                StationTwoConfigurator.Home.return_sump_info(parsed_data) +
                StationTwoConfigurator.Home.return_station_flow(parsed_data) +
                StationTwoConfigurator.Home.flow_l1400_a(parsed_data) +
                StationTwoConfigurator.Home.flow_l1400_b(parsed_data) +
                StationTwoConfigurator.Home.flow_l1000(parsed_data)
            )
            return report
        
class StationFourConfigurator(object):
    class Home:
        @staticmethod
        def return_transformers_info(parsed_data: dict) -> str:

            """
            Generate and return information about transformers based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about transformers.

            Returns:
            str: A string containing information about transformers.
            """
            return (
                f"معلومات المحولات:\n"
                f"عدد المحولات التي تعمل : {int(float(parsed_data['transfomers_on']))} محولات\n"
                f"عدد المحولات التي لا تعمل : {int(float(parsed_data['transfomers_off']))} محولات\n\n"
            )
        
        @staticmethod
        def return_working_transformers_info(parsed_data: dict) -> str:

            """
            Generate and return information about working transformers based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about transformers.

            Returns:
            str: A string containing information about transformers.
            """
            return (
                f"معلومات المحولات:\n"
                f"عدد المحولات التي تعمل : {int(float(parsed_data['transformers_on']))} محولات\n\n"
            )
        
        @staticmethod
        def return_not_working_transformers_info(parsed_data: dict) -> str:

            """
            Generate and return information about working transformers based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about transformers.

            Returns:
            str: A string containing information about transformers.
            """
            return (
                f"معلومات المحولات:\n"
                f"عدد المحولات التي لا تعمل : {int(float(parsed_data['transformers_off']))} محولات\n\n"
            )

        @staticmethod
        def return_generators_info(parsed_data: dict) -> str:
            """
            Generate and return information about generators based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about generators.

            Returns:
            str: A string containing information about generators.
            """
            return (
                f"معلومات المولدات:\n"
                f"عدد المولدات التي تعمل : {int(float(parsed_data['generators_on']))} مولدات\n"
                f"عدد المولدات التي لا تعمل : {int(float(parsed_data['generators_off']))} مولدات\n\n"
            )
        
        @staticmethod
        def return_working_generators_info(parsed_data: dict) -> str:
            """
            Generate and return information about working generators based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about generators.

            Returns:
            str: A string containing information about working generators.
            """
            return (
                f"عدد المولدات التي تعمل : {int(float(parsed_data['generators_on']))} مولدات\n\n"
            )

        @staticmethod
        def return_not_working_generators_info(parsed_data: dict) -> str:
            """
            Generate and return information about non-working generators based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about generators.

            Returns:
            str: A string containing information about non-working generators.
            """
            return (
                f"عدد المولدات التي لا تعمل : {int(float(parsed_data['generators_off']))} مولدات\n\n"
            )



        def return_electrical_info(parsed_data: dict) -> str:

            """
            Generate and return information about electrical panels based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about electrical panels.

            Returns:
            str: A string containing information about electrical panels.
            """
            return (
                f"معلومات لوحات الكهرباء:\n"
                f"عدد لوحات الكهرباء التي تعمل : {int(float(parsed_data['ele_on']))} لوحات\n"
                f"عدد لوحات الكهرباء التي لا تعمل : {int(float(parsed_data['ele_off']))} لوحات\n\n"
            )
        @staticmethod
        def return_working_electrical_info(parsed_data: dict) -> str:
            """
            Generate and return information about working electrical panels based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about electrical panels.

            Returns:
            str: A string containing information about working electrical panels.
            """
            return (
                f"عدد لوحات الكهرباء التي تعمل : {int(float(parsed_data['ele_on']))} لوحات\n\n"
            )

        @staticmethod
        def return_not_working_electrical_info(parsed_data: dict) -> str:
            """
            Generate and return information about non-working electrical panels based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about electrical panels.

            Returns:
            str: A string containing information about non-working electrical panels.
            """
            return (
                f"عدد لوحات الكهرباء التي لا تعمل : {int(float(parsed_data['ele_off']))} لوحات\n\n"
            )


        @staticmethod
        def return_system_status_info(parsed_data: dict) -> str:

            """
            Generate and return system status information based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about the system status.

            Returns:
            str: A string containing system status information.
            """
            return (
                f"معلومات الانذارت:\n"
            # f"حالة نظام النقل التلقائي: {int(float(parsed_data['ats_status']))} %\n"
                f"{'يوجد' if int(float(parsed_data['ele_alarms'])) else 'لا يوجد'} إنذار كهربائي\n\n"
                f"{'يوجد' if int(float(parsed_data['pumps_alarms'])) else 'لا يوجد'} إنذار مضخات\n\n"
                f"{'يوجد' if int(float(parsed_data['valves_alarms'])) else 'لا يوجد'} إنذار محابس\n\n"
                f"{'يوجد' if int(float(parsed_data['hammer_alarms'])) else 'لا يوجد'} إنذار في المطرقة\n\n"
                f"{'يوجد' if int(float(parsed_data['generator_alarms'])) else 'لا يوجد'} إنذار مولدات\n\n"
            )

        @staticmethod
        def return_working_pumps_info(parsed_data: dict) -> str:
            """
            Generate and return information about pumps based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about pumps.

            Returns:
            str: A string containing information about pumps.

            """
            TOTAL_WORKING_GROUP_A = int(float(parsed_data['pumps_ga_on']))
            TOTAL_WORKING_GROUP_B = int(float(parsed_data['pumps_gb_on']))
            TOTAL_WORKING_ALL_GROUPS = TOTAL_WORKING_GROUP_A + TOTAL_WORKING_GROUP_B
            print(TOTAL_WORKING_GROUP_A, TOTAL_WORKING_GROUP_B, flush=True)

            return (
                f"معلومات المضخات:\n"
                f"إجمالي عدد المضخات العاملة في محطة رقم 4 : {TOTAL_WORKING_ALL_GROUPS} مضخات\n"
                f"عدد المضخات العاملة في مجموعة ا: {TOTAL_WORKING_GROUP_A} مضخة\n"
                f"عدد المضخات العاملة في مجموعة ب: {TOTAL_WORKING_GROUP_B} مضخة\n"
            )
        
        @staticmethod
        def return_not_working_pumps_info(parsed_data: dict) -> str:
            """
            Generate and return information about pumps based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about pumps.

            Returns:
            str: A string containing information about pumps.
            
            """
            TOTAL_NOT_WORKING_GROUP_A = int(float(parsed_data['pumps_ga_off']))
            TOTAL_NOT_WORKING_GROUP_B = int(float(parsed_data['pumps_gb_on']))
            TOTAL_NOT_WORKING_ALL_GROUPS = TOTAL_NOT_WORKING_GROUP_A + TOTAL_NOT_WORKING_GROUP_B

            return (
                f"معلومات المضخات:\n"
                f"إجمالي عدد المضخات الغير عاملة في محطة رقم 4 : {TOTAL_NOT_WORKING_ALL_GROUPS} مضخات\n"
                f"عدد المضخات الغير عاملة في مجموعة ا: {TOTAL_NOT_WORKING_GROUP_A} مضخة\n"
                f"عدد المضخات الغير عاملة في مجموعة ب: {TOTAL_NOT_WORKING_GROUP_B} مضخة\n"
            )
        
        @staticmethod
        def return_group_a_pumps_info(parsed_data: dict) -> str:
            """
            Generate and return information about group A pumps based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about group A pumps.

            Returns:
            str: A string containing information about group A pumps.
            """
            TOTAL_WORKING_GROUP_A = int(float(parsed_data['pumps_ga_on']))
            TOTAL_NOT_WORKING_GROUP_A = int(float(parsed_data['pumps_ga_off']))

            return (
                f"معلومات المضخات في مجموعة ا:\n"
                f"إجمالي عدد المضخات العاملة في مجموعة ا: {TOTAL_WORKING_GROUP_A} مضخة\n"
                f"عدد المضخات الغير عاملة في مجموعة ا: {TOTAL_NOT_WORKING_GROUP_A} مضخة\n"
            )
        
        @staticmethod
        def return_group_b_pumps_info(parsed_data: dict) -> str:
            """
            Generate and return information about group B pumps based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about group B pumps.

            Returns:
            str: A string containing information about group B pumps.
            """
            TOTAL_WORKING_GROUP_B = int(float(parsed_data['pumps_gb_on']))
            TOTAL_NOT_WORKING_GROUP_B = int(float(parsed_data['pumps_gb_off']))

            return (
                f"معلومات المضخات في مجموعة ب:\n"
                f"إجمالي عدد المضخات العاملة في مجموعة ب: {TOTAL_WORKING_GROUP_B} مضخة\n"
                f"عدد المضخات الغير عاملة في مجموعة ب: {TOTAL_NOT_WORKING_GROUP_B} مضخة\n"
            )


        @staticmethod
        def return_pressure_info(parsed_data: dict) -> str:
            """
            Generate and return information about pressure based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about pressure.

            Returns:
            str: A string containing information about pressure.
            """
            return (
                f"معلومات الضغط:\n"
                f"قيمة الضغط في الخط 1200 ا هي : {round(float(parsed_data['pressure_1200a']), 1)} بَارْ\n"
                f"قيمة الضغط في الخط 1200 ب هي : {round(float(parsed_data['pressure_1200b']), 1)} بَارْ\n"
                f"قيمة الضغط في الخط 1000 ا هي: {round(float(parsed_data['pressure_1000a']), 1)} بَارْ\n\n"
                f"قيمة الضغط في الخط 1000 ب هي: {round(float(parsed_data['pressure_1000b']), 1)} بَارْ\n\n"
            )
        @staticmethod
        def pressure_1200(parsed_data: dict) -> str:
            """
            Return information about pressure at line 1200 based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about pressure.

            Returns:
            str: A string containing information about pressure at line 1200.
            """
            return (
                f"قيمة الضغط في الخط 1200 ا هي : {round(float(parsed_data['pressure_1200a']), 1)} بَارْ\n"
                f"قيمة الضغط في الخط 1200 ب هي : {round(float(parsed_data['pressure_1200b']), 1)} بَارْ\n"
            )
        @staticmethod
        def pressure_1000(parsed_data: dict) -> str:
            """
            Return information about pressure at line 800 based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about pressure.

            Returns:
            str: A string containing information about pressure at line 1000.
            """
            return (
                f"قيمة الضغط في الخط 1000 ا هي: {round(float(parsed_data['pressure_1000a']), 1)} بَارْ\n\n"
                f"قيمة الضغط في الخط 1000 ب هي: {round(float(parsed_data['pressure_1000b']), 1)} بَارْ\n\n"
            )

        @staticmethod
        def return_tanks_info(parsed_data: dict) -> str:
            """
            Generate and return information about all tanks based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about all tank.

            Returns:
            str: A string containing information about all tanks.
            """
            return (
                f"معلومات الخزانات: \n"
                f"مستوى الخزان 1: {round(float(parsed_data['tank1_lvl']), 1)} امتار\n"
                f"نسبة الخزان 1: {int(float(parsed_data['tank1_lvl_centage']))} % \n"
                f"مستوى الخزان 2: {round(float(parsed_data['tank2_lvl']), 1)} امتار\n"
                f"نسبة الخزان 2: {int(float(parsed_data['tank2_lvl_centage']))} % \n"
                f"مستوى الخزان 3: {round(float(parsed_data['tank3_lvl']), 1)} امتار\n"
                f"نسبة الخزان 3: {int(float(parsed_data['tank3_lvl_centage']))} % \n"
            )
        
        @staticmethod
        def return_tank1_info(parsed_data: dict) -> str:
            """
            Generate and return information about tank 1 based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about tank 1.

            Returns:
            str: A string containing information about tank 1.
            """
            return (
                f"معلومات الخزان 1:\n"
                f"مستوى الخزان 1: {round(float(parsed_data['tank1_lvl']), 1)} امتار\n"
                f"نسبة الخزان 1: {round(float(parsed_data['tank1_lvl_centage']), 1)} % \n"
            )


        @staticmethod
        def return_tank2_info(parsed_data: dict) -> str:
            """
            Generate and return information about tank 2 based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about tank 2.

            Returns:
            str: A string containing information about tank 2.
            """
            return (
                f"معلومات الخزان 2:\n"
                f"مستوى الخزان 2: {round(float(parsed_data['tank2_lvl']), 1)} امتار\n"
                f"نسبة الخزان 2: {round(float(parsed_data['tank2_lvl_centage']), 1)} % \n"
            )


        @staticmethod
        def return_tank3_info(parsed_data: dict) -> str:
            """
            Generate and return information about tank 3 based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about tank 3.

            Returns:
            str: A string containing information about tank 3.
            """
            return (
                f"معلومات الخزان 3:\n"
                f"مستوى الخزان 3: {round(float(parsed_data['tank2_lvl']), 1)} امتار\n"
                f"نسبة الخزان 3: {round(float(parsed_data['tank3_lvl_centage']), 1)} % \n"
            )
        
        @staticmethod
        def return_station_flow(parsed_data:dict) -> str:
            """
            This static method returns a string describing the flow rate of water in a station based on parsed data.

            Args:
            - parsed_data (dict): A dictionary containing parsed data.
            
            Returns:
            - str: A string describing the flow rate of water in the station.
            """
            return f"معدل تدفق المياه في المحطة {parsed_data['station_flow']} متر مكعب في الساعة \n"
        
        @staticmethod
        def flow_1200(parsed_data: dict) -> str:
            """
            Return information about flow at line 1200 based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about flow.

            Returns:
            str: A string containing information about flow at line 1200.
            """
            return (
                f"قيمة معدل تدفق المياه في الخط 1200 ا هي : {round(float(parsed_data['flow_1200a']), 1)} متر مكعب في الساعة \n"
                f"قيمة معدل تدفق المياه في الخط 1200 ب هي : {round(float(parsed_data['flow_1200b']), 1)} متر مكعب في الساعة \n"
            )

        @staticmethod
        def flow_1000(parsed_data: dict) -> str:
            """
            Return information about flow at line 800 based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about flow.

            Returns:
            str: A string containing information about flow at line 1000.
            """
            return (
                f"قيمة معدل تدفق المياه في الخط 1000 ا هي : {round(float(parsed_data['flow_1000a']), 1)} متر مكعب في الساعة \n"
                f"قيمة معدل تدفق المياه في الخط 1000 ب هي : {round(float(parsed_data['flow_1000b']), 1)} متر مكعب في الساعة \n"
            )

        @staticmethod
        def return_station_report(parsed_data: dict) -> str:
            """
            Generate and return station report based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about the station.

            Returns:
            str: A string containing the station report.
            """
            report = ""

            report += StationFourConfigurator.Home.return_working_transformers_info(parsed_data)
            report += StationFourConfigurator.Home.return_working_generators_info(parsed_data)
            report += StationFourConfigurator.Home.return_working_electrical_info(parsed_data)
            report += StationFourConfigurator.Home.return_working_pumps_info(parsed_data)
            report += StationFourConfigurator.Home.return_tanks_info(parsed_data)
            report += StationFourConfigurator.Home.return_station_flow(parsed_data)
            return report
        
        @staticmethod
        def return_flows_report(parsed_data: dict) -> str:
            """
            Generate and return flow report based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about the flow.

            Returns:
            str: A string containing the flow report.
            """
            report = ""
            report += StationFourConfigurator.Home.flow_1200(parsed_data)
            report += StationFourConfigurator.Home.flow_1000(parsed_data)
            return report  
        @staticmethod
        def return_hammer1_level_info(data):
            """
            Returns the hammer 1 level information.
            """
            return f"Hammer 1 level: {data.get('hammer1_lvl', 'Data not available')}%"

        @staticmethod
        def return_hammer2_level_info(data):
            """
            Returns the hammer 2 level information.
            """
            return f"Hammer 2 level: {data.get('hammer2_lvl', 'Data not available')}%"

class StationFiveConfigurator(object):
    class Home:
        @staticmethod
        def return_transformers_info(parsed_data: dict) -> str:

            """
            Generate and return information about transformers based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about transformers.

            Returns:
            str: A string containing information about transformers.
            """
            return (
                f"معلومات المحولات:\n"
                f"عدد المحولات التي تعمل : {int(float(parsed_data['transformers_on_count']))} محولات\n"
                f"عدد المحولات التي لا تعمل : {int(float(parsed_data['transformers_off_count']))} محولات\n\n"
            )
        
        @staticmethod
        def return_working_transformers_info(parsed_data: dict) -> str:

            """
            Generate and return information about working transformers based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about transformers.

            Returns:
            str: A string containing information about transformers.
            """
            return (
                f"معلومات المحولات:\n"
                f"عدد المحولات التي تعمل : {int(float(parsed_data['transformers_on_count']))} محولات\n\n"
            )
        
        @staticmethod
        def return_not_working_transformers_info(parsed_data: dict) -> str:

            """
            Generate and return information about working transformers based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about transformers.

            Returns:
            str: A string containing information about transformers.
            """
            return (
                f"معلومات المحولات:\n"
                f"عدد المحولات التي لا تعمل : {int(float(parsed_data['transformers_off_count']))} محولات\n\n"
            )

        @staticmethod
        def return_generators_info(parsed_data: dict) -> str:
            """
            Generate and return information about generators based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about generators.

            Returns:
            str: A string containing information about generators.
            """
            return (
                f"معلومات المولدات:\n"
                f"عدد المولدات التي تعمل : {int(float(parsed_data['generators_on_count']))} مولدات\n"
                f"عدد المولدات التي لا تعمل : {int(float(parsed_data['generators_off_count']))} مولدات\n\n"
            )
        
        @staticmethod
        def return_working_generators_info(parsed_data: dict) -> str:
            """
            Generate and return information about working generators based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about generators.

            Returns:
            str: A string containing information about working generators.
            """
            return (
                f"عدد المولدات التي تعمل : {int(float(parsed_data['generators_on_count']))} مولدات\n\n"
            )

        @staticmethod
        def return_not_working_generators_info(parsed_data: dict) -> str:
            """
            Generate and return information about non-working generators based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about generators.

            Returns:
            str: A string containing information about non-working generators.
            """
            return (
                f"عدد المولدات التي لا تعمل : {int(float(parsed_data['generators_off_count']))} مولدات\n\n"
            )



        def return_electrical_info(parsed_data: dict) -> str:

            """
            Generate and return information about electrical panels based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about electrical panels.

            Returns:
            str: A string containing information about electrical panels.
            """
            return (
                f"معلومات لوحات الكهرباء:\n"
                f"عدد لوحات الكهرباء التي تعمل : {int(float(parsed_data['ele_on_count']))} لوحات\n"
                f"عدد لوحات الكهرباء التي لا تعمل : {int(float(parsed_data['ele_off_count']))} لوحات\n\n"
            )
        @staticmethod
        def return_working_electrical_info(parsed_data: dict) -> str:
            """
            Generate and return information about working electrical panels based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about electrical panels.

            Returns:
            str: A string containing information about working electrical panels.
            """
            return (
                f"عدد لوحات الكهرباء التي تعمل : {int(float(parsed_data['ele_on_count']))} لوحات\n\n"
            )

        @staticmethod
        def return_not_working_electrical_info(parsed_data: dict) -> str:
            """
            Generate and return information about non-working electrical panels based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about electrical panels.

            Returns:
            str: A string containing information about non-working electrical panels.
            """
            return (
                f"عدد لوحات الكهرباء التي لا تعمل : {int(float(parsed_data['ele_off_count']))} لوحات\n\n"
            )


        @staticmethod
        def return_system_status_info(parsed_data: dict) -> str:

            """
            Generate and return system status information based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about the system status.

            Returns:
            str: A string containing system status information.
            """
            return (
                f"معلومات الانذارت:\n"
            # f"حالة نظام النقل التلقائي: {int(float(parsed_data['ats_status']))} %\n"
                f"{'يوجد' if int(float(parsed_data['electrical_alarm'])) else 'لا يوجد'} إنذار كهربائي\n\n"
                f"{'يوجد' if int(float(parsed_data['pumps_alarm'])) else 'لا يوجد'} إنذار مضخات\n\n"
                f"{'يوجد' if int(float(parsed_data['valves_alarm'])) else 'لا يوجد'} إنذار محابس\n\n"
                f"{'يوجد' if int(float(parsed_data['hammer_alarm'])) else 'لا يوجد'} إنذار في المطرقة\n\n"
                f"{'يوجد' if int(float(parsed_data['generator_alarm'])) else 'لا يوجد'} إنذار مولدات\n\n"
            )

        @staticmethod
        def return_working_pumps_info(parsed_data: dict) -> str:
            """
            Generate and return information about pumps based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about pumps.

            Returns:
            str: A string containing information about pumps.

            """
            TOTAL_WORKING_GROUP_A = int(float(parsed_data['pumps_g_a_on_count']))
            TOTAL_WORKING_GROUP_B = int(float(parsed_data['pumps_g_b_on_count']))
            TOTAL_WORKING_ALL_GROUPS = TOTAL_WORKING_GROUP_A + TOTAL_WORKING_GROUP_B
            print(TOTAL_WORKING_GROUP_A, TOTAL_WORKING_GROUP_B, flush=True)

            return (
                f"معلومات المضخات:\n"
                f"إجمالي عدد المضخات العاملة في محطة رقم 5 : {TOTAL_WORKING_ALL_GROUPS} مضخات\n"
                f"عدد المضخات العاملة في مجموعة ا: {TOTAL_WORKING_GROUP_A} مضخة\n"
                f"عدد المضخات العاملة في مجموعة ب: {TOTAL_WORKING_GROUP_B} مضخة\n"
            )
        
        @staticmethod
        def return_not_working_pumps_info(parsed_data: dict) -> str:
            """
            Generate and return information about pumps based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about pumps.

            Returns:
            str: A string containing information about pumps.
            
            """
            TOTAL_NOT_WORKING_GROUP_A = int(float(parsed_data['pumps_g_a_off_count']))
            TOTAL_NOT_WORKING_GROUP_B = int(float(parsed_data['pumps_g_b_off_count']))
            TOTAL_NOT_WORKING_ALL_GROUPS = TOTAL_NOT_WORKING_GROUP_A + TOTAL_NOT_WORKING_GROUP_B

            return (
                f"معلومات المضخات:\n"
                f"إجمالي عدد المضخات الغير عاملة في محطة رقم 5 : {TOTAL_NOT_WORKING_ALL_GROUPS} مضخات\n"
                f"عدد المضخات الغير عاملة في مجموعة ا: {TOTAL_NOT_WORKING_GROUP_A} مضخة\n"
                f"عدد المضخات الغير عاملة في مجموعة ب: {TOTAL_NOT_WORKING_GROUP_B} مضخة\n"
            )
        
        @staticmethod
        def return_group_a_pumps_info(parsed_data: dict) -> str:
            """
            Generate and return information about group A pumps based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about group A pumps.

            Returns:
            str: A string containing information about group A pumps.
            """
            TOTAL_WORKING_GROUP_A = int(float(parsed_data['pumps_g_a_on_count']))
            TOTAL_NOT_WORKING_GROUP_A = int(float(parsed_data['pumps_g_a_off_count']))

            return (
                f"معلومات المضخات في مجموعة ا:\n"
                f"إجمالي عدد المضخات العاملة في مجموعة ا: {TOTAL_WORKING_GROUP_A} مضخة\n"
                f"عدد المضخات الغير عاملة في مجموعة ا: {TOTAL_NOT_WORKING_GROUP_A} مضخة\n"
            )
        
        @staticmethod
        def return_group_b_pumps_info(parsed_data: dict) -> str:
            """
            Generate and return information about group B pumps based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about group B pumps.

            Returns:
            str: A string containing information about group B pumps.
            """
            TOTAL_WORKING_GROUP_B = int(float(parsed_data['pumps_g_b_on_count']))
            TOTAL_NOT_WORKING_GROUP_B = int(float(parsed_data['pumps_g_b_off_count']))

            return (
                f"معلومات المضخات في مجموعة ب:\n"
                f"إجمالي عدد المضخات العاملة في مجموعة ب: {TOTAL_WORKING_GROUP_B} مضخة\n"
                f"عدد المضخات الغير عاملة في مجموعة ب: {TOTAL_NOT_WORKING_GROUP_B} مضخة\n"
            )


        @staticmethod
        def return_pressure_info(parsed_data: dict) -> str:
            """
            Generate and return information about pressure based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about pressure.

            Returns:
            str: A string containing information about pressure.
            """
            return (
                f"معلومات الضغط:\n"
                f"قيمة الضغط في الخط 1200 هي : {round(float(parsed_data['pressure_1200_value']), 1)} بَارْ\n"
                f"قيمة الضغط في الخط 800 هي : {round(float(parsed_data['pressure_800_value']), 1)} بَارْ\n"
                f"قيمة الضغط في الخط 900 هي: {round(float(parsed_data['pressure_900_value']), 1)} بَارْ\n\n"
            )
        @staticmethod
        def pressure_1200(parsed_data: dict) -> str:
            """
            Return information about pressure at line 1200 based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about pressure.

            Returns:
            str: A string containing information about pressure at line 1200.
            """
            return f"قيمة الضغط في الخط 1200 هي : {round(float(parsed_data['pressure_1200_value']), 1)} بَارْ"

        @staticmethod
        def pressure_800(parsed_data: dict) -> str:
            """
            Return information about pressure at line 800 based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about pressure.

            Returns:
            str: A string containing information about pressure at line 800.
            """
            return f"قيمة الضغط في الخط 800 هي : {round(float(parsed_data['pressure_800_value']), 1)} بَارْ"

        @staticmethod
        def pressure_900(parsed_data: dict) -> str:
            """
            Return information about pressure at line 900 based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about pressure.

            Returns:
            str: A string containing information about pressure at line 900.
            """
            return f"قيمة الضغط في الخط 900 هي: {round(float(parsed_data['pressure_900_value']), 1)} بَارْ"

        @staticmethod
        def return_tanks_info(parsed_data: dict) -> str:
            """
            Generate and return information about all tanks based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about all tank.

            Returns:
            str: A string containing information about all tanks.
            """
            return (
                f"معلومات الخزانات: \n"
                f"مستوى الخزان 1: {round(float(parsed_data['tank_1_level']), 1)} امتار\n"
                f"نسبة الخزان 1: {int(float(parsed_data['tank_1_percent']))} % \n"
                f"مستوى الخزان 2: {round(float(parsed_data['tank_2_level']), 1)} امتار\n"
                f"نسبة الخزان 2: {int(float(parsed_data['tank_2_percent']))} % \n"
                f"مستوى الخزان 3: {round(float(parsed_data['tank_3_level']), 1)} امتار\n"
                f"نسبة الخزان 3: {int(float(parsed_data['tank_3_percent']))} % \n"
            )
        
        @staticmethod
        def return_tank1_info(parsed_data: dict) -> str:
            """
            Generate and return information about tank 1 based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about tank 1.

            Returns:
            str: A string containing information about tank 1.
            """
            return (
                f"معلومات الخزان 1:\n"
                f"مستوى الخزان 1: {round(float(parsed_data['tank_1_level']), 1)} امتار\n"
                f"نسبة الخزان 1: {round(float(parsed_data['tank_1_percent']), 1)} % \n"
            )


        @staticmethod
        def return_tank2_info(parsed_data: dict) -> str:
            """
            Generate and return information about tank 2 based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about tank 2.

            Returns:
            str: A string containing information about tank 2.
            """
            return (
                f"معلومات الخزان 2:\n"
                f"مستوى الخزان 2: {round(float(parsed_data['tank_2_level']), 1)} امتار\n"
                f"نسبة الخزان 2: {round(float(parsed_data['tank_2_percent']), 1)} % \n"
            )


        @staticmethod
        def return_tank3_info(parsed_data: dict) -> str:
            """
            Generate and return information about tank 3 based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about tank 3.

            Returns:
            str: A string containing information about tank 3.
            """
            return (
                f"معلومات الخزان 3:\n"
                f"مستوى الخزان 3: {round(float(parsed_data['tank_3_level']), 1)} امتار\n"
                f"نسبة الخزان 3: {round(float(parsed_data['tank_3_percent']), 1)} % \n"
            )

        @staticmethod
        def return_sump_info(parsed_data: dict) -> str:
            """
            Generate and return information about the sump based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about the sump.

            Returns:
            str: A string containing information about the sump.
            """
            return (
                f"معلومات مجمع المياه :\n"
                f"نسبة مجمع المياه : {int(float(parsed_data['sump_percent']))} % \n"
                f"قيمة مجمع المياه : {int(float(parsed_data['sump_value']))} امتار\n\n"
            )
        
        @staticmethod
        def return_station_flow(parsed_data:dict) -> str:
            """
            This static method returns a string describing the flow rate of water in a station based on parsed data.

            Args:
            - parsed_data (dict): A dictionary containing parsed data.
            
            Returns:
            - str: A string describing the flow rate of water in the station.
            """
            return f"معدل تدفق المياه في المحطة {parsed_data['flowr_station']} متر مكعب في الساعة \n"
        
        @staticmethod
        def return_flow_per_day(parsed_data:dict) -> str:
           
            return f"معدل تدفق المياه في المحطة {parsed_data['flow_per_day']} متر مكعب في الساعة \n"
        
        @staticmethod
        def flow_1200(parsed_data: dict) -> str:
            """
            Return information about flow at line 1200 based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about flow.

            Returns:
            str: A string containing information about flow at line 1200.
            """
            return f"قيمة معدل تدفق المياه في الخط 1200 هي : {round(float(parsed_data['flow_1200_rate']), 1)} متر مكعب في الساعة \n"

        @staticmethod
        def flow_800(parsed_data: dict) -> str:
            """
            Return information about flow at line 800 based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about flow.

            Returns:
            str: A string containing information about flow at line 800.
            """
            return f"قيمة معدل تدفق المياه في الخط 800 هي : {round(float(parsed_data['flow_800_rate']), 1)} متر مكعب في الساعة \n"

        @staticmethod
        def flow_900(parsed_data: dict) -> str:
            """
            Return information about flow at line 900 based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about flow.

            Returns:
            str: A string containing information about flow at line 900.
            """
            return f"قيمة معدل تدفق المياه في الخط 900 هي: {round(float(parsed_data['flow_900_rate']), 1)} متر مكعب في الساعة \n"
        
        @staticmethod
        def flow_military(parsed_data: dict) -> str:
            """
            Return information about flow at military line based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about flow.

            Returns:
            str: A string containing information about flow at military line.
            """
            return f"قيمة معدل تدفق المياه في خط الجيش هي : {round(float(parsed_data['flow_military_line']), 1)} متر مكعب في الساعة \n"
        
        @staticmethod
        def return_station_report(parsed_data: dict) -> str:
            """
            Generate and return station report based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about the station.

            Returns:
            str: A string containing the station report.
            """
            report = ""

            report += StationFiveConfigurator.Home.return_working_transformers_info(parsed_data)
            report += StationFiveConfigurator.Home.return_working_generators_info(parsed_data)
            report += StationFiveConfigurator.Home.return_working_electrical_info(parsed_data)
            report += StationFiveConfigurator.Home.return_working_pumps_info(parsed_data)
            report += StationFiveConfigurator.Home.return_tanks_info(parsed_data)
            report += StationFiveConfigurator.Home.return_sump_info(parsed_data)
            report += StationFiveConfigurator.Home.return_station_flow(parsed_data)
            return report
        
        @staticmethod
        def return_flows_report(parsed_data: dict) -> str:
            """
            Generate and return flow report based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about the flow.

            Returns:
            str: A string containing the flow report.
            """
            report = ""

            report += StationFiveConfigurator.Home.flow_1200(parsed_data)
            report += StationFiveConfigurator.Home.flow_900(parsed_data)
            report += StationFiveConfigurator.Home.flow_800(parsed_data)
            report += StationFiveConfigurator.Home.flow_military(parsed_data)
            return report
        

class StationInvConfigurator(object):

    class Home:

        @staticmethod
        def return_system_status_info(parsed_data: dict) -> str:

            """
            Generate and return system status information based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about the system status.

            Returns:
            str: A string containing system status information.
            """
            return (
                f"{'يوجد' if int(float(parsed_data['electrical_alarm'])) else 'لا يوجد'} إنذار كهربائي\n\n"
                f"{'يوجد' if int(float(parsed_data['pumps_alarm'])) else 'لا يوجد'} إنذار مضخات\n\n"
                f"{'يوجد' if int(float(parsed_data['valves_alarm'])) else 'لا يوجد'} إنذار محابس\n\n"
        )

        @staticmethod
        def return_transformers_info(parsed_data: dict) -> str:

            """
            Generate and return information about transformers based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about transformers.

            Returns:
            str: A string containing information about transformers.
            """
            return (
                f"معلومات المحولات:\n"
                f"عدد المحولات التي تعمل : {int(float(parsed_data['transformers_on']))} محولات\n"
                f"عدد المحولات التي لا تعمل : {int(float(parsed_data['transformers_off']))} محولات\n\n"
            )
    
        @staticmethod
        def return_working_transformers_info(parsed_data: dict) -> str:

            """
            Generate and return information about working transformers based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about transformers.

            Returns:
            str: A string containing information about transformers.
            """
            return (
                f"معلومات المحولات:\n"
                f"عدد المحولات التي تعمل : {int(float(parsed_data['transformers_on']))} محولات\n\n"
            )
    
        @staticmethod
        def return_not_working_transformers_info(parsed_data: dict) -> str:

            """
            Generate and return information about working transformers based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about transformers.

            Returns:
            str: A string containing information about transformers.
            """
            return (
                f"معلومات المحولات:\n"
                f"عدد المحولات التي لا تعمل : {int(float(parsed_data['transformers_off']))} محولات\n\n"
            )

        @staticmethod
        def return_generators_info(parsed_data: dict) -> str:
            """
            Generate and return information about generators based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about generators.

            Returns:
            str: A string containing information about generators.
            """
            return (
                f"معلومات المولدات:\n"
                f"عدد المولدات التي تعمل : {int(float(parsed_data['generators_on']))} مولدات\n"
                f"عدد المولدات التي لا تعمل : {int(float(parsed_data['generators_off']))} مولدات\n\n"
            )
        
        @staticmethod
        def return_working_generators_info(parsed_data: dict) -> str:
            """
            Generate and return information about working generators based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about generators.

            Returns:
            str: A string containing information about working generators.
            """
            return (
                f"عدد المولدات التي تعمل : {int(float(parsed_data['generators_on']))} مولدات\n\n"
            )

        @staticmethod
        def return_not_working_generators_info(parsed_data: dict) -> str:
            """
            Generate and return information about non-working generators based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about generators.

            Returns:
            str: A string containing information about non-working generators.
            """
            return (
                f"عدد المولدات التي لا تعمل : {int(float(parsed_data['generators_off']))} مولدات\n\n"
            )


        @staticmethod
        def return_electrical_info(parsed_data: dict) -> str:

            """
            Generate and return information about electrical panels based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about electrical panels.

            Returns:
            str: A string containing information about electrical panels.
            """
            return (
                f"معلومات لوحات الكهرباء:\n"
                f"عدد لوحات الكهرباء التي تعمل : {int(float(parsed_data['ele_panels_on']))} لوحات\n"
                f"عدد لوحات الكهرباء التي لا تعمل : {int(float(parsed_data['ele_panels_off']))} لوحات\n\n"
            )
        
        @staticmethod
        def return_working_electrical_info(parsed_data: dict) -> str:
            """
            Generate and return information about working electrical panels based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about electrical panels.

            Returns:
            str: A string containing information about working electrical panels.
            """
            return (
                f"عدد لوحات الكهرباء التي تعمل : {int(float(parsed_data['ele_panels_on']))} لوحات\n\n"
            )

        @staticmethod
        def return_not_working_electrical_info(parsed_data: dict) -> str:
            """
            Generate and return information about non-working electrical panels based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about electrical panels.

            Returns:
            str: A string containing information about non-working electrical panels.
            """
            return (
                f"عدد لوحات الكهرباء التي لا تعمل : {int(float(parsed_data['ele_panels_off']))} لوحات\n\n"
            )
        
        @staticmethod
        def return_pressure_info(parsed_data: dict) -> str:
            """
            Generate and return information about pressure based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about pressure.

            Returns:
            str: A string containing information about pressure.
            """
            return (
                f"معلومات الضغط:\n"
                f"قيمة الضغط في المستوي الأول هي : {round(float(parsed_data['pressure1']), 1)} بَارْ\n"
                f"قيمة الضغط في المستوي الثاني هي : {round(float(parsed_data['pressure2']), 1)} بَارْ\n"
            )
        @staticmethod
        def pressure_L1(parsed_data: dict) -> str:
            """
            Return information about pressure at level 1 based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about pressure.

            Returns:
            str: A string containing information about pressure at line 1.
            """
            return f"قيمة الضغط في الخط الأول هي : {round(float(parsed_data['pressure1']), 1)} بَارْ\n"

        @staticmethod
        def pressure_L2(parsed_data: dict) -> str:
            """
            Return information about pressure at level 2 based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about pressure.

            Returns:
            str: A string containing information about pressure at line 2.
            """
            return f"قيمة الضغط في الخط الثاني هي : {round(float(parsed_data['pressure2']), 1)} بَارْ\n"


        @staticmethod
        def return_station_flow(parsed_data:dict) -> str:
            """
            This static method returns a string describing the flow rate of water in a station based on parsed data.

            Args:
            - parsed_data (dict): A dictionary containing parsed data.
            
            Returns:
            - str: A string describing the flow rate of water in the station.
            """
            return f"معدل تدفق المياه في المحطة {parsed_data['total_flow_rate']} متر مكعب في الساعة \n"
        
        @staticmethod
        def flow_L1(parsed_data: dict) -> str:
            """
            Return information about flow at line 1200 based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about flow.

            Returns:
            str: A string containing information about flow at line 1.
            """
            return f"قيمة معدل تدفق المياه في الخط الأول هي : {round(float(parsed_data['flow_rate1']), 1)} متر مكعب في الساعة \n"

        @staticmethod
        def flow_L2(parsed_data: dict) -> str:
            """
            Return information about flow at line 800 based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about flow.

            Returns:
            str: A string containing information about flow at line 2.
            """
            return f"قيمة معدل تدفق المياه في الخط الثاني هي : {round(float(parsed_data['flow_rate2']), 1)} متر مكعب في الساعة \n"

        @staticmethod
        def return_pump_info(parsed_data: dict) -> str:
            """
            Generate and return information about the pump based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about the pump.

            Returns:
            str: A string containing information about the pump.
        
            """
            TOTAL_WORKING_GROUP_A = int(float(parsed_data['pumps_ga_on']))
            TOTAL_NOT_WORKING_GROUP_A = int(float(parsed_data['pumps_ga_off']))
            TOTAL_WORKING_GROUP_B = int(float(parsed_data['pumps_gb_on']))
            TOTAL_NOT_WORKING_GROUP_B = int(float(parsed_data['pumps_gb_off']))
            return (
                f"معلومات المضخات:\n"
                f"إجمالي عدد المضخات العاملة في مجموعة ا: {TOTAL_WORKING_GROUP_A} مضخة\n"
                f"عدد المضخات الغير عاملة في مجموعة ا: {TOTAL_NOT_WORKING_GROUP_A} مضخة\n"
                f"عدد المضخات العاملة في مجموعة ب: {TOTAL_WORKING_GROUP_B} مضخة\n"
                f"عدد المضخات الغير عاملة في مجموعة ب: {TOTAL_NOT_WORKING_GROUP_B} مضخة\n"
  
            )


        @staticmethod
        def return_working_pumps_info(parsed_data: dict) -> str:
            """
            Generate and return information about pumps based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about pumps.

            Returns:
            str: A string containing information about pumps.

            """
            TOTAL_WORKING_GROUP_A = int(float(parsed_data['pumps_ga_on']))
            TOTAL_WORKING_GROUP_B = int(float(parsed_data['pumps_gb_on']))
            TOTAL_WORKING_ALL_GROUPS = TOTAL_WORKING_GROUP_A + TOTAL_WORKING_GROUP_B
            print(TOTAL_WORKING_GROUP_A, TOTAL_WORKING_GROUP_B, flush=True)

            return (
                f"معلومات المضخات:\n"
                f"إجمالي عدد المضخات العاملة في محطة الامتداد : {TOTAL_WORKING_ALL_GROUPS} مضخات\n"
                f"عدد المضخات العاملة في مجموعة ا: {TOTAL_WORKING_GROUP_A} مضخة\n"
                f"عدد المضخات العاملة في مجموعة ب: {TOTAL_WORKING_GROUP_B} مضخة\n"
            )
        
        @staticmethod
        def return_not_working_pumps_info(parsed_data: dict) -> str:
            """
            Generate and return information about pumps based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about pumps.

            Returns:
            str: A string containing information about pumps.
            
            """
            TOTAL_NOT_WORKING_GROUP_A = int(float(parsed_data['pumps_ga_off']))
            TOTAL_NOT_WORKING_GROUP_B = int(float(parsed_data['pumps_gb_off']))
            TOTAL_NOT_WORKING_ALL_GROUPS = TOTAL_NOT_WORKING_GROUP_A + TOTAL_NOT_WORKING_GROUP_B

            return (
                f"معلومات المضخات:\n"
                f"إجمالي عدد المضخات الغير عاملة في محطة الامتداد : {TOTAL_NOT_WORKING_ALL_GROUPS} مضخات\n"
                f"عدد المضخات الغير عاملة في مجموعة ا: {TOTAL_NOT_WORKING_GROUP_A} مضخة\n"
                f"عدد المضخات الغير عاملة في مجموعة ب: {TOTAL_NOT_WORKING_GROUP_B} مضخة\n"
            )
        
        @staticmethod
        def return_group_a_pumps_info(parsed_data: dict) -> str:
            """
            Generate and return information about group A pumps based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about group A pumps.

            Returns:
            str: A string containing information about group A pumps.
            """
            TOTAL_WORKING_GROUP_A = int(float(parsed_data['pumps_ga_on']))
            TOTAL_NOT_WORKING_GROUP_A = int(float(parsed_data['pumps_ga_off']))

            return (
                f"معلومات المضخات في مجموعة ا:\n"
                f"إجمالي عدد المضخات العاملة في مجموعة ا: {TOTAL_WORKING_GROUP_A} مضخة\n"
                f"عدد المضخات الغير عاملة في مجموعة ا: {TOTAL_NOT_WORKING_GROUP_A} مضخة\n"
            )
        
        @staticmethod
        def return_group_b_pumps_info(parsed_data: dict) -> str:
            """
            Generate and return information about group B pumps based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about group B pumps.

            Returns:
            str: A string containing information about group B pumps.
            """
            TOTAL_WORKING_GROUP_B = int(float(parsed_data['pumps_gb_on']))
            TOTAL_NOT_WORKING_GROUP_B = int(float(parsed_data['pumps_gb_off']))

            return (
                f"معلومات المضخات في مجموعة ب:\n"
                f"إجمالي عدد المضخات العاملة في مجموعة ب: {TOTAL_WORKING_GROUP_B} مضخة\n"
                f"عدد المضخات الغير عاملة في مجموعة ب: {TOTAL_NOT_WORKING_GROUP_B} مضخة\n"
            )
        



        @staticmethod
        def return_sump_info(parsed_data: dict) -> str:
            """
            Generate and return information about the sump based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about the sump.

            Returns:
            str: A string containing information about the sump.
            """
            return (
                f"معلومات مجمع المياه :\n"
                f"نسبة مجمع المياه مجموعة ا: {int(float(parsed_data['sump_a_percentage']))} % \n"
                f"نسبة مجمع المياه مجموعة ب: {int(float(parsed_data['sump_b_percentage']))} % \n"
                f"قيمة مجمع المياه مجموعة ا: {int(float(parsed_data['sump_a_level']))} امتار\n"
                f"قيمة مجمع المياه مجموعة ب: {int(float(parsed_data['sump_b_level']))} امتار\n\n"
                f"متوسط نسبة مجمعات المياه : {int(float(parsed_data['sump_level_average_percentage']))} % \n"
                f"متوسط قيمة مجمعات المياه : {int(float(parsed_data['sump_level_average']))} % \n"

            )


        
        @staticmethod
        def return_group_a_sumps_info(parsed_data: dict) -> str:
            """
            Generate and return information about group A pumps based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about group A sumps.

            Returns:
            str: A string containing information about group A sumps.
            """

            return (
                f"معلومات مجمع المياه مجموعة ا:\n"
                f"نسبة مجمع المياه مجموعة ا: {int(float(parsed_data['sump_a_percentage']))} % \n"
                f"قيمة مجمع المياه مجموعة ا: {int(float(parsed_data['sump_a_level']))} امتار\n"

            )
        
        @staticmethod
        def return_group_b_sumps_info(parsed_data: dict) -> str:
            """
            Generate and return information about group B pumps based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about group B sumps.

            Returns:
            str: A string containing information about group B sumps.
            """

            return (
                f"معلومات مجمع المياه مجموعة ب:\n"
                f"نسبة مجمع المياه مجموعة ب: {int(float(parsed_data['sump_b_percentage']))} % \n"
                f"قيمة مجمع المياه مجموعة ب: {int(float(parsed_data['sump_b_level']))} امتار\n"
            )
        @staticmethod
        def return_station_report(parsed_data: dict) -> str:
            """
            Generate and return station report based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about the station.

            Returns:
            str: A string containing the station report.
            """
            report = ""

            report += StationInvConfigurator.Home.return_working_transformers_info(parsed_data)
            report += StationInvConfigurator.Home.return_working_generators_info(parsed_data)
            report += StationInvConfigurator.Home.return_working_electrical_info(parsed_data)
            report += StationInvConfigurator.Home.return_working_pumps_info(parsed_data)
            report += StationInvConfigurator.Home.return_sump_info(parsed_data)
            report += StationInvConfigurator.Home.return_station_flow(parsed_data)
            return report
        
        @staticmethod
        def return_system_status_info(parsed_data: dict) -> str:

            """
            Generate and return system status information based on the provided parsed data.

            Args:
            parsed_data (dict): A dictionary containing parsed data about the system status.

            Returns:
            str: A string containing system status information.
            """
            return (
                f"معلومات الانظاارت:\n"
            # f"حالة نظام النقل التلقائي: {int(float(parsed_data['ats_status']))} %\n"
                f"{'يوجد' if int(float(parsed_data['electrical_alarm'])) else 'لا يوجد'} إنذار كهربائي\n\n"
                f"{'يوجد' if int(float(parsed_data['pumps_alarm'])) else 'لا يوجد'} إنذار مضخات\n\n"
                f"{'يوجد' if int(float(parsed_data['valves_alarm'])) else 'لا يوجد'} إنذار محابس\n\n"
                f"{'يوجد' if int(float(parsed_data['hammer_alarm'])) else 'لا يوجد'} إنذار في المطرقة\n\n"
            )