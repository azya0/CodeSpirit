function check() {
    var console_ = document.getElementById('console');
    var txt = document.createElement('span');
    var br_ = document.createElement('br');
    var input_ = document.getElementById('email');

    txt.innerHTML = input_.value+' -> incorrect email';
    txt.classList.add("main-warning");
    console_.appendChild(txt);

    input_.outerHTML = "<span>"+input_.value+"</span><br>";
    console_.appendChild(br_);

    var script = document.getElementById('script');
    script.parentNode.removeChild(script);

    // <span class="mr-1">$</span><input id="email" class="main-input-auth">

    var input_ = document.createElement('input');
    var doll__ = document.createElement('span');
    doll__.classList.add("mr-1");
    input_.classList.add("main-input-auth");
    input_.classList.add("pl-0");
    input_.id = 'email';
    doll__.innerHTML = '$';

    console_.appendChild(doll__);
    console_.appendChild(input_);

    document.getElementById("email").focus();

    var script = document.createElement('script');
    script.innerHTML = 'tab()';
    script.id = 'script';
    console_.appendChild(script);
}

function tab() {
    var input = document.getElementById("email");

    input.addEventListener("DOMContentLoaded", function() {
        input.focus();
    });

    input.addEventListener("keyup", function(event) {
        if (event.keyCode === 13) {
            check();
        }
    });
}