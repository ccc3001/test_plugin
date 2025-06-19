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

#from nomad.datamodel.context import ServerContext

#from reportlab.pdfgen import canvas
#from io import BytesIO
#pdf_buffer = BytesIO()
#pdf = canvas.Canvas(pdf_buffer)
#pdf.save()
#pdf_buffer.seek(0) 


class NewParser(MatchingParser):
    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
        child_archives: dict[str, 'EntryArchive'] = None,
    ) -> None:
        archive.data= NewSchemaPackage()
        logger.info('NewParser.parse', parameter=configuration.parameter)
        with h5py.File(mainfile, "r") as f:
            if "demo_instrument_detectorZ" in list(f["CAMELS_entry"]["data"].keys()):
                logger.info("finding detector")
                archive.data.detectorZ =f["CAMELS_entry"]["data"]["demo_instrument_detectorZ"][()]
            archive.data.certain_value= "test"
        logger.info("h5 was read propperly")
        logger.info(str(os.getcwd()))
        #creating the pdf
        #output = f'test.html'
        #with archive.m_context.raw_file(output,'w') as outfile:
        #    outfile.write("test")#pdf_buffer.read())
        #archive.data.results_pdf = output