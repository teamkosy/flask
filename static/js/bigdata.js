function drawImage1() {
    var found = null;
    var sel = document.getElementById("data1");
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

function drawImage2() {
    var found = null;
    var sel = document.getElementById("data2");
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

function drawImage3() {
    var found = null;
    var sel = document.getElementById("data3");
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