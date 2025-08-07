import h5py
from typing import (
    TYPE_CHECKING,
)
import os

from nomad.datamodel.datamodel import EntryArchive
from structlog.stdlib import (
        BoundLogger,
    )

from nomad.config import config
from nomad.datamodel.metainfo.workflow import Workflow
from nomad.parsing.parser import MatchingParser
from test_plugin.schema_packages.schema_package import NewSchemaPackage,MIOData,ACTIF2Data,ACTIFData,HP_CANData

configuration = config.get_plugin_entry_point(
    'test_plugin.parsers:parser_entry_point'
)


class NewParser(MatchingParser):
    def set_atribute(self,value,_object,_atribute,keys):
        for key in keys[:-1]:
            value=value[key]
            
        if keys[-1] in list(value.keys()):
            value=value[keys[-1]][()]
            if isinstance(value, bytes):
                setattr(_object,_atribute,value.decode('utf-8'))
            else:
                setattr(_object,_atribute,value)    
        else:
            setattr(_object,_atribute,None)
    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
        #child_archives: dict[str, 'EntryArchive'] = None,
    ) -> None:
        schema= NewSchemaPackage()
        logger.info('NewParser.parse', parameter=configuration.parameter)
        mio_data= schema.m_create(MIOData)#MIOData()
        actif2_data= schema.m_create(ACTIF2Data)#ACTIF2Data()
        actif_data= schema.m_create(ACTIFData)#ACTIFData()
        hp_can_data= schema.m_create(HP_CANData)#HP_CANData()
        
        #for instrument in f["CAMELS_entry"]["user"]:
        #    instrument_names= instrument_names
        with h5py.File(mainfile, "r") as f:
            if "measurement_comments" in f["CAMELS_entry"]["measurement_details"]:
                if str(f["CAMELS_entry"]["measurement_details"]["measurement_comments"][()]) != "b''":
                    self.set_atribute(f,schema, "measurement_comments" , ["CAMELS_entry" "measurement_details" "measurement_comments"]) 
            if "measurement_description" in f["CAMELS_entry"]["measurement_details"]: 
                if str(f["CAMELS_entry"]["measurement_details"]["measurement_description"][()]) != "b''":
                    self.set_atribute(f,schema,"measurement_description",["CAMELS_entry","measurement_details","measurement_description"])
            if "protocol_description" in f["CAMELS_entry"]["measurement_details"]:             
                if str(f["CAMELS_entry"]["measurement_details"]["protocol_description"][()]) != "b''":
                    self.set_atribute(f,schema,"protocol_description",["CAMELS_entry","measurement_details","protocol_description"])
            self.set_atribute(f,schema,"time",["CAMELS_entry","data","time"])
            self.set_atribute(f,schema,"ElapsedTime",["CAMELS_entry","data","ElapsedTime"])
            self.set_atribute(f,schema,"first_name",["CAMELS_entry","user","first_name"])
            self.set_atribute(f,schema,"last_name",["CAMELS_entry","user","last_name"])
            self.set_atribute(f,schema,"email",["CAMELS_entry","user","email"])
            self.set_atribute(f,schema,"affiliation",["CAMELS_entry","user","affiliation"])
            for key in f["CAMELS_entry"]["instruments"]:
                if "opc" and "ua" in key:
                    if key+"_MIO_TV_01_A_PWM_pwmDutyCycle" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"TV_01_A_PWM_pwmDutyCycle",["CAMELS_entry","data",key+"_MIO_TV_01_A_PWM_pwmDutyCycle"])
                    if key+"_MIO_TV_01_B_PWM_pwmDutyCycle" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"TV_01_B_PWM_pwmDutyCycle",["CAMELS_entry","data",key+"_MIO_TV_01_B_PWM_pwmDutyCycle"])
                    if key+"_MIO_TV_02_A_PWM_doDiagnostics" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"TV_02_A_PWM_doDiagnostics",["CAMELS_entry","data",key+"_MIO_TV_02_A_PWM_doDiagnostics"])
                    if key+"_MIO_TV_02_A_PWM_pwmDutyCycle" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"TV_02_A_PWM_pwmDutyCycle",["CAMELS_entry","data",key+"_MIO_TV_02_A_PWM_pwmDutyCycle"])
                    if key+"_MIO_TV_02_B_PWM_pwmDutyCycle" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"TV_02_B_PWM_pwmDutyCycle",["CAMELS_entry","data",key+"_MIO_TV_02_B_PWM_pwmDutyCycle"])
                    if key+"_MIO_TV_03_A_PWM_pwmDutyCycle" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"TV_03_A_PWM_pwmDutyCycle",["CAMELS_entry","data",key+"_MIO_TV_03_A_PWM_pwmDutyCycle"])
                    if key+"_MIO_TV_03_B_PWM_pwmDutyCycle" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"TV_03_B_PWM_pwmDutyCycle",["CAMELS_entry","data",key+"_MIO_TV_03_B_PWM_pwmDutyCycle"])
                    if key+"_MIO_TV_01_A_pos_viDiagnostics" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"TV_01_A_pos_viDiagnostics",["CAMELS_entry","data",key+"_MIO_TV_01_A_pos_viDiagnostics"])
                    if key+"_MIO_TV_01_B_pos_viDiagnostics" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"TV_01_B_pos_viDiagnostics",["CAMELS_entry","data",key+"_MIO_TV_01_B_pos_viDiagnostics"])
                    if key+"_MIO_TV_02_A_pos_viDiagnostics" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"TV_02_A_pos_viDiagnostics",["CAMELS_entry","data",key+"_MIO_TV_02_A_pos_viDiagnostics"])
                    if key+"_MIO_TV_02_B_pos_viDiagnostics" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"TV_02_B_pos_viDiagnostics",["CAMELS_entry","data",key+"_MIO_TV_02_B_pos_viDiagnostics"])
                    if key+"_MIO_TV_03_A_pos_viDiagnostics" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"TV_03_A_pos_viDiagnostics",["CAMELS_entry","data",key+"_MIO_TV_03_A_pos_viDiagnostics"])
                    if key+"_MIO_TV_03_B_pos_viDiagnostics" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"TV_03_B_pos_viDiagnostics",["CAMELS_entry","data",key+"_MIO_TV_03_B_pos_viDiagnostics"])
                    if key+"_MIO_AR_01_PWM_pwmDutyCycle" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"AR_01_PWM_pwmDutyCycle",["CAMELS_entry","data",key+"_MIO_AR_01_PWM_pwmDutyCycle"])
                    if key+"_MIO_Supply_Position_Sensors_TV_voDiagnostics" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Supply_Position_Sensors_TV_voDiagnostics",["CAMELS_entry","data",key+"_MIO_Supply_Position_Sensors_TV_voDiagnostics"])
                    if key+"_MIO_T_ambient" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"T_ambient",["CAMELS_entry","data",key+"_MIO_T_ambient"])
                    if key+"_MIO_p_ambient" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"p_ambient",["CAMELS_entry","data",key+"_MIO_p_ambient"])
                    if key+"_MIO_RoundTrip_in_diDiagnostics" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"RoundTrip_in_diDiagnostics",["CAMELS_entry","data",key+"_MIO_RoundTrip_in_diDiagnostics"])
                    if key+"_MIO_T_ambient_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"T_ambient_Celsius",["CAMELS_entry","data",key+"_MIO_T_ambient_Celsius"])
                    if key+"_MIO_p_ambient_barA" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"p_ambient_barA",["CAMELS_entry","data",key+"_MIO_p_ambient_barA"])
                    if key+"_MIO_Actuators_Anode_A_PV_01_prct" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Anode_A_PV_01_prct",["CAMELS_entry","data",key+"_MIO_Actuators_Anode_A_PV_01_prct"])
                    if key+"_MIO_Actuators_Anode_A_PC_01_pDiff" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Anode_A_PC_01_pDiff",["CAMELS_entry","data",key+"_MIO_Actuators_Anode_A_PC_01_pDiff"])
                    if key+"_MIO_Actuators_Anode_A_PC_01_pDiff_ref" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Anode_A_PC_01_pDiff_ref",["CAMELS_entry","data",key+"_MIO_Actuators_Anode_A_PC_01_pDiff_ref"])
                    if key+"_MIO_Actuators_Anode_B_PV_01_prct" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Anode_B_PV_01_prct",["CAMELS_entry","data",key+"_MIO_Actuators_Anode_B_PV_01_prct"])
                    if key+"_MIO_Actuators_Anode_B_PC_01_pDiff" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Anode_B_PC_01_pDiff",["CAMELS_entry","data",key+"_MIO_Actuators_Anode_B_PC_01_pDiff"])
                    if key+"_MIO_Actuators_Anode_B_PC_01_pDiff_ref" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Anode_B_PC_01_pDiff_ref",["CAMELS_entry","data",key+"_MIO_Actuators_Anode_B_PC_01_pDiff_ref"])
                    if key+"_MIO_Actuators_Thermal_FLKS_01_freq_ref_Hz" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Thermal_FLKS_01_freq_ref_Hz",["CAMELS_entry","data",key+"_MIO_Actuators_Thermal_FLKS_01_freq_ref_Hz"])
                    if key+"_MIO_Actuators_Thermal_FLKS_01_fan_prct" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Thermal_FLKS_01_fan_prct",["CAMELS_entry","data",key+"_MIO_Actuators_Thermal_FLKS_01_fan_prct"])
                    if key+"_MIO_Actuators_Thermal_PV_01_prct" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Thermal_PV_01_prct",["CAMELS_entry","data",key+"_MIO_Actuators_Thermal_PV_01_prct"])
                    if key+"_MIO_Actuators_Thermal_PV_02_prct" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Thermal_PV_02_prct",["CAMELS_entry","data",key+"_MIO_Actuators_Thermal_PV_02_prct"])
                    if key+"_MIO_Actuators_Thermal_MV_01_ref_prct" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Thermal_MV_01_ref_prct",["CAMELS_entry","data",key+"_MIO_Actuators_Thermal_MV_01_ref_prct"])
                    if key+"_MIO_Actuators_Thermal_MV_01_act_prct" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Thermal_MV_01_act_prct",["CAMELS_entry","data",key+"_MIO_Actuators_Thermal_MV_01_act_prct"])
                    if key+"_MIO_Actuators_Thermal_CP_01_freq_ref_Hz" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Thermal_CP_01_freq_ref_Hz",["CAMELS_entry","data",key+"_MIO_Actuators_Thermal_CP_01_freq_ref_Hz"])
                    if key+"_MIO_Actuators_Thermal_CP_01_freq_act_Hz" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Thermal_CP_01_freq_act_Hz",["CAMELS_entry","data",key+"_MIO_Actuators_Thermal_CP_01_freq_act_Hz"])
                    if key+"_MIO_Actuators_Thermal_A_AV_01_ref_prct" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Thermal_A_AV_01_ref_prct",["CAMELS_entry","data",key+"_MIO_Actuators_Thermal_A_AV_01_ref_prct"])
                    if key+"_MIO_Actuators_Thermal_A_AV_01_act_prct" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Thermal_A_AV_01_act_prct",["CAMELS_entry","data",key+"_MIO_Actuators_Thermal_A_AV_01_act_prct"])
                    if key+"_MIO_Actuators_Thermal_B_AV_01_ref_prct" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Thermal_B_AV_01_ref_prct",["CAMELS_entry","data",key+"_MIO_Actuators_Thermal_B_AV_01_ref_prct"])
                    if key+"_MIO_Actuators_Thermal_B_AV_01_act_prct" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Thermal_B_AV_01_act_prct",["CAMELS_entry","data",key+"_MIO_Actuators_Thermal_B_AV_01_act_prct"])
                    if key+"_MIO_Actuators_Cathode_AR_01_prct" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Cathode_AR_01_prct",["CAMELS_entry","data",key+"_MIO_Actuators_Cathode_AR_01_prct"])
                    if key+"_MIO_Actuators_Cathode_EH_01_Power_prct" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Cathode_EH_01_Power_prct",["CAMELS_entry","data",key+"_MIO_Actuators_Cathode_EH_01_Power_prct"])
                    if key+"_MIO_Actuators_Cathode_EH_02_Power_prct" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Cathode_EH_02_Power_prct",["CAMELS_entry","data",key+"_MIO_Actuators_Cathode_EH_02_Power_prct"])
                    if key+"_MIO_Actuators_Cathode_A_TV_01_pos_V" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Cathode_A_TV_01_pos_V",["CAMELS_entry","data",key+"_MIO_Actuators_Cathode_A_TV_01_pos_V"])
                    if key+"_MIO_Actuators_Cathode_A_TV_01_pwmDutyCycle" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Cathode_A_TV_01_pwmDutyCycle",["CAMELS_entry","data",key+"_MIO_Actuators_Cathode_A_TV_01_pwmDutyCycle"])
                    if key+"_MIO_Actuators_Cathode_A_TV_02_pos_V" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Cathode_A_TV_02_pos_V",["CAMELS_entry","data",key+"_MIO_Actuators_Cathode_A_TV_02_pos_V"])
                    if key+"_MIO_Actuators_Cathode_A_TV_02_pwmDutyCycle" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Cathode_A_TV_02_pwmDutyCycle",["CAMELS_entry","data",key+"_MIO_Actuators_Cathode_A_TV_02_pwmDutyCycle"])
                    if key+"_MIO_Actuators_Cathode_A_TV_03_pos_V" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Cathode_A_TV_03_pos_V",["CAMELS_entry","data",key+"_MIO_Actuators_Cathode_A_TV_03_pos_V"])
                    if key+"_MIO_Actuators_Cathode_A_TV_03_pwmDutyCycle" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Cathode_A_TV_03_pwmDutyCycle",["CAMELS_entry","data",key+"_MIO_Actuators_Cathode_A_TV_03_pwmDutyCycle"])
                    if key+"_MIO_Actuators_Cathode_B_TV_01_pos_V" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Cathode_B_TV_01_pos_V",["CAMELS_entry","data",key+"_MIO_Actuators_Cathode_B_TV_01_pos_V"])
                    if key+"_MIO_Actuators_Cathode_B_TV_01_pwmDutyCycle" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Cathode_B_TV_01_pwmDutyCycle",["CAMELS_entry","data",key+"_MIO_Actuators_Cathode_B_TV_01_pwmDutyCycle"])
                    if key+"_MIO_Actuators_Cathode_B_TV_02_pos_V" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Cathode_B_TV_02_pos_V",["CAMELS_entry","data",key+"_MIO_Actuators_Cathode_B_TV_02_pos_V"])
                    if key+"_MIO_Actuators_Cathode_B_TV_02_pwmDutyCycle" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Cathode_B_TV_02_pwmDutyCycle",["CAMELS_entry","data",key+"_MIO_Actuators_Cathode_B_TV_02_pwmDutyCycle"])
                    if key+"_MIO_Actuators_Cathode_B_TV_03_pos_V" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Cathode_B_TV_03_pos_V",["CAMELS_entry","data",key+"_MIO_Actuators_Cathode_B_TV_03_pos_V"])
                    if key+"_MIO_Actuators_Cathode_B_TV_03_pwmDutyCycle" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Cathode_B_TV_03_pwmDutyCycle",["CAMELS_entry","data",key+"_MIO_Actuators_Cathode_B_TV_03_pwmDutyCycle"])
                    if key+"_MIO_Actuators_Cathode_MFC_01_00_p_PSIA" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Cathode_MFC_01_00_p_PSIA",["CAMELS_entry","data",key+"_MIO_Actuators_Cathode_MFC_01_00_p_PSIA"])
                    if key+"_MIO_Actuators_Cathode_MFC_01_00_T_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Cathode_MFC_01_00_T_Celsius",["CAMELS_entry","data",key+"_MIO_Actuators_Cathode_MFC_01_00_T_Celsius"])
                    if key+"_MIO_Actuators_Cathode_MFC_01_00_Vflow_LPM" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Cathode_MFC_01_00_Vflow_LPM",["CAMELS_entry","data",key+"_MIO_Actuators_Cathode_MFC_01_00_Vflow_LPM"])
                    if key+"_MIO_Actuators_Cathode_MFC_01_00_mflow_SLPM" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Cathode_MFC_01_00_mflow_SLPM",["CAMELS_entry","data",key+"_MIO_Actuators_Cathode_MFC_01_00_mflow_SLPM"])
                    if key+"_MIO_Actuators_Cathode_MFC_01_00_ref_SLPM" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Cathode_MFC_01_00_ref_SLPM",["CAMELS_entry","data",key+"_MIO_Actuators_Cathode_MFC_01_00_ref_SLPM"])
                    if key+"_MIO_Actuators_Cathode_MFC_01_00_set_SLPM" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Actuators_Cathode_MFC_01_00_set_SLPM",["CAMELS_entry","data",key+"_MIO_Actuators_Cathode_MFC_01_00_set_SLPM"])
                    if key+"_MIO_ECAT_10301_moduleQuality" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"ECAT_10301_moduleQuality",["CAMELS_entry","data",key+"_MIO_ECAT_10301_moduleQuality"])
                    if key+"_MIO_ECAT_10302_moduleQuality" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"ECAT_10302_moduleQuality",["CAMELS_entry","data",key+"_MIO_ECAT_10302_moduleQuality"])
                    if key+"_MIO_ECAT_10303_moduleQuality" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"ECAT_10303_moduleQuality",["CAMELS_entry","data",key+"_MIO_ECAT_10303_moduleQuality"])
                    if key+"_MIO_ECAT_1001_RX_Device_Readings_Gas_Index" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"ECAT_1001_RX_Device_Readings_Gas_Index",["CAMELS_entry","data",key+"_MIO_ECAT_1001_RX_Device_Readings_Gas_Index"])
                    if key+"_MIO_ECAT_1001_RX_Command_Result_Last_Command_ID" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"ECAT_1001_RX_Command_Result_Last_Command_ID",["CAMELS_entry","data",key+"_MIO_ECAT_1001_RX_Command_Result_Last_Command_ID"])
                    if key+"_MIO_ECAT_1001_RX_Command_Result_Last_Command_Status" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"ECAT_1001_RX_Command_Result_Last_Command_Status",["CAMELS_entry","data",key+"_MIO_ECAT_1001_RX_Command_Result_Last_Command_Status"])
                    if key+"_MIO_ECAT_1001_TX_Setpoint_Setpoint" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"ECAT_1001_TX_Setpoint_Setpoint",["CAMELS_entry","data",key+"_MIO_ECAT_1001_TX_Setpoint_Setpoint"])
                    if key+"_MIO_ECAT_1001_TX_Command_Request_Command_ID" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"ECAT_1001_TX_Command_Request_Command_ID",["CAMELS_entry","data",key+"_MIO_ECAT_1001_TX_Command_Request_Command_ID"])
                    if key+"_MIO_ECAT_1001_TX_Command_Request_Command_Argument" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"ECAT_1001_TX_Command_Request_Command_Argument",["CAMELS_entry","data",key+"_MIO_ECAT_1001_TX_Command_Request_Command_Argument"])
                    if key+"_MIO_ECAT_1002_RX_Device_Readings_Gas_Index" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"ECAT_1002_RX_Device_Readings_Gas_Index",["CAMELS_entry","data",key+"_MIO_ECAT_1002_RX_Device_Readings_Gas_Index"])
                    if key+"_MIO_ECAT_1002_RX_Command_Result_Last_Command_ID" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"ECAT_1002_RX_Command_Result_Last_Command_ID",["CAMELS_entry","data",key+"_MIO_ECAT_1002_RX_Command_Result_Last_Command_ID"])
                    if key+"_MIO_ECAT_1002_RX_Command_Result_Last_Command_Status" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"ECAT_1002_RX_Command_Result_Last_Command_Status",["CAMELS_entry","data",key+"_MIO_ECAT_1002_RX_Command_Result_Last_Command_Status"])
                    if key+"_MIO_ECAT_1002_TX_Setpoint_Setpoint" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"ECAT_1002_TX_Setpoint_Setpoint",["CAMELS_entry","data",key+"_MIO_ECAT_1002_TX_Setpoint_Setpoint"])
                    if key+"_MIO_ECAT_1002_TX_Command_Request_Command_ID" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"ECAT_1002_TX_Command_Request_Command_ID",["CAMELS_entry","data",key+"_MIO_ECAT_1002_TX_Command_Request_Command_ID"])
                    if key+"_MIO_ECAT_1002_TX_Command_Request_Command_Argument" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"ECAT_1002_TX_Command_Request_Command_Argument",["CAMELS_entry","data",key+"_MIO_ECAT_1002_TX_Command_Request_Command_Argument"])
                    if key+"_MIO_ECAT_1004_RX_Device_Readings_Gas_Index" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"ECAT_1004_RX_Device_Readings_Gas_Index",["CAMELS_entry","data",key+"_MIO_ECAT_1004_RX_Device_Readings_Gas_Index"])
                    if key+"_MIO_ECAT_1004_RX_Command_Result_Last_Command_ID" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"ECAT_1004_RX_Command_Result_Last_Command_ID",["CAMELS_entry","data",key+"_MIO_ECAT_1004_RX_Command_Result_Last_Command_ID"])
                    if key+"_MIO_ECAT_1004_RX_Command_Result_Last_Command_Status" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"ECAT_1004_RX_Command_Result_Last_Command_Status",["CAMELS_entry","data",key+"_MIO_ECAT_1004_RX_Command_Result_Last_Command_Status"])
                    if key+"_MIO_ECAT_1004_TX_Setpoint_Setpoint" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"ECAT_1004_TX_Setpoint_Setpoint",["CAMELS_entry","data",key+"_MIO_ECAT_1004_TX_Setpoint_Setpoint"])
                    if key+"_MIO_ECAT_1004_TX_Command_Request_Command_ID" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"ECAT_1004_TX_Command_Request_Command_ID",["CAMELS_entry","data",key+"_MIO_ECAT_1004_TX_Command_Request_Command_ID"])
                    if key+"_MIO_ECAT_1004_TX_Command_Request_Command_Argument" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"ECAT_1004_TX_Command_Request_Command_Argument",["CAMELS_entry","data",key+"_MIO_ECAT_1004_TX_Command_Request_Command_Argument"])
                    if key+"_MIO_Fluids_Cathode_PT_01_barG" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_PT_01_barG",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_PT_01_barG"])
                    if key+"_MIO_Fluids_Cathode_PT_02_barG" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_PT_02_barG",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_PT_02_barG"])
                    if key+"_MIO_Fluids_Cathode_PT_03_barG" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_PT_03_barG",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_PT_03_barG"])
                    if key+"_MIO_Fluids_Cathode_TT_01_0_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_TT_01_0_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_TT_01_0_Celsius"])
                    if key+"_MIO_Fluids_Cathode_TT_05_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_TT_05_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_TT_05_Celsius"])
                    if key+"_MIO_Fluids_Cathode_TT_02_0_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_TT_02_0_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_TT_02_0_Celsius"])
                    if key+"_MIO_Fluids_Cathode_TT_06_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_TT_06_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_TT_06_Celsius"])
                    if key+"_MIO_Fluids_Cathode_TT_03_0_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_TT_03_0_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_TT_03_0_Celsius"])
                    if key+"_MIO_Fluids_Cathode_TT_07_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_TT_07_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_TT_07_Celsius"])
                    if key+"_MIO_Fluids_Cathode_TT_01_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_TT_01_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_TT_01_Celsius"])
                    if key+"_MIO_Fluids_Cathode_TT_02_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_TT_02_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_TT_02_Celsius"])
                    if key+"_MIO_Fluids_Cathode_TT_04_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_TT_04_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_TT_04_Celsius"])
                    if key+"_MIO_Fluids_Cathode_A_PT_04_barG" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_A_PT_04_barG",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_A_PT_04_barG"])
                    if key+"_MIO_Fluids_Cathode_A_PT_05_barG" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_A_PT_05_barG",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_A_PT_05_barG"])
                    if key+"_MIO_Fluids_Cathode_A_PT_06_barG" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_A_PT_06_barG",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_A_PT_06_barG"])
                    if key+"_MIO_Fluids_Cathode_A_MFT_02_slpm" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_A_MFT_02_slpm",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_A_MFT_02_slpm"])
                    if key+"_MIO_Fluids_Cathode_A_RHT_01_prctRH" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_A_RHT_01_prctRH",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_A_RHT_01_prctRH"])
                    if key+"_MIO_Fluids_Cathode_A_TT_09_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_A_TT_09_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_A_TT_09_Celsius"])
                    if key+"_MIO_Fluids_Cathode_A_TT_08_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_A_TT_08_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_A_TT_08_Celsius"])
                    if key+"_MIO_Fluids_Cathode_A_TT_10_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_A_TT_10_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_A_TT_10_Celsius"])
                    if key+"_MIO_Fluids_Cathode_A_TT_11_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_A_TT_11_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_A_TT_11_Celsius"])
                    if key+"_MIO_Fluids_Cathode_A_TT_12_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_A_TT_12_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_A_TT_12_Celsius"])
                    if key+"_MIO_Fluids_Cathode_B_PT_04_barG" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_B_PT_04_barG",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_B_PT_04_barG"])
                    if key+"_MIO_Fluids_Cathode_B_PT_05_barG" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_B_PT_05_barG",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_B_PT_05_barG"])
                    if key+"_MIO_Fluids_Cathode_B_PT_06_barG" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_B_PT_06_barG",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_B_PT_06_barG"])
                    if key+"_MIO_Fluids_Cathode_B_MFT_02_slpm" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_B_MFT_02_slpm",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_B_MFT_02_slpm"])
                    if key+"_MIO_Fluids_Cathode_B_TT_08_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_B_TT_08_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_B_TT_08_Celsius"])
                    if key+"_MIO_Fluids_Cathode_B_TT_10_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_B_TT_10_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_B_TT_10_Celsius"])
                    if key+"_MIO_Fluids_Cathode_B_TT_11_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_B_TT_11_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_B_TT_11_Celsius"])
                    if key+"_MIO_Fluids_Cathode_B_TT_12_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Cathode_B_TT_12_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Cathode_B_TT_12_Celsius"])
                    if key+"_MIO_Fluids_Anode_PT_01_barG" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Anode_PT_01_barG",["CAMELS_entry","data",key+"_MIO_Fluids_Anode_PT_01_barG"])
                    if key+"_MIO_Fluids_Anode_TT_01_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Anode_TT_01_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Anode_TT_01_Celsius"])
                    if key+"_MIO_Fluids_Anode_A_PT_03_barG" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Anode_A_PT_03_barG",["CAMELS_entry","data",key+"_MIO_Fluids_Anode_A_PT_03_barG"])
                    if key+"_MIO_Fluids_Anode_A_PT_04_barG" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Anode_A_PT_04_barG",["CAMELS_entry","data",key+"_MIO_Fluids_Anode_A_PT_04_barG"])
                    if key+"_MIO_Fluids_Anode_A_TT_02_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Anode_A_TT_02_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Anode_A_TT_02_Celsius"])
                    if key+"_MIO_Fluids_Anode_A_TT_03_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Anode_A_TT_03_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Anode_A_TT_03_Celsius"])
                    if key+"_MIO_Fluids_Anode_B_PT_03_barG" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Anode_B_PT_03_barG",["CAMELS_entry","data",key+"_MIO_Fluids_Anode_B_PT_03_barG"])
                    if key+"_MIO_Fluids_Anode_B_PT_04_barG" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Anode_B_PT_04_barG",["CAMELS_entry","data",key+"_MIO_Fluids_Anode_B_PT_04_barG"])
                    if key+"_MIO_Fluids_Anode_B_TT_02_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Anode_B_TT_02_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Anode_B_TT_02_Celsius"])
                    if key+"_MIO_Fluids_Anode_B_TT_03_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Anode_B_TT_03_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Anode_B_TT_03_Celsius"])
                    if key+"_MIO_Fluids_Anode_MFT_01_A_p_PSIA" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Anode_MFT_01_A_p_PSIA",["CAMELS_entry","data",key+"_MIO_Fluids_Anode_MFT_01_A_p_PSIA"])
                    if key+"_MIO_Fluids_Anode_MFT_01_A_T_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Anode_MFT_01_A_T_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Anode_MFT_01_A_T_Celsius"])
                    if key+"_MIO_Fluids_Anode_MFT_01_A_Vflow_LPM" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Anode_MFT_01_A_Vflow_LPM",["CAMELS_entry","data",key+"_MIO_Fluids_Anode_MFT_01_A_Vflow_LPM"])
                    if key+"_MIO_Fluids_Anode_MFT_01_A_mflow_SLPM" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Anode_MFT_01_A_mflow_SLPM",["CAMELS_entry","data",key+"_MIO_Fluids_Anode_MFT_01_A_mflow_SLPM"])
                    if key+"_MIO_Fluids_Anode_MFT_01_A_mTotal_SL" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Anode_MFT_01_A_mTotal_SL",["CAMELS_entry","data",key+"_MIO_Fluids_Anode_MFT_01_A_mTotal_SL"])
                    if key+"_MIO_Fluids_Anode_MFT_01_B_p_PSIA" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Anode_MFT_01_B_p_PSIA",["CAMELS_entry","data",key+"_MIO_Fluids_Anode_MFT_01_B_p_PSIA"])
                    if key+"_MIO_Fluids_Anode_MFT_01_B_T_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Anode_MFT_01_B_T_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Anode_MFT_01_B_T_Celsius"])
                    if key+"_MIO_Fluids_Anode_MFT_01_B_Vflow_LPM" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Anode_MFT_01_B_Vflow_LPM",["CAMELS_entry","data",key+"_MIO_Fluids_Anode_MFT_01_B_Vflow_LPM"])
                    if key+"_MIO_Fluids_Anode_MFT_01_B_mflow_SLPM" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Anode_MFT_01_B_mflow_SLPM",["CAMELS_entry","data",key+"_MIO_Fluids_Anode_MFT_01_B_mflow_SLPM"])
                    if key+"_MIO_Fluids_Anode_MFT_01_B_mTotal_SL" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Anode_MFT_01_B_mTotal_SL",["CAMELS_entry","data",key+"_MIO_Fluids_Anode_MFT_01_B_mTotal_SL"])
                    if key+"_MIO_Fluids_Thermal_PT_01_barG" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_PT_01_barG",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_PT_01_barG"])
                    if key+"_MIO_Fluids_Thermal_PT_02_barG" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_PT_02_barG",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_PT_02_barG"])
                    if key+"_MIO_Fluids_Thermal_PT_03_A_barG" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_PT_03_A_barG",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_PT_03_A_barG"])
                    if key+"_MIO_Fluids_Thermal_PT_03_B_barG" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_PT_03_B_barG",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_PT_03_B_barG"])
                    if key+"_MIO_Fluids_Thermal_PT_04_A_barG" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_PT_04_A_barG",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_PT_04_A_barG"])
                    if key+"_MIO_Fluids_Thermal_PT_04_B_barG" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_PT_04_B_barG",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_PT_04_B_barG"])
                    if key+"_MIO_Fluids_Thermal_PT_05_barG" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_PT_05_barG",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_PT_05_barG"])
                    if key+"_MIO_Fluids_Thermal_PT_06_barG" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_PT_06_barG",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_PT_06_barG"])
                    if key+"_MIO_Fluids_Thermal_MFT_01_02_lpm" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_MFT_01_02_lpm",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_MFT_01_02_lpm"])
                    if key+"_MIO_Fluids_Thermal_MFT_02_lpm" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_MFT_02_lpm",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_MFT_02_lpm"])
                    if key+"_MIO_Fluids_Thermal_TT_01_01_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_TT_01_01_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_TT_01_01_Celsius"])
                    if key+"_MIO_Fluids_Thermal_TT_03_02_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_TT_03_02_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_TT_03_02_Celsius"])
                    if key+"_MIO_Fluids_Thermal_TT_01_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_TT_01_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_TT_01_Celsius"])
                    if key+"_MIO_Fluids_Thermal_TT_05_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_TT_05_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_TT_05_Celsius"])
                    if key+"_MIO_Fluids_Thermal_TT_02_01_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_TT_02_01_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_TT_02_01_Celsius"])
                    if key+"_MIO_Fluids_Thermal_TT_04_02_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_TT_04_02_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_TT_04_02_Celsius"])
                    if key+"_MIO_Fluids_Thermal_TT_06_01_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_TT_06_01_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_TT_06_01_Celsius"])
                    if key+"_MIO_Fluids_Thermal_TT_08_02_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_TT_08_02_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_TT_08_02_Celsius"])
                    if key+"_MIO_Fluids_Thermal_TT_07_01_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_TT_07_01_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_TT_07_01_Celsius"])
                    if key+"_MIO_Fluids_Thermal_TT_09_02_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_TT_09_02_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_TT_09_02_Celsius"])
                    if key+"_MIO_Fluids_Thermal_TT_11_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_TT_11_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_TT_11_Celsius"])
                    if key+"_MIO_Fluids_Thermal_TT_01_02_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_TT_01_02_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_TT_01_02_Celsius"])
                    if key+"_MIO_Fluids_Thermal_A_MFT_01_lpm" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_A_MFT_01_lpm",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_A_MFT_01_lpm"])
                    if key+"_MIO_Fluids_Thermal_A_TT_03_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_A_TT_03_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_A_TT_03_Celsius"])
                    if key+"_MIO_Fluids_Thermal_A_TT_04_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_A_TT_04_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_A_TT_04_Celsius"])
                    if key+"_MIO_Fluids_Thermal_B_MFT_01_lpm" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_B_MFT_01_lpm",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_B_MFT_01_lpm"])
                    if key+"_MIO_Fluids_Thermal_B_TT_03_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_B_TT_03_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_B_TT_03_Celsius"])
                    if key+"_MIO_Fluids_Thermal_B_TT_04_Celsius" in f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,mio_data,"Fluids_Thermal_B_TT_04_Celsius",["CAMELS_entry","data",key+"_MIO_Fluids_Thermal_B_TT_04_Celsius"])
                    if key+"_HP_CAN_Net_A_fbCAN_FSM_iStep" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,hp_can_data,"AN_Net_A_fbCAN_FSM_iStep",["CAMELS_entry","data",key+"_HP_CAN_Net_A_fbCAN_FSM_iStep"])
                    if key+"_HP_CAN_Net_A_RH01_actValues_current_act_A" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,hp_can_data,"AN_Net_A_RH01_actValues_current_act_A",["CAMELS_entry","data",key+"_HP_CAN_Net_A_RH01_actValues_current_act_A"])
                    if key+"_HP_CAN_Net_A_RH01_actValues_power_act_W" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,hp_can_data,"AN_Net_A_RH01_actValues_power_act_W",["CAMELS_entry","data",key+"_HP_CAN_Net_A_RH01_actValues_power_act_W"])
                    if key+"_HP_CAN_Net_A_RH01_actValues_speed_act_rpm" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,hp_can_data,"AN_Net_A_RH01_actValues_speed_act_rpm",["CAMELS_entry","data",key+"_HP_CAN_Net_A_RH01_actValues_speed_act_rpm"])
                    if key+"_HP_CAN_Net_A_RH01_actValues_T_circuit_C" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,hp_can_data,"AN_Net_A_RH01_actValues_T_circuit_C",["CAMELS_entry","data",key+"_HP_CAN_Net_A_RH01_actValues_T_circuit_C"])
                    if key+"_HP_CAN_Net_A_RH01_actValues_voltage_act_V" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,hp_can_data,"AN_Net_A_RH01_actValues_voltage_act_V",["CAMELS_entry","data",key+"_HP_CAN_Net_A_RH01_actValues_voltage_act_V"])
                    if key+"_HP_CAN_Net_A_RH01_cmd_mDot_cmd_kgph" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,hp_can_data,"AN_Net_A_RH01_cmd_mDot_cmd_kgph",["CAMELS_entry","data",key+"_HP_CAN_Net_A_RH01_cmd_mDot_cmd_kgph"])
                    if key+"_HP_CAN_Net_A_RH01_cmd_speed_cmd_rpm" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,hp_can_data,"AN_Net_A_RH01_cmd_speed_cmd_rpm",["CAMELS_entry","data",key+"_HP_CAN_Net_A_RH01_cmd_speed_cmd_rpm"])
                    if key+"_HP_CAN_Net_B_fbCAN_FSM_iStep" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,hp_can_data,"AN_Net_B_fbCAN_FSM_iStep",["CAMELS_entry","data",key+"_HP_CAN_Net_B_fbCAN_FSM_iStep"])
                    if key+"_HP_CAN_Net_B_RH01_actValues_current_act_A" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,hp_can_data,"AN_Net_B_RH01_actValues_current_act_A",["CAMELS_entry","data",key+"_HP_CAN_Net_B_RH01_actValues_current_act_A"])
                    if key+"_HP_CAN_Net_B_RH01_actValues_power_act_W" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,hp_can_data,"AN_Net_B_RH01_actValues_power_act_W",["CAMELS_entry","data",key+"_HP_CAN_Net_B_RH01_actValues_power_act_W"])
                    if key+"_HP_CAN_Net_B_RH01_actValues_speed_act_rpm" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,hp_can_data,"AN_Net_B_RH01_actValues_speed_act_rpm",["CAMELS_entry","data",key+"_HP_CAN_Net_B_RH01_actValues_speed_act_rpm"])
                    if key+"_HP_CAN_Net_B_RH01_actValues_T_circuit_C" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,hp_can_data,"AN_Net_B_RH01_actValues_T_circuit_C",["CAMELS_entry","data",key+"_HP_CAN_Net_B_RH01_actValues_T_circuit_C"])
                    if key+"_HP_CAN_Net_B_RH01_actValues_voltage_act_V" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,hp_can_data,"AN_Net_B_RH01_actValues_voltage_act_V",["CAMELS_entry","data",key+"_HP_CAN_Net_B_RH01_actValues_voltage_act_V"])
                    if key+"_HP_CAN_Net_B_RH01_cmd_mDot_cmd_kgph" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,hp_can_data,"AN_Net_B_RH01_cmd_mDot_cmd_kgph",["CAMELS_entry","data",key+"_HP_CAN_Net_B_RH01_cmd_mDot_cmd_kgph"])
                    if key+"_HP_CAN_Net_B_RH01_cmd_speed_cmd_rpm" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,hp_can_data,"AN_Net_B_RH01_cmd_speed_cmd_rpm",["CAMELS_entry","data",key+"_HP_CAN_Net_B_RH01_cmd_speed_cmd_rpm"])
                    if key+"_ACTIF_Anode_GasSupply_state" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Anode_GasSupply_state",["CAMELS_entry","data",key+"_ACTIF_Anode_GasSupply_state"])
                    if key+"_ACTIF_Anode_PC_01_A_cmd" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Anode_PC_01_A_cmd",["CAMELS_entry","data",key+"_ACTIF_Anode_PC_01_A_cmd"])
                    if key+"_ACTIF_Anode_PC_01_A_state" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Anode_PC_01_A_state",["CAMELS_entry","data",key+"_ACTIF_Anode_PC_01_A_state"])
                    if key+"_ACTIF_Anode_PC_01_B_cmd" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Anode_PC_01_B_cmd",["CAMELS_entry","data",key+"_ACTIF_Anode_PC_01_B_cmd"])
                    if key+"_ACTIF_Anode_PC_01_B_state" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Anode_PC_01_B_state",["CAMELS_entry","data",key+"_ACTIF_Anode_PC_01_B_state"])
                    if key+"_ACTIF_Anode_PV_01_A_cmd" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Anode_PV_01_A_cmd",["CAMELS_entry","data",key+"_ACTIF_Anode_PV_01_A_cmd"])
                    if key+"_ACTIF_Anode_PV_01_A_state" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Anode_PV_01_A_state",["CAMELS_entry","data",key+"_ACTIF_Anode_PV_01_A_state"])
                    if key+"_ACTIF_Anode_PV_01_B_cmd" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Anode_PV_01_B_cmd",["CAMELS_entry","data",key+"_ACTIF_Anode_PV_01_B_cmd"])
                    if key+"_ACTIF_Anode_PV_01_B_state" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Anode_PV_01_B_state",["CAMELS_entry","data",key+"_ACTIF_Anode_PV_01_B_state"])
                    if key+"_ACTIF_Cathode_AC_01_cmd" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Cathode_AC_01_cmd",["CAMELS_entry","data",key+"_ACTIF_Cathode_AC_01_cmd"])
                    if key+"_ACTIF_Cathode_AC_01_state" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Cathode_AC_01_state",["CAMELS_entry","data",key+"_ACTIF_Cathode_AC_01_state"])
                    if key+"_ACTIF_Cathode_EH_01_cmd" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Cathode_EH_01_cmd",["CAMELS_entry","data",key+"_ACTIF_Cathode_EH_01_cmd"])
                    if key+"_ACTIF_Cathode_EH_01_state" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Cathode_EH_01_state",["CAMELS_entry","data",key+"_ACTIF_Cathode_EH_01_state"])
                    if key+"_ACTIF_Cathode_EH_02_cmd" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Cathode_EH_02_cmd",["CAMELS_entry","data",key+"_ACTIF_Cathode_EH_02_cmd"])
                    if key+"_ACTIF_Cathode_EH_02_state" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Cathode_EH_02_state",["CAMELS_entry","data",key+"_ACTIF_Cathode_EH_02_state"])
                    if key+"_ACTIF_Cathode_MFC_01_00_cmd" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Cathode_MFC_01_00_cmd",["CAMELS_entry","data",key+"_ACTIF_Cathode_MFC_01_00_cmd"])
                    if key+"_ACTIF_Cathode_MFC_01_00_state" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Cathode_MFC_01_00_state",["CAMELS_entry","data",key+"_ACTIF_Cathode_MFC_01_00_state"])
                    if key+"_ACTIF_Cathode_TV_01_A_cmd" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Cathode_TV_01_A_cmd",["CAMELS_entry","data",key+"_ACTIF_Cathode_TV_01_A_cmd"])
                    if key+"_ACTIF_Cathode_TV_01_A_state" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Cathode_TV_01_A_state",["CAMELS_entry","data",key+"_ACTIF_Cathode_TV_01_A_state"])
                    if key+"_ACTIF_Cathode_TV_01_A_theta_prct" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Cathode_TV_01_A_theta_prct",["CAMELS_entry","data",key+"_ACTIF_Cathode_TV_01_A_theta_prct"])
                    if key+"_ACTIF_Cathode_TV_01_B_cmd" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Cathode_TV_01_B_cmd",["CAMELS_entry","data",key+"_ACTIF_Cathode_TV_01_B_cmd"])
                    if key+"_ACTIF_Cathode_TV_01_B_state" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Cathode_TV_01_B_state",["CAMELS_entry","data",key+"_ACTIF_Cathode_TV_01_B_state"])
                    if key+"_ACTIF_Cathode_TV_01_B_theta_prct" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Cathode_TV_01_B_theta_prct",["CAMELS_entry","data",key+"_ACTIF_Cathode_TV_01_B_theta_prct"])
                    if key+"_ACTIF_Cathode_TV_02_A_cmd" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Cathode_TV_02_A_cmd",["CAMELS_entry","data",key+"_ACTIF_Cathode_TV_02_A_cmd"])
                    if key+"_ACTIF_Cathode_TV_02_A_state" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Cathode_TV_02_A_state",["CAMELS_entry","data",key+"_ACTIF_Cathode_TV_02_A_state"])
                    if key+"_ACTIF_Cathode_TV_02_A_theta_prct" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Cathode_TV_02_A_theta_prct",["CAMELS_entry","data",key+"_ACTIF_Cathode_TV_02_A_theta_prct"])
                    if key+"_ACTIF_Cathode_TV_02_B_cmd" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Cathode_TV_02_B_cmd",["CAMELS_entry","data",key+"_ACTIF_Cathode_TV_02_B_cmd"])
                    if key+"_ACTIF_Cathode_TV_02_B_state" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Cathode_TV_02_B_state",["CAMELS_entry","data",key+"_ACTIF_Cathode_TV_02_B_state"])
                    if key+"_ACTIF_Cathode_TV_02_B_theta_prct" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Cathode_TV_02_B_theta_prct",["CAMELS_entry","data",key+"_ACTIF_Cathode_TV_02_B_theta_prct"])
                    if key+"_ACTIF_Cathode_TV_03_A_cmd" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Cathode_TV_03_A_cmd",["CAMELS_entry","data",key+"_ACTIF_Cathode_TV_03_A_cmd"])
                    if key+"_ACTIF_Cathode_TV_03_A_state" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Cathode_TV_03_A_state",["CAMELS_entry","data",key+"_ACTIF_Cathode_TV_03_A_state"])
                    if key+"_ACTIF_Cathode_TV_03_A_theta_prct" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Cathode_TV_03_A_theta_prct",["CAMELS_entry","data",key+"_ACTIF_Cathode_TV_03_A_theta_prct"])
                    if key+"_ACTIF_Cathode_TV_03_B_cmd" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Cathode_TV_03_B_cmd",["CAMELS_entry","data",key+"_ACTIF_Cathode_TV_03_B_cmd"])
                    if key+"_ACTIF_Cathode_TV_03_B_state" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Cathode_TV_03_B_state",["CAMELS_entry","data",key+"_ACTIF_Cathode_TV_03_B_state"])
                    if key+"_ACTIF_Cathode_TV_03_B_theta_prct" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Cathode_TV_03_B_theta_prct",["CAMELS_entry","data",key+"_ACTIF_Cathode_TV_03_B_theta_prct"])
                    if key+"_ACTIF_Thermal_AV_01_A_cmd" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Thermal_AV_01_A_cmd",["CAMELS_entry","data",key+"_ACTIF_Thermal_AV_01_A_cmd"])
                    if key+"_ACTIF_Thermal_AV_01_A_state" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Thermal_AV_01_A_state",["CAMELS_entry","data",key+"_ACTIF_Thermal_AV_01_A_state"])
                    if key+"_ACTIF_Thermal_AV_01_B_cmd" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Thermal_AV_01_B_cmd",["CAMELS_entry","data",key+"_ACTIF_Thermal_AV_01_B_cmd"])
                    if key+"_ACTIF_Thermal_AV_01_B_state" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Thermal_AV_01_B_state",["CAMELS_entry","data",key+"_ACTIF_Thermal_AV_01_B_state"])
                    if key+"_ACTIF_Thermal_CP_01_cmd_prct" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Thermal_CP_01_cmd_prct",["CAMELS_entry","data",key+"_ACTIF_Thermal_CP_01_cmd_prct"])
                    if key+"_ACTIF_Thermal_CP_01_state" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Thermal_CP_01_state",["CAMELS_entry","data",key+"_ACTIF_Thermal_CP_01_state"])
                    if key+"_ACTIF_Thermal_FLKS_01_CP_01_cmd_prct" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Thermal_FLKS_01_CP_01_cmd_prct",["CAMELS_entry","data",key+"_ACTIF_Thermal_FLKS_01_CP_01_cmd_prct"])
                    if key+"_ACTIF_Thermal_FLKS_01_CP_01_state" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Thermal_FLKS_01_CP_01_state",["CAMELS_entry","data",key+"_ACTIF_Thermal_FLKS_01_CP_01_state"])
                    if key+"_ACTIF_Thermal_FLKS_01_Fan_01_cmd" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Thermal_FLKS_01_Fan_01_cmd",["CAMELS_entry","data",key+"_ACTIF_Thermal_FLKS_01_Fan_01_cmd"])
                    if key+"_ACTIF_Thermal_FLKS_01_Fan_01_state" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Thermal_FLKS_01_Fan_01_state",["CAMELS_entry","data",key+"_ACTIF_Thermal_FLKS_01_Fan_01_state"])
                    if key+"_ACTIF_Thermal_MV_01_cmd" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Thermal_MV_01_cmd",["CAMELS_entry","data",key+"_ACTIF_Thermal_MV_01_cmd"])
                    if key+"_ACTIF_Thermal_MV_01_state" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Thermal_MV_01_state",["CAMELS_entry","data",key+"_ACTIF_Thermal_MV_01_state"])
                    if key+"_ACTIF_Thermal_PV_01_cmd" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Thermal_PV_01_cmd",["CAMELS_entry","data",key+"_ACTIF_Thermal_PV_01_cmd"])
                    if key+"_ACTIF_Thermal_PV_01_state" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Thermal_PV_01_state",["CAMELS_entry","data",key+"_ACTIF_Thermal_PV_01_state"])
                    if key+"_ACTIF_Thermal_PV_02_cmd" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Thermal_PV_02_cmd",["CAMELS_entry","data",key+"_ACTIF_Thermal_PV_02_cmd"])
                    if key+"_ACTIF_Thermal_PV_02_state" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif_data,"F_Thermal_PV_02_state",["CAMELS_entry","data",key+"_ACTIF_Thermal_PV_02_state"])
                    if key+"_ACTIF2_RH_01_A_state" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif2_data,"F2_RH_01_A_state",["CAMELS_entry","data",key+"_ACTIF2_RH_01_A_state"])
                    if key+"_ACTIF2_RH_01_A_cmd" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif2_data,"F2_RH_01_A_cmd",["CAMELS_entry","data",key+"_ACTIF2_RH_01_A_cmd"])
                    if key+"_ACTIF2_RH_01_B_state" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif2_data,"F2_RH_01_B_state",["CAMELS_entry","data",key+"_ACTIF2_RH_01_B_state"])
                    if key+"_ACTIF2_RH_01_B_cmd" in  f["CAMELS_entry"]["data"]:
                        self.set_atribute(f,actif2_data,"F2_RH_01_B_cmd",["CAMELS_entry","data",key+"_ACTIF2_RH_01_B_cmd"])

                #schema.mio_data.append(mio_data)
                #schema.data.actif_data.append(actif_data)
                #schema.data.actif2_data.append(actif2_data)
                #schema.data.hp_can_data.append(hp_can_data)
                archive.data=schema
        logger.info("h5 was read propperly")
        logger.info(str(os.getcwd()))
