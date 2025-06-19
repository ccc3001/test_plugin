
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
    return base64.b64encode(img.getvalue())








import matplotlib.pyplot as plt


# Define your schema class
class NewSchemaPackage(ArchiveSection):
    measurement_comments = Quantity(
        type= str 
    )
    measurement_description = Quantity(
        type = str
    )
    protocol_description = Quantity(
        type = str
    )
    time = Quantity(
        type = np.float64,
        shape = ['*']
    )
    elapsed_time = Quantity(
        type=np.float64,
        shape = ['*']
    )
    first_name = Quantity(
        type=str
    )    
    last_name = Quantity(
        type= str 
    )
    email =  Quantity(
        type = str 
    )
    affiliation = Quantity(
        type = str 
    )


    results_pdf = Quantity(
        type=str,
        a_browser=dict(adaptor='RawFileAdaptor',render_value ='HtmlValue')
    )
    results_html = Quantity(
        type= str,
        a_browser=dict(render_value ='HtmlValue')
    )
    
    
    certain_value = Quantity(
        type=str
    )
    detectorZ = Quantity(
        type=np.float64,
        shape=['*'])


    def create_pdf(self,image):
        minimum = np.min(self.detectorZ)
        maximum = np.max(self.detectorZ)
        average =np.average(self.detectorZ)
        mean = np.mean(self)
        return f"""
<!DOCTYPE html>
<html>
<head>
<style>
#outline {{
    outline: 2px solid black;
}}

</style>
</head>
<body>
<h1>Test report</h1>

<p id="outline"> Researcher: {self.first_name} {self.last_name}
<br>Email: {self.email}
<br>Institute: {self.affiliation}</p>


<h2>Protocol description </h2>
<p id="outline"><br>{self.protocol_description}<br><br><p><br>
<h2>Measurement description </h2>
<p id="outline"><br>{self.measurement_description}<br><br><p><br>
{image}
<p id="outline"><br>min: {minimum} max: {maximum} <br>mean: {mean} average: {average} <br><br></p>
<h2>Measurement Comments</h2>

<p id="outline"><br>{self.measurement_comments}<br><br><p>
</body>
</html>
"""

    def normalize(self, archive:'EntryArchive',logger:'BoundLogger')-> None:
        super(NewSchemaPackage,self).normalize(archive,logger)
        output=f"test.html"
        if self.detectorZ is not None:
            fig,ax = plt.subplots()
            ax.plot(self.ElapsedTime , self.detectorZ)
            ax.set_title("Simple Line Plot")
            ax.set_xlabel("X-axis")
            ax.set_ylabel("Y-axis")
            encoded = fig_to_base64(fig)
            image_html = '<img src="data:image/png;base64, {}">'.format(encoded.decode('utf-8'))
            final_html = create_pdf(self,image_html)
            with archive.m_context.raw_file(output,'w') as file:
                file.write(final_html)
            self.results_html=str(final_html)