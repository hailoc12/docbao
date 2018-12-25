<?php
error_reporting(E_ALL ^ E_NOTICE);
function append_to_file($filename, $value)
{
    return file_put_contents($filename, $value, FILE_APPEND | LOCK_EX);
}

if(isset($_POST['keyword'])) {
	$keyword = strtolower($_POST['keyword']);
	$categories = [
	    "chinh_tri" => "Chính Trị",
	    "kinh_te" => "Kinh Tế",
	    "xa_hoi" => "Xã Hội",
	    "an_ninh" => "An Ninh",
	    "quoc_phong" => "Quốc Phòng",
	    "van_hoa" => "Văn Hoá",
	    "giao_duc" => "Giáo Dục",
	    "the_thao" => "Thể Thao",
	    "giai_tri" => "Giải Trí",
	    "cong_nghe" => "Công Nghệ",
	    "giao_thong" => "Giao Thông",
	    "quoc_gia" => "Quốc Gia",
	    "dia_danh" => "Địa Danh",
	    "su_kien" => "Sự kiện",
	    "nhan_vat" => "Nhân Vật",
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
