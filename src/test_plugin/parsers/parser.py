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
from test_plugin.schema_packages.schema_package import NewSchemaPackage

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
        child_archives: dict[str, 'EntryArchive'] = None,
    ) -> None:
        archive.data= NewSchemaPackage()
        logger.info('NewParser.parse', parameter=configuration.parameter)
        
        
        #for instrument in f["CAMELS_entry"]["user"]:
        #    instrument_names= instrument_names
        with h5py.File(mainfile, "r") as f:
            self.set_atribute(f,archive.data, "measurement_comments" , ["CAMELS_entry" "measurement_details" "measurement_comments"])
            self.set_atribute(f,archive.data,"measurement_description",["CAMELS_entry","measurement_details","measurement_description"])
            self.set_atribute(f,archive.data,"protocol_description",["CAMELS_entry","measurement_details","protocol_description"])
            self.set_atribute(f,archive.data,"time",["CAMELS_entry","data","time"])
            self.set_atribute(f,archive.data,"ElapsedTime",["CAMELS_entry","data","ElapsedTime"])
            self.set_atribute(f,archive.data,"first_name",["CAMELS_entry","user","first_name"])
            self.set_atribute(f,archive.data,"last_name",["CAMELS_entry","user","last_name"])
            self.set_atribute(f,archive.data,"email",["CAMELS_entry","user","email"])
            self.set_atribute(f,archive.data,"affiliation",["CAMELS_entry","user","affiliation"])
            self.set_atribute(f,archive.data,"detectorX",["CAMELS_entry","data","demo_instrument_detectorX"])
            archive.data.certain_value= "test"
        logger.info("h5 was read propperly")
        logger.info(str(os.getcwd()))
