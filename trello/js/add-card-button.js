
var elements = document.getElementsByClassName("add-card-button");

var myFunction = function() {
    var attribute = "Hello";
    var parent = this.caller.;
    alert(parent);
};

for (var i = 0; i < elements.length; i++) {
    elements[i].addEventListener('click', myFunction, false);
}
