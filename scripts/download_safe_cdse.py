import argparse
from pathlib import Path
import requests
import json

CDSE_API = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"

def query_products(aoi_wkt, start, end, product_type="GRD"):
    params = {
        "$filter": (
            f"Collection/Name eq 'SENTINEL-1' "
            f"and OData.CSC.Intersects(area=geography'{aoi_wkt}') "
            f"and ContentDate/Start ge {start} "
            f"and ContentDate/End le {end} "
            f"and Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and att/Value eq '{product_type}')"
        )
    }
    r = requests.get(CDSE_API, params=params)
    r.raise_for_status()
    return r.json().get("value", [])

def download(url, out):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(out, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aoi", required=True, help="WKT POLYGON")
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--type", default="GRD")
    ap.add_argument("--outdir", default="../data")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(exist_ok=True, parents=True)

    print("[INFO] Querying Sentinel‑1 products...")
    products = query_products(args.aoi, args.start, args.end, args.type)

    print(f"[INFO] Found {len(products)} products")
    for p in products:
        name = p["Name"]
        url = p["RemoteLocation"]
        print("[DL]", name)
        download(url, outdir / f"{name}.zip")

if __name__ == "__main__":
    main()