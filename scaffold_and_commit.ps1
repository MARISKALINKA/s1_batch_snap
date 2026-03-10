Param(
  [string]$ProjectDir = "E:\Marim\esa_gith\s1_batch_snap",
  [string]$RepoUrl    = ""
)

$ErrorActionPreference = "Stop"

function Ensure-Dir($p) { New-Item -ItemType Directory -Path $p -Force | Out-Null }
function Write-UTF8($path, $content) {
  Ensure-Dir (Split-Path -Parent $path)
  $enc = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText($path, $content, $enc)
}

Write-Host "=== Creating full file package (no processing) ==="
Ensure-Dir $ProjectDir
Set-Location $ProjectDir

# --------------------------------------------------------------------------------
# FOLDERS
# --------------------------------------------------------------------------------
@(
  "data",
  "outputs\stac",
  "scripts",
  "graphs",
  "notebooks",
  "docs",
  "docs\diagrams",
  "docs\usage",
  ".github\workflows",
  "docs\exports"
) | ForEach-Object { Ensure-Dir "$ProjectDir\$_" }

# --------------------------------------------------------------------------------
# environment.yml
# --------------------------------------------------------------------------------
$environment_yml = @"
name: s1-snap
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - pip
  - numpy
  - scipy
  - pandas
  - shapely
  - rasterio
  - gdal
  - matplotlib
  - jupyterlab
  - python-dotenv
  - sentinelsat
  - python-dateutil
  - pip:
      - pystac
      - pystac-client
      - tqdm
      - rich
"@
Write-UTF8 "$ProjectDir\environment.yml" $environment_yml

# --------------------------------------------------------------------------------
# Makefile
# --------------------------------------------------------------------------------
$makefile = @"
PY ?= python
GPT ?= "C:\Program Files\snap\bin\gpt.exe"
DATA_DIR ?= ./data
OUT_DIR ?= ./outputs
WORKERS ?= 4

SIGMA_GRAPH = graphs/s1_grd_sigma0_tc.xml
RTC_GRAPH   = graphs/s1_grd_gamma0_rtc_tc.xml

all: sigma rtc

sigma:
    $(PY) scripts/batch_gpt.py $(DATA_DIR) $(OUT_DIR) $(SIGMA_GRAPH) --workers $(WORKERS)

rtc:
    $(PY) scripts/batch_gpt.py $(DATA_DIR) $(OUT_DIR) $(RTC_GRAPH) --workers $(WORKERS)

cogs:
    $(PY) scripts/cogify.py $(OUT_DIR)/*.tif -o $(OUT_DIR)

cogs3059:
    $(PY) scripts/cogify.py $(OUT_DIR)/*.tif -o $(OUT_DIR) --epsg 3059

stac:
    $(PY) scripts/make_stac.py $(OUT_DIR)/*.tif -o $(OUT_DIR)/stac --collection s1-batch
"@
Write-UTF8 "$ProjectDir\Makefile" $makefile

# --------------------------------------------------------------------------------
# README.md
# --------------------------------------------------------------------------------
$readme = @"
# Sentinel‑1 Batch Processing Pipeline

## A) Compact overview

- σ⁰ Terrain Correction (TC) with ESA SNAP GPT  
- γ⁰ RTC (Terrain‑Flattened) with SNAP Terrain‑Flattening operator  
- COG creation using GDAL COG driver  
- STAC Item generation  
- SAFE auto‑download via Copernicus Data Space Ecosystem (CDSE)  
- Reproducible conda env, Makefile automation

## B) Full documentation

### Install
- SNAP installers are available from ESA STEP.  
- Miniconda silent install: `/InstallationType=JustMe /AddToPath=1 /S /D=E:\Miniconda3`  
- Git via winget: `winget install Git.Git`

### Download SAFE (CDSE)
```bash
python scripts/download_safe_cdse.py --aoi "POLYGON((24 56,24 57,25 57,25 56,24 56))" \
  --start 2025-01-01 --end 2025-01-05 --type GRD --outdir data