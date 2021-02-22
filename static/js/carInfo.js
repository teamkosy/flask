function drawImage() {
    var found = null;
    var sel = document.getElementById("carInfo");
    var img = document.getElementById("dataimage");
for(var i=0; i<sel.length; i++)
{
    if(sel[i].selected == true)
    {
        found = sel[i];
        break;
    }
}
img.src = found.value;
}