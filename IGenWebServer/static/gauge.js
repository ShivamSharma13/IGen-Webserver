var opts = {
    angle: 0, // The span of the gauge arc
    lineWidth: 0.2, // The line thickness
    radiusScale: 0.89, // Relative radius
    pointer: {
      length: 0.54, // // Relative to gauge radius
      strokeWidth: 0.053, // The thickness
      color: '#000000' // Fill color
    },
    limitMax: false,     // If false, max value increases automatically if value > maxValue
    limitMin: false,     // If true, the min value of the gauge will be fixed
    colorStart: '#6FADCF',   // Colors
    colorStop: '#8FC0DA',    // just experiment with them
    strokeColor: '#E0E0E0',  // to see which ones work best for you
    generateGradient: true,
    highDpiSupport: true,     // High resolution support
    staticZones: [
        {strokeStyle: "#0000FF", min: 0, max: 60}, // Red from 100 to 60
        {strokeStyle: "#00FF00", min: 60, max: 120}, // Yellow
        {strokeStyle: "#FFDD00", min: 120, max: 180}, // Green
        {strokeStyle: "#FF6600", min: 180, max: 240}, // Yellow
        {strokeStyle: "#FF0000", min: 240, max: 300}  // Red
     ],
    
  };
  var target = document.getElementById('foo'); // your canvas element
  var gauge = new Gauge(target).setOptions(opts); // create sexy gauge!
  gauge.maxValue = 300; // set max gauge value
  gauge.setMinValue(0);  // Prefer setter over gauge.minValue = 0
  gauge.animationSpeed = 50; // set animation speed (32 is default value)
  gauge.set(200); // set actual value