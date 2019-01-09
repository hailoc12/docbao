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
	docbao_crawler:
		tự động chia tập báo cần quét thành các tập nhỏ để quét song song. Số tập để quét song song quy định trong config --> dùng chung config_queue, blacklist database, log database
		các crawler sẽ nhận job từ config_queue và quét
			(có thể dùng chung firefox browser được không ?)
		crawler quét xong báo nào thì đẩy dữ liệu lên mysql luôn cho nóng
		blacklist database cũng được lưu luôn để đề phòng crash ?
		kết thúc mỗi phiên chạy, blacklist database sẽ được optimize để tự động loại bỏ và lưu rra file
	docbao_analyse.py:
		phân tích từ khoá từ những bài viết mới, đếm trước và update kết quả lên mysql
	docbao_manage:
		dùng để report trạng thái số lần chạy, từ đó phát hiện ra các báo bị lỗi liên tục để có phương án xử lý
		cung cấp shell để nghiên cứu trang / fix lỗi cấu hình báo
	docbao_config:
		build config mới từ config_database
