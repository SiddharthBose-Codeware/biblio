function getVerifiedAccessKey() {

  var verifyFormData = new FormData();

  var isValid = false;

  verifyFormData.append("token", window.localStorage.biblioaccess);

  $.ajax({

    "url": "http://localhost:8000/api/auth/verify_token",

    "method": "POST",

    "contentType": false,

    "processData": false,

    "XHRFields": {
      "withCredentials": true
    },

    "data": verifyFormData,

    "cache": false,

    "enctype": "multipart/form-data",

    "success": function(response) {

      isValid = true;

    }

  });

  if (!isValid) {

    var formData = new FormData();

    formData.append("refresh", window.localStorage.bibliorefresh);

    $.ajax({

        url: "http://localhost:8000/api/auth/refresh_token",

        data: formData,

        method: "POST",

        processData: false,

        XHRFields: {

          "withCredentials": true

        },

        enctype: "multipart/form-data",

        cache: false,

        contentType: false,

        success: function(response) {

          window.localStorage.setItem("biblioaccess", response.access);

        }

    });

  }

  return window.localStorage.biblioaccess;

}

function setJWTToken(accessToken, refreshToken) {

  window.localStorage.setItem('biblioaccess', accessToken);

  window.localStorage.setItem('bibliorefresh', refreshToken);

}
