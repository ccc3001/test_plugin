from nomad.config import config
from nomad.datamodel.data import EntryData,ArchiveSection
from nomad.metainfo import Quantity, SchemaPackage
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
import numpy as np

configuration = config.get_plugin_entry_point(
    'test_plugin.schema_packages:schema_package_entry_point'
)

m_package = SchemaPackage()





import base64
import io 
def fig_to_base64(fig):
    img =io.BytesIO()
    fig.savefig(img,format='png',bbox_inches='tight')
    img.seek(0)


html_begining= """<!DOCTYPE html>
<html>
<head>
</head>
<body>
<h1>Test report</h1>
<p>This is the description of the report<p>"""

html_end="""</body>
</html>"""

# Define your schema class
class NewSchemaPackage(ArchiveSection):
    detectorZ = Quantity(
        type=np.float64,
        shape=['*'])
    certain_value = Quantity(
        type=str
    )
    results_pdf = Quantity(
        type=str,
         a_browser=dict(adaptor='RawFileAdaptor')
    )
    import matplotlib.pyplot as plt
    from reportlab.pdfgen import canvas
    from io import BytesIO
    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer)
    pdf.save()
    pdf_buffer.seek(0) 

    def normalize(self, archive:'EntryArchive',logger:'BoundLogger')-> None:
        super(NewSchemaPackage,self).normalize(archive,logger)
        output=f"test.html"
        fig =fig = plt.figure()
        encoded = fig_to_base64(fig)
        my_html = '<img src="data:image/png;base64, {}">'.format(encoded.decode('utf-8'))
        with archive.m_context.raw_file(output,'w') as file:
            file.write(html_begining+my_html+html_end)#self.pdf_buffer.read())
        results_pdf = output