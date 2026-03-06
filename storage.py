import json
import os

def save_to_json(data, filename="movies_data.json"):
    folder = "database"

    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"--- Đã tạo thư mục: {folder} ---")
    filepath = os.path.join(folder, filename)
    existing_data = []
    
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = []
    existing_data.append(data)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)
        
    print(f"--- Đã lưu dữ liệu vào: {filepath} ---")