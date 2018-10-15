<?php
error_reporting(E_ALL ^ E_NOTICE);
function append_to_file($filename, $value)
{
    return file_put_contents($filename, $value, FILE_APPEND | LOCK_EX);
}

if(isset($_POST['keyword'])) {
	$keyword = strtolower($_POST['keyword']);
	$categories = [
	    "san_pham" => "Sản phẩm",
	    "thiet_bi" => "Thiết bị",
	    "game" => "Game",
	    "thuong_hieu" => "Thương hiệu",
	    "cong_nghe" => "Công nghệ",
	    "nghien_cuu" => "Nghiên cứu",
	    "tri_tue_nhan_tao" => "Trí tuệ nhân tạo",
	    "khoi_nghiep" => "Khởi nghiệp",
	    "huong_dan" => "Hướng dẫn",
	    "quoc_gia" => "Quốc gia",
	    "dia_phuong" => "Địa phương",
	    "su_kien" => "Sự kiện",
	    "nhan_vat" => "Nhân vật",
	];
	foreach($categories as $category_key => $category_name) {
	    if(isset($_POST[$category_key]) && $_POST[$category_key] == "yes") {
		$filename = "./category/". $category_key .".txt";
		$ret = append_to_file($filename, $keyword . "\r\n");
		if($ret === false) {
		    die('There was an error writing this file');
		}
		else {
		    echo "<p>Từ khóa $keyword đã được phân vào chuyên mục ". $category_name . "</p>";
		}    
	    }
	}
}
?>
