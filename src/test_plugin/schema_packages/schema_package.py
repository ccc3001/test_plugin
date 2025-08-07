
from nomad.config import config
from nomad.datamodel.data import EntryData,ArchiveSection
from nomad.metainfo import Quantity, SchemaPackage , Section , SubSection , MSection,SectionProxy
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
import numpy as np
#import test_plugin.parsers.graphs as graphs
configuration = config.get_plugin_entry_point(
    'test_plugin.schema_packages:schema_package_entry_point'
)

m_package = SchemaPackage()



def import_graph_lib(x,y):
    return [
        """
canvas {
      border: 1px solid #ccc;
      margin: 40px auto;
      display: block;
      outline: none;
       border: none;
    }

""",
"""<canvas id="graphCanvas" width="600" height="400"></canvas>"""
,
f"""<script>
  const xValues = {x};
  const yValues = {y};

  const canvas = document.getElementById('graphCanvas');
  const ctx = canvas.getContext('2d');

  const padding = 50;
  const width = canvas.width - padding * 2;
  const height = canvas.height - padding * 2;

  const minX = Math.min(...xValues);
  const maxX = Math.max(...xValues);
  const minY = Math.min(...yValues);
  const maxY = Math.max(...yValues);

  // Transform data point to canvas coordinates
  function getCanvasCoords(x, y) {{
    const xNorm = (x - minX) / (maxX - minX);
    const yNorm = (y - minY) / (maxY - minY);
    return {{
      x: padding + xNorm * width,
      y: canvas.height - padding - yNorm * height
  }};
  }}

  // Draw axes
  function drawAxes() {{
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, canvas.height - padding);
    ctx.lineTo(canvas.width - padding, canvas.height - padding);
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 2;
    ctx.stroke();
  }}

  // Draw grid and labels
  function drawGrid() {{
    ctx.fillStyle = '#000';
    ctx.font = '12px Arial';
    ctx.textAlign = 'center';

    // X-axis labels
    xValues.forEach(x => {{
      const pt = getCanvasCoords(x, minY);
      ctx.fillText(x, pt.x, canvas.height - padding + 15);
    }});

    // Y-axis labels
    const ySteps = 5;
    for (let i = 0; i <= ySteps; i++) {{
      const y = minY + (i * (maxY - minY)) / ySteps;
      const pt = getCanvasCoords(minX, y);
      ctx.fillText(y.toFixed(2), padding - 25, pt.y + 3);
    }}
  }}

  // Draw line graph
  function drawLine() {{
    ctx.beginPath();
    xValues.forEach((x, i) => {{
      const pt = getCanvasCoords(x, yValues[i]);
      if (i === 0) ctx.moveTo(pt.x, pt.y);
      else ctx.lineTo(pt.x, pt.y);
    }});
    ctx.strokeStyle = 'blue';
    ctx.lineWidth = 2;
    ctx.stroke();
  }}

  // Draw data points
  function drawPoints() {{
    ctx.fillStyle = 'red';
    xValues.forEach((x, i) => {{
      const pt = getCanvasCoords(x, yValues[i]);
      ctx.beginPath();
      ctx.arc(pt.x, pt.y, 4, 0, 2 * Math.PI);
      ctx.fill();
    }});
  }}
  function drawAxisLabels() {{
  ctx.fillStyle = '#000';
  ctx.font = '14px Arial';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';

  // X axis label
  ctx.fillText('X Axis', canvas.width / 2, canvas.height - padding + 35);

  // Y axis label (rotated)
  ctx.save(); // Save current canvas state
  ctx.translate(padding - 40, canvas.height / 2);
  ctx.rotate(-Math.PI / 2);
  ctx.fillText('Y Axis', 0, 0);
  ctx.restore(); // Restore original state
  }}

  // Render graph
  drawAxes();
  drawGrid();
  drawLine();
  drawPoints();
  drawAxisLabels(); 
</script>"""]


def import_avg_plot_basics():
    return ["""  
    .scale-wrapper {
      position: relative;
      width: 400px;
      margin: 60px auto;
      font-family: Arial, sans-serif;
    }

    .scale-container {
      position: relative;
      width: 100%;
      height: 20px;
      background: #ddd;
      border-radius: 10px;
    }

    .scale-soft-range {
      position: absolute;
      top: 0;
      height: 20px;
      background: #8bc34a;
      border-radius: 10px;
    }

    .scale-marker {
      position: absolute;
      top: -10px;
      width: 2px;
      height: 40px;
      background: #333;
    }

    .soft-min-marker { background: orange; }
    .soft-max-marker { background: blue; }
    .avg-marker      { background: purple; }

    .label-row {
      position: relative;
      height: 20px;
      margin-top: 8px; /* spacing between scale and labels */
    }

    .label {
      position: absolute;
      font-size: 12px;
      transform: translateX(-50%);
      white-space: nowrap;
    }
"""
,
"""
<script>
  function createScale({ hardMin, hardMax, softMin, softMax, avg, containerId }) {
    softMin =parseFloat(softMin.toFixed(2));
    softMax=parseFloat(softMax.toFixed(2));
    avg=parseFloat(avg.toFixed(2));
    
    const wrapper = document.getElementById(containerId);

    const valueToPercent = val => ((val - hardMin) / (hardMax - hardMin)) * 100;

    // === Scale container ===
    const scale = document.createElement('div');
    scale.className = 'scale-container';

    const softRange = document.createElement('div');
    softRange.className = 'scale-soft-range';
    softRange.style.left = valueToPercent(softMin) + '%';
    softRange.style.width = (valueToPercent(softMax) - valueToPercent(softMin)) + '%';
    scale.appendChild(softRange);

    // Add markers
    const markerData = [
      { val: softMin, className: 'soft-min-marker' },
      { val: softMax, className: 'soft-max-marker' },
      { val: avg,     className: 'avg-marker' }
    ];

    markerData.forEach(({ val, className }) => {
      const marker = document.createElement('div');
      marker.className = `scale-marker ${className}`;
      marker.style.left = valueToPercent(val) + '%';
      scale.appendChild(marker);
    });

    wrapper.appendChild(scale);

    // === Label row below ===
    const labelRow = document.createElement('div');
    labelRow.className = 'label-row';

    markerData.forEach(({ val, className }) => {
      const label = document.createElement('div');
      label.className = 'label';
      label.style.left = valueToPercent(val) + '%';
      label.textContent = `${className.includes('min') ? 'Min' : className.includes('max') ? 'Max' : 'Avg'}: ${val}`;
      labelRow.appendChild(label);
    });

    wrapper.appendChild(labelRow);
  }
</script>
  """]

def import_avg_plot(minimum,maximum,average,container_name):
    return [f"""
    <div class="scale-wrapper" id="{container_name}"></div>
    """,
    f"""
    <script>
      createScale({{hardMin: 1, hardMax: 50, softMin: {minimum}, softMax: {maximum}, avg: {average}, containerId: '{container_name}'}});
    </script>
    """]




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





import base64
import io 
def fig_to_base64(fig):
    img =io.BytesIO()
    fig.savefig(img,format='png',bbox_inches='tight')
    img.seek(0)
    return base64.b64encode(img.getvalue())








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

class MIOData(ArchiveSection):
  TV_01_A_PWM_pwmDutyCycle= Quantity( type=np.float64, shape=['*'])
  TV_01_B_PWM_pwmDutyCycle= Quantity( type=np.float64, shape=['*'])
  TV_02_A_PWM_doDiagnostics= Quantity( type=np.float64, shape=['*'])
  TV_02_A_PWM_pwmDutyCycle= Quantity( type=np.float64, shape=['*'])
  TV_02_B_PWM_pwmDutyCycle= Quantity( type=np.float64, shape=['*'])
  TV_03_A_PWM_pwmDutyCycle= Quantity( type=np.float64, shape=['*'])
  TV_03_B_PWM_pwmDutyCycle= Quantity( type=np.float64, shape=['*'])
  TV_01_A_pos_viDiagnostics= Quantity( type=np.float64, shape=['*'])
  TV_01_B_pos_viDiagnostics= Quantity( type=np.float64, shape=['*'])
  TV_02_A_pos_viDiagnostics= Quantity( type=np.float64, shape=['*'])
  TV_02_B_pos_viDiagnostics= Quantity( type=np.float64, shape=['*'])
  TV_03_A_pos_viDiagnostics= Quantity( type=np.float64, shape=['*'])
  TV_03_B_pos_viDiagnostics= Quantity( type=np.float64, shape=['*'])
  AR_01_PWM_pwmDutyCycle= Quantity( type=np.float64, shape=['*'])
  Supply_Position_Sensors_TV_voDiagnostics= Quantity( type=np.float64, shape=['*'])
  T_ambient= Quantity( type=np.float64, shape=['*'])
  p_ambient= Quantity( type=np.float64, shape=['*'])
  RoundTrip_in_diDiagnostics= Quantity( type=np.float64, shape=['*'])
  T_ambient_Celsius= Quantity( type=np.float64, shape=['*'])
  p_ambient_barA= Quantity( type=np.float64, shape=['*'])
  Actuators_Anode_A_PV_01_prct= Quantity( type=np.float64, shape=['*'])
  Actuators_Anode_A_PC_01_pDiff= Quantity( type=np.float64, shape=['*'])
  Actuators_Anode_A_PC_01_pDiff_ref= Quantity( type=np.float64, shape=['*'])
  Actuators_Anode_B_PV_01_prct= Quantity( type=np.float64, shape=['*'])
  Actuators_Anode_B_PC_01_pDiff= Quantity( type=np.float64, shape=['*'])
  Actuators_Anode_B_PC_01_pDiff_ref= Quantity( type=np.float64, shape=['*'])
  Actuators_Thermal_FLKS_01_freq_ref_Hz= Quantity( type=np.float64, shape=['*'])
  Actuators_Thermal_FLKS_01_fan_prct= Quantity( type=np.float64, shape=['*'])
  Actuators_Thermal_PV_01_prct= Quantity( type=np.float64, shape=['*'])
  Actuators_Thermal_PV_02_prct= Quantity( type=np.float64, shape=['*'])
  Actuators_Thermal_MV_01_ref_prct= Quantity( type=np.float64, shape=['*'])
  Actuators_Thermal_MV_01_act_prct= Quantity( type=np.float64, shape=['*'])
  Actuators_Thermal_CP_01_freq_ref_Hz= Quantity( type=np.float64, shape=['*'])
  Actuators_Thermal_CP_01_freq_act_Hz= Quantity( type=np.float64, shape=['*'])
  Actuators_Thermal_A_AV_01_ref_prct= Quantity( type=np.float64, shape=['*'])
  Actuators_Thermal_A_AV_01_act_prct= Quantity( type=np.float64, shape=['*'])
  Actuators_Thermal_B_AV_01_ref_prct= Quantity( type=np.float64, shape=['*'])
  Actuators_Thermal_B_AV_01_act_prct= Quantity( type=np.float64, shape=['*'])
  Actuators_Cathode_AR_01_prct= Quantity( type=np.float64, shape=['*'])
  Actuators_Cathode_EH_01_Power_prct= Quantity( type=np.float64, shape=['*'])
  Actuators_Cathode_EH_02_Power_prct= Quantity( type=np.float64, shape=['*'])
  Actuators_Cathode_A_TV_01_pos_V= Quantity( type=np.float64, shape=['*'])
  Actuators_Cathode_A_TV_01_pwmDutyCycle= Quantity( type=np.float64, shape=['*'])
  Actuators_Cathode_A_TV_02_pos_V= Quantity( type=np.float64, shape=['*'])
  Actuators_Cathode_A_TV_02_pwmDutyCycle= Quantity( type=np.float64, shape=['*'])
  Actuators_Cathode_A_TV_03_pos_V= Quantity( type=np.float64, shape=['*'])
  Actuators_Cathode_A_TV_03_pwmDutyCycle= Quantity( type=np.float64, shape=['*'])
  Actuators_Cathode_B_TV_01_pos_V= Quantity( type=np.float64, shape=['*'])
  Actuators_Cathode_B_TV_01_pwmDutyCycle= Quantity( type=np.float64, shape=['*'])
  Actuators_Cathode_B_TV_02_pos_V= Quantity( type=np.float64, shape=['*'])
  Actuators_Cathode_B_TV_02_pwmDutyCycle= Quantity( type=np.float64, shape=['*'])
  Actuators_Cathode_B_TV_03_pos_V= Quantity( type=np.float64, shape=['*'])
  Actuators_Cathode_B_TV_03_pwmDutyCycle= Quantity( type=np.float64, shape=['*'])
  Actuators_Cathode_MFC_01_00_p_PSIA= Quantity( type=np.float64, shape=['*'])
  Actuators_Cathode_MFC_01_00_T_Celsius= Quantity( type=np.float64, shape=['*'])
  Actuators_Cathode_MFC_01_00_Vflow_LPM= Quantity( type=np.float64, shape=['*'])
  Actuators_Cathode_MFC_01_00_mflow_SLPM= Quantity( type=np.float64, shape=['*'])
  Actuators_Cathode_MFC_01_00_ref_SLPM= Quantity( type=np.float64, shape=['*'])
  Actuators_Cathode_MFC_01_00_set_SLPM= Quantity( type=np.float64, shape=['*'])
  ECAT_10301_moduleQuality= Quantity( type=np.float64, shape=['*'])
  ECAT_10302_moduleQuality= Quantity( type=np.float64, shape=['*'])
  ECAT_10303_moduleQuality= Quantity( type=np.float64, shape=['*'])
  ECAT_1001_RX_Device_Readings_Gas_Index= Quantity( type=np.float64, shape=['*'])
  ECAT_1001_RX_Command_Result_Last_Command_ID= Quantity( type=np.float64, shape=['*'])
  ECAT_1001_RX_Command_Result_Last_Command_Status= Quantity( type=np.float64, shape=['*'])
  ECAT_1001_TX_Setpoint_Setpoint= Quantity( type=np.float64, shape=['*'])
  ECAT_1001_TX_Command_Request_Command_ID= Quantity( type=np.float64, shape=['*'])
  ECAT_1001_TX_Command_Request_Command_Argument= Quantity( type=np.float64, shape=['*'])
  ECAT_1002_RX_Device_Readings_Gas_Index= Quantity( type=np.float64, shape=['*'])
  ECAT_1002_RX_Command_Result_Last_Command_ID= Quantity( type=np.float64, shape=['*'])
  ECAT_1002_RX_Command_Result_Last_Command_Status= Quantity( type=np.float64, shape=['*'])
  ECAT_1002_TX_Setpoint_Setpoint= Quantity( type=np.float64, shape=['*'])
  ECAT_1002_TX_Command_Request_Command_ID= Quantity( type=np.float64, shape=['*'])
  ECAT_1002_TX_Command_Request_Command_Argument= Quantity( type=np.float64, shape=['*'])
  ECAT_1004_RX_Device_Readings_Gas_Index= Quantity( type=np.float64, shape=['*'])
  ECAT_1004_RX_Command_Result_Last_Command_ID= Quantity( type=np.float64, shape=['*'])
  ECAT_1004_RX_Command_Result_Last_Command_Status= Quantity( type=np.float64, shape=['*'])
  ECAT_1004_TX_Setpoint_Setpoint= Quantity( type=np.float64, shape=['*'])
  ECAT_1004_TX_Command_Request_Command_ID= Quantity( type=np.float64, shape=['*'])
  ECAT_1004_TX_Command_Request_Command_Argument= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_PT_01_barG= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_PT_02_barG= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_PT_03_barG= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_TT_01_0_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_TT_05_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_TT_02_0_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_TT_06_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_TT_03_0_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_TT_07_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_TT_01_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_TT_02_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_TT_04_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_A_PT_04_barG= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_A_PT_05_barG= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_A_PT_06_barG= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_A_MFT_02_slpm= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_A_RHT_01_prctRH= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_A_TT_09_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_A_TT_08_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_A_TT_10_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_A_TT_11_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_A_TT_12_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_B_PT_04_barG= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_B_PT_05_barG= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_B_PT_06_barG= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_B_MFT_02_slpm= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_B_TT_08_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_B_TT_10_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_B_TT_11_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Cathode_B_TT_12_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Anode_PT_01_barG= Quantity( type=np.float64, shape=['*'])
  Fluids_Anode_TT_01_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Anode_A_PT_03_barG= Quantity( type=np.float64, shape=['*'])
  Fluids_Anode_A_PT_04_barG= Quantity( type=np.float64, shape=['*'])
  Fluids_Anode_A_TT_02_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Anode_A_TT_03_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Anode_B_PT_03_barG= Quantity( type=np.float64, shape=['*'])
  Fluids_Anode_B_PT_04_barG= Quantity( type=np.float64, shape=['*'])
  Fluids_Anode_B_TT_02_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Anode_B_TT_03_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Anode_MFT_01_A_p_PSIA= Quantity( type=np.float64, shape=['*'])
  Fluids_Anode_MFT_01_A_T_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Anode_MFT_01_A_Vflow_LPM= Quantity( type=np.float64, shape=['*'])
  Fluids_Anode_MFT_01_A_mflow_SLPM= Quantity( type=np.float64, shape=['*'])
  Fluids_Anode_MFT_01_A_mTotal_SL= Quantity( type=np.float64, shape=['*'])
  Fluids_Anode_MFT_01_B_p_PSIA= Quantity( type=np.float64, shape=['*'])
  Fluids_Anode_MFT_01_B_T_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Anode_MFT_01_B_Vflow_LPM= Quantity( type=np.float64, shape=['*'])
  Fluids_Anode_MFT_01_B_mflow_SLPM= Quantity( type=np.float64, shape=['*'])
  Fluids_Anode_MFT_01_B_mTotal_SL= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_PT_01_barG= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_PT_02_barG= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_PT_03_A_barG= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_PT_03_B_barG= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_PT_04_A_barG= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_PT_04_B_barG= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_PT_05_barG= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_PT_06_barG= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_MFT_01_02_lpm= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_MFT_02_lpm= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_TT_01_01_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_TT_03_02_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_TT_01_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_TT_05_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_TT_02_01_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_TT_04_02_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_TT_06_01_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_TT_08_02_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_TT_07_01_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_TT_09_02_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_TT_11_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_TT_01_02_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_A_MFT_01_lpm= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_A_TT_03_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_A_TT_04_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_B_MFT_01_lpm= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_B_TT_03_Celsius= Quantity( type=np.float64, shape=['*'])
  Fluids_Thermal_B_TT_04_Celsius= Quantity( type=np.float64, shape=['*'])

class ACTIFData(ArchiveSection):
  #m_def=Section()
  Anode_GasSupply_state= Quantity( type=np.float64, shape=['*'])
  Anode_PC_01_A_cmd= Quantity( type=np.float64, shape=['*'])
  Anode_PC_01_A_state= Quantity( type=np.float64, shape=['*'])
  Anode_PC_01_B_cmd= Quantity( type=np.float64, shape=['*'])
  Anode_PC_01_B_state= Quantity( type=np.float64, shape=['*'])
  Anode_PV_01_A_cmd= Quantity( type=np.float64, shape=['*'])
  Anode_PV_01_A_state= Quantity( type=np.float64, shape=['*'])
  Anode_PV_01_B_cmd= Quantity( type=np.float64, shape=['*'])
  Anode_PV_01_B_state= Quantity( type=np.float64, shape=['*'])
  Cathode_AC_01_cmd= Quantity( type=np.float64, shape=['*'])
  Cathode_AC_01_state= Quantity( type=np.float64, shape=['*'])
  Cathode_EH_01_cmd= Quantity( type=np.float64, shape=['*'])
  Cathode_EH_01_state= Quantity( type=np.float64, shape=['*'])
  Cathode_EH_02_cmd= Quantity( type=np.float64, shape=['*'])
  Cathode_EH_02_state= Quantity( type=np.float64, shape=['*'])
  Cathode_MFC_01_00_cmd= Quantity( type=np.float64, shape=['*'])
  Cathode_MFC_01_00_state= Quantity( type=np.float64, shape=['*'])
  Cathode_TV_01_A_cmd= Quantity( type=np.float64, shape=['*'])
  Cathode_TV_01_A_state= Quantity( type=np.float64, shape=['*'])
  Cathode_TV_01_A_theta_prct= Quantity( type=np.float64, shape=['*'])
  Cathode_TV_01_B_cmd= Quantity( type=np.float64, shape=['*'])
  Cathode_TV_01_B_state= Quantity( type=np.float64, shape=['*'])
  Cathode_TV_01_B_theta_prct= Quantity( type=np.float64, shape=['*'])
  Cathode_TV_02_A_cmd= Quantity( type=np.float64, shape=['*'])
  Cathode_TV_02_A_state= Quantity( type=np.float64, shape=['*'])
  Cathode_TV_02_A_theta_prct= Quantity( type=np.float64, shape=['*'])
  Cathode_TV_02_B_cmd= Quantity( type=np.float64, shape=['*'])
  Cathode_TV_02_B_state= Quantity( type=np.float64, shape=['*'])
  Cathode_TV_02_B_theta_prct= Quantity( type=np.float64, shape=['*'])
  Cathode_TV_03_A_cmd= Quantity( type=np.float64, shape=['*'])
  Cathode_TV_03_A_state= Quantity( type=np.float64, shape=['*'])
  Cathode_TV_03_A_theta_prct= Quantity( type=np.float64, shape=['*'])
  Cathode_TV_03_B_cmd= Quantity( type=np.float64, shape=['*'])
  Cathode_TV_03_B_state= Quantity( type=np.float64, shape=['*'])
  Cathode_TV_03_B_theta_prct= Quantity( type=np.float64, shape=['*'])
  Thermal_AV_01_A_cmd= Quantity( type=np.float64, shape=['*'])
  Thermal_AV_01_A_state= Quantity( type=np.float64, shape=['*'])
  Thermal_AV_01_B_cmd= Quantity( type=np.float64, shape=['*'])
  Thermal_AV_01_B_state= Quantity( type=np.float64, shape=['*'])
  Thermal_CP_01_cmd_prct= Quantity( type=np.float64, shape=['*'])
  Thermal_CP_01_state= Quantity( type=np.float64, shape=['*'])
  Thermal_FLKS_01_CP_01_cmd_prct= Quantity( type=np.float64, shape=['*'])
  Thermal_FLKS_01_CP_01_state= Quantity( type=np.float64, shape=['*'])
  Thermal_FLKS_01_Fan_01_cmd= Quantity( type=np.float64, shape=['*'])
  Thermal_FLKS_01_Fan_01_state= Quantity( type=np.float64, shape=['*'])
  Thermal_MV_01_cmd= Quantity( type=np.float64, shape=['*'])
  Thermal_MV_01_state= Quantity( type=np.float64, shape=['*'])
  Thermal_PV_01_cmd= Quantity( type=np.float64, shape=['*'])
  Thermal_PV_01_state= Quantity( type=np.float64, shape=['*'])
  Thermal_PV_02_cmd= Quantity( type=np.float64, shape=['*'])
  Thermal_PV_02_state= Quantity( type=np.float64, shape=['*'])

class ACTIF2Data(ArchiveSection):
  #m_def=Section()
  RH_01_A_state= Quantity( type=np.float64, shape=['*'])
  RH_01_A_cmd= Quantity( type=np.float64, shape=['*'])
  RH_01_B_state= Quantity( type=np.float64, shape=['*'])
  RH_01_B_cmd= Quantity( type=np.float64, shape=['*'])

class HP_CANData(ArchiveSection):
  #m_def=Section()
  Net_A_fbCAN_FSM_iStep= Quantity( type=np.float64, shape=['*'])
  Net_A_RH01_actValues_current_act_A= Quantity( type=np.float64, shape=['*'])
  Net_A_RH01_actValues_power_act_W= Quantity( type=np.float64, shape=['*'])
  Net_A_RH01_actValues_speed_act_rpm= Quantity( type=np.float64, shape=['*'])
  Net_A_RH01_actValues_T_circuit_C= Quantity( type=np.float64, shape=['*'])
  Net_A_RH01_actValues_voltage_act_V= Quantity( type=np.float64, shape=['*'])
  Net_A_RH01_cmd_mDot_cmd_kgph= Quantity( type=np.float64, shape=['*'])
  Net_A_RH01_cmd_speed_cmd_rpm= Quantity( type=np.float64, shape=['*'])
  Net_B_fbCAN_FSM_iStep= Quantity( type=np.float64, shape=['*'])
  Net_B_RH01_actValues_current_act_A= Quantity( type=np.float64, shape=['*'])
  Net_B_RH01_actValues_power_act_W= Quantity( type=np.float64, shape=['*'])
  Net_B_RH01_actValues_speed_act_rpm= Quantity( type=np.float64, shape=['*'])
  Net_B_RH01_actValues_T_circuit_C= Quantity( type=np.float64, shape=['*'])
  Net_B_RH01_actValues_voltage_act_V= Quantity( type=np.float64, shape=['*'])
  Net_B_RH01_cmd_mDot_cmd_kgph= Quantity( type=np.float64, shape=['*'])
  Net_B_RH01_cmd_speed_cmd_rpm= Quantity( type=np.float64, shape=['*'])

# Define your schema class
class NewSchemaPackage(ArchiveSection):
    #m_def=Section()
    #m_def = Section(label='New Schema Package')
    mio_data = SubSection(section=SectionProxy("MIOData"), repeat =False)
    actif_data= SubSection(section=SectionProxy("ACTIFData"), repeat = False)
    actif2_data= SubSection(section=SectionProxy("ACTIF2Data"),repeat = False)
    hp_can_data= SubSection(section=SectionProxy("HP_CANData"), repeat= False)


    #user_info = SubSection(sub_section=UserInfo)
    #protocol_info = SubSection(sub_section=MeasurementInfo)
    ##time_series = SubSection(sub_section=TimeSeries)
  #class UserInfo(MSection):
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
        minimum = np.min(self.detectorX)
        maximum = np.max(self.detectorX)
        average =np.average(self.detectorX)
        mean = np.mean(self.detectorX)
        avg_plot_style,avg_plot_script = import_avg_plot_basics()#graphs.
        plot_style,plot_canvas,plot_script = import_graph_lib([i for i in range(0,len(self.detectorX))],list(self.detectorX))#graphs.
        kathode_1_container,kathode_1_script =import_avg_plot(minimum,maximum,average,"test")#graphs.
        print_style,print_button, print_script = import_print_button()#graphs.
        return f"""
<!DOCTYPE html>
<html>
<head>
<style>
{plot_style}
{avg_plot_style}
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
</head>
<body>
<div class="content">
{print_button}
<h1>Test report</h1>

<p id="outline"> Researcher: {self.user_info.first_name} {self.user_info.last_name}
<br>Email: {self.user_info.email}
<br>Institute: {self.user_info.affiliation}</p>


<h2>Protocol description </h2>
<p id="outline"><br>{self.protocol_info.protocol_description}<br><br><p><br>
<h2>Measurement description </h2>
<p id="outline"><br>{self.protocol_info.measurement_description}<br><br><p><br>
<p id="outline"><br>min: {minimum} max: {maximum} <br>mean: {mean} average: {average} <br><br></p>
<h2>Measurement Comments</h2>
{plot_canvas}
<p id="outline"><br>{self.protocol_info.measurement_comments}<br><br><p>
{kathode_1_container}

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
            ax.plot(self.time_series.ElapsedTime , self.detectorX)
            ax.set_title("Simple Line Plot")
            ax.set_xlabel("X-axis")
            ax.set_ylabel("Y-axis")
            #encoded = fig_to_base64(fig)
            #image_html = '<img src="data:image/png;base64, {}" widht=60%% style="display: block; margin: 0 auto;">'.format(encoded.decode('utf-8'))
            final_html = self.create_pdf()
            with archive.m_context.raw_file(output,'w') as file:
                file.write(final_html)
            self.results_html=str(final_html)