import argparse
import json
import os

def main():
    parser = argparse.ArgumentParser(description='Evaluate Phase A experiment results.')
    parser.add_argument('--config', type=str, required=True, help='Path to the config file.')
    parser.add_argument('--outdir', type=str, required=True, help='Path to the output directory.')
    args = parser.parse_args()

    print(f"Evaluating results in {args.outdir} using config {args.config}")
    # a simple check for the output file
    mp4_files = [f for f in os.listdir(args.outdir) if f.endswith('.mp4')]
    if not mp4_files:
        print("No MP4 file found in the output directory.")
        exit(1)

    print(f"Found MP4 file: {mp4_files[0]}")
    print("Evaluation complete.")

if __name__ == '__main__':
    main()
