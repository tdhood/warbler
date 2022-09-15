"use strict";

/** Likes a post without causing the page to reload */

const BASE_URL = "http://localhost:5000";

async function likePost(evt) {
  evt.preventDefault();
  console.log("likePostajax");

  console.log("target", evt.currentTarget);
  debugger;
  let messageId = Number(
    evt.currentTarget.parentElement.parentElement.querySelector(
      "input[name=message_id]"
    ).value
  );
  let csrf_token = $("#csrf_token").val();
  console.log("messageId", messageId);
  console.log("token", csrf_token);

  const params = new URLSearchParams();
  params.append("csrf_token", csrf_token);
  params.append("message_id", messageId);
  console.log("params", params.toString());

  // let response = await axios.post('/like', params)

  let response = await axios({
    url: "/like",
    method: "post",
    baseURL: BASE_URL,
    data: params,
    xsrfCookieName: csrf_token,
    headers: { "content-type": "application/x-www-form-urlencoded" },
  }).catch(function (error) {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.log("data", error.response.data);
      console.log("status", error.response.status);
      console.log("headers", error.response.headers);
    } else if (error.request) {
      // The request was made but no response was received
      // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
      // http.ClientRequest in node.js
      console.log(error.request);
    } else {
      // Something happened in setting up the request that triggered an Error
      console.log("Error", error.message);
    }
    console.log(error.config);
  });

  console.log("response", response);
}

$(document).ready((evt) => {
  $(".starButton").on("click", likePost);
});
