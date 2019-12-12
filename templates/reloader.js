var req;

function updateData()
{
   var now = new Date();
   const target = document.getElementById(element)
   url = target.innerHTML;

   try {
      req = new XMLHttpRequest();
   } catch (e) {
      try {
         req = new ActiveXObject("Msxml2.XMLHTTP");
      } catch (e) {
         try {
            req = new ActiveXObject("Microsoft.XMLHTTP");
         } catch (oc) {
            alert("No AJAX Support");
            return;
         }
      }
   }

   req.onreadystatechange = processReqChange;
   req.open("GET", url, true);
   req.send(null);
}

function processReqChange()
{
   // If req shows "complete"
   if (req.readyState == 4)
   {
      dataDiv = document.getElementById('time', 'temperature');

      // If "OK"
      if (req.status == 200)
      {
         // Set current data text
         dataDiv.innerHTML = req.responseText;

         // Start new timer (1 min)
         timeoutID = setTimeout('updateData()', 4000);
      }
      else
      {
         // Flag error
         dataDiv.innerHTML = '<p>There was a problem retrieving data: ' + req.statusText + '</p>';
      }
   }
}