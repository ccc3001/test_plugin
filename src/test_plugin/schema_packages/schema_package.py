
from nomad.config import config
from nomad.datamodel.data import EntryData,ArchiveSection
from nomad.metainfo import Quantity, SchemaPackage , Section , SubSection , MSection,SectionProxy

from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
import numpy as np

from nomad.datamodel.metainfo.plot import PlotSection, PlotlyFigure
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import os
import plotly.express as px
import pandas as pd

#import test_plugin.parsers.graphs as graphs
configuration = config.get_plugin_entry_point(
    'test_plugin.schema_packages:schema_package_entry_point'
)

m_package = SchemaPackage()


def import_plot(x_data,y_data,x_label,y_label):
  df=pd.DataFrame(dict(
    x=x_data,
    y=y_data
  ))
  fig= px.line(df,x=x_label,y=y_label,title="test title")
  return (fig.to_html(full_html=False,include_plotlyjs=False))

# data is a list of touple [(data,name,label),(data,name)]
def import_box_plot(data,x_label,y_label,include_plotlyjs_bool):
    tabular_data = {}
    fig = go.Figure()
    for (dataitem,var_name,label) in data:
      if label == "in":
        fig.add_trace(go.Box( y=list(dataitem),x=[var_name for i in range(0,len(dataitem))] ,quartilemethod="linear", name= "in",marker_color='darkblue'))
      elif label =="out":
        fig.add_trace(go.Box( y=list(dataitem),x=[var_name for i in range(0,len(dataitem))] ,quartilemethod="linear", name= "out",marker_color='indianred'))
      tabular_data[var_name,label,"max"]=(np.max(list(dataitem)),3)
      tabular_data[var_name,label,"min"]=(np.min(list(dataitem)),3)
      tabular_data[var_name,label,"avg"]=(np.avg(list(dataitem)),3)

    fig.update_layout(
      yaxis=dict(
        title=dict(
          text= y_label
        )
      ),
      xaxis=dict(
        title=dict(
          text=x_label
        )
      ),
      color="Direction",
      boxmode='group'
    )



    table =f"""<table><thead>
  <tr>
    <th></th>
    <th colspan="2">Anode</th>
    <th colspan="2">Cathode</th>
    <th colspan="2">Thermal</th>
  </tr></thead>
<tbody>
  <tr>
    <td></td>
    <td>in</td>
    <td>out</td>
    <td>in</td>
    <td>out</td>
    <td>in</td>
    <td>out</td>
  </tr>
  <tr>
    <td>min</td>
    <td>{tabular_data["Anode","in","min"]}</td>
    <td>{tabular_data["Anode","out","min"]}</td>
    <td>{tabular_data["Cathode","in","min"]}</td>
    <td>{tabular_data["Cathode","out","min"]}</td>
    <td>{tabular_data["Thermal","in","min"]}</td>
    <td>{tabular_data["Thermal","out","min"]}</td>
  </tr>
  <tr>
    <td>avg</td>
    <td>{tabular_data["Anode","in","avg"]}</td>
    <td>{tabular_data["Anode","out","avg"]}</td>
    <td>{tabular_data["Cathode","in","avg"]}</td>
    <td>{tabular_data["Cathode","out","avg"]}</td>
    <td>{tabular_data["Thermal","in","avg"]}</td>
    <td>{tabular_data["Thermal","out","avg"]}</td>
  </tr>
  <tr>
    <td>max</td>
    <td>{tabular_data["Anode","in","max"]}</td>
    <td>{tabular_data["Anode","out","max"]}</td>
    <td>{tabular_data["Cathode","in","max"]}</td>
    <td>{tabular_data["Cathode","out","max"]}</td>
    <td>{tabular_data["Thermal","in","max"]}</td>
    <td>{tabular_data["Thermal","out","max"]}</td>
  </tr>
</tbody></table>"""

    return(fig.to_html(full_html=False,include_plotlyjs=include_plotlyjs_bool)+"\n"+table)

def import_print_button():
  return ["""
  button.print-button {
  width: 100px;
  height: 100px;
}
span.print-icon, span.print-icon::before, span.print-icon::after, button.print-button:hover .print-icon::after {
  border: solid 4px #333;
}
span.print-icon::after {
  border-width: 2px;
}

button.print-button {
  position: relative;
  padding: 0;
  border: 0;

  border: none;
  background: transparent;
}

span.print-icon, span.print-icon::before, span.print-icon::after, button.print-button:hover .print-icon::after {
  box-sizing: border-box;
  background-color: #fff;
}

span.print-icon {
  position: relative;
  display: inline-block;
  padding: 0;
  margin-top: 20%;

  width: 60%;
  height: 35%;
  background: #fff;
  border-radius: 20% 20% 0 0;
}

span.print-icon::before {
  content: "";
  position: absolute;
  bottom: 100%;
  left: 12%;
  right: 12%;
  height: 110%;

  transition: height .2s .15s;
}

span.print-icon::after {
  content: "";
  position: absolute;
  top: 55%;
  left: 12%;
  right: 12%;
  height: 0%;
  background: #fff;
  background-repeat: no-repeat;
  background-size: 70% 90%;
  background-position: center;

}

button.print-button:hover {
  cursor: pointer;
}

button.print-button:hover .print-icon::before {
  height:0px;
  transition: height .2s;
}
  """ ,"""
  <div class="content">
<button href="#" id="print" class="print-button"><span class="print-icon"></span> <a href="#" id="print"></a></button>
  """
  ,"""
  <script>
  document.addEventListener("DOMContentLoaded", () => {
    let printLink = document.getElementById("print");
    let container = document.getElementById("container");

    printLink.addEventListener("click", event => {
        event.preventDefault();
        printLink.style.display = "none";
        window.print();
        printLink.style.display = "flex";
    }, false);
}, false);
</script>
  """]





#import base64
#import io
#def fig_to_base64(fig):
#    img =io.BytesIO()
#    fig.savefig(img,format='png',bbox_inches='tight')
#    img.seek(0)
#    return base64.b64encode(img.getvalue())








import matplotlib.pyplot as plt


class UserInfo(MSection):
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
class MeasurementInfo(MSection):
  measurement_comments = Quantity(
      type= str
  )
  measurement_description = Quantity(
      type = str
  )
  protocol_description = Quantity(
      type = str
  )
class TimeSeries(MSection):


  time = Quantity(
      type = np.float64,
      shape = ['*']
  )
  elapsed_time = Quantity(
      type=np.float64,
      shape = ['*']
  )
class Ploted_values(PlotSection,ArchiveSection):
    data=Quantity(type=np.float64,shape =['*'])
    name=Quantity(type=  str)
    """
    def get_trace_index(self,left_idx, right_idx):
          divider= int(len(data)/50)
          if divider<=6:
            divider=5
          left_indices = list(range(0, len(self.data), divider))
          right_indices = list(range(0, len(self.data), divider))
          count = 0
          for l in left_indices:
              for r in right_indices:
                  if r > l:
                      if l == left_idx and r == right_idx:
                          return count
                      count += 1
          return None
    def generate_scan_plot(self):

        fig = go.Figure()
        for left in left_indices:
          for right in right_indices:
              if right > left:  # Only valid slices
                  fig.add_trace(
                      go.Scatter(
                          visible=False,
                          line=dict(color='#00CED1', width=1),
                          name=f"Slice {left}:{right}",
                          x=self.m_parent.m_parent.elapsed_time[left:right],
                          y=self.data[left:right]
                      )
                  )
        fig.data[0].visible = True



        steps_left = []
        for left in left_indices:
            step = dict(
                method="update",
                args=[{"visible": [False]*len(fig.data)}],
                label=str(left)
            )
            for right in right_indices:
                if right > left:
                    idx = self._trace_index(left, right)
                    step["args"][0]["visible"][idx] = True
            steps_left.append(step)

        slider_left = dict(
            active=0,
            currentvalue={"prefix": "Left index: "},
            pad={"t": 50},
            steps=steps_left
        )

        # Slider for 'right'
        steps_right = []
        for right in right_indices:
            step = dict(
                method="update",
                args=[{"visible": [False]*len(fig.data)}],
                label=str(right)
            )
            for left in left_indices:
                if right > left:
                    idx = self.get_trace_index(left, right)
                    step["args"][0]["visible"][idx] = True
            steps_right.append(step)

        slider_right = dict(
            active=0,
            currentvalue={"prefix": "Right index: "},
            pad={"t": 50},
            steps=steps_right
        )

        fig.update_layout(sliders=[slider_left, slider_right])

        return PlotlyFigure(label='data', figure=fig.to_plotly_json())
"""
    def normalize(self, archive, logger):
      super(Ploted_values, self).normalize(archive, logger)
      if self.data is None or len(self.data) == 0:
        return 0
        #self.append(self.generate_scan_plot())
      figure1= px.line(x=self.m_parent.m_parent.elapsed_time, y=self.data, title="")
      self.figures.append(PlotlyFigure(label='figure', figure=figure1.to_plotly_json()))
      try:
        figure2 = go.Figure()
        figure2.add_trace(go.Box( y=self.data, quartilemethod="linear", name=  "" ))
        self.figures.append(PlotlyFigure(label="figure2",figure = figure2.to_plotly_json()))
      except NameError:
          print("variable namme wasnt defined")
      """
      m_def=Section(
        a_plot={
        'label': 'Pressure and Temperature vs Time',
        'x': f'{self.m_parent.time}',
        'y': './data',
        'config': {'editable': False, 'scrollZoom': True}
        },
        a_table={
        'columns': ['./data'],
        'label': 'Measurement Table'
        }
      )
      m_annotations={
        "eln": {
            "show": True,
            "widgets": [
                {"type": "DataTable", "label": "Table View"},
                {"type": "PlotlyGraph", "label": "Graph View"}
            ]
        }
    }
    """


class MIOData(ArchiveSection):
  TV_01_A_PWM_pwmDutyCycle= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  TV_01_B_PWM_pwmDutyCycle= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  TV_02_A_PWM_doDiagnostics= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  TV_02_A_PWM_pwmDutyCycle= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  TV_02_B_PWM_pwmDutyCycle= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  TV_03_A_PWM_pwmDutyCycle= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  TV_03_B_PWM_pwmDutyCycle= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  TV_01_A_pos_viDiagnostics= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  TV_01_B_pos_viDiagnostics= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  TV_02_A_pos_viDiagnostics= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  TV_02_B_pos_viDiagnostics= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  TV_03_A_pos_viDiagnostics= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  TV_03_B_pos_viDiagnostics= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  AR_01_PWM_pwmDutyCycle= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Supply_Position_Sensors_TV_voDiagnostics= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  T_ambient= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  p_ambient= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  RoundTrip_in_diDiagnostics= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  T_ambient_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  p_ambient_barA= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Anode_A_PV_01_prct= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Anode_A_PC_01_pDiff= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Anode_A_PC_01_pDiff_ref= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Anode_B_PV_01_prct= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Anode_B_PC_01_pDiff= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Anode_B_PC_01_pDiff_ref= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Thermal_FLKS_01_freq_ref_Hz= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Thermal_FLKS_01_fan_prct= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Thermal_PV_01_prct= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Thermal_PV_02_prct= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Thermal_MV_01_ref_prct= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Thermal_MV_01_act_prct= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Thermal_CP_01_freq_ref_Hz= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Thermal_CP_01_freq_act_Hz= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Thermal_A_AV_01_ref_prct= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Thermal_A_AV_01_act_prct= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Thermal_B_AV_01_ref_prct= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Thermal_B_AV_01_act_prct= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Cathode_AR_01_prct= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Cathode_EH_01_Power_prct= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Cathode_EH_02_Power_prct= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Cathode_A_TV_01_pos_V= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Cathode_A_TV_01_pwmDutyCycle= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Cathode_A_TV_02_pos_V= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Cathode_A_TV_02_pwmDutyCycle= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Cathode_A_TV_03_pos_V= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Cathode_A_TV_03_pwmDutyCycle= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Cathode_B_TV_01_pos_V= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Cathode_B_TV_01_pwmDutyCycle= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Cathode_B_TV_02_pos_V= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Cathode_B_TV_02_pwmDutyCycle= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Cathode_B_TV_03_pos_V= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Cathode_B_TV_03_pwmDutyCycle= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Cathode_MFC_01_00_p_PSIA= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Cathode_MFC_01_00_T_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Cathode_MFC_01_00_Vflow_LPM= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Cathode_MFC_01_00_mflow_SLPM= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Cathode_MFC_01_00_ref_SLPM= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Actuators_Cathode_MFC_01_00_set_SLPM= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  ECAT_10301_moduleQuality= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  ECAT_10302_moduleQuality= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  ECAT_10303_moduleQuality= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  ECAT_1001_RX_Device_Readings_Gas_Index= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  ECAT_1001_RX_Command_Result_Last_Command_ID= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  ECAT_1001_RX_Command_Result_Last_Command_Status= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  ECAT_1001_TX_Setpoint_Setpoint= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  ECAT_1001_TX_Command_Request_Command_ID= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  ECAT_1001_TX_Command_Request_Command_Argument= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  ECAT_1002_RX_Device_Readings_Gas_Index= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  ECAT_1002_RX_Command_Result_Last_Command_ID= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  ECAT_1002_RX_Command_Result_Last_Command_Status= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  ECAT_1002_TX_Setpoint_Setpoint= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  ECAT_1002_TX_Command_Request_Command_ID= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  ECAT_1002_TX_Command_Request_Command_Argument= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  ECAT_1004_RX_Device_Readings_Gas_Index= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  ECAT_1004_RX_Command_Result_Last_Command_ID= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  ECAT_1004_RX_Command_Result_Last_Command_Status= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  ECAT_1004_TX_Setpoint_Setpoint= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  ECAT_1004_TX_Command_Request_Command_ID= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  ECAT_1004_TX_Command_Request_Command_Argument= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_PT_01_barG= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_PT_02_barG= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_PT_03_barG= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_TT_01_0_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_TT_05_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_TT_02_0_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_TT_06_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_TT_03_0_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_TT_07_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_TT_01_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_TT_02_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_TT_04_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_A_PT_04_barG= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_A_PT_05_barG= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_A_PT_06_barG= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_A_MFT_02_slpm= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_A_RHT_01_prctRH= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_A_TT_09_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_A_TT_08_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_A_TT_10_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_A_TT_11_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_A_TT_12_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_B_PT_04_barG= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_B_PT_05_barG= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_B_PT_06_barG= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_B_MFT_02_slpm= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_B_TT_08_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_B_TT_10_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_B_TT_11_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Cathode_B_TT_12_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Anode_PT_01_barG= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Anode_TT_01_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Anode_A_PT_03_barG= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Anode_A_PT_04_barG= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Anode_A_TT_02_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Anode_A_TT_03_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Anode_B_PT_03_barG= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Anode_B_PT_04_barG= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Anode_B_TT_02_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Anode_B_TT_03_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Anode_MFT_01_A_p_PSIA= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Anode_MFT_01_A_T_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Anode_MFT_01_A_Vflow_LPM= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Anode_MFT_01_A_mflow_SLPM= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Anode_MFT_01_A_mTotal_SL= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Anode_MFT_01_B_p_PSIA= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Anode_MFT_01_B_T_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Anode_MFT_01_B_Vflow_LPM= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Anode_MFT_01_B_mflow_SLPM= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Anode_MFT_01_B_mTotal_SL= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_PT_01_barG= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_PT_02_barG= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_PT_03_A_barG= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_PT_03_B_barG= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_PT_04_A_barG= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_PT_04_B_barG= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_PT_05_barG= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_PT_06_barG= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_MFT_01_02_lpm= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_MFT_02_lpm= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_TT_01_01_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_TT_03_02_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_TT_01_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_TT_05_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_TT_02_01_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_TT_04_02_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_TT_06_01_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_TT_08_02_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_TT_07_01_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_TT_09_02_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_TT_11_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_TT_01_02_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_A_MFT_01_lpm= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_A_TT_03_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_A_TT_04_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_B_MFT_01_lpm= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_B_TT_03_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Fluids_Thermal_B_TT_04_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeat = False)


class ACTIFData(ArchiveSection):
  #m_def=Section()
  Anode_GasSupply_state= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Anode_PC_01_A_cmd= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Anode_PC_01_A_state= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Anode_PC_01_B_cmd= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Anode_PC_01_B_state= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Anode_PV_01_A_cmd= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Anode_PV_01_A_state= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Anode_PV_01_B_cmd= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Anode_PV_01_B_state= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Cathode_AC_01_cmd= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Cathode_AC_01_state= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Cathode_EH_01_cmd= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Cathode_EH_01_state= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Cathode_EH_02_cmd= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Cathode_EH_02_state= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Cathode_MFC_01_00_cmd= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Cathode_MFC_01_00_state= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Cathode_TV_01_A_cmd= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Cathode_TV_01_A_state= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Cathode_TV_01_A_theta_prct= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Cathode_TV_01_B_cmd= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Cathode_TV_01_B_state= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Cathode_TV_01_B_theta_prct= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Cathode_TV_02_A_cmd= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Cathode_TV_02_A_state= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Cathode_TV_02_A_theta_prct= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Cathode_TV_02_B_cmd= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Cathode_TV_02_B_state= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Cathode_TV_02_B_theta_prct= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Cathode_TV_03_A_cmd= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Cathode_TV_03_A_state= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Cathode_TV_03_A_theta_prct= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Cathode_TV_03_B_cmd= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Cathode_TV_03_B_state= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Cathode_TV_03_B_theta_prct= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Thermal_AV_01_A_cmd= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Thermal_AV_01_A_state= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Thermal_AV_01_B_cmd= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Thermal_AV_01_B_state= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Thermal_CP_01_cmd_prct= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Thermal_CP_01_state= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Thermal_FLKS_01_CP_01_cmd_prct= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Thermal_FLKS_01_CP_01_state= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Thermal_FLKS_01_Fan_01_cmd= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Thermal_FLKS_01_Fan_01_state= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Thermal_MV_01_cmd= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Thermal_MV_01_state= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Thermal_PV_01_cmd= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Thermal_PV_01_state= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Thermal_PV_02_cmd= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Thermal_PV_02_state= SubSection(section=SectionProxy("Ploted_values"), repeat = False)


class ACTIF2Data(ArchiveSection):
  #m_def=Section()
  RH_01_A_state= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  RH_01_A_cmd= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  RH_01_B_state= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  RH_01_B_cmd= SubSection(section=SectionProxy("Ploted_values"), repeat = False)


class HP_CANData(ArchiveSection):
  #m_def=Section()
  Net_A_fbCAN_FSM_iStep= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Net_A_RH01_actValues_current_act_A= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Net_A_RH01_actValues_power_act_W= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Net_A_RH01_actValues_speed_act_rpm= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Net_A_RH01_actValues_T_circuit_C= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Net_A_RH01_actValues_voltage_act_V= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Net_A_RH01_cmd_mDot_cmd_kgph= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Net_A_RH01_cmd_speed_cmd_rpm= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Net_B_fbCAN_FSM_iStep= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Net_B_RH01_actValues_current_act_A= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Net_B_RH01_actValues_power_act_W= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Net_B_RH01_actValues_speed_act_rpm= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Net_B_RH01_actValues_T_circuit_C= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Net_B_RH01_actValues_voltage_act_V= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Net_B_RH01_cmd_mDot_cmd_kgph= SubSection(section=SectionProxy("Ploted_values"), repeat = False)
  Net_B_RH01_cmd_speed_cmd_rpm= SubSection(section=SectionProxy("Ploted_values"), repeat = False)


class test_Section(PlotSection, EntryData):
    time = Quantity(type=np.float64, shape=['*'], unit = 's')
    chamber_pressure = Quantity(type=np.float64, shape=['*'], unit='Pa' )
    substrate_temperature = Quantity(type=np.float64, shape=['*'], unit='K')

    m_def = Section(
        a_plot={
        'label': 'Pressure and Temperature vs Time',
        'x': './time',
        'y': ['./chamber_pressure', './substrate_temperature'],
        'config': {'editable': True, 'scrollZoom': False}
        },
        a_table={
        'columns': ['./time', './chamber_pressure', './substrate_temperature'],
        'label': 'Measurement Table'
        }
    )
    m_annotations = {
        "eln": {
            "show": True,
            "widgets": [
                {"type": "DataTable", "label": "Table View"},
                {"type": "PlotlyGraph", "label": "Graph View"}
            ]
        }
    }


    """
  m_def = Section()
  time = Quantity(type=np.float64, shape=['*'], unit = 's')
  substrate_temperature = Quantity(type=np.float64, shape=['*'], unit='K')
  chamber_pressure = Quantity(type=np.float64, shape=['*'], unit='Pa' )
  def normalize(self, archive, logger):
        super(test_Section, self).normalize(archive, logger)

        first_line = px.scatter(x=self.time, y=self.m_parent.elapsed_time)
        second_line = px.scatter(x=self.time, y=self.chamber_pressure)
        figure1 = make_subplots(rows=1, cols=2, shared_yaxes=True)
        figure1.add_trace(first_line.data[0], row=1, col=1)
        figure1.add_trace(second_line.data[0], row=1, col=2)
        figure1.update_layout(height=400, width=716, title_text="Creating Subplots in Plotly")
        self.figures.append(PlotlyFigure(label='figure 1', figure=figure1.to_plotly_json()))

        figure2 = px.scatter(x=self.substrate_temperature, y=self.chamber_pressure, color=self.chamber_pressure, title="Chamber as a function of Temperature")
        self.figures.append(PlotlyFigure(label='figure 2', index=1, figure=figure2.to_plotly_json()))
        """

# Define your schema class
class NewSchemaPackage(ArchiveSection):
    #m_def=Section()
    #m_def = Section(label='New Schema Package')
    mio_data = SubSection(section=SectionProxy("MIOData"), repeat =False)
    actif_data= SubSection(section=SectionProxy("ACTIFData"), repeat = False)
    actif2_data= SubSection(section=SectionProxy("ACTIF2Data"),repeat = False)
    hp_can_data= SubSection(section=SectionProxy("HP_CANData"), repeat= False)
    test_section= SubSection(section=SectionProxy("test_Section"), repeat = False)
    """
    m_def = Section(a_plot={
        'label': 'Temperature and Pressure',
        'x': './time',
        'y': ['./time', './elapsed_time'],
        'config': {
            'editable': True,
            'scrollZoom': False
        }})
        """
    file_name = Quantity(
      type = str
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
  #class MeasurementInfo(MSection):
    measurement_comments = Quantity(
        type= str
    )
    measurement_description = Quantity(
        type = str
    )
    protocol_description = Quantity(
        type = str
    )
  #class TimeSeries(MSection)  :


    time = Quantity(
        type = np.float64,
        shape = ['*']
    )
    elapsed_time = Quantity(
        type=np.float64,
        shape = ['*']
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


    def create_pdf(self):


        minimum = np.min(self.mio_data.Fluids_Thermal_B_TT_03_Celsius.data)
        maximum = np.max(self.mio_data.Fluids_Thermal_B_TT_03_Celsius.data)
        average =np.average(self.mio_data.Fluids_Thermal_B_TT_03_Celsius.data)
        mean = np.mean(self.mio_data.Fluids_Thermal_B_TT_03_Celsius.data)
        #avg_plot_style,avg_plot_script = import_avg_plot_basics()#graphs.
        #plot_style,plot_canvas,plot_script = import_graph_lib(list(self.elapsed_time),list(self.mio_data.Fluids_Thermal_B_TT_03_Celsius.data))#graphs.
        # data is a list of touple [(data,name,label),(data,name)]
        boxplot_temp_A=import_box_plot([(self.mio_data.Fluids_Anode_A_TT_02_Celsius.data,"Anode","in"),(self.mio_data.Fluids_Anode_A_TT_03_Celsius.data,"Anode","out"),(self.mio_data.Fluids_Cathode_A_TT_10_Celsius.data,"Cathode","in"),(self.mio_data.Fluids_Cathode_A_TT_11_Celsius.data,"Cathode","out"),(self.mio_data.Fluids_Thermal_A_TT_03_Celsius.data,"Thermal","in"),(self.mio_data.Fluids_Thermal_A_TT_04_Celsius.data,"Thermal","out")]," ","Temp[C°]",True)
        boxplot_preassure_A=import_box_plot([(self.mio_data.Fluids_Anode_A_PT_03_barG.data,"Anode","in"),(self.mio_data.Fluids_Cathode_A_PT_05_barG.data,"Cathode","in"),(self.mio_data.Fluids_Thermal_PT_03_A_barG.data,"Thermal","in"),(self.mio_data.Fluids_Anode_A_PT_04_barG.data,"Anode","out"),(self.mio_data.Fluids_Cathode_A_PT_06_barG.data,"Cathode","out"),(self.mio_data.Fluids_Thermal_PT_04_A_barG.data,"Thermal","out")]," ","Pressure[barg]",False)
        boxplot_temp_B=import_box_plot([(self.mio_data.Fluids_Anode_B_TT_02_Celsius.data,"Anode","in"),(self.mio_data.Fluids_Anode_B_TT_03_Celsius.data,"Anode","out"),(self.mio_data.Fluids_Cathode_B_TT_10_Celsius.data,"Cathode","in"),(self.mio_data.Fluids_Cathode_B_TT_11_Celsius.data,"Cathode","out"),(self.mio_data.Fluids_Thermal_B_TT_03_Celsius.data,"Thermal","in"),(self.mio_data.Fluids_Thermal_B_TT_04_Celsius.data,"Thermal","out")]," ","Temp[C°]",True)
        boxplot_preassure_B=import_box_plot([(self.mio_data.Fluids_Anode_B_PT_03_barG.data,"Anode","in"),(self.mio_data.Fluids_Cathode_B_PT_05_barG.data,"Cathode","in"),(self.mio_data.Fluids_Thermal_PT_03_B_barG.data,"Thermal","in"),(self.mio_data.Fluids_Anode_B_PT_04_barG.data,"Anode","out"),(self.mio_data.Fluids_Cathode_B_PT_06_barG.data,"Cathode","out"),(self.mio_data.Fluids_Thermal_PT_04_B_barG.data,"Thermal","out")]," ","Pressure[barg]",False)
        import_plot(self.elapsed_time, self.mio_data.Fluids_Thermal_B_TT_03_Celsius.data, "elapsed time","Temp[°C]")
        print_style,print_button, print_script = import_print_button()#graphs.
        return f"""
<!DOCTYPE html>
<html>
<head>
<style>
{print_style}
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
<style type="text/css">
.tg  {{border-collapse:collapse;border-spacing:0;}}
.tg td{{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  overflow:hidden;padding:10px 5px;word-break:normal;}}
.tg th{{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}}
.tg .tg-baqh{{text-align:center;vertical-align:top}}
.tg .tg-0pky{{border-color:inherit;text-align:left;vertical-align:top}}
</style>
</head>
<body>
<div class="content">
{print_button}
<h1>Test report</h1>

<p id="outline"> Researcher: {self.first_name} {self.last_name}
<br>Email: {self.email}
<br>Institute: {self.affiliation}</p>


<h2>Protocol description </h2>
<p id="outline"><br>{self.protocol_description}<br><br><p><br>
<h2>Measurement description </h2>
<p id="outline"><br>{self.measurement_description}<br><br><p><br>
<p id="outline"><br>min: {minimum} max: {maximum} <br>mean: {mean} average: {average} <br><br></p>
<h2>Measurement Comments</h2>
{plot_canvas}
<p id="outline"><br>{self.measurement_comments}<br><br><p>

<h2>Stack A</h2>
<p id="outline">{boxplot_temp_A}<br>{boxplot_preassure_A}<p>


<h2>Stack B</h2>
<p id="outline">{boxplot_temp_B}<br>{boxplot_preassure_B}<p>



</div>
{print_script}
</body>
</html>
"""

    def normalize(self, archive:'EntryArchive',logger:'BoundLogger')-> None:
        super(NewSchemaPackage,self).normalize(archive,logger)

        output=f"{self.file_name}.html"
        if self.mio_data.Fluids_Thermal_B_TT_03_Celsius is not None:
            final_html = self.create_pdf()
            with archive.m_context.raw_file(output,'w') as file:
                file.write(final_html)
            self.results_html=str(final_html)