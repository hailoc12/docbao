# ỨNG DỤNG ĐỌC BÁO THEO TỪ KHÓA
Công cụ quét và phân tích từ khóa các trang báo mạng Việt Nam  
Demo: http://www.docbao.danghailoc.com

Version: 1.9.0  
Author: hailoc12  
Email: danghailochp@gmail.com  
Published Date: 2/10/2018  

# Note:
Ứng dụng hoàn toàn miễn phí và sẽ luôn miễn phí. Các phiên bản tốt hơn vẫn sẽ liên tục được cập nhật. Nếu ứng dụng này hữu ích với công việc của bạn, rất mong bạn có thể ủng hộ để tác giả tiếp tục đầu tư cải tiến.

Mọi đóng góp xin gửi về:
- Chủ tài khoản: ĐẶNG HẢI LỘC
- Số tài khoản: 0491000010179
- Ngân hàng: Vietcombank chi nhánh Hoàng Quốc Việt 

Và đừng quên star cho mình nhé :d

# Tính năng nổi bật:
1. Quét được hầu hết các trang báo (cấu hình mặc định quét 31 báo)
2. Phân tích từ khóa thông minh, chỉ giữ lại những từ khóa mạnh (có nội dung thông tin cao)
3. Xác định các từ khóa đang là trends
4. Xác định những từ khóa đang tăng trưởng nhanh
5. Xác định những từ khóa mới xuất hiện
6. Liệt kê toàn bộ các bài báo có chứa từ khóa chỉ trong một nút nhấn
7. Tự động phân mục cho từ khóa
8. Download dữ liệu báo chí dưới dạng excel để phân tích bổ sung
9. Data mở dưới dạng json (click vào mục Tải dữ liệu)

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



