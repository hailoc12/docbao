<?php
// Display all error
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Use UTF-8
mb_internal_encoding("UTF-8");
// Set timezone
$timezone = 'Asia/Ho_Chi_Minh';  // +2 hours 

function mb_trim($string, $charlist = null) 
{
	if (is_null($charlist)) 
	{
		return trim($string);
	} 
	else 
	{
		$charlist = preg_quote($charlist, '/');
		return preg_replace("/(^[$charlist]+)|([$charlist]+$)/us", '', $string);
	}
}
// Get request data
$draw = intval(isset($_GET['draw']) ? $_GET['draw']:0);
$search = isset($_GET['search']) ? $_GET['search']: '';
$start = intval(isset($_GET['start'])?$_GET['start']:0);
$length = intval(isset($_GET['length'])?$_GET['length']:50);

#$search = mb_convert_encoding($search['value'], 'HTML-ENTITIES', "UTF-8");
$search = mb_trim(mb_strtolower($search['value']));

// Ordering  

$order = isset($_GET['order'])?$_GET['order'][0]: array('column'=>0,'dir'=>'asc');
$order_index = intval($order['column']);
$order_direction = $order['dir'];

# default sort on publish date  
if (empty($search) or empty($order_index)){
	$order_index=4;
	$order_direction="desc";
}

if($order_index==0)
{
	$column_name = 'stt';
}
else if($order_index==1)
{
	$column_name = 'topic';
}
else if($order_index==2)
{
	$column_name = 'newspaper';
}
else if($order_index==3)
{
	$column_name = 'created_date';
}

else
{
	$column_name = 'publish_date';
}



//
// Build query string  
//

$term = $search;

if(empty($term))
{
$param = '
{
  "query": 
  {
    "match_all":
    {
    }
  },
  "from": "'.$start.'", "size": "'.$length.'",
  "_source":{
       "includes": ["topic", "newspaper", "href", "publish_date", "created_date"]
		 },
  "sort": [{"'.$column_name.'":"'.$order_direction.'"}]
}
	';

}
else 
{
$param = '
{
  "query": 
  {
    "match_phrase":
    {
      "topic":'.'"'.$term.'" 
    }
  },
  "from": "'.$start.'", "size": "'.$length.'",
  "_source":{
       "includes": ["topic", "newspaper", "href", "publish_date", "created_date"]
	         },
  "sort": [{"'.$column_name.'":"'.$order_direction.'"}]
}
	';

}

$header = array(
	    "content-type: application/json; charset=UTF-8"
		);

$curl = curl_init();
curl_setopt($curl, CURLOPT_URL, "http://hailocworkstation.ddns.net:21/docbao_pvn/_search");
curl_setopt($curl, CURLOPT_HTTPHEADER, $header);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($curl, CURLOPT_POSTFIELDS, $param);

$es_result = curl_exec($curl);
curl_close($curl);

// Convert result to UTF-8 article data
$es_result = json_decode($es_result, true);

$database_size = $es_result['hits']['total'];

if ($database_size >10000) # elasticsearch limit from+size <= 10000 to avoid deep pagination  
{
	$database_size = 10000;
}

$es_result_json = $es_result['hits']['hits'];

$article_data = array();
$stt = $start;

date_default_timezone_set($timezone);
$current_time = time();

foreach($es_result_json as $key => $value)
{
	# process each article 
	$item = $value['_source'];
	$item["stt"] = $stt;

	$item_date = date_create($item['publish_date'], new DateTimeZone("Asia/Ho_Chi_Minh"));
	date_timezone_set($item_date, new DateTimeZone($timezone));

	#echo $item_date;
	
	$item["publish_date"]= date_format($item_date, 'd/m/y H:i');

	$difference = intval(($current_time -  date_timestamp_get(date_create($item['created_date'], new DateTimeZone("Asia/Ho_Chi_Minh"))))/60);

	if ($difference < 60)
	{
		$item["created_date"]= $difference." phút trước";
	}
	else if($difference < 720)
	{
		$item["created_date"]= intval($difference/60)." giờ trước";
	}
	else
	{
		$item["created_date"]= intval($difference/1440)." ngày trước";
	}
	
	

	array_push($article_data, $item);
	$stt++;
}

// Filter first
/*
if($search !== '')
{
	$filtered_data = array();
	foreach($article_data as $key=>$value)
	{
		$topic = mb_strtolower($value['topic']);
		if(mb_strpos($topic, $search) !== false){
			array_push($filtered_data, $value);
		}
	}
}
else
{
	$filtered_data = $article_data;
}
 */
$filtered_data = $article_data;
$filtered_data_size = $database_size;
#$columns = array_column($filtered_data, $column_name);
#array_multisort($columns, $direction, $filtered_data);


// Pagination  
$data_size=$database_size;
$upper_bound = 0+count($article_data); # data is filtered by query

if($upper_bound > $filtered_data_size)
{
	$upper_bound = $filtered_data_size;
}

$output_data = array();

for($index=0; $index< $upper_bound; $index+=1)
{
	$value=$filtered_data[$index];

	array_push($output_data, array('stt'=>$value['stt'], 'topic'=>$value['topic'], 'newspaper'=>$value['newspaper'], 'update_time'=>$value['created_date'],'publish_time'=>$value['publish_date'], 'href'=>$value['href']));

};


// Output data
$result = array('draw' => $draw, 'recordsTotal' => $data_size, 'recordsFiltered' => $filtered_data_size,
	'data' => $output_data);

echo json_encode($result, JSON_UNESCAPED_UNICODE);

?>
