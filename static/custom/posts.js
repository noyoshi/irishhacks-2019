function getList() {
    filters = {}
    if (navigator.geolocation){
        console.log("geo on ");
        navigator.geolocation.getCurrentPosition(function(position) {
            console.log("geo in");
            filters['maxdist'] = document.getElementById('distance').value;
            postData("/posts/handle_post_filter", filters).then(res => {
                if (res.status === "success") {
                    console.log("post filter success");
                    alert("yeet baby");
                } else {
                    console.log("post filter failure");
                    alert(res.issue);
                }
            });
        });
    } else {
        filters['maxdist'] = document.getElementById('distance').value;
        postData("/posts/handle_post_filter", filters).then(res => {
            if (res.status === "success") {
                console.log("post filter success");
                alert("yeet baby");
            } else {
                console.log("post filter failure");
                alert(res.issue);
            }
        });
    }
}


async function postData(url = '', data = {}) {
    // Default options are marked with *
    console.log(url);
    const response = await fetch(url, {
      method: 'POST', // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
      credentials: 'same-origin', // include, *same-origin, omit
      headers: {
        'Content-Type': 'application/json'
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      redirect: 'follow', // manual, *follow, error
      referrer: 'no-referrer', // no-referrer, *client
      body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return await response.json(); // parses JSON response into native JavaScript objects
}