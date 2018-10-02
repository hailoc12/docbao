<?php
echo '
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="">
  <meta name="author" content="">
  <title>Đọc báo theo từ khóa</title>
  <!-- Bootstrap core CSS-->
  <link href="vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">
  <!-- Custom fonts for this template-->
  <link href="vendor/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">
  <!-- Custom styles for this template-->
  <link href="css/sb-admin.css" rel="stylesheet">
  <!--Autocomplete-->
  <script>  
      function clickKeyword(object){
                  document.getElementById("myInput").value = object.innerHTML;
                  myFunction()
            }
      </script>
</head>

<body class="fixed-nav sticky-footer bg-dark" id="page-top">
  <div ng-app="docbaoApp" ng-controller="logCtrl">

    <!-- Navigation-->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top" id="mainNav">
      <a class="navbar-brand" href="index.html">
      ĐỌC BÁO THEO TỪ KHÓA</a>
      <button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="`lse" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <!--Phan Nav bar ben tay trai-->
      <div class="collapse navbar-collapse" id="navbarResponsive">
        <ul class="navbar-nav navbar-sidenav" id="exampleAccordion">
          <li class="nav-item" data-toggle="tooltip" data-placement="right" title="Dashboard">
            <a class="nav-link" href="index.html">
              <i class="fa fa-fw fa-dashboard"></i>
              <span class="nav-link-text">Đọc báo</span>
            </a>
          </li>
          <li class="nav-item" data-toggle="tooltip" data-placement="right" title="Tables">
            <a class="nav-link" href="update_csdl.html">
              <i class="fa fa-fw fa-table"></i>
              <span class="nav-link-text">Bổ sung từ ghép và stopword</span>
            </a>
          </li>
          <li class="nav-item" data-toggle="tooltip" data-placement="right" title="Tables">
            <a class="nav-link" href="display_category.php">
              <i class="fa fa-fw fa-table"></i>
              <span class="nav-link-text">Phân mục cho từ khóa</span>
            </a>
          </li>
          <li class="nav-item" data-toggle="tooltip" data-placement="right" title="Tables">
            <a class="nav-link" href="about.html">
              <i class="fa fa-fw fa-table"></i>
              <span class="nav-link-text">Giới thiệu</span>
            </a>
          </li>
        </ul>
        <ul class="navbar-nav sidenav-toggler">
          <li class="nav-item">
            <a class="nav-link text-center" id="sidenavToggler">
              <i class="fa fa-fw fa-angle-left"></i>
            </a>
          </li>
        </ul>

        <ul class="navbar-nav ml-auto">
          <li class="nav-item">
          </li>
          <li class="nav-item">
          </li>
        </ul>
      </div>
    </nav>

    <div class="content-wrapper">
      <div class="container-fluid">
        
        <div class="card mb-3">  
          <div class="card-header">
            <a data-toggle="collapse" href="#search_card" aria-expanded="true" aria-controls="search_card">
              <i class="fa fa-bar-chart"></i>Phân mục từ khóa
              <i class="fa fa-angle-down rotate-icon"></i>
            </a>
            

          </div>
          <div class="card-body" id="search_card" class="collapse">
            <div class="card-title">
              <h5>Phân mục từ khóa</h5>
            </div>
            <div class="card-text">
              - Mỗi từ khóa có thể thuộc vào nhiều lĩnh vực: kinh tế, chính trị...</br>
              - Phân từ khóa vào các mục giúp hệ thống xác định lĩnh vực của từ khóa chính xác hơn
              <hr>
          
            <br>';
              echo ' <h5>Bước 1: chọn từ khóa để phân mục</h5>';
              $tag_string = "";

              $lines = file('./export/uncategorized_keyword.txt', FILE_IGNORE_NEW_LINES);
              foreach ($lines as $value) {
                $tag_string = '<a href="javascript:void(0)"><font size="3px">' . 
                '<span id="keyword" onclick="clickKeyword(this)">' . $value  . '</span></font></a>' . '   •   ';
                echo  $tag_string;
              }
              echo '<h5>Bước 2: chọn chuyên mục cho từ khóa và nhấn Phân chuyên mục khi hoàn tất</h5>';
              echo '<form action="update_category.php" method="POST" target="formDestination" >
                    <div class="form-group">
                    <input class="form-control" type="text" id="myInput" name="keyword" placeholder="Từ khóa cần phân loại">    
                    </div>
                    <div class="form-group">
                    <div class="container">

                      <div class="row">
                        <div class="col-md-3">
                          <input type="checkbox" name="chinh_tri" value="yes" id="chinh_tri"></input>
                          <label class="form-check-label" for="chinh_tri">Chính trị</label>
                        </div>
                         <div class="col-md-3">
                          <input type="checkbox" name="kinh_te" value="yes" id="kinh_te"></input>
                         <label class="form-check-label" for="kinh_te">Kinh tế</label>
                        </div>

                         <div class="col-md-3">
                          <input type="checkbox" name="van_hoa" value="yes">   Văn hóa </input>
                        </div>
                        <div class="col-md-3">
                          <input type="checkbox" name="xa_hoi" value="yes">   Xa hoi   </input>
                        </div>
                        

                      </div>
                      <div class="row">
                        <div class="col-md-3">
                            <input type="checkbox" name="giao_duc" value="yes">   Giao duc   </input>
                        </div>
                        <div class="col-md-3">
                            <input type="checkbox" name="the_thao" value="yes">   The thao   </input>
                        </div>
                        <div class="col-md-3">
                            <input type="checkbox" name="giai_tri" value="yes">   Giải trí   </input>
                        </div>
                        <div class="col-md-3">
                            <input type="checkbox" name="cong_nghe" value="yes">   Khoa hoc Cong nghe   </input>
                        </div>
                      </div>

                      <div class="row">
                        <div class="col-md-3">
                              <input type="checkbox" name="an_ninh" value="yes">   An ninh   </input>
                        </div>
                        <div class="col-md-3">
                              <input type="checkbox" name="quoc_phong" value="yes">   Quoc phong   </input>
                        </div>
                        <div class="col-md-3">
                              <input type="checkbox" name="suc_khoe" value="yes">   Suc khoe   </input>
                        </div>
                        <div class="col-md-3">
                              <input type="checkbox" name="doi_song" value="yes">   Doi song   </input>
                        </div>
                      </div>

                      <div class="row">
                        <div class="col-md-3">
                              <input type="checkbox" name="giao_thong" value="yes">   Giao thong   </input>
                        </div>
                        <div class="col-md-3">
                              <input type="checkbox" name="moi_truong" value="yes">   Moi truong   </input>
                        </div>
                        <div class="col-md-3">
                              <input type="checkbox" name="quoc_gia" value="yes">   Quoc gia   </input>
                        </div>
                        <div class="col-md-3">
                              <input type="checkbox" name="dia_phuong" value="yes">   Dia phuong   </input>
                        </div>
                      </div>

                      <div class="row">
                        <div class="col-md-3">
                              <input type="checkbox" name="su_kien" value="yes">   Su kien   </input>
                        </div>
                        <div class="col-md-3">
                              <input type="checkbox" name="nhan_vat" value="yes">   Nhan vat   </input>
                        </div>
                        <div class="col-md-3">
                              <input type="checkbox" name="dia_danh" value="yes">   Dia danh   </input>
                        </div>
                        <div class="col-md-3">
                              <input type="checkbox" name="tac_pham" value="yes">   Tac pham   </input>
                        </div>
                      </div>

                      </div>
                    <div class="form-group">
                        <input class="btn btn-primary" type="submit" name="Update" value="Phân chuyên mục">
                    </div>
                    </div>

                   </form>';
                 echo '<iframe width="100%" name="formDestination" frameborder="0" >           </iframe>
                </form>
              </div>
          </div>
        </div>';
echo '
      <!-- /.container-fluid-->
      <!-- /.content-wrapper-->
      <footer class="sticky-footer">
        <div class="container">
          <div class="text-center">
            <small>Copyright © Đặng Hải Lộc 2018</small>
          </div>
        </div>
      </footer>
      <!-- Scroll to Top Button-->
      <a class="scroll-to-top rounded" href="#page-top">
        <i class="fa fa-angle-up"></i>
      </a>
      <!-- Logout Modal-->
      <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="exampleModalLabel">Ready to Leave?</h5>
              <button class="close" type="button" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">×</span>
              </button>
            </div>
            <div class="modal-body">Select "Logout" below if you are ready to end your current session.</div>
            <div class="modal-footer">
              <button class="btn btn-secondary" type="button" data-dismiss="modal">Cancel</button>
              <a class="btn btn-primary" href="login.html">Logout</a>
            </div>
          </div>
        </div>
      </div>
    

    <script src="vendor/jquery/jquery.min.js"></script>
    <script src="vendor/bootstrap/js/bootstrap.bundle.min.js"></script>
    <!-- Custom scripts for all pages-->
    <script src="js/sb-admin.min.js"></script>
    </div>
  </div>
</body>

</html>';

?>
