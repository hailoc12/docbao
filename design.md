Tầng dữ liệu:
	Lựa chọn mysql làm database chính vì hỗ trợ fulltextsearch tốt và tần suất ghi / đọc dữ liệu không quá nhiều
	Các table:
		articles: chứa toàn bộ các link báo:
			id
			topic
			keywords
			description
			content
			image_link
			link
			newspaper
			published_date
			crawled_date
Tầng ứng dụng:
	crawl.py: quét dữ liệu đẩy lên mysql database
		dữ liệu về blacklist link được lưu tại local
		thông số quét cùng tài khoản database lưu tại config.txt
		chỉ các trang báo mới (không nằm trong database) được đẩy lên database
		yêu cầu config của các crawl.py không chứa tờ báo trùng lặp
	analyse.py:
		phân tích từ khoá từ những bài viết mới, đếm trước và update kết quả lên mysql
