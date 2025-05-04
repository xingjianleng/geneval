import argparse
import json
import pickle
import os
from tqdm import trange


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pkl_path", type=str, required=True)
    parser.add_argument("--metadata_path", type=str, default="prompts/evaluation_metadata.jsonl")
    args = parser.parse_args()

    with open(args.pkl_path, "rb") as f:
        data = pickle.load(f)
    with open(args.metadata_path, "r") as f:
        metadatas = [json.loads(line) for line in f.readlines()]

    outer_output_dir = os.path.splitext(args.pkl_path)[0]
    os.makedirs(outer_output_dir, exist_ok=True)

    for i in trange(len(metadatas)):
        metadata = metadatas[i]
        prompt = data["prompts"][i]
        images = data["images"][i]
        assert prompt == metadata["prompt"]

        inner_output_dir = os.path.join(outer_output_dir, str(i).zfill(5))
        os.makedirs(inner_output_dir, exist_ok=True)

        # Save metadata
        metadata_output_path = os.path.join(inner_output_dir, "metadata.jsonl")
        with open(metadata_output_path, "w") as f:
            json.dump(metadata, f)

        inner_sample_output_dir = os.path.join(inner_output_dir, "samples")
        os.makedirs(inner_sample_output_dir, exist_ok=True)

        for j, image in enumerate(images):
            image.save(os.path.join(inner_sample_output_dir, f"{j:05d}.png"))
