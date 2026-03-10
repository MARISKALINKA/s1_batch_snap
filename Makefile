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

