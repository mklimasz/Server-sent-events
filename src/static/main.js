var tweetsSse = new EventSource('/api/stream');
var hashtags;
google.charts.load('current', {'packages':['corechart']});
tweetsSse.onmessage = function(event) {
    console.log(event);
    hashtags = JSON.parse(event.data);
    google.charts.setOnLoadCallback(drawChart);
};

function drawChart() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Hashtag');
    data.addColumn('number', 'Number of occurrences');
    hashtags.forEach(function(el) {
        data.addRow([el.tweet.tag, el.tweet.value])
    });
    var options = {
        title: 'Trending twitter programming hashtags!',
        width: 500,
        height: 500,
        is3D: true

    };
    var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}

function getHashtag(name) {
    if (name === undefined) {
        return;
    }
    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function() {
        if (httpRequest.readyState == 4 && httpRequest.status == 200) {
            var tweet = JSON.parse(httpRequest.responseText);
            var hashtagNode = document.getElementById('hashtag_search_result');
            while (hashtagNode.firstChild) {
                hashtagNode.removeChild(hashtagNode.firstChild);
            }
            var label = document.createElement('p');
            label.textContent = 'Tweet name: ' + tweet.tweet.tag + ' number of occurences: ' + tweet.tweet.value;
            hashtagNode.appendChild(label)
        }
    };
    httpRequest.open('GET', '/api/hashtag/name/' + name.value);
    httpRequest.send(null);
}

