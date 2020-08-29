# Version 1.4.0  

## User story 1: Tự động config website mới  
	- Khi muốn config một website mới, thay vì phải config bằng tay, người dùng có thể chạy file config_manager.py  
	- Bước 1, người dùng sẽ được lựa chọn sửa config cũ / tạo mới config dựa trên một vài template có sẵn (Facebook, website), hoặc config mới hoàn toàn  
	- Bước 2: nếu người dùng lựa chọn tạo một config mới từ đầu thì sẽ được list ra toàn bộ các thuộc tính cần config, bao gồm các thuộc tính bắt buộc / mặc định. Người dùng sẽ lựa chọn stt để chỉnh sửa các thuộc tính  
	- Bước 3: khi đã chỉnh sửa xong, người dùng có thể chạy test cấu hình mà mình đã dùng. Hệ thống sẽ report kết quả, và trả về một số thông số để giúp người dùng quyết định phần config có ổn hay không  
	- Bước 4: nếu ổn, người dùng có thể export config ra file trong resources/config/newspaper  

## Design: 

## Plan:  
	2019-06-21: 
		- xây dựng trang theo dõi education dựa trên việc lọc tin tức có chứa một số dạng từ khoá 
			+ Bổ sung trường contains  
