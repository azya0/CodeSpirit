function check() {
    var console_ = document.getElementById('console');
    var txt = document.createElement('span');
    var br_ = document.createElement('br');

    txt.innerHTML = 'incorrect email';
    console_.appendChild(txt);

    var input_ = document.getElementById('email');
    input_.outerHTML = "<span>"+input_.value+"</span><br>";
    console_.appendChild(br_);

    var script = document.getElementById('script');
    script.parentNode.removeChild(script);

    // <span class="mr-1">$</span><input id="email" class="main-input-auth">

    var input_ = document.createElement('input');
    var doll__ = document.createElement('span');
    doll__.classList.add("mr-1");
    input_.classList.add("main-input-auth");
    input_.id = 'email';
    doll__.innerHTML = '$';

    console_.appendChild(doll__);
    console_.appendChild(input_);

    var script = document.createElement('script');
    script.innerHTML = 'tab()';
    script.id = 'script';
    console_.appendChild(script);
}

function tab() {
    var input = document.getElementById("email");

    input.addEventListener("keyup", function(event) {
        if (event.keyCode === 13) {
            check();
        }
    });
}