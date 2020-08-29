# 1.4.5
	- Sử dụng virtual environment để chạy python
# 1.4.4
	- Bổ sung trường tag cho Webconfig và gán vào mỗi post crawl từ Webconfig đó
	- Bổ sung CDNManager quản lý việc download ảnh và lưu trong local hoặc Amazone S3
	- Bổ sung API suggest relate post và recommendation
# 1.4.3
	- Bổ sung quét Kols từ input/kols_list.txt
		+ mỗi lần chạy sẽ lấy ngẫu nhiên một lượng max_kols và set ngẫu nhiên fb_profile dùng để crawl nó
	- Bổ sung sử dụng nhiều tài khoản Facebook khác nhau để quét dữ liệu
	- Fix lại thuật toán scheduler crawl task:
		+ các webconfig set browser_profile nào sẽ được quét bằng đúng browser profile đó
		+ không có profile nào được hai browser sử dụng cùng lúc
		+ vẫn bảo đảm duy trì số lượng browser hoạt động cùng lúc < max
		+ các crawler tự động thay nhau crawl các task có browser_profile là ''
# 1.4.2
	- Bổ sung config cho phép quét bài báo giữ nguyên vẹn định dạng gốc
	- Mặc định sẽ quét cả sapo 
# 1.4.1
	- Bổ sung trường avatar trong Article để lưu avatar KOLs, avatar báo
	- Bổ sung trường avatar_xpath trong WebConfig để lấy avatar báo cùng với detail. Trường này có thể rỗng
	- Bổ sung tính năng remove_html cho trường sapo trong trường hợp sapo_xpath trả về element thay vì text. Cách cũ (trả về text) vẫn work
	- Update tool config_manager.py để tạo và test crawl profile facebook
# 1.4.0
	- Bổ sung field crawl_type nhận giá trị ['newspaper', 'facebook user', 'facebook page', 'facebook group'] để chạy bộ crawl riêng cho facebook
	- Bổ sung function add_articles_from_facebook() trong backend/lib/data.py
	- Tách phần parse date từ string trong get_time_of_url() ra parse_date_from_string() trong backend/lib/utils.py

tốc độ chạy trên file 
python3.6 maybe 
