# ỨNG DỤNG ĐỌC BÁO THEO TỪ KHÓA
Công cụ quét và tổng hợp từ khóa từ các trang báo, blog tiếng Việt và tiếng Anh 

Demo
1. Trang tổng hợp 31 báo tiếng Việt: http://www.docbao.danghailoc.com
2. Chuyên trang công nghệ tiếng Việt + tiếng Anh: http://www.congnghe.danghailoc.c


Version: 1.9.2  
Author: hailoc12  
Email: danghailochp@gmail.com  
Updated: 15/10/2018  

# Note:
Ứng dụng hoàn toàn miễn phí và sẽ luôn miễn phí. Các phiên bản tốt hơn vẫn sẽ liên tục được cập nhật. Nếu ứng dụng này hữu ích với công việc của bạn, rất mong bạn có thể ủng hộ để tác giả tiếp tục đầu tư cải tiến.

Mọi đóng góp xin gửi về:
- Chủ tài khoản: ĐẶNG HẢI LỘC
- Số tài khoản: 0491000010179
- Ngân hàng: Vietcombank chi nhánh Hoàng Quốc Việt 

Và đừng quên star cho mình nhé :d

# Tính năng nổi bật:
1. Quét được hầu hết các trang báo, blog tiếng Anh và tiếng Việt nhờ phương pháp quét linh hoạt
2. Sử dụng xử lý ngôn ngữ (NLP) để phân tích tiêu đề báo thành các keyword
3. Thuật toán lọc từ khóa thông minh, giúp loại bỏ keyword yếu, chỉ giữ lại keyword mạnh, giàu thông tin
4. Tự động phân keyword vào các chuyên mục. Có thể tùy biến chuyên mục theo nhu cầu cá nhân
5. Phân tích nâng cao giúp xác định keyword mới xuất hiện, keyword có tần suất tăng trưởng nhanh, keyword đang là trends. Dễ dàng code mở rộng để thực hiện các phân tích khác
6. Tìm kiếm nhanh chóng toàn bộ các bài báo có chứa keyword
7. Hệ sinh thái phong phú, gồm backend quét và phân tích dữ liệu, frontend hiển thị cài đặt trên web, tool command-line để truy cập dữ liệu từ laptop/pc (hỗ trợ của Windows và Linux)
8. Hỗ trợ export database dễ dàng dưới dạng excel và json để phân tích bổ sung hoặc tái sử dụng trong các dự án khác

# Ưu tiên phát triển (Backlog)
1. Xây dựng tính năng tự động phân bài báo vào các chủ đề (topic)
2. Hỗ trợ quét báo sử dụng proxy để tránh bị block
3. Sử dụng scrapy để quét song song, nhằm tăng tốc độ quét
4. Sử dụng MongoDB/Redis làm database để lưu trữ dữ liệu lâu hơn
5. Sử dụng Go làm RESTFUL API server
6. Sử dụng wordpress / static web làm frontend
7. Thiết kế lại UI/UX cho frontend
8. Xây dựng tool truy cập dữ liệu trên Android
9. Xây dựng tool GUI truy cập dữ liệu trên Windows
10. Xây dựng các thuật toán phân tích keywords mới

# Cài đặt frontend
1. Chuẩn bị host php, tạo tài khoản ftp để đẩy file lên host (nếu bạn không có host, có thể liên hệ với mình qua email để mượn account)
2. Cài rclone. Add new config với tên gọi "docbao" và account ftp đã tạo ỏ trên để đẩy file lên host
3. Đẩy frontend lên host
~~~~
rclone copy -v ~/docbao/frontend docbao:
~~~~
4. Mở host bằng browser để kiểm tra

# Cài đặt backend
A. Cài trên linux (ubuntu / raspberry pi 3)
1. Clone mã nguồn về địa chỉ ~/docbao
2. Chmod file
~~~~
chmod 755 ~/docbao/backend/run
chmod 755 ~/docbao/run_docbao.sh
~~~~
3. Chạy quét dữ liệu lần đầu: 
~~~~
bash ~/docbao/backend/run
~~~~
Nếu báo lỗi thiếu thư viện thì sử dụng pip3 để cài bổ sung  
Quá trình chạy có thể kéo dài 10-20 phút  
4. Test kết quả: mở file ~/docbao/backend/export/local_html/index.html  
5. Test chạy và đẩy dữ liệu lên frontend  
~~~~
bash ~/docbao/run_docbao.sh
~~~~
6. Mở địa chỉ host để kiểm tra. CLick vào "Tải dữ liệu". Mở file keyword_freq_log.json. Nếu trường time sát với thời điểm hiện tại là ok
7. Cài đặt crontab để chạy tự động
~~~~
crontab -e
~~~~
Bổ sung dòng sau vào cuối file. Thay /home/pi bằng username của bạn
Backend sẽ chạy tự động 10p / lần. Nếu bạn muốn thay đổi thông số này, thì cần thay đổi cả loop_interval trong ~/docbao/backend/input/config.txt
~~~~
*/10 * * * * /bin/bash /home/pi/docbao/run_docbao.sh > ~/cron_log
~~~~
8. Mở file ~/docbao/backend/input/config.txt để tùy biến theo nhu cầu



