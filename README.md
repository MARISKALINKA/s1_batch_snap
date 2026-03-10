### Project Structure

s1\_batch\_snap/

│   environment.yml

│   Makefile

│   README.md

│

├── data/                 # SAFE scenes go here

├── outputs/              # SNAP outputs

│   └── stac/             # STAC metadata

│

├── scripts/

│     batch\_gpt.py        # Runs SNAP GPT in parallel

│     cogify.py           # GeoTIFF → COG

│     make\_stac.py        # STAC Item generator

│     download\_safe\_cdse.py  # SAFE auto‑download

│

├── graphs/

│     s1\_grd\_sigma0\_tc.xml        # ESA σ0 TC graph

│     s1\_grd\_gamma0\_rtc\_tc.xml    # ESA γ0 RTC graph

│

└── notebooks/

&nbsp;     S1\_sigma0.ipynb

&nbsp;     S1\_gamma0\_RTC.ipynb



### &nbsp;2.Installation



#### 2.1 Install SNAP (ESA)

SNAP installers are distributed through the ESA STEP portal, providing Sentinel‑1,‑2,‑3 toolboxes and updated with each major version. 

The STEP website confirms current installers are available for Windows, macOS and Linux, built via Install4J. \[pypi.org]

Download the Windows 64‑bit SNAP installer:

https://step.esa.int/main/download/snap-download/

SNAP uses the install4j installer engine, supporting unattended install with:

SNAP\_Installer.exe -q -dir "C:\\Program Files\\snap"



#### 2.2 Install Miniconda (silent)

The official Miniconda docs describe silent installation as:

Miniconda3.exe /InstallationType=JustMe /RegisterPython=0 /AddToPath=1 /S /D=E:\\Miniconda3



### 2.3 Install Git (winget)

Microsoft's Windows Package Manager (winget) allows silent Git install:

winget install --id Git.Git -e --source winget



### 2.4 Create environment



conda env create -f environment.yml

conda activate s1-snap



### 3.Download Sentinel‑1 SAFE (CDSE)



SA transitioned from SciHub to the Copernicus Data Space Ecosystem (CDSE) as the primary data hub for Sentinel‑1,‑2,‑3 products. 

The SNAP documentation references CDSE as the authoritative download source.



Use the provided script:

python scripts/download\_safe\_cdse.py \\

&nbsp;   --aoi "POLYGON((...))" \\

&nbsp;   --start 2024-01-01 \\

&nbsp;   --end   2024-01-10 \\

&nbsp;   --type GRD \\

&nbsp;   --outdir data



### 4.SNAP Processing Workflows

#### 4.1 σ⁰ Terrain Correction

Using ESA workflow:



Read

Apply‑Orbit‑File

Calibration → σ⁰

Terrain Correction (R-D TC using Copernicus DEM)

Write GeoTIFF





#### 4.2 γ⁰ RTC (Terrain‑Flattening) — ESA Official

The SNAP documentation highlights:



Terrain‑Flattening operator

Copernicus 30m DEM

Local incidence angle output

Use in RTC workflows



The installer page and SNAP guides confirm RTC processing is part of the Microwave Toolbox in SNAP. 

Graph stages:



1.Read

2.Apply‑Orbit‑File

3.Thermal Noise Removal

4.Calibration → γ⁰

5\.Terrain‑Flattening

6.Terrain Correction

7.Output GeoTIFF



### 5.Run SNAP Batch Processing



σ⁰ TC:

make sigma



γ⁰ RTC:

make rtc



These call:

scripts/batch\_gpt.py data outputs graphs/s1\_grd\_\_\_\_.xml --workers 4



### 6\.Convert to Cloud‑Optimized GeoTIFF (COG)



he GDAL documentation confirms that the COG raster driver performs tiled, overview‑enabled, HTTP‑range request optimized output via CreateCopy. 

Built-in via:



make cogs



or:

make cogs3059



for EPSG:3059 reprojection.



### 7.Generate STAC Metadata



***make stac***



Produces \*.stac-item.json in outputs/stac/.





### 8.Notebooks



**S1\_sigma0.ipynb**



Quicklook

Histogram

Metadata viewer



**S1\_gamma0\_RTC.ipynb**



γ⁰ linear preview

γ⁰ dB preview

Angle layers

Time series ready





### 9\.Usage Examples



**Download data**

python scripts/download\_safe\_cdse.py --aoi "POLYGON((24 56, 24 57, 25 57, 25 56, 24 56))" --start 2025-05-01 --end 2025-05-05





**Process σ⁰**

make sigma



**Process RTC**

make rtc



**Convert to COG**

make cogs3059



**Generate STAC**

make stac



**Visualize**

jupyter lab





### 10\. Troubleshooting



**SNAP fails to execute**

Ensure SNAP is installed in:

C:\\Program Files\\snap



Install4J silent mode -q is supported for SNAP installation. 



**CDSE download fails**

Check that the AOI is valid.

The STEP website confirms CDSE is the correct service for Sentinel‑1 access. 



**COG creation errors**

Ensure gdal and rasterio match versions.

GDAL's COG driver is provided by GDAL ≥ 3.1. 





flowchart TD

&nbsp; start(\[Start]) --> sigma\[make sigma<br/>Run σ⁰ TC GPT]

&nbsp; start --> rtc\[make rtc<br/>Run γ⁰ RTC GPT]

&nbsp; sigma --> cogs\[make cogs / cogs3059<br/>GeoTIFF → COG (GDAL COG)]

&nbsp; rtc --> cogs

&nbsp; cogs --> stac\[make stac<br/>Build STAC Items]

&nbsp; stac --> nb\[Open notebooks<br/>jupyter lab]

