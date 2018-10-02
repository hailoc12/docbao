<?php
error_reporting(E_ALL ^ E_NOTICE);
function append_to_file($filename, $value)
{
    return file_put_contents($filename, $value, FILE_APPEND | LOCK_EX);
}

	if(isset($_POST['keyword'])) {
		$keyword = strtolower($_POST['keyword']);
		if($_POST['chinh_tri'] == "yes")
		{
			$ret = append_to_file("./category/chinh_tri.txt", $keyword . "\r\n");
			if($ret === false) {
            die('There was an error writing this file');
        	}
            else {
            echo "<p>Từ khóa $keyword đã được phân vào chuyên mục Chính trị</p>";
        	}
        }
		if($_POST['kinh_te'] == "yes")
		{
			$ret = append_to_file("./category/kinh_te.txt", $keyword . "\r\n");
			if($ret === false) {
            die('There was an error writing this file');
        	}
            else {
            echo "<p>Từ khóa $keyword đã được phân vào chuyên mục Kinh tế</p>";
        	}
        }        
		if($_POST['van_hoa'] == "yes")
		{
			$ret = append_to_file("./category/van_hoa.txt", $keyword . "\r\n");
			if($ret === false) {
            die('There was an error writing this file');
        	}
            else {
            echo "<p>Từ khóa $keyword đã được phân vào chuyên mục Văn hóa</p>";
        	}
        }	
		if($_POST['xa_hoi'] == "yes")
		{
			$ret = append_to_file("./category/xa_hoi.txt", $keyword . "\r\n");
			if($ret === false) {
            die('There was an error writing this file');
        	}
            else {
            echo "<p>Từ khóa $keyword đã được phân vào chuyên mục Xã hội </p>";
        	}
        }	if($_POST['giao_duc'] == "yes")
		{
			$ret = append_to_file("./category/giao_duc.txt", $keyword . "\r\n");
			if($ret === false) {
            die('There was an error writing this file');
        	}
            else {
            echo "<p>Từ khóa $keyword đã được phân vào chuyên mục Giao duc</p>";
        	}
        }	if($_POST['the_thao'] == "yes")
		{
			$ret = append_to_file("./category/the_thao.txt", $keyword . "\r\n");
			if($ret === false) {
            die('There was an error writing this file');
        	}
            else {
            echo "<p>Từ khóa $keyword đã được phân vào chuyên mục The thao</p>";
        	}
        }	if($_POST['giai_tri'] == "yes")
		{
			$ret = append_to_file("./category/giai_tri.txt", $keyword . "\r\n");
			if($ret === false) {
            die('There was an error writing this file');
        	}
            else {
            echo "<p>Từ khóa $keyword đã được phân vào chuyên mục Giai tri</p>";
        	}
        }       if($_POST['cong_nghe'] == "yes")
		{
			$ret = append_to_file("./category/cong_nghe.txt", $keyword . "\r\n");
			if($ret === false) {
            die('There was an error writing this file');
        	}
            else {
            echo "<p>Từ khóa $keyword đã được phân vào chuyên mục Cong nghe </p>";
        	}
        }       if($_POST['an_ninh'] == "yes")
		{
			$ret = append_to_file("./category/an_ninh.txt", $keyword . "\r\n");
			if($ret === false) {
            die('There was an error writing this file');
        	}
            else {
            echo "<p>Từ khóa $keyword đã được phân vào chuyên mục An ninh </p>";
        	}
        }        
		if($_POST['quoc_phong'] == "yes")
		{
			$ret = append_to_file("./category/quoc_phong.txt", $keyword . "\r\n");
			if($ret === false) {
            die('There was an error writing this file');
        	}
            else {
            echo "<p>Từ khóa $keyword đã được phân vào chuyên mục An ninh quốc phòng</p>";
        	}
        }                	
		if($_POST['suc_khoe'] == "yes")
		{
			$ret = append_to_file("./category/suc_khoe.txt", $keyword . "\r\n");
			if($ret === false) {
            die('There was an error writing this file');
        	}
            else {
            echo "<p>Từ khóa $keyword đã được phân vào chuyên mục Suc khoe</p>";
        	}
        }	if($_POST['doi_song'] == "yes")
		{
			$ret = append_to_file("./category/doi_song.txt", $keyword . "\r\n");
			if($ret === false) {
            die('There was an error writing this file');
        	}
            else {
            echo "<p>Từ khóa $keyword đã được phân vào chuyên mục Doi song</p>";
        	}
        }	if($_POST['giao_thong'] == "yes")
		{
			$ret = append_to_file("./category/giao_thong.txt", $keyword . "\r\n");
			if($ret === false) {
            die('There was an error writing this file');
        	}
            else {
            echo "<p>Từ khóa $keyword đã được phân vào chuyên mục Giao thong</p>";
        	}
        }	if($_POST['moi_truong'] == "yes")
		{
			$ret = append_to_file("./category/moi_truong.txt", $keyword . "\r\n");
			if($ret === false) {
            die('There was an error writing this file');
        	}
            else {
            echo "<p>Từ khóa $keyword đã được phân vào chuyên mục Moi truong</p>";
        	}
        }
		if($_POST['quoc_gia'] == "yes")
		{
			$ret = append_to_file("./category/quoc_gia.txt", $keyword . "\r\n");
			if($ret === false) {
            die('There was an error writing this file');
        	}
            else {
            echo "<p>Từ khóa $keyword đã được phân vào chuyên mục Quốc gia</p>";
        	}
        }
		if($_POST['dia_phuong'] == "yes")
		{
			$ret = append_to_file("./category/dia_phuong.txt", $keyword . "\r\n");
			if($ret === false) {
            die('There was an error writing this file');
        	}
            else {
            echo "<p>Từ khóa $keyword đã được phân vào chuyên mục Địa phương</p>";
        	}
        }                        
		if($_POST['su_kien'] == "yes")
		{
			$ret = append_to_file("./category/su_kien.txt", $keyword . "\r\n");
			if($ret === false) {
            die('There was an error writing this file');
        	}
            else {
            echo "<p>Từ khóa $keyword đã được phân vào chuyên mục Sự kiện</p>";
        	}
        }
		if($_POST['nhan_vat'] == "yes")
		{
			$ret = append_to_file("./category/nhan_vat.txt", $keyword . "\r\n");
			if($ret === false) {
            die('There was an error writing this file');
        	}
            else {
            echo "<p>Từ khóa $keyword đã được phân vào chuyên mục Nhân vật</p>";
        	}
        }
		if($_POST['dia_danh'] == "yes")
		{
			$ret = append_to_file("./category/dia_danh.txt", $keyword . "\r\n");
			if($ret === false) {
            die('There was an error writing this file');
        	}
            else {
            echo "<p>Từ khóa $keyword đã được phân vào chuyên mục Địa danh</p>";
        	}
        }
		if($_POST['tac_pham'] == "yes")
		{
			$ret = append_to_file("./category/tac_pham.txt", $keyword . "\r\n");
			if($ret === false) {
            die('There was an error writing this file');
        	}
            else {
            echo "<p>Từ khóa $keyword đã được phân vào chuyên mục Tác phẩm</p>";
        	}
        }      
	}
?>
