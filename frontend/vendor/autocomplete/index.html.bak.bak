<!DOCTYPE html>
<html lang="ru">
<head>
<!--<base href="" /><!-- -->
<meta http-equiv="content-type" content="text/html; charset=utf-8"/>
<title>jQuery Automplite Plugin</title>
<link rel="stylesheet" href="./demo/prettify.css">
<link href='http://fonts.googleapis.com/css?family=Cinzel+Decorative:400,700,900' rel='stylesheet' type='text/css'>
<link href='http://fonts.googleapis.com/css?family=Dosis:200,300,400,500,600,700,800|Roboto+Slab:400,300,700,100' rel='stylesheet' type='text/css'>
<link href='http://fonts.googleapis.com/css?family=Roboto:400,100,100italic,300,300italic,400italic,500,500italic,700,700italic,900,900italic|Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800' rel='stylesheet' type='text/css'>
</head>
<body>
<div class="container-fluid">
	<nav class="navbar navbar-default navbar-fixed-top" role="navigation">
	  <div class="container">
		<div class="auto">
			<ul class="nav navbar-nav">
				<li><a href="/">XDsoft.net</a></li>
				<li class="active"><a href="http://xdsoft.net/jqplugins/autocomplete/">Autocomplete</a></li>
				<li><a href="http://xdsoft.net/jqplugins/datetimepicker/">DateTimePicker</a></li>
				<li><a href="http://xdsoft.net/jqplugins/range2dslider/">Range2DSlider</a></li>
			</ul>
			<form class="navbar-form navbar-right">
				<a class="btn btn-info" href="https://github.com/xdan/autocomplete/">Source</a>
				<a class="btn btn-success" href="https://github.com/xdan/autocomplete/archive/master.zip">Download</a>
			</form>
		</div>
	  </div>
	</nav>
	<div class="auto" style="margin-top:100px">
		<h1 class="text-center">Autocomplete like Google <small>jQuery Plugin</small></h1>
		<p class="desc">JQuery Autocomplete plugin is a lightweight simple and easy in settings autocomplete like Google. Accents support</p>
		<p class="text-center">
			<a id="local" class="btn btn-link" href="#local">Local</a>
			<a class="btn btn-link" href="#remote">Remote</a>
		</p>
		<div class="form-group" style="margin:20px 0px;">
			<input type="text" class="form-control" id="auto1" placeholder="enter state">
		</div>
		<h2>How to use autocomplete?</h2>
		<h3>Insert code</h2>
		<p>add this code after &lt;/body&gt; in your document.</p>
		<pre class="prettyprint linenums">&lt;link type="text/css" rel="stylesheet" href="autocomplete.css" /&gt;                  
&lt;script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"&gt;&lt;/script&gt;
&lt;script src="autocomplete.js"&gt;&lt;/script&gt;</pre>
				<h3>Add data for autocomplete</h2>
<pre class="prettyprint linenums">&lt;script type="text/javascript"&gt;
var states = [
	'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
	'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii',
	'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
	'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
	'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
	'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota',
	'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
	'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
	'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
];
&lt;/script&gt;</pre>
		<h3>Init autocomplete plugin</h2>
		<pre class="prettyprint linenums">&lt;script type="text/javascript"&gt;
$(function() {
	$("input").autocomplete({
		source:[states]
	}); 
});
&lt;/script&gt;</pre>


		<h2 id="remote">Autocomplete from remote data</h2>
		<div class="input-group" style="margin:20px 0px;">
			<input type="text" class="form-control" id="remote_input" placeholder="Enter movie">
			<span class="input-group-btn">
				<button id="open" class="btn btn-default" type="button"><span class="caret"></span></button>
			</span>
		</div>
		<h3>Ajax</h2>
		<p>use ajax for getting data from server</p>
		<pre class="prettyprint linenums">&lt;script&gt;
$('#remote_input').autocomplete({
	valueKey:'title',
	source:[{
		url:"/test.php?query=%QUERY%",
		type:'remote',
		getValue:function(item){
			return item.title
		},
		ajax:{
			dataType : 'jsonp'
		}
	}]
});
$('button#open').click(function(){
	$('#remote_input').trigger('updateContent open');
	$('#remote_input').focus();
});
&lt;/script&gt;</pre>
		<h2>Set source after init</h2>
		<div class="form-group" style="margin:20px 0px;">
			<input type="text" class="form-control" id="combine" placeholder="Enter movie or state or digit">
		</div>
		<p>Plugin has some methods for manipulate it</p>
		<pre class="prettyprint linenums">$('#combine').autocomplete();

$('#combine')
	.autocomplete('setSource',{
		{
			valueKey:'title',
			url:"",
			type:'remote',
			getValue:function(item){
				return item.title
			},
			ajax:{
				dataType : 'jsonp'
			}
		},
		[],
		[]
	});
	
$('#combine')
	.autocomplete('setSource',states,1)
	.autocomplete('setSource',['one','two','three','for','five','six','seven','eight','nine','zero'],2);
	
var first = $('#combine')
	.autocomplete('getSource',0);
first.url = "/test.php?query=%QUERY%&amp;test=1",

</pre>
	</div>
</div>
<p class="text-center">
	<a id="local" class="btn btn-link" href="http://xdsoft.net/jqplugins/autocomplete">Documentation</a>
	<a id="local" class="btn btn-link" href="#local">Local</a>
	<a class="btn btn-link" href="#remote">Remote</a>
</p><!--
<input id="select_course">
<input id="select_unit">
<br>
<br>
<br>
<br>
<br>
<br>
<br>--></br>
</body>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css">
<link rel="stylesheet" href="./demo/demo.css">
<script src="./demo/jquery.js" type="text/javascript"></script>
<script src="./demo/prettify.js" type="text/javascript"></script>
<script type="text/javascript">
window.prettyPrint && prettyPrint()
</script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
<link rel="stylesheet" href="jquery.autocomplete.css">
<script src="jquery.autocomplete.js" type="text/javascript"></script>
<script>

/********************************** local start ************************************************/
var states = [
	'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
	'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii',
	'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
	'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
	'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
	'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota',
	'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
	'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
	'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
];

$('#auto1').autocomplete({
	source:[states]
});
/*********************************** local end *****************************************************/


/*********************************** remote start *****************************************************/
$('#remote_input').autocomplete({
valueKey:'title',
source:[{
	url:"http://xdsoft.net/jquery-plugins/?task=demodata&s=%QUERY%",
	type:'remote',
	getValueFromItem:function(item){
		return item.title
	},
	ajax:{
		dataType : 'jsonp'	
	}
}]});

$('#open').click(function(){
	$('#remote_input').trigger('updateContent.xdsoft');
	$('#remote_input').trigger('open.xdsoft');
	$('#remote_input').focus();
});
/*********************************** remote end *****************************************************/

$('#auto2').autocomplete({
	source:[{
		data:states,
		preparse:function(items,query,sourse){
			for(i in items)
				items[i]=items[i].replace('a','b');
			return items;
		},
		filter:function(items,query){
			var res = [];
			for(i in items){
				if( items[i]==query )
					res.push(items[i]);
			}
			return res;
		}
	}]
});


$('#combine').autocomplete();

$('#combine')
	.autocomplete('setSource',[
		{
			valueKey:'title',
			url:"",
			type:'remote',
			getValue:function(item){
				return item.title
			},
			ajax:{
				dataType : 'jsonp'
			}
		},
		[],
		[]
	]);
	
$('#combine')
	.autocomplete('setSource',states,1)
	.autocomplete('setSource',['one','two','three','for','five','six','seven','eight','nine','zero'],2);
	
var first = $('#combine')
	.autocomplete('getSource',0);
first.url = "http://xdsoft.net/jquery-plugins/?task=demodata&s=%QUERY%";
/*
var states1 = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California']
var states2 = ['Colorado', 'Connecticut']
$("#select_course").autocomplete({source:[states1], visibleHeight:200});
$("#select_unit").autocomplete({source:[states1]});
$('#select_course').on('selected.xdsoft', function(event, item){
$("#select_unit").autocomplete('setSource',states2,0); 
});*/
</script>
</html>
