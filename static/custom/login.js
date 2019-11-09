function login() {
    // Sends the stuff to the server?
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    console.log(email, password);
    // TODO change to handle_login
    postData("/handle_login", {email: email, password:password}).then(res => {
        if (res.status === "success") {
            console.log("login success");
            alert("login success");
        } else {
            console.log("login failure");
            alert(res.issue);
        }
    });
}

async function postData(url = '', data = {}) {
    // Default options are marked with *
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