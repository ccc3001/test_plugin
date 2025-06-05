
from nomad.datamodel.data import EntryData,ArchiveSection
from nomad.metainfo import Quantity, SchemaPackage
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
import numpy as np

m_package = SchemaPackage()


# Define your schema class
class NewSchemaPackage(ArchiveSection):
    detectorZ = Quantity(
        type=np.float64,
        shape=['*'])
    certain_value = Quantity(
        type=str
    )