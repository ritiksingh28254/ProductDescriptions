document.getElementById('descriptionForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    const productName = document.getElementById('productName').value;
    const category = document.getElementById('category').value;
    // console.log("hello");
    

    // Call the API
    fetch('https://now3n9etzj.execute-api.us-east-1.amazonaws.com/prod/generate-description', {
        
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product_name: productName, category: category })
    })
    .then(response => response.json())
    .then(data => {
        // Display the generated description
        if (data.description) {
            document.getElementById('result').innerText = data.description;
        } else {
            document.getElementById('result').innerText = 'Error generating description: ' + data.error;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerText = 'An error occurred.';
    });
});
