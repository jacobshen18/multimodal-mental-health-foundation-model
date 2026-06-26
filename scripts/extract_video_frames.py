from __future__ import annotations

import argparse
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract evenly spaced frames from a local video file.")
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--num-frames", type=int, default=8)
    return parser


def main() -> None:
    args = build_parser().parse_args()

    try:
        import cv2
    except ImportError as error:
        raise SystemExit("Install video extras first: pip install -e '.[video]'") from error

    args.output_dir.mkdir(parents=True, exist_ok=True)
    capture = cv2.VideoCapture(str(args.video))
    if not capture.isOpened():
        raise SystemExit(f"Could not open video: {args.video}")

    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    if frame_count <= 0:
        raise SystemExit(f"Video has no readable frames: {args.video}")

    indexes = _even_indexes(frame_count, args.num_frames)
    written: list[Path] = []

    for output_index, frame_index in enumerate(indexes):
        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ok, frame = capture.read()
        if not ok:
            continue
        output_path = args.output_dir / f"{output_index:04d}.jpg"
        cv2.imwrite(str(output_path), frame)
        written.append(output_path)

    capture.release()
    for path in written:
        print(path)


def _even_indexes(frame_count: int, num_frames: int) -> list[int]:
    if num_frames <= 1:
        return [0]
    step = max(1, frame_count // num_frames)
    return [min(frame_count - 1, index * step) for index in range(num_frames)]


if __name__ == "__main__":
    main()
