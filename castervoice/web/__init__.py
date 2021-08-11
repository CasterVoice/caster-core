from flask import Flask, Response, request

from castervoice.watcher import stream_recognitions

app = Flask(__package__)


@app.route('/events')
def index():
    if request.headers.get('accept') == 'text/event-stream':
        return Response(stream_recognitions(),
                        content_type='text/event-stream')
    return """
<!doctype html>
<title>Caster-Core Events</title>
<style>
  html {
    height: 10%
  }
  body,p {
    white-space: nowrap;
    margin: 0;
    padding: 0;
    text-align: left;
  }
  #data {
    text-align: center;
    #background-color: yellow;
    display: inline-block;
  }
  .hidden {
    display: none;
  }
  .entry {
    background: rgba(255,255,255,0.8);
    display: block;
    margin: 0px 6px;

    animation: signup-response 1s;
    animation-delay: 10.0s;
    -webkit-animation: signup-response 1s;
    -webkit-animation-delay: 10.0s;
  }

  @keyframes signup-response{
      from {opacity :1;}
      to {opacity :0;}
  }

  @-webkit-keyframes signup-response{
      from {opacity :1;}
      to {opacity :0;}
  }
</style>
<script src="http://code.jquery.com/jquery-latest.js"></script>
<script>
if (!!window.EventSource) {
  var source = new EventSource('/events');
  var logs = []
  var max_entries = 10
  source.onmessage = function(e) {
    $("#data").append('<p class="entry">' + e.data + '</p>');

    setTimeout(function(){$("#data").find(':first-child').remove()}, 11000);
  }
}
</script>
<div id="data"></div>
"""
