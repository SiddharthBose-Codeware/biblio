window.onload = function() {

  $("#loader-wrapper").fadeOut();

};

function App() {

  this.libraryItemsWorkarea = null;
  this.subjectTypesWorkarea = null;
  this.itemTypesWorkarea = null;
  this.authorsWorkarea = null;
  this.issueItemWorkarea = null;

}

(function() {

  var app = new App();

  $("#manage-library-items-sidebar-link").click(function() {

    if (app.libraryItemsWorkarea) {

      $("#work-area-container").html(app.libraryItemsWorkarea);

    } else {

      $.ajax({

        url: "/ajaxHTML/manageLibraryItems",

        success: function(response) {

          app.libraryItemsWorkarea = response;

          $("#work-area-container").html(app.libraryItemsWorkarea);

        }

      });

    }

  });

  $("#manage-subject-types-sidebar-link").click(function() {

    if (app.subjectTypesWorkarea) {

      $("#work-area-container").html(app.subjectTypesWorkarea);

    } else {

      $.ajax({

        url: "/ajaxHTML/manageSubjectTypes",

        success: function(response) {

          app.subjectTypesWorkarea = response;

          $("#work-area-container").html(app.subjectTypesWorkarea);

        }

      });

    }

  });

  $("#manage-item-types-sidebar-link").click(function() {

    if (app.itemTypesWorkarea) {

      $("#work-area-container").html(app.itemTypesWorkarea);

    } else {

      $.ajax({

        url: "/ajaxHTML/manageItemTypes",

        success: function(response) {

          app.itemTypesWorkarea = response;

          $("#work-area-container").html(app.itemTypesWorkarea);

        }

      });

    }

  });

  $("#manage-authors-sidebar-link").click(function() {

    if (app.authorsWorkarea) {

      $("#work-area-container").html(app.authorsWorkarea);

    } else {

      $.ajax({

        url: "/ajaxHTML/manageAuthors",

        success: function(response) {

          app.authorsWorkarea = response;

          $("#work-area-container").html(app.authorsWorkarea);

        }

      });

    }

  });

  $("#issue-item-sidebar-link").click(function() {

    if (app.issueItemWorkarea) {

      $("#work-area-container").html(app.issueItemWorkarea);

    } else {

      $.ajax({

        url: "/ajaxHTML/manageIssueItems",

        success: function(response) {

          app.issueItemWorkarea = response;

          $("#work-area-container").html(app.issueItemWorkarea);

        }

      });

    }

  });

})();
