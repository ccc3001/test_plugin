
from nomad.config import config
from nomad.datamodel.data import EntryData,ArchiveSection
from nomad.metainfo import Quantity, SchemaPackage
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
import numpy as np
import test_plugin.parsers.graphs as graphs
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
    detectorX = Quantity(
        type=np.float64,
        shape=['*'])


    def create_pdf(self,image):
        minimum = np.min(self.detectorX)
        maximum = np.max(self.detectorX)
        average =np.average(self.detectorX)
        mean = np.mean(self.detectorX)
        avg_plot_style,avg_plot_script = graphs.import_avg_plot_basics()
        plot_style,plot_canvas,plot_script = graphs.import_graph_lib([i for i in range(0,len(self.detectorX))],self.detectorX.round(2))
        kathode_1_container,kathode_1_script =graphs.import_avg_plot(minimum,maximum,average,"test")
        return f"""
<!DOCTYPE html>
<html>
<head>
<style>
{plot_style}
{avg_plot_style}
#outline {{
    outline: 2px solid black;
}}
.content {{
      width: 210mm;
      min-height: 297mm;
      margin: 10mm auto;
      padding: 20mm;
      background: white;   
        }}
@media print {{
      @page {{
        size: A4 portrait;
        margin: 0;
      }}

      * {{
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }}

      .page {{
        page-break-after: always;
      }}
    }}       
</style>
</head>
<body>
<div class="content">
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
{kathode_1_container}
{plot_canvas}
</div>
{avg_plot_script}
{plot_script}
{kathode_1_script}
</body>
</html>
"""

    def normalize(self, archive:'EntryArchive',logger:'BoundLogger')-> None:
        super(NewSchemaPackage,self).normalize(archive,logger)
        output=f"test.html"
        if self.detectorX is not None:
            fig,ax = plt.subplots()
            ax.plot(self.ElapsedTime , self.detectorX)
            ax.set_title("Simple Line Plot")
            ax.set_xlabel("X-axis")
            ax.set_ylabel("Y-axis")
            encoded = fig_to_base64(fig)
            image_html = '<img src="data:image/png;base64, {}" widht=60%% style="display: block; margin: 0 auto;">'.format(encoded.decode('utf-8'))
            final_html = self.create_pdf(image_html)
            with archive.m_context.raw_file(output,'w') as file:
                file.write(final_html)
            self.results_html=str(final_html)