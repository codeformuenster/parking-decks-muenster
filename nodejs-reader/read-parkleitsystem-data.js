var request = require('request');
var cheerio = require('cheerio');
var fs = require('fs');

request("https://www.stadt-muenster.de/tiefbauamt/parkleitsystem", function(error, response, body) {
  if(error) {
    console.log("Error: " + error);
  }
  console.log("Status code: " + response.statusCode);

  var $ = cheerio.load(body);
  /*

  <tr>
  <td class="name area1">
      <a onclick="self.open(this.href, '', 'width=550,height=630,toolbar=0'); return false;" class="parkingLink marker1" href="tiefbauamt/parkleitsystem/parkhaeuser/detailansicht/parkhaus/1.html">
          PH Theater
      </a>
  </td>
  <td class="freeCount">664</td>
  
          <td class="status free">frei</td>
      
</tr>
*/
  var results = $('div#parkingList tr');
  console.log("Found results:", results.length);
  
  var d = new Date();
  var datestring = d.getFullYear() + "-" + ("0"+(d.getMonth()+1)).slice(-2) + "-" + + ("0" + d.getDate()).slice(-2);
  var timestring = ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2);

  results.each(function( index ) {
    var title = $(this).find('td.name a').text().trim();
    var score = $(this).find('td.freeCount').text().trim();
    var status = $(this).find('td.status').text().trim();
    console.log("Title: " + title);
    console.log("Score: " + score);
    console.log("Status: " + status);
    fs.appendFileSync('parkleitdata-' + datestring + '.csv',datestring + " " + timestring +'\t' + title + '\t' + score + '\t' + status + '\n');
  });

});
