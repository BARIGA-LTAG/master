var map = L.map('map').setView([0, 0], 2);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

function loadLayers() {
    // Remplissez dynamiquement la liste des couches depuis Django
    // Exemple :
    var layers = ["Couche 1", "Couche 2", "Couche 3"];
    var layerSelect = document.getElementById("layer");

    layers.forEach(function(layer) {
        var option = document.createElement("option");
        option.text = layer;
        option.value = layer;
        layerSelect.add(option);
    });
}

function getLayerData(layerName) {
    // Implémentez la logique pour récupérer les données de la couche depuis Django
    // Exemple : Utilisez des requêtes AJAX pour récupérer les données depuis votre API Django
}

function performSpatialAnalysis() {
    var selectedOperation = document.getElementById("operation").value;
    var selectedLayer = document.getElementById("layer").value;
    var layerData = getLayerData(selectedLayer);

    var result = performTurfOperation(selectedOperation, layerData);
    displayResultOnMap(result);
}

function performTurfOperation(operation, layerData) {
    var turfLayer = turf.geoJSON(layerData);

    switch (operation) {
        case "buffer":
            // Exemple: Appliquer un tampon de 10 unités autour de chaque entité
            var bufferedLayer = turf.buffer(turfLayer, 10, { units: 'kilometers' });
            return bufferedLayer;

        case "center":
            return turf.center(turfLayer);

        case "centerOfMass":
            return turf.centerOfMass(turfLayer);

        case "centroid":
            return turf.centroid(turfLayer);

        // Ajoutez d'autres cas pour différentes opérations selon les besoins

        default:
            console.error("Opération d'analyse spatiale non gérée");
            return null;
    }
}

function displayResultOnMap(result) {
    // Implémentez la logique pour afficher le résultat sur la carte
    // Exemple : Ajoutez une nouvelle couche à la carte avec le résultat
}

window.onload = function() {
    loadLayers();
};
