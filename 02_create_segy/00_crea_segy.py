import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import segyio

# load data and coordinates
data = np.load('data_elab_static.npy').astype(np.float32)[:, :]
coords = np.genfromtxt('./chain_path_Z.txt', skip_header=0)

# function is directly derived from https://segyio.readthedocs.io/en/latest/segyio.html
# input: LPR data [ndarray], coordinates [ndarray], file name [str]
# since data and coordinates are saved as integer we multiply coordinates *1e3 and data * 1e5
def crea_segy(y_data, y_coords, name):
    y_data = y_data.astype(np.float32)
    y_coords = y_coords.astype(np.float32)
    # Data
    nx, ny, nz = y_data.shape[0], 1, y_data.shape[1] # Size
    dx, dy, dz = 0.1, 1, 1 # Spacing
    print(y_coords)
    # Inline & Xline
    x = np.linspace(0, nx-1, nx, dtype=int)
    y = np.linspace(0, ny-1, ny, dtype=int)
    
    xl, il = np.meshgrid(x, y)
    
    # Source & Receivers 
    tracecount = nx*ny
    iline = il.reshape(tracecount)
    xline = xl.reshape(tracecount)
    
    
    # SEG-Y file definition
    path = './'+name+'.sgy'
    
    spec = segyio.spec()
    spec.samples = range(nz)
    spec.sorting = segyio.TraceSortingFormat.CROSSLINE_SORTING 
    spec.format  = segyio.SegySampleFormat.IBM_FLOAT_4_BYTE
    spec.ilines  = [10]
    spec.xlines  = range(y_data.shape[0])
    
    mov = dx
    
    lati = ((y_coords[:, 0])*1000).astype(int)
    long = ((y_coords[:, 1])*1000).astype(int)
    print(lati)
    print(long)
    with segyio.create(path, spec) as f:
        # for tr in range(nx*ny):
        tr = 0
        for j, xl in enumerate(tqdm(spec.xlines)):
                f.header[tr] = {
                                    segyio.TraceField.TRACE_SEQUENCE_LINE : tr+100,
                                    segyio.TraceField.TRACE_SEQUENCE_FILE : tr+100,
                                    segyio.TraceField.FieldRecord : tr+100,
                                    segyio.TraceField.TraceNumber : tr+100,
                                    segyio.TraceField.CDP : tr+100,
                                    segyio.TraceField.offset : int(1),
                                    segyio.TraceField.ReceiverGroupElevation : 10,
                                    segyio.TraceField.SourceSurfaceElevation : 10,
                                    segyio.TraceField.SourceDepth : 0,
                                    segyio.TraceField.ElevationScalar : 1,
                                    segyio.TraceField.SourceGroupScalar : 1,
                                    segyio.TraceField.SourceX : (long[j]).astype(int),
                                    segyio.TraceField.SourceY : (lati[j]).astype(int),
                                    segyio.TraceField.SourceSurfaceElevation  : 100,
                                    segyio.TraceField.GroupX : 1,
                                    segyio.TraceField.GroupY : 1,
                                    segyio.TraceField.CoordinateUnits : 0,
                                    segyio.TraceField.DelayRecordingTime : 0,
                                    segyio.TraceField.MuteTimeStart : 0,
                                    segyio.TraceField.MuteTimeEND : 0,
                                    segyio.TraceField.TRACE_SAMPLE_COUNT : nz,
                                    segyio.TraceField.TRACE_SAMPLE_INTERVAL : dz,
                                    segyio.TraceField.INLINE_3D : 1,
                                    segyio.TraceField.CROSSLINE_3D : xl,
                                    segyio.TraceField.ShotPoint : tr,
                                    segyio.TraceField.CDP_X : tr,
                                    segyio.TraceField.CDP_Y : 0,
                                }
                f.trace[tr] = y_data[j, :]*1e5
    
                tr += 1
                

crea_segy(data, coords, '02_moon_elab_static')