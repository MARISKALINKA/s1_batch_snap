import argparse
import json
from pathlib import Path
import rasterio
from shapely.geometry import mapping, Polygon

def stac_item(path: Path, collection):
    with rasterio.open(path) as src:
        b = src.bounds
        w, s, e, n = b.left, b.bottom, b.right, b.top
        geom = mapping(Polygon([[w,s],[e,s],[e,n],[w,n],[w,s]]))

        return {
            "type": "Feature",
            "stac_version": "1.0.0",
            "id": path.stem,
            "collection": collection,
            "bbox": [w, s, e, n],
            "geometry": geom,
            "properties": {
                "proj:epsg": src.crs.to_epsg()
            },
            "assets": {
                "data": {
                    "href": path.name,
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized"
                }
            },
            "links": []
        }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("-o", "--outdir", required=True)
    ap.add_argument("--collection", default="s1-batch")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    for p in args.inputs:
        p = Path(p)
        item = stac_item(p, args.collection)
        out_file = outdir / f"{p.stem}.stac-item.json"
        out_file.write_text(json.dumps(item, indent=2))
        print("[STAC] ", out_file)

if __name__ == "__main__":
    main()
