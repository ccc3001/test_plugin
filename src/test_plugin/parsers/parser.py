from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

from nomad.config import config
from nomad.datamodel.metainfo.workflow import Workflow
from nomad.parsing.parser import MatchingParser

configuration = config.get_plugin_entry_point(
    'test_plugin.parsers:parser_entry_point'
)


class NewParser(MatchingParser):
    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
        child_archives: dict[str, 'EntryArchive'] = None,
    ) -> None:
        logger.info('NewParser.parse', parameter=configuration.parameter)
        with h5py.File(filename, "r") as f:
            if "demo_instrument_detectorZ" in list(f["CAMELS_entry"]["data"].keys())
                logger.info("finding detector")
                archive.data.detectorZ =f["CAMELS_entry"]["data"]["demo_instrument_detectorZ"][()]
            archive.data.certain_value= "test"
        logger.info("h5 was read propperly")
