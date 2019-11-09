function editProfile() {
    // Sends the stuff to the server?
    var firstname = document.getElementById('firstname').value;
    var lastname = document.getElementById('lastname').value;
    var email = document.getElementById('email').value;
    var bio = document.getElementById("bio").value;
    var dob = document.getElementById("dob").value;
    var phone_number = document.getElementById("phone_number").value;

    console.log(firstname, lastname);
    // TODO change to handle_login
    postData("/profile/save_edits", {
        firstname: firstname, 
        lastname: lastname, 
        email: email, 
        bio: bio,
        phone_number: phone_number,
        bio: bio})
    .then(res => {
        if (res.status === "success") {
            console.log("edit success");
            window.location.href = "/profile/" + res.uuid;
        } else {
            console.log("edit failure");
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