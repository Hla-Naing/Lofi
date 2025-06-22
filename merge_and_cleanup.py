from pydub import AudioSegment
from pathlib import Path

def merge_and_cleanup(folder: str, output_filename: str = "merged_output.wav") -> str:
    folder_path = Path(folder)
    audio_files = sorted(folder_path.glob("*_stem.wav"))

    if not audio_files:
        raise RuntimeError("No stem files found to merge.")

    # Load and normalize durations
    segments = []
    for file in audio_files:
        try:
            seg = AudioSegment.from_file(file)
            segments.append(seg)
        except Exception as e:
            print(f"❌ Skipping {file.name}: {e}")

    max_duration = max(len(seg) for seg in segments)
    normalized = [(seg * (max_duration // len(seg) + 1))[:max_duration] for seg in segments]

    # Overlay all segments
    mixed = normalized[0]
    for seg in normalized[1:]:
        mixed = mixed.overlay(seg)

    # Export merged file
    output_path = folder_path / output_filename
    mixed.export(output_path, format="wav")
    print(f"✅ Merged output saved to: {output_path}")

    # Delete all stem files
    for file in audio_files:
        try:
            file.unlink()
            print(f"🗑️ Deleted: {file}")
        except Exception as e:
            print(f"❌ Failed to delete {file.name}: {e}")

    return str(output_path)
