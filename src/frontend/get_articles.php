<?php
// Display all error
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
ini_set('memory_limit', -1);
error_reporting(E_ALL);
// Use UTF-8
mb_internal_encoding("UTF-8");

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

// Read data and convert to UTF-8 
$article_file = file_get_contents('./export/article_data.json');
$article_file = mb_convert_encoding($article_file, 'HTML-ENTITIES', "UTF-8");

$article_data = json_decode($article_file, true)['article_list'];

// Get request data
$draw = intval(isset($_GET['draw']) ? $_GET['draw']:0);
$search = isset($_GET['search']) ? $_GET['search']: '';

#$search = mb_convert_encoding($search['value'], 'HTML-ENTITIES', "UTF-8");
$search = mb_trim(mb_strtolower($search['value']));

// Filter first
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

// Ordering  

$order = isset($_GET['order'])?$_GET['order'][0]: array('column'=>0,'dir'=>'asc');
$order_index = intval($order['column']);
$order_direction = $order['dir'];

if($order_direction === 'asc')
{
	$direction = SORT_ASC;
}
else
{
	$direction = SORT_DESC;
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
	$column_name = 'update_time';
}

else
{
	$column_name = 'publish_time';
}

$columns = array_column($filtered_data, $column_name);
array_multisort($columns, $direction, $filtered_data);


// Pagination  
$data_size=count($article_data);
$filtered_data_size = count($filtered_data);
$start = intval(isset($_GET['start'])?$_GET['start']:0);
$length = intval(isset($_GET['length'])?$_GET['length']:50);
$upper_bound = $start+$length;

if($upper_bound > $filtered_data_size)
{
	$upper_bound = $filtered_data_size;
}

$output_data = array();

for($index=$start; $index< $upper_bound; $index+=1)
{
	$value=$filtered_data[$index];

	array_push($output_data, array('stt'=>$value['stt'], 'topic'=>$value['topic'], 'newspaper'=>$value['newspaper'], 'update_time'=>$value['update_time'],'publish_time'=>$value['publish_time'], 'href'=>$value['href'], 'sapo'=>$value['sapo'], 'feature_image'=>$value['feature_image'], 'id'=>$value['id']));

};


// Output data
$result = array('draw' => $draw, 'recordsTotal' => $data_size, 'recordsFiltered' => $filtered_data_size,
	'data' => $output_data);

echo json_encode($result, JSON_UNESCAPED_UNICODE);

?>
