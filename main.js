document.querySelector('.btn').addEventListener('click', function() {
    var product = document.querySelector('.form-control').value;
    fetch('https://api.example.com/prices?product=' + encodeURIComponent(product))
        .then(function(response) {
            if (!response.ok) {
                throw new Error("HTTP error " + response.status);
            }
            return response.json();
        })
        .then(function(json) {
            // Atualize a página com os dados de preços
            console.log(json);
        })
        .catch(function(error) {
            console.log('Houve um problema com a solicitação fetch: ' + error.message);
        });
});