from ulab import fft as fft
from ulab import numerical as num
from ulab import array as u_array
from ulab import zeros as u_zeros
from ulab import vector as u_vector
from ulab import filter as u_filter
from constants import PALETTE_LENGTH, CHUNK, MIN_SENSITIVITY
from math import sqrt as m_sqrt
from math import pow as m_pow

EQ = u_array([
    0.000000000000000000,
    0.000000000000000000,
    0.000000000000000000,
    0.000000000000000000,
    -0.000010730691133147,
    -0.000049630693699653,
    -0.000124990185205676,
    -0.000241604768389648,
    -0.000398823711920936,
    -0.000588021549422442,
    -0.000789734755716765,
    -0.000970880132717708,
    -0.001082602106644035,
    -0.001059352294376332,
    -0.000819765824730972,
    -0.000269757877226986,
    0.000691970740637879,
    0.002166134358360450,
    0.004243221620120144,
    0.006992788859855075,
    0.010452726481843257,
    0.014619696333284051,
    0.019441961309204479,
    0.024815700007396350,
    0.030585622909160969,
    0.036550306140921612,
    0.042472176086982241,
    0.048091567788218791,
    0.053143803333771396,
    0.057377852988123597,
    0.060574901860620471,
    0.062565082557105592,
    0.063240762431155922,
    0.062565082557105592,
    0.060574901860620471,
    0.057377852988123597,
    0.053143803333771389,
    0.048091567788218784,
    0.042472176086982262,
    0.036550306140921626,
    0.030585622909160958,
    0.024815700007396357,
    0.019441961309204493,
    0.014619696333284056,
    0.010452726481843262,
    0.006992788859855075,
    0.004243221620120148,
    0.002166134358360453,
    0.000691970740637879,
    -0.000269757877226986,
    -0.000819765824730973,
    -0.001059352294376331,
    -0.001082602106644035,
    -0.000970880132717707,
    -0.000789734755716765,
    -0.000588021549422441,
    -0.000398823711920936,
    -0.000241604768389648,
    -0.000124990185205676,
    -0.000049630693699653,
    -0.000010730691133148,
    0.000000000000000000,
    0.000000000000000000,
    0.000000000000000000,
    0.000000000000000000,])

EQ_ARRAY = u_array([1, 1,1,1,0.9,0.8,0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1,  0,  0,  0,
      0,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,])

def calculate_fft(values):
    #print(len(values))
    spectro = fft.spectrogram(values)
    #finalSpectro = u_vector.log(spectro + 1e-7)
    #spectro = spectro[1:]
    spectroEQ = u_zeros(len(spectro))
    for i in range(len(spectroEQ)):
        spectroEQ[i] = spectro[i] * EQ[i]
    #print(finalSpectro)
    finalSpectro = spectroEQ[1:(CHUNK//2)-1]
    return finalSpectro

def rms(data):
    n = len(data)
    sm = 0
    for i in range(n):
        sm += data[i]
    return m_sqrt(1/(n) * abs(sm)**2)
    #return m_sqrt((1/n) * sm)

def normalized_rms(data):
        mean = num.mean(data)
        corrected = data - mean
        sampleSum = num.sum(corrected * corrected)
        return m_sqrt(sampleSum / len(data))

def clamp(value, maxValue):
    return max(0, min(value, maxValue))

def scale_data(data, totalMax, sensitivity):
    currMin = 10000000
    currMax = -1
    for i in range(len(data)):
        if data[i] < currMin:
            currMin = data[i]
        if data[i] > currMax:
            currMax = data[i]
    newMax = totalMax

    if currMax > newMax:
        newMax = currMax
    else:
        currMax -= 1

    currMin = max(currMin, 3)

    scaled = (data - currMin) * (float(PALETTE_LENGTH*2-1) / (newMax - currMin))
    #print(newMax)
    return scaled, max(sensitivity+MIN_SENSITIVITY, newMax - 100)
