import requests
import json
import time
import os
from pydub import AudioSegment  # 👈 required for merging
from merge_and_cleanup import merge_and_cleanup


license_key = "ad86fdf82d4f4d5b"
splitter_type = "phoenix"
output_dir = "split"
os.makedirs(output_dir, exist_ok=True)

def split_file_with_lalal(file_path: str, stems: list[str]):
    upload_url = "https://www.lalal.ai/api/upload/"
    upload_headers = {
        "Authorization": f"license {license_key}",
        "Content-Disposition": f"attachment; filename={os.path.basename(file_path)}"
    }

    print("🎧 Uploading file...")
    with open(file_path, "rb") as f:
        upload_resp = requests.post(upload_url, headers=upload_headers, data=f)
    upload_json = upload_resp.json()
    print(upload_json)

    if upload_json.get("status") != "success":
        print("❌ Upload failed.")
        return {"status": "error", "message": "Upload failed."}

    file_id = upload_json["id"]
    print(f"✅ Uploaded. File ID: {file_id}")

    results = []
    for stem in stems:
        result = process_stem(file_id, stem)
        results.append(result)

        # Wait until stem file is actually saved before continuing
        expected_filename = f"{stem}_stem.wav"
        expected_path = os.path.join(output_dir, expected_filename)
        while not os.path.exists(expected_path):
            print(f"⏳ Waiting for {expected_filename} to finish downloading...")
            time.sleep(1)

    # ✅ All stems processed — now merge
    try:
        merged_output_path = merge_and_cleanup(output_dir)
        print(f"✅ Merged output: {merged_output_path}")
    except Exception as e:
        return {"status": "error", "message": f"Merge failed: {str(e)}"}

    return {
        "status": "ok",
        "results": results,
        "merged_file": os.path.basename(merged_output_path)
    }


def process_stem(file_id, stem_type):
    print(f"\n🎶 Processing stem: {stem_type}")
    split_url = "https://www.lalal.ai/api/split/"
    split_headers = {"Authorization": f"license {license_key}"}
    split_params = [{
        "id": file_id,
        "stem": stem_type,
        "splitter": splitter_type,
        "dereverb_enabled": True,
        "enhanced_processing_enabled": False
    }]
    split_data = {"params": json.dumps(split_params)}

    split_resp = requests.post(split_url, headers=split_headers, data=split_data)
    split_json = split_resp.json()
    print(split_json)

    if split_json.get("status") != "success":
        return {"stem": stem_type, "status": "error", "message": "split request failed"}

    check_url = "https://www.lalal.ai/api/check/"
    check_data = {"id": file_id}
    while True:
        time.sleep(5)
        check_resp = requests.post(check_url, headers=split_headers, data=check_data)
        check_json = check_resp.json()
        result = check_json["result"].get(file_id, {})
        task = result.get("task", {})
        split_result = result.get("split")

        if task.get("state") == "success" and split_result:
            stem_url = split_result["stem_track"]
            download_file(stem_url, f"{stem_type}_stem.wav")
            return {"stem": stem_type, "status": "ok"}
        elif task.get("state") == "error":
            return {"stem": stem_type, "status": "error", "message": task.get("error")}
        else:
            print(f"⏳ {stem_type} Progress: {task.get('progress', 0)}%")

def download_file(url, filename):
    print(f"⬇️ Downloading {filename}...")
    r = requests.get(url)
    save_path = os.path.join(output_dir, filename)
    with open(save_path, "wb") as f:
        f.write(r.content)
    print(f"✅ Saved: {save_path}")

def merge_stems(folder: str, output_filename: str = "merged_output.wav") -> str:
    audio_files = [f for f in os.listdir(folder) if f.endswith("_stem.wav")]
    audio_files.sort()

    merged = None
    for filename in audio_files:
        filepath = os.path.join(folder, filename)
        segment = AudioSegment.from_wav(filepath)
        if merged is None:
            merged = segment
        else:
            merged = merged.overlay(segment)

    if merged:
        output_path = os.path.join(folder, output_filename)
        merged.export(output_path, format="wav")

        # Clean up original stems
        for filename in audio_files:
            os.remove(os.path.join(folder, filename))

        return output_path
    else:
        raise RuntimeError("No stem files found to merge.")
