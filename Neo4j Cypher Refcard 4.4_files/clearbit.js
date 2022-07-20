;(function (w) {
  if (w.__clearbit_tagsjs) {
    w.console &&
      w.console.error &&
      w.console.error("Clearbit tags.js snippet included twice.");
    return;
  }

  w.__clearbit_tagsjs = true;

  

  var destjs = document.createElement("script");
  destjs.src = 'https://x.clearbitjs.com/v2/pk_0cf50a967c574ba5041ad7e2581017d6/destinations.min.js'

  var first = document.getElementsByTagName("script")[0];
  destjs.async = true;
  first.parentNode.insertBefore(destjs, first);


  
    
      var tracking = (w.clearbit = w.clearbit || []);
      w.clearbit._writeKey = 'pk_0cf50a967c574ba5041ad7e2581017d6';
      w.clearbit._apiHost = 'x.clearbitjs.com';

      

      if (!tracking.initialize) {
        var clearbitjs = document.createElement("script");
        clearbitjs.src = 'https://x.clearbitjs.com/v2/pk_0cf50a967c574ba5041ad7e2581017d6/tracking.min.js';

        var first = document.getElementsByTagName("script")[0];
        clearbitjs.async = true;
        first.parentNode.insertBefore(clearbitjs, first);
      }
    

    
  

  
})(window);
