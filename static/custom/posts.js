function getList() {
  filters = {};
  filters["maxdist"] = document.getElementById("distance").value;
  filters["type"] = document.getElementById("type").value;
  filters["hours"] = document.getElementById("hours").value;
  console.log(filters);
  postData("/posts/handle_post_filter", filters).then(res => {
    if (res.status === "success") {
      console.log("post filter success");
      // alert("yeet baby");
    } else {
      console.log("post filter failure");
      alert(res.issue);
    }
  });
}

function grabPost() {
  var post_id = window.location.href.split("/").pop();
  postData("/grab_post", { post_id: post_id }).then(res => {
    if (res.status === "success") {
      console.log("success");
      document.location.reload();
    } else {
      console.log("fail");
    }
  });
}

function addPost() {
  data = {
    title: document.getElementById("title").value,
    // location: document.getElementById("location").value,
    // skillset: document.getElementById("skillset").value,
    num_volunteers: document.getElementById("num_volunteers").value,
    // username: document.getElementById("username").value,
    tags: document.getElementById("tags").value,
    // start_date: document.getElementById("start_date").value,
    // duration: document.getElementById("duration").value,
    description: document.getElementById("description").value
  };

  console.log(data);
  postData("/posts/create_new/", data).then(res => {
    if (res.status === "success") {
      window.location.href = "/posts/" + res.uuid;
      console.log("post filter success");
      // alert("yeet baby");
    } else {
      window.location.href = "/signup/";
      console.log("post filter failure");
      alert(res.issue);
    }
  });
}

function addVolunteer(postId) {
  filters = {
    postId: postId
  };
  postData("/posts/add_to_post", filters).then(res => {
    if (res.status === "success") {
      console.log("post filter success");
    } else {
      console.log("post filter failure");
      alert(res.issue);
    }
  });
}

async function postData(url = "", data = {}) {
  // Default options are marked with *
  console.log(url);
  const response = await fetch(url, {
    method: "POST", // *GET, POST, PUT, DELETE, etc.
    mode: "cors", // no-cors, *cors, same-origin
    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
    credentials: "same-origin", // include, *same-origin, omit
    headers: {
      "Content-Type": "application/json"
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: "follow", // manual, *follow, error
    referrer: "no-referrer", // no-referrer, *client
    body: JSON.stringify(data) // body data type must match "Content-Type" header
  });
  return await response.json(); // parses JSON response into native JavaScript objects
}
