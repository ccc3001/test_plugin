import h5py
from datetime import datetime 
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
from test_plugin.schema_packages.schema_package import NewSchemaPackage,MIOData,ACTIF2Data,ACTIFData,HP_CANData,Ploted_values

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
        schema.file_name = str(os.path.splitext(os.path.basename(str(mainfile)))[0])
        schema.date = str(datetime.today().strftime('%Y-%m-%d'))
        with h5py.File(mainfile, "r") as f:
            if len(f.keys())==1:
                CAMELS_entry=list(f.keys())[0]
            else:
                CAMELS_entry=list(f.keys())[0]
            if "measurement_comments" in f[CAMELS_entry]["measurement_details"]:
                if str(f[CAMELS_entry]["measurement_details"]["measurement_comments"][()]) != "b''":
                    self.set_atribute(f,schema, "measurement_comments" , [CAMELS_entry, "measurement_details", "measurement_comments"])
            if "measurement_description" in f[CAMELS_entry]["measurement_details"]:
                if str(f[CAMELS_entry]["measurement_details"]["measurement_description"][()]) != "b''":
                    self.set_atribute(f,schema,"measurement_description",[CAMELS_entry,"measurement_details","measurement_description"])
            if "protocol_description" in f[CAMELS_entry]["measurement_details"]:
                if str(f[CAMELS_entry]["measurement_details"]["protocol_description"][()]) != "b''":
                    self.set_atribute(f,schema,"protocol_description",[CAMELS_entry,"measurement_details","protocol_description"])
            if "first_name" in f[CAMELS_entry]["user"]:
                if str(f[CAMELS_entry]["user"]["first_name"][()]) != "b''":
                    self.set_atribute(f,schema,"first_name",[CAMELS_entry,"user","first_name"])
            if "last_name" in f[CAMELS_entry]["user"]:
                if str(f[CAMELS_entry]["user"]["last_name"][()]) != "b''":
                    self.set_atribute(f,schema,"last_name",[CAMELS_entry,"user","last_name"])
            if "email" in f[CAMELS_entry]["user"]:
                if str(f[CAMELS_entry]["user"]["email"][()]) != "b''":
                    self.set_atribute(f,schema,"email",[CAMELS_entry,"user","email"])
            if "affiliation" in f[CAMELS_entry]["user"]:
                if str(f[CAMELS_entry]["user"]["affiliation"][()]) != "b''":
                    self.set_atribute(f,schema,"affiliation",[CAMELS_entry,"user","affiliation"])
            self.set_atribute(f,schema,"time",[CAMELS_entry,"data","time"])
            self.set_atribute(f,actif_data,"time",[CAMELS_entry,"data","time"])

            self.set_atribute(f,schema,"elapsed_time",[CAMELS_entry,"data","ElapsedTime"])
            for key in f[CAMELS_entry]["instruments"]:
                if "opc" and "ua" in key:
                    if key+"_MIO_TV_01_A_PWM_pwmDutyCycle" in f[CAMELS_entry]["data"]:
                        TV_01_A_PWM_pwmDutyCycle=mio_data.m_create(Ploted_values,MIOData.TV_01_A_PWM_pwmDutyCycle)
                        self.set_atribute(f,TV_01_A_PWM_pwmDutyCycle,"data",[CAMELS_entry,"data",key+"_MIO_TV_01_A_PWM_pwmDutyCycle"])
                    if key+"_MIO_TV_01_B_PWM_pwmDutyCycle" in f[CAMELS_entry]["data"]:
                        TV_01_B_PWM_pwmDutyCycle=mio_data.m_create(Ploted_values,MIOData.TV_01_B_PWM_pwmDutyCycle)
                        self.set_atribute(f,TV_01_B_PWM_pwmDutyCycle,"data",[CAMELS_entry,"data",key+"_MIO_TV_01_B_PWM_pwmDutyCycle"])
                    if key+"_MIO_TV_02_A_PWM_doDiagnostics" in f[CAMELS_entry]["data"]:
                        TV_02_A_PWM_doDiagnostics=mio_data.m_create(Ploted_values,MIOData.TV_02_A_PWM_doDiagnostics)
                        self.set_atribute(f,TV_02_A_PWM_doDiagnostics,"data",[CAMELS_entry,"data",key+"_MIO_TV_02_A_PWM_doDiagnostics"])
                    if key+"_MIO_TV_02_A_PWM_pwmDutyCycle" in f[CAMELS_entry]["data"]:
                        TV_02_A_PWM_pwmDutyCycle=mio_data.m_create(Ploted_values,MIOData.TV_02_A_PWM_pwmDutyCycle)
                        self.set_atribute(f,TV_02_A_PWM_pwmDutyCycle,"data",[CAMELS_entry,"data",key+"_MIO_TV_02_A_PWM_pwmDutyCycle"])
                    if key+"_MIO_TV_02_B_PWM_pwmDutyCycle" in f[CAMELS_entry]["data"]:
                        TV_02_B_PWM_pwmDutyCycle=mio_data.m_create(Ploted_values,MIOData.TV_02_B_PWM_pwmDutyCycle)
                        self.set_atribute(f,TV_02_B_PWM_pwmDutyCycle,"data",[CAMELS_entry,"data",key+"_MIO_TV_02_B_PWM_pwmDutyCycle"])
                    if key+"_MIO_TV_03_A_PWM_pwmDutyCycle" in f[CAMELS_entry]["data"]:
                        TV_03_A_PWM_pwmDutyCycle=mio_data.m_create(Ploted_values,MIOData.TV_03_A_PWM_pwmDutyCycle)
                        self.set_atribute(f,TV_03_A_PWM_pwmDutyCycle,"data",[CAMELS_entry,"data",key+"_MIO_TV_03_A_PWM_pwmDutyCycle"])
                    if key+"_MIO_TV_03_B_PWM_pwmDutyCycle" in f[CAMELS_entry]["data"]:
                        TV_03_B_PWM_pwmDutyCycle=mio_data.m_create(Ploted_values,MIOData.TV_03_B_PWM_pwmDutyCycle)
                        self.set_atribute(f,TV_03_B_PWM_pwmDutyCycle,"data",[CAMELS_entry,"data",key+"_MIO_TV_03_B_PWM_pwmDutyCycle"])
                    if key+"_MIO_TV_01_A_pos_viDiagnostics" in f[CAMELS_entry]["data"]:
                        TV_01_A_pos_viDiagnostics=mio_data.m_create(Ploted_values,MIOData.TV_01_A_pos_viDiagnostics)
                        self.set_atribute(f,TV_01_A_pos_viDiagnostics,"data",[CAMELS_entry,"data",key+"_MIO_TV_01_A_pos_viDiagnostics"])
                    if key+"_MIO_TV_01_B_pos_viDiagnostics" in f[CAMELS_entry]["data"]:
                        TV_01_B_pos_viDiagnostics=mio_data.m_create(Ploted_values,MIOData.TV_01_B_pos_viDiagnostics)
                        self.set_atribute(f,TV_01_B_pos_viDiagnostics,"data",[CAMELS_entry,"data",key+"_MIO_TV_01_B_pos_viDiagnostics"])
                    if key+"_MIO_TV_02_A_pos_viDiagnostics" in f[CAMELS_entry]["data"]:
                        TV_02_A_pos_viDiagnostics=mio_data.m_create(Ploted_values,MIOData.TV_02_A_pos_viDiagnostics)
                        self.set_atribute(f,TV_02_A_pos_viDiagnostics,"data",[CAMELS_entry,"data",key+"_MIO_TV_02_A_pos_viDiagnostics"])
                    if key+"_MIO_TV_02_B_pos_viDiagnostics" in f[CAMELS_entry]["data"]:
                        TV_02_B_pos_viDiagnostics=mio_data.m_create(Ploted_values,MIOData.TV_02_B_pos_viDiagnostics)
                        self.set_atribute(f,TV_02_B_pos_viDiagnostics,"data",[CAMELS_entry,"data",key+"_MIO_TV_02_B_pos_viDiagnostics"])
                    if key+"_MIO_TV_03_A_pos_viDiagnostics" in f[CAMELS_entry]["data"]:
                        TV_03_A_pos_viDiagnostics=mio_data.m_create(Ploted_values,MIOData.TV_03_A_pos_viDiagnostics)
                        self.set_atribute(f,TV_03_A_pos_viDiagnostics,"data",[CAMELS_entry,"data",key+"_MIO_TV_03_A_pos_viDiagnostics"])
                    if key+"_MIO_TV_03_B_pos_viDiagnostics" in f[CAMELS_entry]["data"]:
                        TV_03_B_pos_viDiagnostics=mio_data.m_create(Ploted_values,MIOData.TV_03_B_pos_viDiagnostics)
                        self.set_atribute(f,TV_03_B_pos_viDiagnostics,"data",[CAMELS_entry,"data",key+"_MIO_TV_03_B_pos_viDiagnostics"])
                    if key+"_MIO_AR_01_PWM_pwmDutyCycle" in f[CAMELS_entry]["data"]:
                        AR_01_PWM_pwmDutyCycle=mio_data.m_create(Ploted_values,MIOData.AR_01_PWM_pwmDutyCycle)
                        self.set_atribute(f,AR_01_PWM_pwmDutyCycle,"data",[CAMELS_entry,"data",key+"_MIO_AR_01_PWM_pwmDutyCycle"])
                    if key+"_MIO_Supply_Position_Sensors_TV_voDiagnostics" in f[CAMELS_entry]["data"]:
                        Supply_Position_Sensors_TV_voDiagnostics=mio_data.m_create(Ploted_values,MIOData.Supply_Position_Sensors_TV_voDiagnostics)
                        self.set_atribute(f,Supply_Position_Sensors_TV_voDiagnostics,"data",[CAMELS_entry,"data",key+"_MIO_Supply_Position_Sensors_TV_voDiagnostics"])
                    if key+"_MIO_T_ambient" in f[CAMELS_entry]["data"]:
                        T_ambient=mio_data.m_create(Ploted_values,MIOData.T_ambient)
                        self.set_atribute(f,T_ambient,"data",[CAMELS_entry,"data",key+"_MIO_T_ambient"])
                    if key+"_MIO_p_ambient" in f[CAMELS_entry]["data"]:
                        p_ambient=mio_data.m_create(Ploted_values,MIOData.p_ambient)
                        self.set_atribute(f,p_ambient,"data",[CAMELS_entry,"data",key+"_MIO_p_ambient"])
                    if key+"_MIO_RoundTrip_in_diDiagnostics" in f[CAMELS_entry]["data"]:
                        RoundTrip_in_diDiagnostics=mio_data.m_create(Ploted_values,MIOData.RoundTrip_in_diDiagnostics)
                        self.set_atribute(f,RoundTrip_in_diDiagnostics,"data",[CAMELS_entry,"data",key+"_MIO_RoundTrip_in_diDiagnostics"])
                    if key+"_MIO_T_ambient_Celsius" in f[CAMELS_entry]["data"]:
                        T_ambient_Celsius=mio_data.m_create(Ploted_values,MIOData.T_ambient_Celsius)
                        self.set_atribute(f,T_ambient_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_T_ambient_Celsius"])
                    if key+"_MIO_p_ambient_barA" in f[CAMELS_entry]["data"]:
                        p_ambient_barA=mio_data.m_create(Ploted_values,MIOData.p_ambient_barA)
                        self.set_atribute(f,p_ambient_barA,"data",[CAMELS_entry,"data",key+"_MIO_p_ambient_barA"])
                    if key+"_MIO_Actuators_Anode_A_PV_01_prct" in f[CAMELS_entry]["data"]:
                        Actuators_Anode_A_PV_01_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Anode_A_PV_01_prct)
                        self.set_atribute(f,Actuators_Anode_A_PV_01_prct,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Anode_A_PV_01_prct"])
                    if key+"_MIO_Actuators_Anode_A_PC_01_pDiff" in f[CAMELS_entry]["data"]:
                        Actuators_Anode_A_PC_01_pDiff=mio_data.m_create(Ploted_values,MIOData.Actuators_Anode_A_PC_01_pDiff)
                        self.set_atribute(f,Actuators_Anode_A_PC_01_pDiff,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Anode_A_PC_01_pDiff"])
                    if key+"_MIO_Actuators_Anode_A_PC_01_pDiff_ref" in f[CAMELS_entry]["data"]:
                        Actuators_Anode_A_PC_01_pDiff_ref=mio_data.m_create(Ploted_values,MIOData.Actuators_Anode_A_PC_01_pDiff_ref)
                        self.set_atribute(f,Actuators_Anode_A_PC_01_pDiff_ref,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Anode_A_PC_01_pDiff_ref"])
                    if key+"_MIO_Actuators_Anode_B_PV_01_prct" in f[CAMELS_entry]["data"]:
                        Actuators_Anode_B_PV_01_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Anode_B_PV_01_prct)
                        self.set_atribute(f,Actuators_Anode_B_PV_01_prct,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Anode_B_PV_01_prct"])
                    if key+"_MIO_Actuators_Anode_B_PC_01_pDiff" in f[CAMELS_entry]["data"]:
                        Actuators_Anode_B_PC_01_pDiff=mio_data.m_create(Ploted_values,MIOData.Actuators_Anode_B_PC_01_pDiff)
                        self.set_atribute(f,Actuators_Anode_B_PC_01_pDiff,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Anode_B_PC_01_pDiff"])
                    if key+"_MIO_Actuators_Anode_B_PC_01_pDiff_ref" in f[CAMELS_entry]["data"]:
                        Actuators_Anode_B_PC_01_pDiff_ref=mio_data.m_create(Ploted_values,MIOData.Actuators_Anode_B_PC_01_pDiff_ref)
                        self.set_atribute(f,Actuators_Anode_B_PC_01_pDiff_ref,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Anode_B_PC_01_pDiff_ref"])
                    if key+"_MIO_Actuators_Thermal_FLKS_01_freq_ref_Hz" in f[CAMELS_entry]["data"]:
                        Actuators_Thermal_FLKS_01_freq_ref_Hz=mio_data.m_create(Ploted_values,MIOData.Actuators_Thermal_FLKS_01_freq_ref_Hz)
                        self.set_atribute(f,Actuators_Thermal_FLKS_01_freq_ref_Hz,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Thermal_FLKS_01_freq_ref_Hz"])
                    if key+"_MIO_Actuators_Thermal_FLKS_01_fan_prct" in f[CAMELS_entry]["data"]:
                        Actuators_Thermal_FLKS_01_fan_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Thermal_FLKS_01_fan_prct)
                        self.set_atribute(f,Actuators_Thermal_FLKS_01_fan_prct,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Thermal_FLKS_01_fan_prct"])
                    if key+"_MIO_Actuators_Thermal_PV_01_prct" in f[CAMELS_entry]["data"]:
                        Actuators_Thermal_PV_01_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Thermal_PV_01_prct)
                        self.set_atribute(f,Actuators_Thermal_PV_01_prct,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Thermal_PV_01_prct"])
                    if key+"_MIO_Actuators_Thermal_PV_02_prct" in f[CAMELS_entry]["data"]:
                        Actuators_Thermal_PV_02_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Thermal_PV_02_prct)
                        self.set_atribute(f,Actuators_Thermal_PV_02_prct,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Thermal_PV_02_prct"])
                    if key+"_MIO_Actuators_Thermal_MV_01_ref_prct" in f[CAMELS_entry]["data"]:
                        Actuators_Thermal_MV_01_ref_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Thermal_MV_01_ref_prct)
                        self.set_atribute(f,Actuators_Thermal_MV_01_ref_prct,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Thermal_MV_01_ref_prct"])
                    if key+"_MIO_Actuators_Thermal_MV_01_act_prct" in f[CAMELS_entry]["data"]:
                        Actuators_Thermal_MV_01_act_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Thermal_MV_01_act_prct)
                        self.set_atribute(f,Actuators_Thermal_MV_01_act_prct,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Thermal_MV_01_act_prct"])
                    if key+"_MIO_Actuators_Thermal_CP_01_freq_ref_Hz" in f[CAMELS_entry]["data"]:
                        Actuators_Thermal_CP_01_freq_ref_Hz=mio_data.m_create(Ploted_values,MIOData.Actuators_Thermal_CP_01_freq_ref_Hz)
                        self.set_atribute(f,Actuators_Thermal_CP_01_freq_ref_Hz,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Thermal_CP_01_freq_ref_Hz"])
                    if key+"_MIO_Actuators_Thermal_CP_01_freq_act_Hz" in f[CAMELS_entry]["data"]:
                        Actuators_Thermal_CP_01_freq_act_Hz=mio_data.m_create(Ploted_values,MIOData.Actuators_Thermal_CP_01_freq_act_Hz)
                        self.set_atribute(f,Actuators_Thermal_CP_01_freq_act_Hz,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Thermal_CP_01_freq_act_Hz"])
                    if key+"_MIO_Actuators_Thermal_A_AV_01_ref_prct" in f[CAMELS_entry]["data"]:
                        Actuators_Thermal_A_AV_01_ref_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Thermal_A_AV_01_ref_prct)
                        self.set_atribute(f,Actuators_Thermal_A_AV_01_ref_prct,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Thermal_A_AV_01_ref_prct"])
                    if key+"_MIO_Actuators_Thermal_A_AV_01_act_prct" in f[CAMELS_entry]["data"]:
                        Actuators_Thermal_A_AV_01_act_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Thermal_A_AV_01_act_prct)
                        self.set_atribute(f,Actuators_Thermal_A_AV_01_act_prct,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Thermal_A_AV_01_act_prct"])
                    if key+"_MIO_Actuators_Thermal_B_AV_01_ref_prct" in f[CAMELS_entry]["data"]:
                        Actuators_Thermal_B_AV_01_ref_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Thermal_B_AV_01_ref_prct)
                        self.set_atribute(f,Actuators_Thermal_B_AV_01_ref_prct,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Thermal_B_AV_01_ref_prct"])
                    if key+"_MIO_Actuators_Thermal_B_AV_01_act_prct" in f[CAMELS_entry]["data"]:
                        Actuators_Thermal_B_AV_01_act_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Thermal_B_AV_01_act_prct)
                        self.set_atribute(f,Actuators_Thermal_B_AV_01_act_prct,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Thermal_B_AV_01_act_prct"])
                    if key+"_MIO_Actuators_Cathode_AR_01_prct" in f[CAMELS_entry]["data"]:
                        Actuators_Cathode_AR_01_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_AR_01_prct)
                        self.set_atribute(f,Actuators_Cathode_AR_01_prct,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Cathode_AR_01_prct"])
                    if key+"_MIO_Actuators_Cathode_EH_01_Power_prct" in f[CAMELS_entry]["data"]:
                        Actuators_Cathode_EH_01_Power_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_EH_01_Power_prct)
                        self.set_atribute(f,Actuators_Cathode_EH_01_Power_prct,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Cathode_EH_01_Power_prct"])
                    if key+"_MIO_Actuators_Cathode_EH_02_Power_prct" in f[CAMELS_entry]["data"]:
                        Actuators_Cathode_EH_02_Power_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_EH_02_Power_prct)
                        self.set_atribute(f,Actuators_Cathode_EH_02_Power_prct,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Cathode_EH_02_Power_prct"])
                    if key+"_MIO_Actuators_Cathode_A_TV_01_pos_V" in f[CAMELS_entry]["data"]:
                        Actuators_Cathode_A_TV_01_pos_V=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_A_TV_01_pos_V)
                        self.set_atribute(f,Actuators_Cathode_A_TV_01_pos_V,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Cathode_A_TV_01_pos_V"])
                    if key+"_MIO_Actuators_Cathode_A_TV_01_pwmDutyCycle" in f[CAMELS_entry]["data"]:
                        Actuators_Cathode_A_TV_01_pwmDutyCycle=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_A_TV_01_pwmDutyCycle)
                        self.set_atribute(f,Actuators_Cathode_A_TV_01_pwmDutyCycle,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Cathode_A_TV_01_pwmDutyCycle"])
                    if key+"_MIO_Actuators_Cathode_A_TV_02_pos_V" in f[CAMELS_entry]["data"]:
                        Actuators_Cathode_A_TV_02_pos_V=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_A_TV_02_pos_V)
                        self.set_atribute(f,Actuators_Cathode_A_TV_02_pos_V,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Cathode_A_TV_02_pos_V"])
                    if key+"_MIO_Actuators_Cathode_A_TV_02_pwmDutyCycle" in f[CAMELS_entry]["data"]:
                        Actuators_Cathode_A_TV_02_pwmDutyCycle=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_A_TV_02_pwmDutyCycle)
                        self.set_atribute(f,Actuators_Cathode_A_TV_02_pwmDutyCycle,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Cathode_A_TV_02_pwmDutyCycle"])
                    if key+"_MIO_Actuators_Cathode_A_TV_03_pos_V" in f[CAMELS_entry]["data"]:
                        Actuators_Cathode_A_TV_03_pos_V=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_A_TV_03_pos_V)
                        self.set_atribute(f,Actuators_Cathode_A_TV_03_pos_V,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Cathode_A_TV_03_pos_V"])
                    if key+"_MIO_Actuators_Cathode_A_TV_03_pwmDutyCycle" in f[CAMELS_entry]["data"]:
                        Actuators_Cathode_A_TV_03_pwmDutyCycle=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_A_TV_03_pwmDutyCycle)
                        self.set_atribute(f,Actuators_Cathode_A_TV_03_pwmDutyCycle,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Cathode_A_TV_03_pwmDutyCycle"])
                    if key+"_MIO_Actuators_Cathode_B_TV_01_pos_V" in f[CAMELS_entry]["data"]:
                        Actuators_Cathode_B_TV_01_pos_V=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_B_TV_01_pos_V)
                        self.set_atribute(f,Actuators_Cathode_B_TV_01_pos_V,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Cathode_B_TV_01_pos_V"])
                    if key+"_MIO_Actuators_Cathode_B_TV_01_pwmDutyCycle" in f[CAMELS_entry]["data"]:
                        Actuators_Cathode_B_TV_01_pwmDutyCycle=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_B_TV_01_pwmDutyCycle)
                        self.set_atribute(f,Actuators_Cathode_B_TV_01_pwmDutyCycle,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Cathode_B_TV_01_pwmDutyCycle"])
                    if key+"_MIO_Actuators_Cathode_B_TV_02_pos_V" in f[CAMELS_entry]["data"]:
                        Actuators_Cathode_B_TV_02_pos_V=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_B_TV_02_pos_V)
                        self.set_atribute(f,Actuators_Cathode_B_TV_02_pos_V,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Cathode_B_TV_02_pos_V"])
                    if key+"_MIO_Actuators_Cathode_B_TV_02_pwmDutyCycle" in f[CAMELS_entry]["data"]:
                        Actuators_Cathode_B_TV_02_pwmDutyCycle=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_B_TV_02_pwmDutyCycle)
                        self.set_atribute(f,Actuators_Cathode_B_TV_02_pwmDutyCycle,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Cathode_B_TV_02_pwmDutyCycle"])
                    if key+"_MIO_Actuators_Cathode_B_TV_03_pos_V" in f[CAMELS_entry]["data"]:
                        Actuators_Cathode_B_TV_03_pos_V=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_B_TV_03_pos_V)
                        self.set_atribute(f,Actuators_Cathode_B_TV_03_pos_V,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Cathode_B_TV_03_pos_V"])
                    if key+"_MIO_Actuators_Cathode_B_TV_03_pwmDutyCycle" in f[CAMELS_entry]["data"]:
                        Actuators_Cathode_B_TV_03_pwmDutyCycle=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_B_TV_03_pwmDutyCycle)
                        self.set_atribute(f,Actuators_Cathode_B_TV_03_pwmDutyCycle,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Cathode_B_TV_03_pwmDutyCycle"])
                    if key+"_MIO_Actuators_Cathode_MFC_01_00_p_PSIA" in f[CAMELS_entry]["data"]:
                        Actuators_Cathode_MFC_01_00_p_PSIA=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_MFC_01_00_p_PSIA)
                        self.set_atribute(f,Actuators_Cathode_MFC_01_00_p_PSIA,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Cathode_MFC_01_00_p_PSIA"])
                    if key+"_MIO_Actuators_Cathode_MFC_01_00_T_Celsius" in f[CAMELS_entry]["data"]:
                        Actuators_Cathode_MFC_01_00_T_Celsius=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_MFC_01_00_T_Celsius)
                        self.set_atribute(f,Actuators_Cathode_MFC_01_00_T_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Cathode_MFC_01_00_T_Celsius"])
                    if key+"_MIO_Actuators_Cathode_MFC_01_00_Vflow_LPM" in f[CAMELS_entry]["data"]:
                        Actuators_Cathode_MFC_01_00_Vflow_LPM=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_MFC_01_00_Vflow_LPM)
                        self.set_atribute(f,Actuators_Cathode_MFC_01_00_Vflow_LPM,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Cathode_MFC_01_00_Vflow_LPM"])
                    if key+"_MIO_Actuators_Cathode_MFC_01_00_mflow_SLPM" in f[CAMELS_entry]["data"]:
                        Actuators_Cathode_MFC_01_00_mflow_SLPM=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_MFC_01_00_mflow_SLPM)
                        self.set_atribute(f,Actuators_Cathode_MFC_01_00_mflow_SLPM,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Cathode_MFC_01_00_mflow_SLPM"])
                    if key+"_MIO_Actuators_Cathode_MFC_01_00_ref_SLPM" in f[CAMELS_entry]["data"]:
                        Actuators_Cathode_MFC_01_00_ref_SLPM=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_MFC_01_00_ref_SLPM)
                        self.set_atribute(f,Actuators_Cathode_MFC_01_00_ref_SLPM,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Cathode_MFC_01_00_ref_SLPM"])
                    if key+"_MIO_Actuators_Cathode_MFC_01_00_set_SLPM" in f[CAMELS_entry]["data"]:
                        Actuators_Cathode_MFC_01_00_set_SLPM=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_MFC_01_00_set_SLPM)
                        self.set_atribute(f,Actuators_Cathode_MFC_01_00_set_SLPM,"data",[CAMELS_entry,"data",key+"_MIO_Actuators_Cathode_MFC_01_00_set_SLPM"])
                    if key+"_MIO_ECAT_10301_moduleQuality" in f[CAMELS_entry]["data"]:
                        ECAT_10301_moduleQuality=mio_data.m_create(Ploted_values,MIOData.ECAT_10301_moduleQuality)
                        self.set_atribute(f,ECAT_10301_moduleQuality,"data",[CAMELS_entry,"data",key+"_MIO_ECAT_10301_moduleQuality"])
                    if key+"_MIO_ECAT_10302_moduleQuality" in f[CAMELS_entry]["data"]:
                        ECAT_10302_moduleQuality=mio_data.m_create(Ploted_values,MIOData.ECAT_10302_moduleQuality)
                        self.set_atribute(f,ECAT_10302_moduleQuality,"data",[CAMELS_entry,"data",key+"_MIO_ECAT_10302_moduleQuality"])
                    if key+"_MIO_ECAT_10303_moduleQuality" in f[CAMELS_entry]["data"]:
                        ECAT_10303_moduleQuality=mio_data.m_create(Ploted_values,MIOData.ECAT_10303_moduleQuality)
                        self.set_atribute(f,ECAT_10303_moduleQuality,"data",[CAMELS_entry,"data",key+"_MIO_ECAT_10303_moduleQuality"])
                    if key+"_MIO_ECAT_1001_RX_Device_Readings_Gas_Index" in f[CAMELS_entry]["data"]:
                        ECAT_1001_RX_Device_Readings_Gas_Index=mio_data.m_create(Ploted_values,MIOData.ECAT_1001_RX_Device_Readings_Gas_Index)
                        self.set_atribute(f,ECAT_1001_RX_Device_Readings_Gas_Index,"data",[CAMELS_entry,"data",key+"_MIO_ECAT_1001_RX_Device_Readings_Gas_Index"])
                    if key+"_MIO_ECAT_1001_RX_Command_Result_Last_Command_ID" in f[CAMELS_entry]["data"]:
                        ECAT_1001_RX_Command_Result_Last_Command_ID=mio_data.m_create(Ploted_values,MIOData.ECAT_1001_RX_Command_Result_Last_Command_ID)
                        self.set_atribute(f,ECAT_1001_RX_Command_Result_Last_Command_ID,"data",[CAMELS_entry,"data",key+"_MIO_ECAT_1001_RX_Command_Result_Last_Command_ID"])
                    if key+"_MIO_ECAT_1001_RX_Command_Result_Last_Command_Status" in f[CAMELS_entry]["data"]:
                        ECAT_1001_RX_Command_Result_Last_Command_Status=mio_data.m_create(Ploted_values,MIOData.ECAT_1001_RX_Command_Result_Last_Command_Status)
                        self.set_atribute(f,ECAT_1001_RX_Command_Result_Last_Command_Status,"data",[CAMELS_entry,"data",key+"_MIO_ECAT_1001_RX_Command_Result_Last_Command_Status"])
                    if key+"_MIO_ECAT_1001_TX_Setpoint_Setpoint" in f[CAMELS_entry]["data"]:
                        ECAT_1001_TX_Setpoint_Setpoint=mio_data.m_create(Ploted_values,MIOData.ECAT_1001_TX_Setpoint_Setpoint)
                        self.set_atribute(f,ECAT_1001_TX_Setpoint_Setpoint,"data",[CAMELS_entry,"data",key+"_MIO_ECAT_1001_TX_Setpoint_Setpoint"])
                    if key+"_MIO_ECAT_1001_TX_Command_Request_Command_ID" in f[CAMELS_entry]["data"]:
                        ECAT_1001_TX_Command_Request_Command_ID=mio_data.m_create(Ploted_values,MIOData.ECAT_1001_TX_Command_Request_Command_ID)
                        self.set_atribute(f,ECAT_1001_TX_Command_Request_Command_ID,"data",[CAMELS_entry,"data",key+"_MIO_ECAT_1001_TX_Command_Request_Command_ID"])
                    if key+"_MIO_ECAT_1001_TX_Command_Request_Command_Argument" in f[CAMELS_entry]["data"]:
                        ECAT_1001_TX_Command_Request_Command_Argument=mio_data.m_create(Ploted_values,MIOData.ECAT_1001_TX_Command_Request_Command_Argument)
                        self.set_atribute(f,ECAT_1001_TX_Command_Request_Command_Argument,"data",[CAMELS_entry,"data",key+"_MIO_ECAT_1001_TX_Command_Request_Command_Argument"])
                    if key+"_MIO_ECAT_1002_RX_Device_Readings_Gas_Index" in f[CAMELS_entry]["data"]:
                        ECAT_1002_RX_Device_Readings_Gas_Index=mio_data.m_create(Ploted_values,MIOData.ECAT_1002_RX_Device_Readings_Gas_Index)
                        self.set_atribute(f,ECAT_1002_RX_Device_Readings_Gas_Index,"data",[CAMELS_entry,"data",key+"_MIO_ECAT_1002_RX_Device_Readings_Gas_Index"])
                    if key+"_MIO_ECAT_1002_RX_Command_Result_Last_Command_ID" in f[CAMELS_entry]["data"]:
                        ECAT_1002_RX_Command_Result_Last_Command_ID=mio_data.m_create(Ploted_values,MIOData.ECAT_1002_RX_Command_Result_Last_Command_ID)
                        self.set_atribute(f,ECAT_1002_RX_Command_Result_Last_Command_ID,"data",[CAMELS_entry,"data",key+"_MIO_ECAT_1002_RX_Command_Result_Last_Command_ID"])
                    if key+"_MIO_ECAT_1002_RX_Command_Result_Last_Command_Status" in f[CAMELS_entry]["data"]:
                        ECAT_1002_RX_Command_Result_Last_Command_Status=mio_data.m_create(Ploted_values,MIOData.ECAT_1002_RX_Command_Result_Last_Command_Status)
                        self.set_atribute(f,ECAT_1002_RX_Command_Result_Last_Command_Status,"data",[CAMELS_entry,"data",key+"_MIO_ECAT_1002_RX_Command_Result_Last_Command_Status"])
                    if key+"_MIO_ECAT_1002_TX_Setpoint_Setpoint" in f[CAMELS_entry]["data"]:
                        ECAT_1002_TX_Setpoint_Setpoint=mio_data.m_create(Ploted_values,MIOData.ECAT_1002_TX_Setpoint_Setpoint)
                        self.set_atribute(f,ECAT_1002_TX_Setpoint_Setpoint,"data",[CAMELS_entry,"data",key+"_MIO_ECAT_1002_TX_Setpoint_Setpoint"])
                    if key+"_MIO_ECAT_1002_TX_Command_Request_Command_ID" in f[CAMELS_entry]["data"]:
                        ECAT_1002_TX_Command_Request_Command_ID=mio_data.m_create(Ploted_values,MIOData.ECAT_1002_TX_Command_Request_Command_ID)
                        self.set_atribute(f,ECAT_1002_TX_Command_Request_Command_ID,"data",[CAMELS_entry,"data",key+"_MIO_ECAT_1002_TX_Command_Request_Command_ID"])
                    if key+"_MIO_ECAT_1002_TX_Command_Request_Command_Argument" in f[CAMELS_entry]["data"]:
                        ECAT_1002_TX_Command_Request_Command_Argument=mio_data.m_create(Ploted_values,MIOData.ECAT_1002_TX_Command_Request_Command_Argument)
                        self.set_atribute(f,ECAT_1002_TX_Command_Request_Command_Argument,"data",[CAMELS_entry,"data",key+"_MIO_ECAT_1002_TX_Command_Request_Command_Argument"])
                    if key+"_MIO_ECAT_1004_RX_Device_Readings_Gas_Index" in f[CAMELS_entry]["data"]:
                        ECAT_1004_RX_Device_Readings_Gas_Index=mio_data.m_create(Ploted_values,MIOData.ECAT_1004_RX_Device_Readings_Gas_Index)
                        self.set_atribute(f,ECAT_1004_RX_Device_Readings_Gas_Index,"data",[CAMELS_entry,"data",key+"_MIO_ECAT_1004_RX_Device_Readings_Gas_Index"])
                    if key+"_MIO_ECAT_1004_RX_Command_Result_Last_Command_ID" in f[CAMELS_entry]["data"]:
                        ECAT_1004_RX_Command_Result_Last_Command_ID=mio_data.m_create(Ploted_values,MIOData.ECAT_1004_RX_Command_Result_Last_Command_ID)
                        self.set_atribute(f,ECAT_1004_RX_Command_Result_Last_Command_ID,"data",[CAMELS_entry,"data",key+"_MIO_ECAT_1004_RX_Command_Result_Last_Command_ID"])
                    if key+"_MIO_ECAT_1004_RX_Command_Result_Last_Command_Status" in f[CAMELS_entry]["data"]:
                        ECAT_1004_RX_Command_Result_Last_Command_Status=mio_data.m_create(Ploted_values,MIOData.ECAT_1004_RX_Command_Result_Last_Command_Status)
                        self.set_atribute(f,ECAT_1004_RX_Command_Result_Last_Command_Status,"data",[CAMELS_entry,"data",key+"_MIO_ECAT_1004_RX_Command_Result_Last_Command_Status"])
                    if key+"_MIO_ECAT_1004_TX_Setpoint_Setpoint" in f[CAMELS_entry]["data"]:
                        ECAT_1004_TX_Setpoint_Setpoint=mio_data.m_create(Ploted_values,MIOData.ECAT_1004_TX_Setpoint_Setpoint)
                        self.set_atribute(f,ECAT_1004_TX_Setpoint_Setpoint,"data",[CAMELS_entry,"data",key+"_MIO_ECAT_1004_TX_Setpoint_Setpoint"])
                    if key+"_MIO_ECAT_1004_TX_Command_Request_Command_ID" in f[CAMELS_entry]["data"]:
                        ECAT_1004_TX_Command_Request_Command_ID=mio_data.m_create(Ploted_values,MIOData.ECAT_1004_TX_Command_Request_Command_ID)
                        self.set_atribute(f,ECAT_1004_TX_Command_Request_Command_ID,"data",[CAMELS_entry,"data",key+"_MIO_ECAT_1004_TX_Command_Request_Command_ID"])
                    if key+"_MIO_ECAT_1004_TX_Command_Request_Command_Argument" in f[CAMELS_entry]["data"]:
                        ECAT_1004_TX_Command_Request_Command_Argument=mio_data.m_create(Ploted_values,MIOData.ECAT_1004_TX_Command_Request_Command_Argument)
                        self.set_atribute(f,ECAT_1004_TX_Command_Request_Command_Argument,"data",[CAMELS_entry,"data",key+"_MIO_ECAT_1004_TX_Command_Request_Command_Argument"])
                    if key+"_MIO_Fluids_Cathode_PT_01_barG" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_PT_01_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_PT_01_barG)
                        self.set_atribute(f,Fluids_Cathode_PT_01_barG,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_PT_01_barG"])
                    if key+"_MIO_Fluids_Cathode_PT_02_barG" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_PT_02_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_PT_02_barG)
                        self.set_atribute(f,Fluids_Cathode_PT_02_barG,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_PT_02_barG"])
                    if key+"_MIO_Fluids_Cathode_PT_03_barG" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_PT_03_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_PT_03_barG)
                        self.set_atribute(f,Fluids_Cathode_PT_03_barG,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_PT_03_barG"])
                    if key+"_MIO_Fluids_Cathode_TT_01_0_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_TT_01_0_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_TT_01_0_Celsius)
                        self.set_atribute(f,Fluids_Cathode_TT_01_0_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_TT_01_0_Celsius"])
                    if key+"_MIO_Fluids_Cathode_TT_05_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_TT_05_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_TT_05_Celsius)
                        self.set_atribute(f,Fluids_Cathode_TT_05_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_TT_05_Celsius"])
                    if key+"_MIO_Fluids_Cathode_TT_02_0_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_TT_02_0_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_TT_02_0_Celsius)
                        self.set_atribute(f,Fluids_Cathode_TT_02_0_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_TT_02_0_Celsius"])
                    if key+"_MIO_Fluids_Cathode_TT_06_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_TT_06_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_TT_06_Celsius)
                        self.set_atribute(f,Fluids_Cathode_TT_06_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_TT_06_Celsius"])
                    if key+"_MIO_Fluids_Cathode_TT_03_0_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_TT_03_0_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_TT_03_0_Celsius)
                        self.set_atribute(f,Fluids_Cathode_TT_03_0_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_TT_03_0_Celsius"])
                    if key+"_MIO_Fluids_Cathode_TT_07_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_TT_07_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_TT_07_Celsius)
                        self.set_atribute(f,Fluids_Cathode_TT_07_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_TT_07_Celsius"])
                    if key+"_MIO_Fluids_Cathode_TT_01_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_TT_01_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_TT_01_Celsius)
                        self.set_atribute(f,Fluids_Cathode_TT_01_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_TT_01_Celsius"])
                    if key+"_MIO_Fluids_Cathode_TT_02_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_TT_02_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_TT_02_Celsius)
                        self.set_atribute(f,Fluids_Cathode_TT_02_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_TT_02_Celsius"])
                    if key+"_MIO_Fluids_Cathode_TT_04_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_TT_04_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_TT_04_Celsius)
                        self.set_atribute(f,Fluids_Cathode_TT_04_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_TT_04_Celsius"])
                    if key+"_MIO_Fluids_Cathode_A_PT_04_barG" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_A_PT_04_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_A_PT_04_barG)
                        self.set_atribute(f,Fluids_Cathode_A_PT_04_barG,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_A_PT_04_barG"])
                    if key+"_MIO_Fluids_Cathode_A_PT_05_barG" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_A_PT_05_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_A_PT_05_barG)
                        self.set_atribute(f,Fluids_Cathode_A_PT_05_barG,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_A_PT_05_barG"])
                    if key+"_MIO_Fluids_Cathode_A_PT_06_barG" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_A_PT_06_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_A_PT_06_barG)
                        self.set_atribute(f,Fluids_Cathode_A_PT_06_barG,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_A_PT_06_barG"])
                    if key+"_MIO_Fluids_Cathode_A_MFT_02_slpm" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_A_MFT_02_slpm=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_A_MFT_02_slpm)
                        self.set_atribute(f,Fluids_Cathode_A_MFT_02_slpm,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_A_MFT_02_slpm"])
                    if key+"_MIO_Fluids_Cathode_A_RHT_01_prctRH" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_A_RHT_01_prctRH=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_A_RHT_01_prctRH)
                        self.set_atribute(f,Fluids_Cathode_A_RHT_01_prctRH,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_A_RHT_01_prctRH"])
                    if key+"_MIO_Fluids_Cathode_A_TT_09_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_A_TT_09_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_A_TT_09_Celsius)
                        self.set_atribute(f,Fluids_Cathode_A_TT_09_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_A_TT_09_Celsius"])
                    if key+"_MIO_Fluids_Cathode_A_TT_08_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_A_TT_08_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_A_TT_08_Celsius)
                        self.set_atribute(f,Fluids_Cathode_A_TT_08_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_A_TT_08_Celsius"])
                    if key+"_MIO_Fluids_Cathode_A_TT_10_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_A_TT_10_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_A_TT_10_Celsius)
                        self.set_atribute(f,Fluids_Cathode_A_TT_10_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_A_TT_10_Celsius"])
                    if key+"_MIO_Fluids_Cathode_A_TT_11_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_A_TT_11_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_A_TT_11_Celsius)
                        self.set_atribute(f,Fluids_Cathode_A_TT_11_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_A_TT_11_Celsius"])
                    if key+"_MIO_Fluids_Cathode_A_TT_12_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_A_TT_12_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_A_TT_12_Celsius)
                        self.set_atribute(f,Fluids_Cathode_A_TT_12_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_A_TT_12_Celsius"])
                    if key+"_MIO_Fluids_Cathode_B_PT_04_barG" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_B_PT_04_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_B_PT_04_barG)
                        self.set_atribute(f,Fluids_Cathode_B_PT_04_barG,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_B_PT_04_barG"])
                    if key+"_MIO_Fluids_Cathode_B_PT_05_barG" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_B_PT_05_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_B_PT_05_barG)
                        self.set_atribute(f,Fluids_Cathode_B_PT_05_barG,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_B_PT_05_barG"])
                    if key+"_MIO_Fluids_Cathode_B_PT_06_barG" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_B_PT_06_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_B_PT_06_barG)
                        self.set_atribute(f,Fluids_Cathode_B_PT_06_barG,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_B_PT_06_barG"])
                    if key+"_MIO_Fluids_Cathode_B_MFT_02_slpm" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_B_MFT_02_slpm=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_B_MFT_02_slpm)
                        self.set_atribute(f,Fluids_Cathode_B_MFT_02_slpm,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_B_MFT_02_slpm"])
                    if key+"_MIO_Fluids_Cathode_B_TT_08_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_B_TT_08_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_B_TT_08_Celsius)
                        self.set_atribute(f,Fluids_Cathode_B_TT_08_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_B_TT_08_Celsius"])
                    if key+"_MIO_Fluids_Cathode_B_TT_10_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_B_TT_10_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_B_TT_10_Celsius)
                        self.set_atribute(f,Fluids_Cathode_B_TT_10_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_B_TT_10_Celsius"])
                    if key+"_MIO_Fluids_Cathode_B_TT_11_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_B_TT_11_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_B_TT_11_Celsius)
                        self.set_atribute(f,Fluids_Cathode_B_TT_11_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_B_TT_11_Celsius"])
                    if key+"_MIO_Fluids_Cathode_B_TT_12_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Cathode_B_TT_12_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_B_TT_12_Celsius)
                        self.set_atribute(f,Fluids_Cathode_B_TT_12_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Cathode_B_TT_12_Celsius"])
                    if key+"_MIO_Fluids_Anode_PT_01_barG" in f[CAMELS_entry]["data"]:
                        Fluids_Anode_PT_01_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_PT_01_barG)
                        self.set_atribute(f,Fluids_Anode_PT_01_barG,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Anode_PT_01_barG"])
                    if key+"_MIO_Fluids_Anode_TT_01_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Anode_TT_01_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_TT_01_Celsius)
                        self.set_atribute(f,Fluids_Anode_TT_01_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Anode_TT_01_Celsius"])
                    if key+"_MIO_Fluids_Anode_A_PT_03_barG" in f[CAMELS_entry]["data"]:
                        Fluids_Anode_A_PT_03_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_A_PT_03_barG)
                        self.set_atribute(f,Fluids_Anode_A_PT_03_barG,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Anode_A_PT_03_barG"])
                    if key+"_MIO_Fluids_Anode_A_PT_04_barG" in f[CAMELS_entry]["data"]:
                        Fluids_Anode_A_PT_04_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_A_PT_04_barG)
                        self.set_atribute(f,Fluids_Anode_A_PT_04_barG,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Anode_A_PT_04_barG"])
                    if key+"_MIO_Fluids_Anode_A_TT_02_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Anode_A_TT_02_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_A_TT_02_Celsius)
                        self.set_atribute(f,Fluids_Anode_A_TT_02_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Anode_A_TT_02_Celsius"])
                    if key+"_MIO_Fluids_Anode_A_TT_03_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Anode_A_TT_03_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_A_TT_03_Celsius)
                        self.set_atribute(f,Fluids_Anode_A_TT_03_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Anode_A_TT_03_Celsius"])
                    if key+"_MIO_Fluids_Anode_B_PT_03_barG" in f[CAMELS_entry]["data"]:
                        Fluids_Anode_B_PT_03_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_B_PT_03_barG)
                        self.set_atribute(f,Fluids_Anode_B_PT_03_barG,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Anode_B_PT_03_barG"])
                    if key+"_MIO_Fluids_Anode_B_PT_04_barG" in f[CAMELS_entry]["data"]:
                        Fluids_Anode_B_PT_04_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_B_PT_04_barG)
                        self.set_atribute(f,Fluids_Anode_B_PT_04_barG,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Anode_B_PT_04_barG"])
                    if key+"_MIO_Fluids_Anode_B_TT_02_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Anode_B_TT_02_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_B_TT_02_Celsius)
                        self.set_atribute(f,Fluids_Anode_B_TT_02_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Anode_B_TT_02_Celsius"])
                    if key+"_MIO_Fluids_Anode_B_TT_03_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Anode_B_TT_03_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_B_TT_03_Celsius)
                        self.set_atribute(f,Fluids_Anode_B_TT_03_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Anode_B_TT_03_Celsius"])
                    if key+"_MIO_Fluids_Anode_MFT_01_A_p_PSIA" in f[CAMELS_entry]["data"]:
                        Fluids_Anode_MFT_01_A_p_PSIA=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_MFT_01_A_p_PSIA)
                        self.set_atribute(f,Fluids_Anode_MFT_01_A_p_PSIA,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Anode_MFT_01_A_p_PSIA"])
                    if key+"_MIO_Fluids_Anode_MFT_01_A_T_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Anode_MFT_01_A_T_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_MFT_01_A_T_Celsius)
                        self.set_atribute(f,Fluids_Anode_MFT_01_A_T_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Anode_MFT_01_A_T_Celsius"])
                    if key+"_MIO_Fluids_Anode_MFT_01_A_Vflow_LPM" in f[CAMELS_entry]["data"]:
                        Fluids_Anode_MFT_01_A_Vflow_LPM=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_MFT_01_A_Vflow_LPM)
                        self.set_atribute(f,Fluids_Anode_MFT_01_A_Vflow_LPM,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Anode_MFT_01_A_Vflow_LPM"])
                    if key+"_MIO_Fluids_Anode_MFT_01_A_mflow_SLPM" in f[CAMELS_entry]["data"]:
                        Fluids_Anode_MFT_01_A_mflow_SLPM=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_MFT_01_A_mflow_SLPM)
                        self.set_atribute(f,Fluids_Anode_MFT_01_A_mflow_SLPM,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Anode_MFT_01_A_mflow_SLPM"])
                    if key+"_MIO_Fluids_Anode_MFT_01_A_mTotal_SL" in f[CAMELS_entry]["data"]:
                        Fluids_Anode_MFT_01_A_mTotal_SL=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_MFT_01_A_mTotal_SL)
                        self.set_atribute(f,Fluids_Anode_MFT_01_A_mTotal_SL,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Anode_MFT_01_A_mTotal_SL"])
                    if key+"_MIO_Fluids_Anode_MFT_01_B_p_PSIA" in f[CAMELS_entry]["data"]:
                        Fluids_Anode_MFT_01_B_p_PSIA=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_MFT_01_B_p_PSIA)
                        self.set_atribute(f,Fluids_Anode_MFT_01_B_p_PSIA,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Anode_MFT_01_B_p_PSIA"])
                    if key+"_MIO_Fluids_Anode_MFT_01_B_T_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Anode_MFT_01_B_T_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_MFT_01_B_T_Celsius)
                        self.set_atribute(f,Fluids_Anode_MFT_01_B_T_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Anode_MFT_01_B_T_Celsius"])
                    if key+"_MIO_Fluids_Anode_MFT_01_B_Vflow_LPM" in f[CAMELS_entry]["data"]:
                        Fluids_Anode_MFT_01_B_Vflow_LPM=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_MFT_01_B_Vflow_LPM)
                        self.set_atribute(f,Fluids_Anode_MFT_01_B_Vflow_LPM,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Anode_MFT_01_B_Vflow_LPM"])
                    if key+"_MIO_Fluids_Anode_MFT_01_B_mflow_SLPM" in f[CAMELS_entry]["data"]:
                        Fluids_Anode_MFT_01_B_mflow_SLPM=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_MFT_01_B_mflow_SLPM)
                        self.set_atribute(f,Fluids_Anode_MFT_01_B_mflow_SLPM,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Anode_MFT_01_B_mflow_SLPM"])
                    if key+"_MIO_Fluids_Anode_MFT_01_B_mTotal_SL" in f[CAMELS_entry]["data"]:
                        Fluids_Anode_MFT_01_B_mTotal_SL=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_MFT_01_B_mTotal_SL)
                        self.set_atribute(f,Fluids_Anode_MFT_01_B_mTotal_SL,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Anode_MFT_01_B_mTotal_SL"])
                    if key+"_MIO_Fluids_Thermal_PT_01_barG" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_PT_01_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_PT_01_barG)
                        self.set_atribute(f,Fluids_Thermal_PT_01_barG,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_PT_01_barG"])
                    if key+"_MIO_Fluids_Thermal_PT_02_barG" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_PT_02_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_PT_02_barG)
                        self.set_atribute(f,Fluids_Thermal_PT_02_barG,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_PT_02_barG"])
                    if key+"_MIO_Fluids_Thermal_PT_03_A_barG" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_PT_03_A_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_PT_03_A_barG)
                        self.set_atribute(f,Fluids_Thermal_PT_03_A_barG,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_PT_03_A_barG"])
                    if key+"_MIO_Fluids_Thermal_PT_03_B_barG" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_PT_03_B_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_PT_03_B_barG)
                        self.set_atribute(f,Fluids_Thermal_PT_03_B_barG,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_PT_03_B_barG"])
                    if key+"_MIO_Fluids_Thermal_PT_04_A_barG" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_PT_04_A_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_PT_04_A_barG)
                        self.set_atribute(f,Fluids_Thermal_PT_04_A_barG,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_PT_04_A_barG"])
                    if key+"_MIO_Fluids_Thermal_PT_04_B_barG" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_PT_04_B_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_PT_04_B_barG)
                        self.set_atribute(f,Fluids_Thermal_PT_04_B_barG,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_PT_04_B_barG"])
                    if key+"_MIO_Fluids_Thermal_PT_05_barG" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_PT_05_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_PT_05_barG)
                        self.set_atribute(f,Fluids_Thermal_PT_05_barG,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_PT_05_barG"])
                    if key+"_MIO_Fluids_Thermal_PT_06_barG" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_PT_06_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_PT_06_barG)
                        self.set_atribute(f,Fluids_Thermal_PT_06_barG,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_PT_06_barG"])
                    if key+"_MIO_Fluids_Thermal_MFT_01_02_lpm" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_MFT_01_02_lpm=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_MFT_01_02_lpm)
                        self.set_atribute(f,Fluids_Thermal_MFT_01_02_lpm,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_MFT_01_02_lpm"])
                    if key+"_MIO_Fluids_Thermal_MFT_02_lpm" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_MFT_02_lpm=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_MFT_02_lpm)
                        self.set_atribute(f,Fluids_Thermal_MFT_02_lpm,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_MFT_02_lpm"])
                    if key+"_MIO_Fluids_Thermal_TT_01_01_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_TT_01_01_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_TT_01_01_Celsius)
                        self.set_atribute(f,Fluids_Thermal_TT_01_01_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_TT_01_01_Celsius"])
                    if key+"_MIO_Fluids_Thermal_TT_03_02_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_TT_03_02_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_TT_03_02_Celsius)
                        self.set_atribute(f,Fluids_Thermal_TT_03_02_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_TT_03_02_Celsius"])
                    if key+"_MIO_Fluids_Thermal_TT_01_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_TT_01_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_TT_01_Celsius)
                        self.set_atribute(f,Fluids_Thermal_TT_01_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_TT_01_Celsius"])
                    if key+"_MIO_Fluids_Thermal_TT_05_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_TT_05_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_TT_05_Celsius)
                        self.set_atribute(f,Fluids_Thermal_TT_05_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_TT_05_Celsius"])
                    if key+"_MIO_Fluids_Thermal_TT_02_01_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_TT_02_01_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_TT_02_01_Celsius)
                        self.set_atribute(f,Fluids_Thermal_TT_02_01_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_TT_02_01_Celsius"])
                    if key+"_MIO_Fluids_Thermal_TT_04_02_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_TT_04_02_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_TT_04_02_Celsius)
                        self.set_atribute(f,Fluids_Thermal_TT_04_02_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_TT_04_02_Celsius"])
                    if key+"_MIO_Fluids_Thermal_TT_06_01_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_TT_06_01_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_TT_06_01_Celsius)
                        self.set_atribute(f,Fluids_Thermal_TT_06_01_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_TT_06_01_Celsius"])
                    if key+"_MIO_Fluids_Thermal_TT_08_02_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_TT_08_02_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_TT_08_02_Celsius)
                        self.set_atribute(f,Fluids_Thermal_TT_08_02_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_TT_08_02_Celsius"])
                    if key+"_MIO_Fluids_Thermal_TT_07_01_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_TT_07_01_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_TT_07_01_Celsius)
                        self.set_atribute(f,Fluids_Thermal_TT_07_01_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_TT_07_01_Celsius"])
                    if key+"_MIO_Fluids_Thermal_TT_09_02_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_TT_09_02_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_TT_09_02_Celsius)
                        self.set_atribute(f,Fluids_Thermal_TT_09_02_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_TT_09_02_Celsius"])
                    if key+"_MIO_Fluids_Thermal_TT_11_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_TT_11_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_TT_11_Celsius)
                        self.set_atribute(f,Fluids_Thermal_TT_11_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_TT_11_Celsius"])
                    if key+"_MIO_Fluids_Thermal_TT_01_02_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_TT_01_02_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_TT_01_02_Celsius)
                        self.set_atribute(f,Fluids_Thermal_TT_01_02_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_TT_01_02_Celsius"])
                    if key+"_MIO_Fluids_Thermal_A_MFT_01_lpm" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_A_MFT_01_lpm=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_A_MFT_01_lpm)
                        self.set_atribute(f,Fluids_Thermal_A_MFT_01_lpm,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_A_MFT_01_lpm"])
                    if key+"_MIO_Fluids_Thermal_A_TT_03_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_A_TT_03_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_A_TT_03_Celsius)
                        self.set_atribute(f,Fluids_Thermal_A_TT_03_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_A_TT_03_Celsius"])
                    if key+"_MIO_Fluids_Thermal_A_TT_04_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_A_TT_04_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_A_TT_04_Celsius)
                        self.set_atribute(f,Fluids_Thermal_A_TT_04_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_A_TT_04_Celsius"])
                    if key+"_MIO_Fluids_Thermal_B_MFT_01_lpm" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_B_MFT_01_lpm=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_B_MFT_01_lpm)
                        self.set_atribute(f,Fluids_Thermal_B_MFT_01_lpm,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_B_MFT_01_lpm"])
                    if key+"_MIO_Fluids_Thermal_B_TT_03_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_B_TT_03_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_B_TT_03_Celsius)
                        self.set_atribute(f,Fluids_Thermal_B_TT_03_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_B_TT_03_Celsius"])
                    if key+"_MIO_Fluids_Thermal_B_TT_04_Celsius" in f[CAMELS_entry]["data"]:
                        Fluids_Thermal_B_TT_04_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_B_TT_04_Celsius)
                        self.set_atribute(f,Fluids_Thermal_B_TT_04_Celsius,"data",[CAMELS_entry,"data",key+"_MIO_Fluids_Thermal_B_TT_04_Celsius"])
                    if key+"_HP_CAN_Net_A_fbCAN_FSM_iStep" in  f[CAMELS_entry]["data"]:
                        Net_A_fbCAN_FSM_iStep=hp_can_data.m_create(Ploted_values,HP_CANData.Net_A_fbCAN_FSM_iStep)
                        self.set_atribute(f,Net_A_fbCAN_FSM_iStep,"data",[CAMELS_entry,"data",key+"_HP_CAN_Net_A_fbCAN_FSM_iStep"])
                    if key+"_HP_CAN_Net_A_RH01_actValues_current_act_A" in  f[CAMELS_entry]["data"]:
                        Net_A_RH01_actValues_current_act_A=hp_can_data.m_create(Ploted_values,HP_CANData.Net_A_RH01_actValues_current_act_A)
                        self.set_atribute(f,Net_A_RH01_actValues_current_act_A,"data",[CAMELS_entry,"data",key+"_HP_CAN_Net_A_RH01_actValues_current_act_A"])
                    if key+"_HP_CAN_Net_A_RH01_actValues_power_act_W" in  f[CAMELS_entry]["data"]:
                        Net_A_RH01_actValues_power_act_W=hp_can_data.m_create(Ploted_values,HP_CANData.Net_A_RH01_actValues_power_act_W)
                        self.set_atribute(f,Net_A_RH01_actValues_power_act_W,"data",[CAMELS_entry,"data",key+"_HP_CAN_Net_A_RH01_actValues_power_act_W"])
                    if key+"_HP_CAN_Net_A_RH01_actValues_speed_act_rpm" in  f[CAMELS_entry]["data"]:
                        Net_A_RH01_actValues_speed_act_rpm=hp_can_data.m_create(Ploted_values,HP_CANData.Net_A_RH01_actValues_speed_act_rpm)
                        self.set_atribute(f,Net_A_RH01_actValues_speed_act_rpm,"data",[CAMELS_entry,"data",key+"_HP_CAN_Net_A_RH01_actValues_speed_act_rpm"])
                    if key+"_HP_CAN_Net_A_RH01_actValues_T_circuit_C" in  f[CAMELS_entry]["data"]:
                        Net_A_RH01_actValues_T_circuit_C=hp_can_data.m_create(Ploted_values,HP_CANData.Net_A_RH01_actValues_T_circuit_C)
                        self.set_atribute(f,Net_A_RH01_actValues_T_circuit_C,"data",[CAMELS_entry,"data",key+"_HP_CAN_Net_A_RH01_actValues_T_circuit_C"])
                    if key+"_HP_CAN_Net_A_RH01_actValues_voltage_act_V" in  f[CAMELS_entry]["data"]:
                        Net_A_RH01_actValues_voltage_act_V=hp_can_data.m_create(Ploted_values,HP_CANData.Net_A_RH01_actValues_voltage_act_V)
                        self.set_atribute(f,Net_A_RH01_actValues_voltage_act_V,"data",[CAMELS_entry,"data",key+"_HP_CAN_Net_A_RH01_actValues_voltage_act_V"])
                    if key+"_HP_CAN_Net_A_RH01_cmd_mDot_cmd_kgph" in  f[CAMELS_entry]["data"]:
                        Net_A_RH01_cmd_mDot_cmd_kgph=hp_can_data.m_create(Ploted_values,HP_CANData.Net_A_RH01_cmd_mDot_cmd_kgph)
                        self.set_atribute(f,Net_A_RH01_cmd_mDot_cmd_kgph,"data",[CAMELS_entry,"data",key+"_HP_CAN_Net_A_RH01_cmd_mDot_cmd_kgph"])
                    if key+"_HP_CAN_Net_A_RH01_cmd_speed_cmd_rpm" in  f[CAMELS_entry]["data"]:
                        Net_A_RH01_cmd_speed_cmd_rpm=hp_can_data.m_create(Ploted_values,HP_CANData.Net_A_RH01_cmd_speed_cmd_rpm)
                        self.set_atribute(f,Net_A_RH01_cmd_speed_cmd_rpm,"data",[CAMELS_entry,"data",key+"_HP_CAN_Net_A_RH01_cmd_speed_cmd_rpm"])
                    if key+"_HP_CAN_Net_B_fbCAN_FSM_iStep" in  f[CAMELS_entry]["data"]:
                        Net_B_fbCAN_FSM_iStep=hp_can_data.m_create(Ploted_values,HP_CANData.Net_B_fbCAN_FSM_iStep)
                        self.set_atribute(f,Net_B_fbCAN_FSM_iStep,"data",[CAMELS_entry,"data",key+"_HP_CAN_Net_B_fbCAN_FSM_iStep"])
                    if key+"_HP_CAN_Net_B_RH01_actValues_current_act_A" in  f[CAMELS_entry]["data"]:
                        Net_B_RH01_actValues_current_act_A=hp_can_data.m_create(Ploted_values,HP_CANData.Net_B_RH01_actValues_current_act_A)
                        self.set_atribute(f,Net_B_RH01_actValues_current_act_A,"data",[CAMELS_entry,"data",key+"_HP_CAN_Net_B_RH01_actValues_current_act_A"])
                    if key+"_HP_CAN_Net_B_RH01_actValues_power_act_W" in  f[CAMELS_entry]["data"]:
                        Net_B_RH01_actValues_power_act_W=hp_can_data.m_create(Ploted_values,HP_CANData.Net_B_RH01_actValues_power_act_W)
                        self.set_atribute(f,Net_B_RH01_actValues_power_act_W,"data",[CAMELS_entry,"data",key+"_HP_CAN_Net_B_RH01_actValues_power_act_W"])
                    if key+"_HP_CAN_Net_B_RH01_actValues_speed_act_rpm" in  f[CAMELS_entry]["data"]:
                        Net_B_RH01_actValues_speed_act_rpm=hp_can_data.m_create(Ploted_values,HP_CANData.Net_B_RH01_actValues_speed_act_rpm)
                        self.set_atribute(f,Net_B_RH01_actValues_speed_act_rpm,"data",[CAMELS_entry,"data",key+"_HP_CAN_Net_B_RH01_actValues_speed_act_rpm"])
                    if key+"_HP_CAN_Net_B_RH01_actValues_T_circuit_C" in  f[CAMELS_entry]["data"]:
                        Net_B_RH01_actValues_T_circuit_C=hp_can_data.m_create(Ploted_values,HP_CANData.Net_B_RH01_actValues_T_circuit_C)
                        self.set_atribute(f,Net_B_RH01_actValues_T_circuit_C,"data",[CAMELS_entry,"data",key+"_HP_CAN_Net_B_RH01_actValues_T_circuit_C"])
                    if key+"_HP_CAN_Net_B_RH01_actValues_voltage_act_V" in  f[CAMELS_entry]["data"]:
                        Net_B_RH01_actValues_voltage_act_V=hp_can_data.m_create(Ploted_values,HP_CANData.Net_B_RH01_actValues_voltage_act_V)
                        self.set_atribute(f,Net_B_RH01_actValues_voltage_act_V,"data",[CAMELS_entry,"data",key+"_HP_CAN_Net_B_RH01_actValues_voltage_act_V"])
                    if key+"_HP_CAN_Net_B_RH01_cmd_mDot_cmd_kgph" in  f[CAMELS_entry]["data"]:
                        Net_B_RH01_cmd_mDot_cmd_kgph=hp_can_data.m_create(Ploted_values,HP_CANData.Net_B_RH01_cmd_mDot_cmd_kgph)
                        self.set_atribute(f,Net_B_RH01_cmd_mDot_cmd_kgph,"data",[CAMELS_entry,"data",key+"_HP_CAN_Net_B_RH01_cmd_mDot_cmd_kgph"])
                    if key+"_HP_CAN_Net_B_RH01_cmd_speed_cmd_rpm" in  f[CAMELS_entry]["data"]:
                        Net_B_RH01_cmd_speed_cmd_rpm=hp_can_data.m_create(Ploted_values,HP_CANData.Net_B_RH01_cmd_speed_cmd_rpm)
                        self.set_atribute(f,Net_B_RH01_cmd_speed_cmd_rpm,"data",[CAMELS_entry,"data",key+"_HP_CAN_Net_B_RH01_cmd_speed_cmd_rpm"])
                    if key+"_ACTIF_Anode_GasSupply_state" in  f[CAMELS_entry]["data"]:
                        Anode_GasSupply_state=actif_data.m_create(Ploted_values,ACTIFData.Anode_GasSupply_state)
                        self.set_atribute(f,Anode_GasSupply_state,"data",[CAMELS_entry,"data",key+"_ACTIF_Anode_GasSupply_state"])
                    if key+"_ACTIF_Anode_PC_01_A_cmd" in  f[CAMELS_entry]["data"]:
                        Anode_PC_01_A_cmd=actif_data.m_create(Ploted_values,ACTIFData.Anode_PC_01_A_cmd)
                        self.set_atribute(f,Anode_PC_01_A_cmd,"data",[CAMELS_entry,"data",key+"_ACTIF_Anode_PC_01_A_cmd"])
                    if key+"_ACTIF_Anode_PC_01_A_state" in  f[CAMELS_entry]["data"]:
                        Anode_PC_01_A_state=actif_data.m_create(Ploted_values,ACTIFData.Anode_PC_01_A_state)
                        self.set_atribute(f,Anode_PC_01_A_state,"data",[CAMELS_entry,"data",key+"_ACTIF_Anode_PC_01_A_state"])
                    if key+"_ACTIF_Anode_PC_01_B_cmd" in  f[CAMELS_entry]["data"]:
                        Anode_PC_01_B_cmd=actif_data.m_create(Ploted_values,ACTIFData.Anode_PC_01_B_cmd)
                        self.set_atribute(f,Anode_PC_01_B_cmd,"data",[CAMELS_entry,"data",key+"_ACTIF_Anode_PC_01_B_cmd"])
                    if key+"_ACTIF_Anode_PC_01_B_state" in  f[CAMELS_entry]["data"]:
                        Anode_PC_01_B_state=actif_data.m_create(Ploted_values,ACTIFData.Anode_PC_01_B_state)
                        self.set_atribute(f,Anode_PC_01_B_state,"data",[CAMELS_entry,"data",key+"_ACTIF_Anode_PC_01_B_state"])
                    if key+"_ACTIF_Anode_PV_01_A_cmd" in  f[CAMELS_entry]["data"]:
                        Anode_PV_01_A_cmd=actif_data.m_create(Ploted_values,ACTIFData.Anode_PV_01_A_cmd)
                        self.set_atribute(f,Anode_PV_01_A_cmd,"data",[CAMELS_entry,"data",key+"_ACTIF_Anode_PV_01_A_cmd"])
                    if key+"_ACTIF_Anode_PV_01_A_state" in  f[CAMELS_entry]["data"]:
                        Anode_PV_01_A_state=actif_data.m_create(Ploted_values,ACTIFData.Anode_PV_01_A_state)
                        self.set_atribute(f,Anode_PV_01_A_state,"data",[CAMELS_entry,"data",key+"_ACTIF_Anode_PV_01_A_state"])
                    if key+"_ACTIF_Anode_PV_01_B_cmd" in  f[CAMELS_entry]["data"]:
                        Anode_PV_01_B_cmd=actif_data.m_create(Ploted_values,ACTIFData.Anode_PV_01_B_cmd)
                        self.set_atribute(f,Anode_PV_01_B_cmd,"data",[CAMELS_entry,"data",key+"_ACTIF_Anode_PV_01_B_cmd"])
                    if key+"_ACTIF_Anode_PV_01_B_state" in  f[CAMELS_entry]["data"]:
                        Anode_PV_01_B_state=actif_data.m_create(Ploted_values,ACTIFData.Anode_PV_01_B_state)
                        self.set_atribute(f,Anode_PV_01_B_state,"data",[CAMELS_entry,"data",key+"_ACTIF_Anode_PV_01_B_state"])
                    if key+"_ACTIF_Cathode_AC_01_cmd" in  f[CAMELS_entry]["data"]:
                        Cathode_AC_01_cmd=actif_data.m_create(Ploted_values,ACTIFData.Cathode_AC_01_cmd)
                        self.set_atribute(f,Cathode_AC_01_cmd,"data",[CAMELS_entry,"data",key+"_ACTIF_Cathode_AC_01_cmd"])
                    if key+"_ACTIF_Cathode_AC_01_state" in  f[CAMELS_entry]["data"]:
                        Cathode_AC_01_state=actif_data.m_create(Ploted_values,ACTIFData.Cathode_AC_01_state)
                        self.set_atribute(f,Cathode_AC_01_state,"data",[CAMELS_entry,"data",key+"_ACTIF_Cathode_AC_01_state"])
                    if key+"_ACTIF_Cathode_EH_01_cmd" in  f[CAMELS_entry]["data"]:
                        Cathode_EH_01_cmd=actif_data.m_create(Ploted_values,ACTIFData.Cathode_EH_01_cmd)
                        self.set_atribute(f,Cathode_EH_01_cmd,"data",[CAMELS_entry,"data",key+"_ACTIF_Cathode_EH_01_cmd"])
                    if key+"_ACTIF_Cathode_EH_01_state" in  f[CAMELS_entry]["data"]:
                        Cathode_EH_01_state=actif_data.m_create(Ploted_values,ACTIFData.Cathode_EH_01_state)
                        self.set_atribute(f,Cathode_EH_01_state,"data",[CAMELS_entry,"data",key+"_ACTIF_Cathode_EH_01_state"])
                    if key+"_ACTIF_Cathode_EH_02_cmd" in  f[CAMELS_entry]["data"]:
                        Cathode_EH_02_cmd=actif_data.m_create(Ploted_values,ACTIFData.Cathode_EH_02_cmd)
                        self.set_atribute(f,Cathode_EH_02_cmd,"data",[CAMELS_entry,"data",key+"_ACTIF_Cathode_EH_02_cmd"])
                    if key+"_ACTIF_Cathode_EH_02_state" in  f[CAMELS_entry]["data"]:
                        Cathode_EH_02_state=actif_data.m_create(Ploted_values,ACTIFData.Cathode_EH_02_state)
                        self.set_atribute(f,Cathode_EH_02_state,"data",[CAMELS_entry,"data",key+"_ACTIF_Cathode_EH_02_state"])
                    if key+"_ACTIF_Cathode_MFC_01_00_cmd" in  f[CAMELS_entry]["data"]:
                        Cathode_MFC_01_00_cmd=actif_data.m_create(Ploted_values,ACTIFData.Cathode_MFC_01_00_cmd)
                        self.set_atribute(f,Cathode_MFC_01_00_cmd,"data",[CAMELS_entry,"data",key+"_ACTIF_Cathode_MFC_01_00_cmd"])
                    if key+"_ACTIF_Cathode_MFC_01_00_state" in  f[CAMELS_entry]["data"]:
                        Cathode_MFC_01_00_state=actif_data.m_create(Ploted_values,ACTIFData.Cathode_MFC_01_00_state)
                        self.set_atribute(f,Cathode_MFC_01_00_state,"data",[CAMELS_entry,"data",key+"_ACTIF_Cathode_MFC_01_00_state"])
                    if key+"_ACTIF_Cathode_TV_01_A_cmd" in  f[CAMELS_entry]["data"]:
                        Cathode_TV_01_A_cmd=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_01_A_cmd)
                        self.set_atribute(f,Cathode_TV_01_A_cmd,"data",[CAMELS_entry,"data",key+"_ACTIF_Cathode_TV_01_A_cmd"])
                    if key+"_ACTIF_Cathode_TV_01_A_state" in  f[CAMELS_entry]["data"]:
                        Cathode_TV_01_A_state=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_01_A_state)
                        self.set_atribute(f,Cathode_TV_01_A_state,"data",[CAMELS_entry,"data",key+"_ACTIF_Cathode_TV_01_A_state"])
                    if key+"_ACTIF_Cathode_TV_01_A_theta_prct" in  f[CAMELS_entry]["data"]:
                        Cathode_TV_01_A_theta_prct=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_01_A_theta_prct)
                        self.set_atribute(f,Cathode_TV_01_A_theta_prct,"data",[CAMELS_entry,"data",key+"_ACTIF_Cathode_TV_01_A_theta_prct"])
                    if key+"_ACTIF_Cathode_TV_01_B_cmd" in  f[CAMELS_entry]["data"]:
                        Cathode_TV_01_B_cmd=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_01_B_cmd)
                        self.set_atribute(f,Cathode_TV_01_B_cmd,"data",[CAMELS_entry,"data",key+"_ACTIF_Cathode_TV_01_B_cmd"])
                    if key+"_ACTIF_Cathode_TV_01_B_state" in  f[CAMELS_entry]["data"]:
                        Cathode_TV_01_B_state=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_01_B_state)
                        self.set_atribute(f,Cathode_TV_01_B_state,"data",[CAMELS_entry,"data",key+"_ACTIF_Cathode_TV_01_B_state"])
                    if key+"_ACTIF_Cathode_TV_01_B_theta_prct" in  f[CAMELS_entry]["data"]:
                        Cathode_TV_01_B_theta_prct=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_01_B_theta_prct)
                        self.set_atribute(f,Cathode_TV_01_B_theta_prct,"data",[CAMELS_entry,"data",key+"_ACTIF_Cathode_TV_01_B_theta_prct"])
                    if key+"_ACTIF_Cathode_TV_02_A_cmd" in  f[CAMELS_entry]["data"]:
                        Cathode_TV_02_A_cmd=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_02_A_cmd)
                        self.set_atribute(f,Cathode_TV_02_A_cmd,"data",[CAMELS_entry,"data",key+"_ACTIF_Cathode_TV_02_A_cmd"])
                    if key+"_ACTIF_Cathode_TV_02_A_state" in  f[CAMELS_entry]["data"]:
                        Cathode_TV_02_A_state=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_02_A_state)
                        self.set_atribute(f,Cathode_TV_02_A_state,"data",[CAMELS_entry,"data",key+"_ACTIF_Cathode_TV_02_A_state"])
                    if key+"_ACTIF_Cathode_TV_02_A_theta_prct" in  f[CAMELS_entry]["data"]:
                        Cathode_TV_02_A_theta_prct=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_02_A_theta_prct)
                        self.set_atribute(f,Cathode_TV_02_A_theta_prct,"data",[CAMELS_entry,"data",key+"_ACTIF_Cathode_TV_02_A_theta_prct"])
                    if key+"_ACTIF_Cathode_TV_02_B_cmd" in  f[CAMELS_entry]["data"]:
                        Cathode_TV_02_B_cmd=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_02_B_cmd)
                        self.set_atribute(f,Cathode_TV_02_B_cmd,"data",[CAMELS_entry,"data",key+"_ACTIF_Cathode_TV_02_B_cmd"])
                    if key+"_ACTIF_Cathode_TV_02_B_state" in  f[CAMELS_entry]["data"]:
                        Cathode_TV_02_B_state=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_02_B_state)
                        self.set_atribute(f,Cathode_TV_02_B_state,"data",[CAMELS_entry,"data",key+"_ACTIF_Cathode_TV_02_B_state"])
                    if key+"_ACTIF_Cathode_TV_02_B_theta_prct" in  f[CAMELS_entry]["data"]:
                        Cathode_TV_02_B_theta_prct=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_02_B_theta_prct)
                        self.set_atribute(f,Cathode_TV_02_B_theta_prct,"data",[CAMELS_entry,"data",key+"_ACTIF_Cathode_TV_02_B_theta_prct"])
                    if key+"_ACTIF_Cathode_TV_03_A_cmd" in  f[CAMELS_entry]["data"]:
                        Cathode_TV_03_A_cmd=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_03_A_cmd)
                        self.set_atribute(f,Cathode_TV_03_A_cmd,"data",[CAMELS_entry,"data",key+"_ACTIF_Cathode_TV_03_A_cmd"])
                    if key+"_ACTIF_Cathode_TV_03_A_state" in  f[CAMELS_entry]["data"]:
                        Cathode_TV_03_A_state=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_03_A_state)
                        self.set_atribute(f,Cathode_TV_03_A_state,"data",[CAMELS_entry,"data",key+"_ACTIF_Cathode_TV_03_A_state"])
                    if key+"_ACTIF_Cathode_TV_03_A_theta_prct" in  f[CAMELS_entry]["data"]:
                        Cathode_TV_03_A_theta_prct=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_03_A_theta_prct)
                        self.set_atribute(f,Cathode_TV_03_A_theta_prct,"data",[CAMELS_entry,"data",key+"_ACTIF_Cathode_TV_03_A_theta_prct"])
                    if key+"_ACTIF_Cathode_TV_03_B_cmd" in  f[CAMELS_entry]["data"]:
                        Cathode_TV_03_B_cmd=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_03_B_cmd)
                        self.set_atribute(f,Cathode_TV_03_B_cmd,"data",[CAMELS_entry,"data",key+"_ACTIF_Cathode_TV_03_B_cmd"])
                    if key+"_ACTIF_Cathode_TV_03_B_state" in  f[CAMELS_entry]["data"]:
                        Cathode_TV_03_B_state=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_03_B_state)
                        self.set_atribute(f,Cathode_TV_03_B_state,"data",[CAMELS_entry,"data",key+"_ACTIF_Cathode_TV_03_B_state"])
                    if key+"_ACTIF_Cathode_TV_03_B_theta_prct" in  f[CAMELS_entry]["data"]:
                        Cathode_TV_03_B_theta_prct=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_03_B_theta_prct)
                        self.set_atribute(f,Cathode_TV_03_B_theta_prct,"data",[CAMELS_entry,"data",key+"_ACTIF_Cathode_TV_03_B_theta_prct"])
                    if key+"_ACTIF_Thermal_AV_01_A_cmd" in  f[CAMELS_entry]["data"]:
                        Thermal_AV_01_A_cmd=actif_data.m_create(Ploted_values,ACTIFData.Thermal_AV_01_A_cmd)
                        self.set_atribute(f,Thermal_AV_01_A_cmd,"data",[CAMELS_entry,"data",key+"_ACTIF_Thermal_AV_01_A_cmd"])
                    if key+"_ACTIF_Thermal_AV_01_A_state" in  f[CAMELS_entry]["data"]:
                        Thermal_AV_01_A_state=actif_data.m_create(Ploted_values,ACTIFData.Thermal_AV_01_A_state)
                        self.set_atribute(f,Thermal_AV_01_A_state,"data",[CAMELS_entry,"data",key+"_ACTIF_Thermal_AV_01_A_state"])
                    if key+"_ACTIF_Thermal_AV_01_B_cmd" in  f[CAMELS_entry]["data"]:
                        Thermal_AV_01_B_cmd=actif_data.m_create(Ploted_values,ACTIFData.Thermal_AV_01_B_cmd)
                        self.set_atribute(f,Thermal_AV_01_B_cmd,"data",[CAMELS_entry,"data",key+"_ACTIF_Thermal_AV_01_B_cmd"])
                    if key+"_ACTIF_Thermal_AV_01_B_state" in  f[CAMELS_entry]["data"]:
                        Thermal_AV_01_B_state=actif_data.m_create(Ploted_values,ACTIFData.Thermal_AV_01_B_state)
                        self.set_atribute(f,Thermal_AV_01_B_state,"data",[CAMELS_entry,"data",key+"_ACTIF_Thermal_AV_01_B_state"])
                    if key+"_ACTIF_Thermal_CP_01_cmd_prct" in  f[CAMELS_entry]["data"]:
                        Thermal_CP_01_cmd_prct=actif_data.m_create(Ploted_values,ACTIFData.Thermal_CP_01_cmd_prct)
                        self.set_atribute(f,Thermal_CP_01_cmd_prct,"data",[CAMELS_entry,"data",key+"_ACTIF_Thermal_CP_01_cmd_prct"])
                    if key+"_ACTIF_Thermal_CP_01_state" in  f[CAMELS_entry]["data"]:
                        Thermal_CP_01_state=actif_data.m_create(Ploted_values,ACTIFData.Thermal_CP_01_state)
                        self.set_atribute(f,Thermal_CP_01_state,"data",[CAMELS_entry,"data",key+"_ACTIF_Thermal_CP_01_state"])
                    if key+"_ACTIF_Thermal_FLKS_01_CP_01_cmd_prct" in  f[CAMELS_entry]["data"]:
                        Thermal_FLKS_01_CP_01_cmd_prct=actif_data.m_create(Ploted_values,ACTIFData.Thermal_FLKS_01_CP_01_cmd_prct)
                        self.set_atribute(f,Thermal_FLKS_01_CP_01_cmd_prct,"data",[CAMELS_entry,"data",key+"_ACTIF_Thermal_FLKS_01_CP_01_cmd_prct"])
                    if key+"_ACTIF_Thermal_FLKS_01_CP_01_state" in  f[CAMELS_entry]["data"]:
                        Thermal_FLKS_01_CP_01_state=actif_data.m_create(Ploted_values,ACTIFData.Thermal_FLKS_01_CP_01_state)
                        self.set_atribute(f,Thermal_FLKS_01_CP_01_state,"data",[CAMELS_entry,"data",key+"_ACTIF_Thermal_FLKS_01_CP_01_state"])
                    if key+"_ACTIF_Thermal_FLKS_01_Fan_01_cmd" in  f[CAMELS_entry]["data"]:
                        Thermal_FLKS_01_Fan_01_cmd=actif_data.m_create(Ploted_values,ACTIFData.Thermal_FLKS_01_Fan_01_cmd)
                        self.set_atribute(f,Thermal_FLKS_01_Fan_01_cmd,"data",[CAMELS_entry,"data",key+"_ACTIF_Thermal_FLKS_01_Fan_01_cmd"])
                    if key+"_ACTIF_Thermal_FLKS_01_Fan_01_state" in  f[CAMELS_entry]["data"]:
                        Thermal_FLKS_01_Fan_01_state=actif_data.m_create(Ploted_values,ACTIFData.Thermal_FLKS_01_Fan_01_state)
                        self.set_atribute(f,Thermal_FLKS_01_Fan_01_state,"data",[CAMELS_entry,"data",key+"_ACTIF_Thermal_FLKS_01_Fan_01_state"])
                    if key+"_ACTIF_Thermal_MV_01_cmd" in  f[CAMELS_entry]["data"]:
                        Thermal_MV_01_cmd=actif_data.m_create(Ploted_values,ACTIFData.Thermal_MV_01_cmd)
                        self.set_atribute(f,Thermal_MV_01_cmd,"data",[CAMELS_entry,"data",key+"_ACTIF_Thermal_MV_01_cmd"])
                    if key+"_ACTIF_Thermal_MV_01_state" in  f[CAMELS_entry]["data"]:
                        Thermal_MV_01_state=actif_data.m_create(Ploted_values,ACTIFData.Thermal_MV_01_state)
                        self.set_atribute(f,Thermal_MV_01_state,"data",[CAMELS_entry,"data",key+"_ACTIF_Thermal_MV_01_state"])
                    if key+"_ACTIF_Thermal_PV_01_cmd" in  f[CAMELS_entry]["data"]:
                        Thermal_PV_01_cmd=actif_data.m_create(Ploted_values,ACTIFData.Thermal_PV_01_cmd)
                        self.set_atribute(f,Thermal_PV_01_cmd,"data",[CAMELS_entry,"data",key+"_ACTIF_Thermal_PV_01_cmd"])
                    if key+"_ACTIF_Thermal_PV_01_state" in  f[CAMELS_entry]["data"]:
                        Thermal_PV_01_state=actif_data.m_create(Ploted_values,ACTIFData.Thermal_PV_01_state)
                        self.set_atribute(f,Thermal_PV_01_state,"data",[CAMELS_entry,"data",key+"_ACTIF_Thermal_PV_01_state"])
                    if key+"_ACTIF_Thermal_PV_02_cmd" in  f[CAMELS_entry]["data"]:
                        Thermal_PV_02_cmd=actif_data.m_create(Ploted_values,ACTIFData.Thermal_PV_02_cmd)
                        self.set_atribute(f,Thermal_PV_02_cmd,"data",[CAMELS_entry,"data",key+"_ACTIF_Thermal_PV_02_cmd"])
                    if key+"_ACTIF_Thermal_PV_02_state" in  f[CAMELS_entry]["data"]:
                        Thermal_PV_02_state=actif_data.m_create(Ploted_values,ACTIFData.Thermal_PV_02_state)
                        self.set_atribute(f,Thermal_PV_02_state,"data",[CAMELS_entry,"data",key+"_ACTIF_Thermal_PV_02_state"])
                    if key+"_ACTIF2_RH_01_A_state" in  f[CAMELS_entry]["data"]:
                        RH_01_A_state=actif2_data.m_create(Ploted_values,ACTIF2Data.RH_01_A_state)
                        self.set_atribute(f,RH_01_A_state,"data",[CAMELS_entry,"data",key+"_ACTIF2_RH_01_A_state"])
                    if key+"_ACTIF2_RH_01_A_cmd" in  f[CAMELS_entry]["data"]:
                        RH_01_A_cmd=actif2_data.m_create(Ploted_values,ACTIF2Data.RH_01_A_cmd)
                        self.set_atribute(f,RH_01_A_cmd,"data",[CAMELS_entry,"data",key+"_ACTIF2_RH_01_A_cmd"])
                    if key+"_ACTIF2_RH_01_B_state" in  f[CAMELS_entry]["data"]:
                        RH_01_B_state=actif2_data.m_create(Ploted_values,ACTIF2Data.RH_01_B_state)
                        self.set_atribute(f,RH_01_B_state,"data",[CAMELS_entry,"data",key+"_ACTIF2_RH_01_B_state"])
                    if key+"_ACTIF2_RH_01_B_cmd" in  f[CAMELS_entry]["data"]:
                        RH_01_B_cmd=actif2_data.m_create(Ploted_values,ACTIF2Data.RH_01_B_cmd)
                        self.set_atribute(f,RH_01_B_cmd,"data",[CAMELS_entry,"data",key+"_ACTIF2_RH_01_B_cmd"])

                #schema.mio_data.append(mio_data)
                #schema.data.actif_data.append(actif_data)
                #schema.data.actif2_data.append(actif2_data)
                #schema.data.hp_can_data.append(hp_can_data)
                archive.data=schema
        logger.info("h5 was read propperly")
        logger.info(str(os.getcwd()))
