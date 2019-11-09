function signup() {
    // Sends the stuff to the server?
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var password_repeat = document.getElementById("password_repeat").value
    var name = document.getElementById("name").value

    if (password != password_repeat) {
        alert("passwords should match");
        return;
    }

    console.log(email, password);
    // TODO change to handle_login
    postData("/handle_signup", {email: email, password:password, name: name}).then(res => {
        if (res.status === "success") {
            // alert("signup success");
            document.getElementById("msg").innerText = "Success!";
            // TODO do something better here
        } else {
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