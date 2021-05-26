
function clearTextField(textFieldList) {
    textFieldList.forEach(id => {
        document.getElementById(id).value = "";
    });
}

function focusOut (fieldId, textFieldList) {
    var eid_val = document.getElementById(fieldId).value;
    var data = document.getElementById("tableBody");
    var n_rows = data.rows.length; 
    var n_col;
    for (i = 0; i < n_rows; ++i) {
        row = data.rows[i];
        n_col = textFieldList.length;
        cell_data = row.cells.item(0).innerText;
        if (cell_data == eid_val) {
            for(j = 0; j < n_col; ++j) {
                id = textFieldList[j];
                cell_data = row.cells.item(j).innerText;
                document.getElementById(id).value = cell_data;
            }
            $("#btnDelete").prop("disabled", false);
            $("#btnClear").prop("disabled", false);
            $("#btnUpdate").prop("disabled",  false);
            return true;
        }
    }
    return false;
}
