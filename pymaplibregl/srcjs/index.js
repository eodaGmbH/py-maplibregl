console.log("Welcome to pymaplibregl!")

/*
if (Shiny) {
	console.log("Shiny");
	Shiny.addCustomMessageHandler("maplibre", (payload) => {
		console.log(payload);
	});
}
*/

if (Shiny) {
  class MapLibreGLOutputBinding extends Shiny.OutputBinding {
    find(scope) {
        console.log("I am here!");
        return scope.find(".shiny-maplibregl-output");
    }

    renderValue(el, payload) {
        console.log(el.id, payload);
        // console.log(maplibregl);
        /*
        const params = {
            container: el.id,
            style: 'https://demotiles.maplibre.org/style.json',
            center: [0, 0],
            zoom: 1
        }
         */
        const params = Object.assign({container: el.id}, payload.data)
        this.map = new maplibregl.Map(params)
    }
  }

  Shiny.outputBindings.register(
      new MapLibreGLOutputBinding(),
      "shiny-maplibregl-output"
  );
}
