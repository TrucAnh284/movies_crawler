import requests

class MovieScraper:
    def __init__(self):
        # API backend chuẩn cho các site phim hiện nay
        self.api_base = "https://phimapi.com/phim/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    def search_movie(self, keyword):
        # API tìm kiếm yêu cầu keyword và thường có giới hạn trả về (limit)
        search_url = f"https://phimapi.com/v1/api/tim-kiem?keyword={keyword}&limit=1"
        try:
            res = requests.get(search_url, headers=self.headers, timeout=10)
            if res.status_code == 200:
                data = res.json()
                
                # Kiểm tra cấu trúc: status có thành công và có danh sách items không
                if data.get('status') == 'success' or data.get('status') == True:
                    items = data.get('data', {}).get('items', [])
                    
                    if items:
                        # Lấy item đầu tiên trong danh sách
                        first_item = items[0]
                        slug = first_item.get('slug')
                        print(f"-> Đã tìm thấy phim: {first_item.get('name')} (Slug: {slug})")
                        return slug
            
            print(f"-> Không tìm thấy kết quả cho từ khóa: {keyword}")
            return None
        except Exception as e:
            print(f"-> Lỗi khi tìm kiếm: {e}")
            return None

    def get_movie_info(self, slug):
        url = f"{self.api_base}{slug}"
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            
            # Kiểm tra nếu API trả về lỗi 404 hoặc 500
            if response.status_code != 200:
                print(f"Lỗi: API trả về mã lỗi {response.status_code}")
                return None

            data = response.json()

            # Nếu data là chuỗi (String), ép nó về rỗng để không bị lỗi .get()
            if isinstance(data, str):
                print(f"Cảnh báo: API trả về nội dung chữ: '{data}' (Có thể slug '{slug}' sai)")
                return None
            
            # Kiểm tra xem có dữ liệu phim không
            if isinstance(data, dict) and (data.get('status') == True or 'movie' in data):
                movie = data.get('movie', {})
                episodes = data.get('episodes', [])
                
                result = {
                    "title": movie.get('name', 'N/A'),
                    "origin_name": movie.get('origin_name', ''),
                    "year": movie.get('year', ''),
                    "content": movie.get('content', '').replace('<p>', '').replace('</p>', ''),
                    "episodes": []
                }

                # Duyệt qua các server để lấy link m3u8
                for server in episodes:
                    server_name = server.get('server_name', 'Server VIP')
                    for item in server.get('server_data', []):
                        result['episodes'].append({
                            "server": server_name,
                            "name": item.get('name'),
                            "link_m3u8": item.get('link_m3u8')
                        })
                return result
            
            print(f"Lỗi: Cấu trúc JSON không đúng hoặc không có phim '{slug}'")
            return None
                
        except Exception as e:
            print(f"Lỗi hệ thống: {e}")
            return None