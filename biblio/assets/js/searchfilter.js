var types = {

  INPUT: 1,
  SELECT: 2

};

function SearchFilterModal(searchField, getUrl, fields, valueId, nameId, exceptions, jsonName, jsonValue) {

  this.searchField = searchField;
  this.getUrl = getUrl;
  this.valueId = valueId;
  this.nameId = nameId;
  this.fields = fields;
  this.exceptions = exceptions;
  this.jsonName = jsonName;
  this.jsonValue = jsonValue;

  this.updateTable = function(data) {

    this.data = data;

    var tableFields = this.tableFields;

    var exceptions = this.exceptions;

    var dataHtml = "";

    var serialNumber = 1;

    data.forEach(function(item) {

      dataHtml += "<tr><td><input type=\"radio\" value=\"" + serialNumber++ + "\" class=\"table-form-select\" name=\"name-fields table-form-select\" /></td>";

      fields.forEach(function(field) {

        if (exceptions[item[field.jsonName]] != undefined) {

            dataHtml += "<td>" + exceptions[item[field.jsonName]] + "</td>";

        } else {

            dataHtml += "<td>" + item[field.jsonName] + "</td>";

        }

      });

      dataHtml += "</tr>";

    });

    $("#table-data").html(dataHtml);

  };

}

function slugify(str) {

    str = str.replace(/^\s+|\s+$/g, '');

    str = str.toLowerCase();

    var from = "àáäâèéëêìíïîòóöôùúüûñç·/_,:;";

    var to   = "aaaaeeeeiiiioooouuuunc------";

    for (var i = 0; i < from.length; i++) {

        str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));

    }

    str = str.replace(/[^a-z0-9 -]/g, '').replace(/\s+/g, '-').replace(/-+/g, '-');

    return str;

}

SearchFilterModal.prototype.getResultAndUpdateTable = function(searchInput) {

  var current = this;

  $.ajax({

    url: this.getUrl,

    headers: {

      "Authorization": "Bearer " + getVerifiedAccessKey()

    },

    data: {

      search: searchInput == undefined ? "" : searchInput.val()

    },

    success: function(result) {

      current.updateTable(result);

    }

  });

};

SearchFilterModal.prototype.generateModal = function(editLinkItemId, updateUrl) {

  var slugId = slugify(this.searchField);

  $("#search-fields").html("");

  $("#table-data").html("");

    $("#search-fields").html($("#search-fields").html() + "<div class=\"form-group\"><label>Enter " + this.searchField + "</label><input id=\"" + slugId + "\" class=\"form-control\" type=\"text\"></div>");

  var tableHeadingsHtml = "<form><th>Select</th>";

  this.fields.forEach(function(field) {

    tableHeadingsHtml += "<th>" + field.tableName + "</th>";

  });

  tableHeadingsHtml += "</form>";

  $("#table-headings").html(tableHeadingsHtml);

  var current = this;

    $("#" + slugId).on("keyup", function() {

      current.getResultAndUpdateTable($(this));

    });

  $("#select-filter-modal").modal().show();

  $("#select-item-button").click(function() {

    debugger;

    var selectedId = $(".table-form-select:checked").attr("value");

    var element = null;

    var data = current.data;

    if (!data) return;

    for (var i = 0; i < data.length; i++) {

      if (data[i].id == selectedId) {

        element = data[i];

        break;

      }

    }

    if (!element) return; // Add error box later

    if (current.exceptions[element[current.jsonName]] != undefined) {

      $(current.nameId).html(current.exceptions[element[current.jsonName]]);

    } else {

      if (!editLinkItemId) {

        $(current.nameId).html(element[current.jsonName]);

      } else {

        var updateData = {};

        var valueSelector = current.nameId.parent().attr('data-update-type');

        var keySelector = current.nameId.parent().attr('data-edit-type');

        updateData[keySelector] = element[valueSelector];

        debugger;

        $.ajax({

          url: updateUrl + editLinkItemId + "/",

          data: updateData,

          method: "PATCH",

          headers: {

            "Authorization": "Bearer " + getVerifiedAccessKey()

          },

          success: function() {

            $(current.nameId).html(element[current.jsonName]);

          }

        });

      }

    }

    if (current.valueId != "") {

        current.valueId.val(element[current.jsonValue]);

    }

    $("#select-filter-modal").modal('hide');

  });

  current.getResultAndUpdateTable();

};
