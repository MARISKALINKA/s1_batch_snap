import argparse
import subprocess
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

def run_gpt(gpt, graph, input_file, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / f"{input_file.stem}.tif"

    cmd = [
        gpt,
        str(graph),
        f"-Pinput={input_file}",
        f"-Poutput={out}"
    ]

    print("[GPT]", " ".join([str(c) for c in cmd]))
    subprocess.run(cmd, check=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_dir", type=Path)
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("graph", type=Path)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--gpt", type=str, default=r"C:\Program Files\snap\bin\gpt.exe")
    args = parser.parse_args()

    files = sorted(args.data_dir.glob("*.SAFE"))
    if not files:
        print("No SAFE files found.")
        sys.exit(1)

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for f in files:
            ex.submit(run_gpt, args.gpt, args.graph, f, args.out_dir)

if __name__ == "__main__":
    main()