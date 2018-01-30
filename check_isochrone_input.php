<!DOCTYPE html>
 
<html lang="en">


    <style>
 
   html{background: #61210B }
.wrap {
width: 100&#37;;
height: 600px; /* optional */
background: #FFFFFF; /* optional */
font-family: 'times new roman', arial, sans-serif;
font-size: 1em;
color: #FFFFFF;
}
    .nav2 {clear: both; margin: 0px; background-color: #FFFFFF;padding: 0px; font-family: verdana, arial, sans serif; font-size: 1.0em;}
.nav2 ul {float: left; width: 770px; margin: 0px; padding: 0px; border-top: solid 1px rgb(54,83,151); border-bottom: solid 1px rgb(54,83,151); background-color: rgb(127,162,202); font-weight: bold;}  
.nav2 li {display: inline; list-style: none; margin: 0px; padding: 0px;}
.nav2 li a {display: block; float: left; margin: 0px 0px 0px 0px; padding: 5px 10px 5px 10px; border-right: solid 1px rgb(54,83,151); color: rgb(255,255,255); text-transform: uppercase; text-decoration: none; font-size: 100%;}
.nav2 a:hover, .nav2 a.selected {color: rgb(50,50,50); text-decoration: none;}
.buffer {clear: both; width: 730px; height: 0px; margin: 20px; padding: 20px; background-color: rgb(255,255,255);}
.content1-pagetitle {overflow: hidden; width: 750px; margin: 0px 0px 0px 0px; padding: 0px 0px 2px 0px; border-bottom: solid 3px rgb(88,144,168);); background-color: #FFFFFF;font-weight: bold; font-size: 180%;}


.page-container-3 {width: 770px;margin: 0px auto; padding: 0px; background-color: url('crimson-background.gif'); border: solid 1px rgb(0,0,250);}

  .style16 {
    margin-left: 40px;
    font-size: medium;
}
body {font-size: 90%; width: 800px;margin: 0px auto; padding: 20px; background-color: rgb(255,255,255); font-family: arial, sans-serif;min-height: 500px;}


.content3 {float: left; width: 800px; min-height: 500px; background-color: #FFFFFF; margin: 0px; padding: 0px 0px 2px 0px; color: rgb(0,0,0); font-size: 1.0em;}

.site-name {
    width: 300px;
    height: 45px;
    top: 12px;
    position: absolute;
    z-index: 4;
    overflow: hidden;
    margin: 0px;
    padding-left: 0px;
   background-image: url('crimson-background.gif');
}








a:link {
    color: blue;
    background-color: transparent;
    text-decoration: none;
}
a:visited {
    color: blue;
    background-color: transparent;
    text-decoration: none;
}
a:hover {
    color: black;
    background-color: transparent;
    text-decoration: underline;
}
a:active {
    color: yellow;
    background-color: transparent;
    text-decoration: underline;
}
</style>
    <head>

    <title>Input Check</title>

<div class="style16">
        <meta charset="utf-8" />


    
         
    </head>
    

    <body>
  


    <table border="0" cellpadding="10">
      <tr>
        <td>
          

<img src="bama.jpg">
  


<?php
session_start();

function goBack() {
    window.history.back();
}

function html_form(){

    ?> <html> <body> <form enctype="multipart/form-data" action="results_isochrone.php" method="POST">
Based on the number of modes selected and number of location pairs in your file, <br><br> You will not be able to fully run this file.<br><br> If you choose to continue, we will run as many as we can and then return those results. <br><br> Otherwise, please go back and add more keys or run with less modes.<br><br>
    <input type="submit" value="Click to Run" />

</form>
<br><br>
    <button onclick="history.back();return false">Click to return to previous page</button>

</form>   
    </body>
</html>
<?php
}

date_default_timezone_set("America/Chicago");

    $_SESSION['Got_key_count'] = 0;
    $_SESSION['time_stretch'] = 0;
    
    $_SESSION['API_KEYs1'] = $_POST['API_KEY1'];
    $_SESSION['API_KEYs2'] = $_POST['API_KEY2'];
    $_SESSION['API_KEYs3'] = $_POST['API_KEY3'];
    $_SESSION['API_KEYs4'] = $_POST['API_KEY4'];
    $_SESSION['API_KEYs5'] = $_POST['API_KEY5'];

$_SESSION['first'] = $_POST['first'];
$_SESSION['second'] = $_POST['second'];
$_SESSION['third'] = $_POST['third'];
$_SESSION['fourth'] = $_POST['fourth'];
$_SESSION['istime'] = $_POST['time'];
$_SESSION['isdist'] = $_POST['dist'];
$_SESSION['distvalue'] = $_POST['dist_value'];
$_SESSION['timevalue'] = $_POST['Time_value'];
$_SESSION['isochronepoints'] = $_POST['points'];
   #print "MODES:";
   #   print $_SESSION['Mode1'];   
    #  print $_SESSION['Mode2'];
    #  print $_SESSION['Mode3'];
    #  print $_SESSION['Mode4'];
$_SESSION['Mode1'] = $_POST['Driving'];
$_SESSION['Mode2'] = $_POST['Walking'];
$_SESSION['Mode3'] = $_POST['Bicycling'];
$_SESSION['Mode4'] = $_POST['Transit'];

#print "TIMES:";
#print $_SESSION['Start_Time'];
#print "ENDTIMES:";

#print $_SESSION['End_Time'];

if($_SESSION['API_KEYs1']==""){
   echo "An API key must be present in the first entry at least. Please Try again.";
}
if($_SESSION['API_KEYs2']==""){
$_SESSION['Filler2'] = "0";
}
else{
    $_SESSION['Filler2'] = $_POST['API_KEY2'];
}
if($_SESSION['API_KEYs3']==""){
$_SESSION['Filler3'] = "0";
}
else{
    $_SESSION['Filler3'] = $_POST['API_KEY3'];
}
if($_SESSION['API_KEYs4']==""){
$_SESSION['Filler4'] = "0";
}
else{
    $_SESSION['Filler4'] = $_POST['API_KEY4'];
}
if($_SESSION['API_KEYs5']==""){
$_SESSION['Filler5'] = "0";
}
else{
    $_SESSION['Filler5'] = $_POST['API_KEY5'];
}
   # $_SESSION['uploaddir'] = __DIR__;
if($_FILES['userfile']['name'] == ""){
    echo "No File was provided. Please try again.";
    exit;
}
    $_SESSION['uploadfile'] =  __DIR__ . '/uploads_isochrone/' . basename($_FILES['userfile']['name']);
    $filename = $_FILES['userfile']['name'];
  
$_SESSION['linecount'] = 0;
$_SESSION['original'] = $_FILES['userfile']['name'];
$_SESSION['temp'] = $_FILES['userfile']['tmp_name'];
$_SESSION['name']='out_'.date('m-d_hisa').'.csv';
move_uploaded_file($_FILES['userfile']['tmp_name'], $_SESSION['uploadfile']);

$handle = fopen($_SESSION['uploadfile'], "r");

   while(!feof($handle)){
  $_SESSION['line'] = fgets($handle);
  $_SESSION['linecount'] += 1;
}
fclose($handle);
if($_SESSION['Filler2'] == "0" and $_SESSION['Got_key_count'] == 0){
    if($_SESSION['linecount'] > 2500){
        $_SESSION['Got_key_count'] = 1;
        $_SESSION['original'] = $_FILES['userfile']['name'];
        $_SESSION['temp'] = $_FILES['userfile']['tmp_name'];
        $_SESSION['name']='out_'.date('m-d_hisa').'.csv';
        move_uploaded_file($_FILES['userfile']['tmp_name'], $_SESSION['uploadfile']);

        html_form();
        exit;
    }
}
if($_SESSION['Filler3'] == "0"){
    if( $_SESSION['linecount'] > 5000){
        $_SESSION['Got_key_count'] = 1;
        $_SESSION['original'] = $_FILES['userfile']['name'];
        $_SESSION['temp'] = $_FILES['userfile']['tmp_name'];
        $_SESSION['name']='out_'.date('m-d_hisa').'.csv';
        move_uploaded_file($_FILES['userfile']['tmp_name'], $_SESSION['uploadfile']);

        html_form();
        exit;
    }
}
if($_SESSION['Filler4'] == "0" and $_SESSION['Got_key_count'] == 0){
    if($_SESSION['linecount'] > 7500){
        $_SESSION['Got_key_count'] = 1;
        $_SESSION['original'] = $_FILES['userfile']['name'];
        $_SESSION['name']='out_'.date('m-d_hisa').'.csv';
        move_uploaded_file($_FILES['userfile']['tmp_name'], $_SESSION['uploadfile']);

        html_form();
        exit;
    }
}
if($_SESSION['Filler5'] == "0" and $_SESSION['Got_key_count'] == 0){
    if($_SESSION['linecount'] > 10000){
        $_SESSION['Got_key_count'] = 1;
        $_SESSION['original'] = $_FILES['userfile']['name'];
        $_SESSION['temp'] = $_FILES['userfile']['tmp_name'];
        $_SESSION['name']='out_'.date('m-d_hisa').'.csv';
        move_uploaded_file($_FILES['userfile']['tmp_name'], $_SESSION['uploadfile']);

        html_form();
        exit;
    }
}
if($_SESSION['Filler5'] != "0" and $_SESSION['Got_key_count'] == 0){
    if($_SESSION['linecount'] > 12500){
        $_SESSION['Got_key_count'] = 1;
        $_SESSION['temp'] = $_FILES['userfile']['tmp_name'];
        $_SESSION['original'] = $_FILES['userfile']['name'];
        $_SESSION['name']='out_'.date('m-d_hisa').'.csv';
        move_uploaded_file($_FILES['userfile']['tmp_name'], $_SESSION['uploadfile']);

        html_form();
        exit;
    }
}
else{
$_SESSION['original'] = $_FILES['userfile']['name'];
$_SESSION['temp'] = $_FILES['userfile']['tmp_name'];

 $_SESSION['name']='out_'.date('m-d_hisa').'.csv';
move_uploaded_file($_FILES['userfile']['tmp_name'], $_SESSION['uploadfile']);
$name = $_SESSION['name'];
$API_KEYs1 = $_SESSION['API_KEYs1'];
$Filler2 = $_SESSION['Filler2'];
$Filler3 = $_SESSION['Filler3'];
$Filler4 = $_SESSION['Filler4'];
$Filler5 = $_SESSION['Filler5'];
$first = $_SESSION['first'];
$second = $_SESSION['second'];
$linecount = $_SESSION['linecount'];
$third = $_SESSION['third'];
$fourth = $_SESSION['fourth'];
$Mode1 = $_SESSION['Mode1'];
$Mode2 = $_SESSION['Mode2'];
$Mode3 = $_SESSION['Mode3'];
$Mode4 = $_SESSION['Mode4'];
$istime = $_SESSION['istime'];
$isdist = $_SESSION['isdist'];
$goaltime = $_SESSION['timevalue'];
$goaldist = $_SESSION['distvalue'];
$numberofpoints = $_SESSION['isochronepoints'];


if ($goaltime != "0"){
    $goaltimedist = $goaltime;
}
else{
    $goaltimedist = $goaldist;
}
if ($istime != "on"){
    $istime = "off";
    $goaltimedist = $goaldist;
}
$my_file = 'gmaps_isochrone_log.txt';
$ipaddress = $_SERVER['REMOTE_ADDR'];
$handle = fopen($my_file, 'a') or die('Cannot open file:  '.$my_file);
$data = "\n|| NEW Query: IPAddress: $ipaddress OutputFilename: $name. Input Filename: $filename. InputFileLength: $linecount. Keys Provided: $API_KEYs1, $Filler2, $Filler3, $Filler4, $Filler5. Modes Selected: $Mode1, $Mode2, $Mode3, $Mode4. Transit Preferences Selected: $first, $second, $third, $fourth. Is Time? $istime. Is Dist? $isdist. GoalTime: $goaltime. GoalDist: $goaldist. numberofpoints: $numberofpoints.";
fwrite($handle, $data);

$string = 'python multithreaded.py "uploads_isochrone' . "\\" . "$filename" . '"' . " output_isochrone" . '\\' . "$name -off $API_KEYs1 $Filler2 $Filler3 $Filler4 $Filler5 $Mode1 $Mode2 $Mode3 $Mode4 $first $second $third $fourth $istime $goaltimedist $numberofpoints 2>&1";

passthru($string);
#echo $string;
#print "python real_schedule_explorer.py uploads_transit/$filename output_transit/$name -off $API_KEYs1 $Filler2 $Filler3 $Filler4 $Filler5 $first $second $third $fourth 2>&1";

 #if ($_SESSION['return_var==0) {
      echo "File is valid, and was successfully uploaded.\n";
  #  } else {
    #   echo "Something went wrong. See error above.\n\n\n\n\n";
   # }
     echo"<br><br><br><br>";
#if($_SESSION['return_var==0){
    ?><html><body><a href="output_isochrone/<?php echo $_SESSION['name'];?>" download="<?php echo $_SESSION['name'];?>">Download The Summary File Here</a>
</body><?php
}

#}
#else{
#    echo "Please try again.";
#}


?>

