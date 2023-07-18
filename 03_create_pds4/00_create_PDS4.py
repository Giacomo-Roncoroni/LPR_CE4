# import of the files
import numpy as np
from tqdm import tqdm

#load LPR data with Float32 data type
data = np.load('./data/data_elab_static.npy')[:, :2048].astype(np.float32)
#load coords data
coords = np.genfromtxt('./data/chain_path_Z.txt', skip_header=0)

#define trace #, i.e. FRAME_IDENTIFICATION as linspace
FRAME_IDENTIFICATION = np.linspace(0, data.shape[0]-1, data.shape[0]).astype(np.float32)
#define X, Y, Z variables from coordinates
X = coords[:, 0].astype(np.float32)
Y = coords[:, 1].astype(np.float32)
Z = coords[:, 2].astype(np.float32)
#set radar working mode, i.e. always 0
RADAR_WORKING_MODE = np.zeros((data.shape[0])).astype(np.int8)
# Set Quality state, i.e. always 1
QUALITY_STATE = np.ones((data.shape[0])).astype(np.int8)

#define the name of the .2B and .2BL file
name = 'CE4_PROCESSED_STATIC_LPR_CH2_20190104_20230327_'+ '0002'+ '.2B'

#define length of the trace, i.e. 2048
trace_length = data.shape[1]
#define length of the tracein byte, i.e. 2048*4
trace_length_byte = trace_length * 4
#define # of traces, i.e. 40022
records = data.shape[0]
#define record length, i.e. ([4 byte] * 4 (FRAME_IDENTIFICATION, X, Y, Z) + RADAR_WORKING_MODE [1 byte] + trace_length_byte + QUALITY_STATE [1 byte]
record_length = 4*4 + 1 + trace_length_byte + 1
#compute total byte dimension
size_byte = record_length * records

#we have defined a base file for PDS4 .2BL
#we  insert the above defined variables
base_file = f"""<?xml version="1.0" encoding="UTF-8"?>
<Product_Observational xmlns="http://pds.nasa.gov/pds4/pds/v1" xmlns:pds="http://pds.nasa.gov/pds4/pds/v1" xmlns:sp="http://pds.nasa.gov/pds4/sp/v1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://pds.nasa.gov/pds4/pds/v1,https://starbase.jpl.nasa.gov/pds4/1500/dph_example_products/xml_schema/PDS4_PDS_1500.xsd,http://pds.nasa.gov/pds4/sp/v1 PDS4_SP_1001.xsd">
	<Identification_Area>
		<logical_identifier>{name}</logical_identifier>
		<version_id>1.0</version_id>
		<title>Chang'E 4(CE-4) mission</title>
		<information_model_version>1.5.0.0</information_model_version>
		<product_class>Product_Observational</product_class>
		<Modification_History>
			<Modification_Detail>
				<modification_date>2023-03-17</modification_date>
				<version_id>1.0</version_id>
				<description>None</description>
			</Modification_Detail>
		</Modification_History>
	</Identification_Area>
	<Reference_List>None</Reference_List>
	<Observation_Area>
		<Time_Coordinates>
			<start_date_time>2019-01-04T00:00:00.000Z</start_date_time>
			<stop_date_time>2023-03-27T00:00:00.000Z</stop_date_time>
		</Time_Coordinates>
		<Primary_Result_Summary>
			<purpose>Science</purpose>
			<processing_level>Calibrated</processing_level>
			<Science_Facets>
				<wavelength_range>Microwave</wavelength_range>
				<domain>Surface</domain>
			</Science_Facets>
		</Primary_Result_Summary>
		<Investigation_Area>
			<name>CE4</name>
			<type>Mission</type>
		</Investigation_Area>
		<Observing_System>
			<name>Observing System for CE4</name>
			<Observing_System_Component>
				<name>CE4</name>
				<type>Spacecraft</type>
			</Observing_System_Component>
		</Observing_System>
		<Target_Identification>
			<name>Lunar</name>
			<type>Satellite</type>
		</Target_Identification>
		<Mission_Area>
			<product_id>{name}</product_id>
			<product_version>A</product_version>
			<product_level>2B</product_level>
			<instrument_name>Lunar Penetrating Radar</instrument_name>
			<instrument_id>LPR</instrument_id>
			<sequence_id>{name[-8:-4]}</sequence_id>
			<Work_Mode_Parm>
				<sampling_interval unit="ns">0.312500</sampling_interval>
			</Work_Mode_Parm>
			<Instrument_Parm>
				<central_frequency unit="MHz">500</central_frequency>
				<working_bandwidth unit="MHz">450</working_bandwidth>
				<antenna_height unit="cm">30</antenna_height>
			</Instrument_Parm>
			<Lander_Location>
				<reference_frame>MOON_COORDINATE_SYSTEM</reference_frame>
				<longitude unit="deg">177.599100</longitude>
				<latitude unit="deg">-45.444600</latitude>
			</Lander_Location>
		</Mission_Area>
	</Observation_Area>
	<File_Area_Observational>
		<File>
			<file_name>{name}</file_name>
			<local_identifier>None</local_identifier>
			<creation_date_time>2023-03-17T00:00:00.000Z</creation_date_time>
			<file_size unit="byte">{size_byte}</file_size>
			<records>{records}</records>
		</File>
		<Table_Binary>
			<offset unit="byte">0</offset>
			<records>{records}</records>
			<Record_Binary>
				<fields>6</fields>
				<groups>1</groups>
				<record_length unit="byte">{record_length}</record_length>
				<Field_Binary>
					<name>FRAME_IDENTIFICATION</name>
					<field_number>1</field_number>
					<field_location unit="byte">1</field_location>
					<data_type>IEEE754LSBSingle</data_type>
					<field_length unit="byte">4</field_length>
					<unit>none</unit>
					<description>Trce number: LPR Channel 2 data</description>
				</Field_Binary>
				<Field_Binary>
					<name>XPOSITION</name>
					<field_number>2</field_number>
					<field_location unit="byte">5</field_location>
					<data_type>IEEE754LSBSingle</data_type>
					<field_length unit="byte">4</field_length>
					<unit>m</unit>
					<description>The xposition,yposition and zposition of Rover are centered in the landing site [0, 0]. The x axis points to north and the y axis points to east and the z axis points to the lunar core.</description>
				</Field_Binary>
				<Field_Binary>
					<name>YPOSITION</name>
					<field_number>3</field_number>
					<field_location unit="byte">9</field_location>
					<data_type>IEEE754LSBSingle</data_type>
					<field_length unit="byte">4</field_length>
					<unit>m</unit>
					<description>The yposition of Rover.</description>
				</Field_Binary>
				<Field_Binary>
					<name>ZPOSITION</name>
					<field_number>4</field_number>
					<field_location unit="byte">13</field_location>
					<data_type>IEEE754LSBSingle</data_type>
					<field_length unit="byte">4</field_length>
					<unit>m</unit>
					<description>The zposition of Rover.</description>
				</Field_Binary>
				<Field_Binary>
					<name>RADAR_WORKING_MODE</name>
					<field_number>5</field_number>
					<field_location unit="byte">17</field_location>
					<data_type>UnsignedByte</data_type>
					<field_length unit="byte">1</field_length>
					<unit>none</unit>
					<description>0x00: standby, 0x0f: only Channel 1 works, 0xf0: only Channel 2 works, 0xff: Channel 1 and Channel 2 work.</description>
				</Field_Binary>
				<Group_Field_Binary>
					<name>ECHO_DATA</name>
					<group_number>1</group_number>
					<repetitions>{trace_length}</repetitions>
					<fields>1</fields>
					<groups>0</groups>
					<group_location unit="byte">18</group_location>
					<group_length unit="byte">{trace_length_byte}</group_length>
					<Field_Binary>
						<name>ECHO_DATA</name>
						<field_number>1</field_number>
						<field_location unit="byte">1</field_location>
						<data_type>IEEE754LSBSingle</data_type>
						<field_length unit="byte">4</field_length>
						<unit>none</unit>
						<description>There are 2048 echoes, with a sample interval of 0.3125ns.</description>
					</Field_Binary>
				</Group_Field_Binary>
				<Field_Binary>
					<name>QUALITY_STATE</name>
					<field_number>6</field_number>
					<field_location unit="byte">{trace_length_byte+18}</field_location>
					<data_type>UnsignedByte</data_type>
					<field_length unit="byte">1</field_length>
					<unit>none</unit>
					<description />
				</Field_Binary>
			</Record_Binary>
		</Table_Binary>
	</File_Area_Observational>
</Product_Observational>"""

# write .2BL file
with open(name + 'L', 'w') as f:
    f.write(base_file)

#Write binary file .2B
for i in tqdm(range(data.shape[0])):
    #overwrite in firt trace, i.e. i==0
    if i == 0:    
        with open(name, 'wb') as f:
            f.write(FRAME_IDENTIFICATION[i].tobytes())
        # append
        with open(name, 'ab') as f:
            f.write(X[i].tobytes())
            f.write(Y[i].tobytes())
            f.write(Z[i].tobytes())
            f.write(RADAR_WORKING_MODE[i].tobytes())
            f.write(data[i, :].tobytes())
            f.write(QUALITY_STATE[i].tobytes())
    else:
        with open(name, 'ab') as f:
            f.write(FRAME_IDENTIFICATION[i].tobytes())
            f.write(X[i].tobytes())
            f.write(Y[i].tobytes())
            f.write(Z[i].tobytes())
            f.write(RADAR_WORKING_MODE[i].tobytes())
            f.write(data[i, :].tobytes())
            f.write(QUALITY_STATE[i].tobytes())