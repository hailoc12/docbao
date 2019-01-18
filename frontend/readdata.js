

var docbao =  angular.module('docbaoApp', []);
var on_same_page = false;
docbao.controller('logCtrl', function($scope, $http)
{
    $http.get('/export/log_data.json').then(function (response)
    {
        $scope.log = response.data; //success callback
    }
    , function (data){
        console.log("Khong doc duoc file log_data.json");
    }    //fail callback
    );

   $http.get('/export/keyword_dict.json').then(function (response)
    {
        draw_category_table(response.data.data);
    }
    , function (data){
        console.log("Khong doc duoc file keyword_dict.json");
    }    //fail callback
    );

   $http.get('/export/trending_keyword.json').then(function (response)
    {
        var data = response.data;
        draw_hot_keyword_barchart(data);
        
    }
    , function (data){
        console.log("Khong doc duoc file trending_keyword.json");
    }    //fail callback
    );
    $http.get('/export/new_keyword.json').then(function (response)
    {
        var data = response.data;
        draw_new_keyword_table(data);
    }
    , function (data){
        console.log("Khong doc duoc file new_keyword.json");
    }    //fail callback
    );
    $http.get('/export/fast_growing_keyword.json').then(function (response)
    {
        var data = response.data;
        draw_fast_growing_keyword_table(data);
    }
    , function (data){
        console.log("Khong doc duoc file fast_growing_keyword.json");
    }    //fail callback
    );
   $http.get('/export/article_data.json').then(function (response)
    {
        $scope.articles = response.data.article_list; //success callback
        draw_article_table(response.data.article_list);
        
        setup_auto_complete(response.data.article_list);
    }
    , function (data){
        console.log("Khong doc duoc file article_data.json");
    }    //fail callback
    );


    setTimeout(function() {
    var fType = decodeURI(getUrlVars()["keyword"]);
    if (fType != "undefined" && !on_same_page) _search_article_table(fType);
    },3000);

});

function draw_hot_keyword_barchart(hot_keyword_dict)
{
    // -- Bar Chart Example
console.log(hot_keyword_dict);
var ctx = document.getElementById("myBarChart");
var myLineChart = new Chart(ctx, {
  type: 'horizontalBar',
  data: {
    labels: Object.keys(hot_keyword_dict),
    datasets: [{
      label: "số bài báo chứa từ khóa này",
      backgroundColor: "rgba(2,117,216,1)",
      borderColor: "rgba(2,117,216,1)",
      data: Object.values(hot_keyword_dict),
    }],
  },
  options: {
    responsive:true,
    maintainAspectRatio:false,
    scales:{
	yAxis:[{
	  ticks:
		{
		  beginAtZero:true
		}
	}
	]
    },
    onClick: function(evt){
    var activeElement = myLineChart.getElementAtEvent(evt)[0]._index;
    var search_string = Object.keys(hot_keyword_dict)[activeElement];
    on_same_page = true;
    _search_article_table(search_string);
    
    },
  }
    });
}

function draw_article_table(article_list)
{
 
$(document).ready(function() {
	create_article_table(article_list);
   } );
}
function create_article_table(article_list)
{

    var dataset = article_list;
    $('#article_table').DataTable( {
        data: dataset,
        columns: [
            { title: "STT", data:"stt", "searchable": false, className: "min-desktop"},
            { title: "Tên bài", data:"topic", "searchable": true, className:"all"},
            { title: "Nguồn báo", data:"newspaper", "searchable": false, className:"min-desktop"},
            { title: "Cập nhật", data:"update_time", "searchable": false, className: "min-desktop" },
            { title: "Ngày xuất bản", data:"publish_time", "searchable": false, className: "min-desktop" },
        ],
        "rowCallback": function( row, data, index ) {
            topic = $('td:eq(1)', row).html();
            $('td:eq(1)', row).html('<a href="' + data.href + '" target="_blank">' + topic + '</a>');
          },
        responsive: true,
        columnDefs: [
            { responsivePriority: 1, targets: 1 },
            { responsivePriority: 2, targets: 2 }
        ],
        nowrap: true,
	"pageLength": 10,
    } );
 
}
function draw_new_keyword_table(new_keyword_list)
{
var data = new_keyword_list;
console.log(data);
$(document).ready(function() 
    {
        keyword_string = "";
        for(i=0; i< data.length; i++)
        {
           keyword_string = keyword_string + '<a href="#article_table" onclick ="search_article_table(this)">' + 
           data[i].keyword + '</a>' + '<sub>(' + data[i].count +
                     ')</sub>' + ' - ';
         }

                $("#new_keyword_row").html(keyword_string);

   }
             );
}

function draw_fast_growing_keyword_table(fast_growing_keyword_list)
{
var data = fast_growing_keyword_list;
console.log(data);
$(document).ready(function() 
    {
        keyword_string = "";
        for(i=0; i< data.length; i++)
        {
           keyword_string = keyword_string + '<a href="#article_table" onclick ="search_article_table(this)">' + 
           data[i].keyword + '</a>' + '<sub>(' + data[i].count +
                     ')</sub>' + ' - ';
         }

                $("#fast_growing_keyword_row").html(keyword_string);

   }
             );
}


function draw_category_table(category_list)
{
var dataset = category_list;
console.log(dataset);
$(document).ready(function() 
    {
        $('#category_table').DataTable( {
            data: dataset,
            columns: [
                { title: "Chuyên mục", data:"category"},
                { title: "Keyword", data:"keywords"},

            ],
            "ordering": false,
            "autoWidth": false,
	    "pageLength": 50,
            "rowCallback": function( row, data, index ) {
                topic = $('td:eq(1)', row).html();
                keyword_string = "";
                console.log(data);
                for(i=0; i< data.keywords.length; i++)
                {
                    keyword_string = keyword_string + '<a href="#article_table" onclick ="search_article_table(this)">' + 
                    data.keywords[i].keyword + '</a>' + '<sub>(' + data.keywords[i].count +
                     ')</sub>' + ' - ';
                }

                $('td:eq(1)', row).html(keyword_string);
              },
        } );
    } );
}

function _search_article_table(search_string)
{
    if(confirm("Đọc các bài báo có chứa từ khóa: " + search_string))
        {
	
	table = $('#article_table').DataTable();
	
	addKeywordToUrl(search_string);
	search_string = '"' + search_string + '"';	
        table.search(search_string).draw();

        $('html, body').animate({
          scrollTop: $("#article_table").offset().top
        }, 900);
    }
}

function search_article_table(keyword)
{
    search_string =  keyword.text ;
    on_same_page = true;
    _search_article_table(search_string);
}

function keyup_on_keyword_search_text(event)
{
    if (event.keyCode === 13) {
        search_keyword();
    }
}

function search_keyword()
{
    on_same_page = true;
    _search_article_table($("#keyword_search_text").val());
}

function go_to_search_card()
{
    $('html, body').animate({
      scrollTop: $("#search_card").offset().top
    }, 900);
}

function setup_auto_complete(article_list)
{
    var states = [];
    var max_item = 2000;
    var isMobile = window.matchMedia("only screen and (max-width:480px)");
    if(isMobile)
	{
		max_item = 500;
	}	
    console.log("Max autocomplete items: ")
    console.log(max_item)

    if(max_item > article_list.length)
	{
		max_item = article_list.length;
	}
    for(var i=0; i < max_item; i++)
    {
        states.push({"title":article_list[i].topic + " (" + article_list[i].newspaper + ")", "value": article_list[i].topic});
    }
  $("#keyword_search_text").autocomplete({
    source:[states],
    visibleLimit: 10,
    autoselect: false
    });
}
function addKeywordToUrl(keyword)
{
	var url = window.location.href.split('?')[0];
	window.history.replaceState({page:"another"}, keyword, url + "?keyword=" + encodeURI(keyword));
}
function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi,    
    function(m,key,value) {
      vars[key] = value;
    });
    return vars;
  }

