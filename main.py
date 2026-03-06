import os
import time
from scraper import MovieScraper
from storage import save_to_json

def name_to_slug(name):
    import re
    import unicodedata
    
    # Chuyển về chữ thường
    name = name.lower().strip()
    # Loại bỏ số thứ tự ở đầu dòng (ví dụ: '1. ')
    name = re.sub(r'^\d+\.\s*', '', name)
    # Khử dấu tiếng Việt
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    # Thay khoảng trắng và ký tự đặc biệt bằng dấu gạch ngang
    slug = re.sub(r'[^a-z0-9]+', '-', name).strip('-')
    return slug

def run_tool_from_file():
    scraper = MovieScraper()
    file_path = "movies.txt"

    if not os.path.exists(file_path):
        print(f"Lỗi: Không tìm thấy file {file_path}!")
        return

    # Đọc danh sách phim từ file txt
    with open(file_path, "r", encoding="utf-8") as f:
        movie_names = [line.strip() for line in f if line.strip()]

    print(f"=== BẮT ĐẦU TRÍCH XUẤT {len(movie_names)} PHIM ===")

    for name in movie_names:
        print(f"\n--- Đang tìm kiếm: {name} ---")
        
        # Bước 1: Tìm slug chuẩn từ tên phim trong file txt
        slug = scraper.search_movie(name)
        
        if slug:
            print(f"Đã thấy slug: {slug}. Đang trích xuất chi tiết...")
            # Bước 2: Cào chi tiết như cũ
            movie_data = scraper.get_movie_info(slug)
            
            if movie_data:
                save_to_json(movie_data)
                print(f"Thành công: {movie_data['title']}")
        else:
            print(f"Thất bại: Không tìm thấy phim '{name}' trên server.")
        
        time.sleep(1) # Tránh bị chặn

    print("\n=== HOÀN THÀNH QUÁ TRÌNH TRÍCH XUẤT ===")

if __name__ == "__main__":
    run_tool_from_file()