import os

extract_dir = r"C:\Users\Admin\Videos\Github\IOS-Emoji-Font\Made By Another Dev\extracted"
for root, dirs, files in os.walk(extract_dir):
    for f in files:
        fp = os.path.join(root, f)
        print(f"File: {os.path.relpath(fp, extract_dir)}")
        if f.endswith(".sh") or f.endswith(".prop"):
            print("--- Content ---")
            with open(fp, "r", encoding="utf-8", errors="ignore") as content_file:
                print(content_file.read())
