# Backlog
	1.4.5:
		Thêm config: use_universial_crawl
			Dựa trên domain của link để load config phù hợp. (Ứng dụng để quét thông tin từ các trang tổng hợp như Báo Mới)
# Todo:
	1.0.1: Docbao Newspaper với frontend được thiết kế lại
		Minh: 
			- Viết lại giao diện
			- Sử dụng php để đọc json và trả về json theo query
			- Hỗ trợ pagination để giảm tải dữ liệu	
			- Lọc kết quả hiển thị theo đầu báo và thời gian
		Lộc:
			- Build thêm một số chuyên trang để tận dụng cấu hình của VPS mới:
				+ elite: trang chất lượng
				+ business: trang thông tin kinh tế
				+ code: trang tổng hợp thông tin lập trình
				+ pr: trang thông tin pr, marketing, branding
				+ review: review sách, phim
			- Fix code để tự động bỏ qua trang khi bị lỗi
	1.1.0: Cung cấp tính năng log lỗi và report trạng thái hoạt động
