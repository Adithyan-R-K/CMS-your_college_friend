// auto increase row size of text area till a limit
textarea = document.querySelector("#text");
        textarea.addEventListener('input', autoResize, false);
      
        function autoResize() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
            this.style.height = this.scrollHeight - 'px';
            if(this.style.height = '84px')
                        return;
        }
        
// auto scroll to bottom of chat 
window.onload = function(e){ 
  var element = document.getElementById('bottom');
  element.scrollIntoView({ behavior: 'smooth' });
}




var counter = 1;
var auto_refresh = setInterval(
function () {
    var newcontent= 'Refresh nr:'+counter;
    $('#chat').html(newcontent);
    counter++;
}, 1000);