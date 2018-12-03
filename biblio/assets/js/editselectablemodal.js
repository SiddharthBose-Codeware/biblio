function EditSelectableModal(elementId, editType, mainEditType, modalEditName, mainEditTypeAttributes) {

  this.elementId = elementId;
  this.editType = editType;
  this.mainEditType = mainEditType;
  this.modalEditName = modalEditName;
  this.mainEditTypeAttributes = mainEditTypeAttributes;

  this.showModal = function() {

    $("#edit-modal-name-type").html(this.modalEditName);

    var tableData = "";

    $.ajax({

      url: "http://localhost:8000/api/" + this.mainEditType + "/",

      method: "GET",

      headers: {

        "Authorization": "Bearer " + getVerifiedAccessKey()

      },

      success: function(response) {

        tableData += "<th><td>Select</td>";

        this.mainEditTypeAttributes.forEach(function(eachAttribute) {

          tableData += "<td>" + eachAttribute.tableName + "</td>";

        });

        tableData += "</th>";

        this.mainEditTypeAttributes += "</th>";

        response.forEach(function(tableRow) {

          tableData += "<tr><td><input data-id=\"" + tableRow.id + "\" type=\"radio\" name=\"edit-modal-table-select\" class=\"edit-modal-table-select\"></td>";

          this.mainEditTypeAttributes.forEach(function(eachAttribute) {

            tableData += "<td>" + tableRow[eachAttribute.jsonName] + "</td>";

          });

          tableData += "</tr>";

          $("#edit-modal-table-body").html(tableData);



        });

      }

    });

    $("#edit-items-modal-confirm").click(function() {

      var data = {};

      data[this.editType] = $("#edit-items-value-input").val();

      $.ajax({

        url: "http://localhost:8000/api/items/" + this.mainEditType + "/" + this.elementId + "/",

        method: "PATCH",

        data: data,

        headers: {

          "Authorization": "Bearer " + getVerifiedAccessKey()

        },

        success: function() {

          // Add success message later

        }

      });

    });

    $("#edit-items-modal").modal('show');

  };

}
