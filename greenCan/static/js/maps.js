var map;
var markers = [];
var markersLayer = new L.LayerGroup();
var latitude = 40.7128;
var longitude = -74.0060; 
var yellowUrl = "/static/images/map-marker/1.svg",
    blueUrl = "/static/images/map-marker/2.svg",
    redUrl = "/static/images/map-marker/3.svg",
    greenUrl = "/static/images/map-marker/4.svg",
    purpleUrl = "/static/images/map-marker/5.svg",
    orangeUrl = "/static/images/map-marker/6.svg",
    tealUrl = "/static/images/map-marker/7.svg";

var yellowIcon = new L.icon({
        iconUrl: yellowUrl,
        iconSize: [32, 37],
        iconAnchor: [16, 37]
    }),
    blueIcon = new L.icon({
        iconUrl: blueUrl,
        iconSize: [32, 37],
        iconAnchor: [16, 37]
    }),
    redIcon = new L.icon({
        iconUrl: redUrl,
        iconSize: [32, 37],
        iconAnchor: [16, 37]
    }),
    greenIcon = new L.icon({
        iconUrl: greenUrl,
        iconSize: [32, 37],
        iconAnchor: [16, 37]
    }),
    purpleIcon = new L.icon({
        iconUrl: purpleUrl,
        iconSize: [32, 37],
        iconAnchor: [16, 37]
    }),
    orangeIcon = new L.icon({
        iconUrl: orangeUrl,
        iconSize: [32, 37],
        iconAnchor: [16, 37]
    }),
    tealIcon = new L.icon({
        iconUrl: tealUrl,
        iconSize: [32, 37],
        iconAnchor: [16, 37]
    });

var colorCategoryMap = {
    'electronics': [redIcon,redUrl],
    'medical': [blueIcon,blueUrl],
    'public recycle bins': [greenIcon,greenUrl],
    'food scrap': [yellowIcon,yellowUrl],
    'textile': [tealIcon,tealUrl]
}

var legend = L.control({position: 'topright'});

legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend py-2 px-1');

    div.style.backgroundColor = "#fff";
    div.style.borderRadius = '5px';
    div.style.border = '2px solid #00000044';
    labels = [];
    // categories = ['Road Surface','Signage','Line Markings','Roadside Hazards','Other'];

    for (var key in colorCategoryMap) {

            div.innerHTML += 
            labels.push('<span><img src="'+ colorCategoryMap[key][1] +'" height="14px" width="14px">'+key.charAt(0).toUpperCase() + key.substr(1).toLowerCase()+'</span>');

        }
        div.innerHTML = labels.join('<br/>');
    return div;
};


var customControl =  L.Control.extend({

    options: {
      position: 'topright'
    },
  
    onAdd: function (map) {
      var container = L.DomUtil.create('input');
      container.type="button";
      container.title="Legend";
      container.value = "Legend";
  
      container.style.backgroundColor = 'white';     
      container.style.width = 'auto';
      container.style.height = '30px';
      container.style.borderRadius = '4px';
      container.style.border = '2px solid #00000044';
      
      container.onmouseover = function(){
        $('.legend').show(); 
      }
      container.onmouseout = function(){
        $('.info.legend').hide();
      }
  
      container.onclick = function(){
        // console.log('buttonClicked');
      }
  
      return container;
    }
  });