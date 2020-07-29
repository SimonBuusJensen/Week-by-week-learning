var signs = "/x+-";
var numbers = "0123456789";
var openParenthesis = 0;

function is_number(input) {
    return numbers.includes(input);
}

function is_sign(input) {
    return signs.includes(input);
}

function on_number_button_click(input) {
    document.getElementById("calculator-expression").value += input;
}

function on_start_paranthese_button_click() {
    var expression = document.getElementById("calculator-expression").value;
    var lastTypedChar = expression.slice(-1);
    // if (is_number(lastTypedChar) || lastTypedChar === "(" || lastTypedChar === ")") {
    document.getElementById("calculator-expression").value += "(";
    openParenthesis += 1;
    // }
}

function on_end_paranthese_button_click(input) {
    var expression = document.getElementById("calculator-expression").value;
    var expressionLength = expression.length;
    if (expressionLength > 0) {
        var lastTypedCharacter = expression.slice(-1);
        if (openParenthesis > 0 && (is_number(lastTypedCharacter) || lastTypedCharacter === ")")) {
            document.getElementById("calculator-expression").value += input;
            openParenthesis -= 1;
        }
    }
}

function on_sign_operator_click(input) {
    var expression = document.getElementById("calculator-expression").value;
    var expression_length = expression.length;
    if (expression_length > 0) {
        var lastTypedCharacter = expression.slice(-1);
        // if ((lastTypedCharacter >= '0' && lastTypedCharacter <= '9') || (lastTypedCharacter === ")")) {
        if (is_number(lastTypedCharacter) || lastTypedCharacter === ")") {
            document.getElementById("calculator-expression").value += input;
        }
    }
}

function on_delete_button_click() {
    var expression = document.getElementById("calculator-expression").value;
    if (expression.length > 1) {

        var lastTypedCharacter = expression.slice(-1);

        if (lastTypedCharacter === "(") {
            openParenthesis -= 1;
        }
        if (lastTypedCharacter === ")") {
            openParenthesis += 1;
        }

        // Remove the last typed character
        document.getElementById("calculator-expression").value = expression.slice(0, expression.length-1);
    }
    else {
        on_ce_button_click()
    }
}

function on_ce_button_click() {

    // Reset the number of open parenthesis
    openParenthesis = 0;

    // hide the previous result if it is visible
    document.getElementById("calculator-result").style.visibility = "hidden";

    // Reset the calculator expression
    document.getElementById("calculator-expression").value = "";
}

function on_dot_button_click() {
    var expression = document.getElementById("calculator-expression").value;
    var lastCharacter = expression.slice(-1);
    if (is_number(lastCharacter)) {

    }
    return 0
}

function parse_expression(expression) {

}

function on_equals_button_click() {

    var expression = document.getElementById("calculator-expression").value;

    if (openParenthesis === 0) {
        var result = 2
        document.getElementById("calculator-result").value = result;
        document.getElementById("calculator-result").style.visibility = "visible";
    }

    return 0
}


