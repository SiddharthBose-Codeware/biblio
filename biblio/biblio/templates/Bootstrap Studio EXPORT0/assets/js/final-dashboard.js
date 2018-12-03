window.onload = function() {

  $("#loader-wrapper").fadeOut();

}

$("#manage-library-items-sidebar-link").click(function() {

    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function() {

      if (this.readyState == 4 && this.status == 200) {

        alert();

      }

    };

    xhr.open("GET", "/libraryitemsworkarea.html", true);
    xhr.send();

});

$("#manage-subject-types-sidebar-link").click(function() {



});

$("#manage-item-types-sidebar-link").click(function() {



});

$("#manage-authors-sidebar-link").click(function() {



});

$("#issue-item-sidebar-link").click(function() {



});
