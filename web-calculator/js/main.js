
function on_number_button_click(input) {
  document.getElementById("calculator-expression").value += input;
}

function on_start_paranthese_button_click(input) {
  document.getElementById("calculator-expression").value += input;
}

function on_end_paranthese_button_click(input) {
  var expression = document.getElementById("calculator-expression").value;
  if (expression.includes("(")) {
    document.getElementById("calculator-expression").value += input;
  }
}

function on_sign_operator_click(input) {
  document.getElementById("calculator-expression").value += input;
}

function on_delete_button_click() {
  document.getElementById("calculator-expression").value = "";
}

function on_dot_button_click() {
  return 0
}

function on_equals_button_click() {
  return 0
}


