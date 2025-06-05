
from nomad.config import config
from nomad.datamodel.data import EntryData,ArchiveSection
from nomad.metainfo import Quantity, SchemaPackage
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
import numpy as np

configuration = config.get_plugin_entry_point(
    'nomad_plugin_test.schema_packages:schema_package_entry_point'
)

m_package = SchemaPackage()


# Define your schema class
class NewSchemaPackage(ArchiveSection):
    detectorZ = Quantity(
        type=np.float64,
        shape=['*'])
    certain_value = Quantity(
        type=str
    )