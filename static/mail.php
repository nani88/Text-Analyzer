
<?php
 require_once "Mail.php";
 error_reporting(0);
 $from = "AiArtist Enquiry <mail@aiartist.io>";
 $to = "support@aiartist.io";
 $subject = $_POST['subject']; 
 $name = $_POST['userName']; 
 $email = $_POST['userEmail'];
 $msg = $_POST['content'];

 
 $host = "smtp.zoho.com";
 $port = "587";
 $username = "mail@aiartist.io";
 $password = "aiartist2017";

 $message = "Name : $name\nEmail : $email\nMessage : $msg";
 
 $headers = array ('From' => $from,
   'To' => $to,
   'Subject' => $subject);
$smtp = Mail::factory('smtp',
   array ('host' => $host,
     'port' => $port,
     'auth' => true,
     'username' => $username,
     'password' => $password));
 

 $mail = $smtp->send($to, $headers, $message);


 
 if (PEAR::isError($mail)) {
   echo '<div class="col-sm-12"><div style="border-color: red; border-width: 4px; background: transparent;" class="well text-center"><h3 class="contacttxt">Email sending failed. Please try again later.</h3></div></div>';
  } else {
   echo '<div class="col-sm-12"><div style="border-color: green; border-width: 4px; background: transparent;" class="well text-center"><h3 class="contacttxt">Mail sent <i style="color: green;" class="fa fa-check" aria-hidden="true"></i></h3><p>Thanks for contacting. We will get back to you soon.</p></div></div>';
  }
 ?>
