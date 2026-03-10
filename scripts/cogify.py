import argparse
from pathlib import Path
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

def make_cog(src_path: Path, dst_path: Path, dst_epsg=None):
    with rasterio.open(src_path) as src:
        data = src.read()
        transform = src.transform
        crs = src.crs
        profile = src.profile.copy()

        # optional reprojection
        if dst_epsg and (not crs or crs.to_epsg() != dst_epsg):
            new_crs = rasterio.crs.CRS.from_epsg(dst_epsg)
            transform, width, height = calculate_default_transform(
                src.crs, new_crs, src.width, src.height, *src.bounds
            )

            mem = rasterio.io.MemoryFile()
            dst_temp = mem.open(
                driver="GTiff",
                height=height,
                width=width,
                count=src.count,
                dtype=src.dtypes[0],
                transform=transform,
                crs=new_crs
            )

            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst_temp, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=new_crs,
                    resampling=Resampling.bilinear,
                )

            data = dst_temp.read()
            crs = new_crs
            transform = dst_temp.transform
            dst_temp.close()

        profile.update(
            driver="COG",
            compress="DEFLATE",
            blocksize=512,
            crs=crs,
            transform=transform
        )

        with rasterio.open(dst_path, "w", **profile) as dst:
            dst.write(data)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("-o", "--outdir", required=True)
    ap.add_argument("--epsg", type=int, default=None)
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    for p in args.inputs:
        p = Path(p)
        dst = outdir / f"{p.stem}.cog.tif"
        print("[COG]", p.name, "->", dst.name)
        make_cog(p, dst, dst_epsg=args.epsg)

if __name__ == "__main__":
    main()