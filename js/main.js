form.addEventListener('submit', function(e) {
    // Prevent default behavior:
    e.preventDefault();
    // Create new FormData object
    const formData = new FormData(form);
    const formDataObject = Object.fromEntries(formData.entries());
    // Post the payload using Fetch:
    fetch('http:// {invoke-url} /test/ddb', {
      method: 'POST',
      mode: 'no-cors',
      body: JSON.stringify(formDataObject)
    }).then(res => console.log(res))
})