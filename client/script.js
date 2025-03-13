fetch("/data")
.then(response => response.json())
.then(data => {
    alert(data);
})