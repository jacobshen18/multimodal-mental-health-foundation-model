from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

from mhfm.multimodal_dataset import load_multimodal_jsonl
from mhfm.multimodal_schema import MultimodalRecord


@dataclass(frozen=True)
class TrainConfig:
    model_name: str
    train_manifest: Path
    image_root: Path
    output_dir: Path
    batch_size: int
    num_epochs: int
    learning_rate: float
    max_frames_per_video: int
    device: str


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Train a CLIP-style image/video-text adapter.")
    parser.add_argument("--train-manifest", type=Path, required=True)
    parser.add_argument("--image-root", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=Path("checkpoints/multimodal-clip"))
    parser.add_argument("--model-name", default="openai/clip-vit-base-patch32")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--num-epochs", type=int, default=1)
    parser.add_argument("--learning-rate", type=float, default=1e-5)
    parser.add_argument("--max-frames-per-video", type=int, default=4)
    parser.add_argument("--device", default="auto")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    config = TrainConfig(
        model_name=args.model_name,
        train_manifest=args.train_manifest,
        image_root=args.image_root,
        output_dir=args.output_dir,
        batch_size=args.batch_size,
        num_epochs=args.num_epochs,
        learning_rate=args.learning_rate,
        max_frames_per_video=args.max_frames_per_video,
        device=args.device,
    )
    train(config)


def train(config: TrainConfig) -> None:
    try:
        import torch
        from PIL import Image
        from torch.utils.data import DataLoader, Dataset
        from tqdm import tqdm
        from transformers import CLIPModel, CLIPProcessor
    except ImportError as error:
        raise SystemExit("Install multimodal extras first: pip install -e '.[multimodal]'") from error

    device = _resolve_device(config.device, torch)
    records = load_multimodal_jsonl(config.train_manifest)
    dataset = _ClipManifestDataset(records, config.image_root, config.max_frames_per_video, Image)
    loader = DataLoader(dataset, batch_size=config.batch_size, shuffle=True, collate_fn=lambda rows: rows)

    processor = CLIPProcessor.from_pretrained(config.model_name)
    model = CLIPModel.from_pretrained(config.model_name).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)

    model.train()
    for epoch in range(config.num_epochs):
        progress = tqdm(loader, desc=f"epoch {epoch + 1}")
        for rows in progress:
            texts = [row["text"] for row in rows]
            images = [row["image"] for row in rows]
            inputs = processor(text=texts, images=images, return_tensors="pt", padding=True).to(device)
            outputs = model(**inputs, return_loss=True)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            progress.set_postfix(loss=float(loss.detach().cpu()))

    config.output_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(config.output_dir)
    processor.save_pretrained(config.output_dir)
    (config.output_dir / "training_config.json").write_text(
        json.dumps(config.__dict__, default=str, indent=2) + "\n",
        encoding="utf-8",
    )


class _ClipManifestDataset:
    def __init__(self, records: list[MultimodalRecord], root: Path, max_frames: int, image_module) -> None:
        self.records = records
        self.root = root
        self.max_frames = max_frames
        self.image_module = image_module

    def __len__(self) -> int:
        return len(self.records)

    def __getitem__(self, index: int) -> dict[str, object]:
        record = self.records[index]
        image_path = self._select_image_path(record)
        image = self.image_module.open(image_path).convert("RGB")
        return {"id": record.id, "text": record.text, "image": image}

    def _select_image_path(self, record: MultimodalRecord) -> Path:
        if record.image_path:
            return self._resolve(record.image_path)
        if record.frame_paths:
            return self._resolve(record.frame_paths[: self.max_frames][0])
        raise ValueError(f"{record.id} has no visual path")

    def _resolve(self, path: str) -> Path:
        candidate = Path(path)
        if candidate.is_absolute():
            return candidate
        return self.root / candidate


def _resolve_device(device: str, torch_module) -> str:
    if device != "auto":
        return device
    if torch_module.cuda.is_available():
        return "cuda"
    if getattr(torch_module.backends, "mps", None) and torch_module.backends.mps.is_available():
        return "mps"
    return "cpu"


if __name__ == "__main__":
    main()
