function check(id) {
    var console_ = document.getElementById('console');
    var txt = document.createElement('span');
    var br_ = document.createElement('br');
    var input_ = document.getElementById(id);

    if (id == 'email') {
        if ((input_.value != '') && (request('http://127.0.0.1:5000/system/valid_email/' + input_.value) == 'true')) {
            if (request('http://127.0.0.1:5000/system/email/' + input_.value) == 'unused') {
                tab_success(id);

            }
            else {
                tab_error(id, 'is already in use')
            }
        }
        else {
            tab_error(id, 'incorrect data for ' + id)
        }
    }
    else if (id == 'login') {
        if ((input_.value != '') && (request('http://127.0.0.1:5000/system/valid_login/' + input_.value) == 'true')) {
            if (request('http://127.0.0.1:5000/system/login/' + input_.value) == 'unused') {
                tab_success(id);
            }
            else {
                tab_error(id, 'is already in use')
            }
        }
        else {
            tab_error(id, 'incorrect data for ' + id)
        }
    }
    else {
        if ((input_.value != '') && (request('http://127.0.0.1:5000/system/valid_login/' + input_.value) == 'true')) {
            tab_success(id);
        }
        else {
            tab_error(id, 'incorrect data for ' + id)
        }
    }
}

function tab(id) {
    var input = document.getElementById(id);

    input.addEventListener("DOMContentLoaded", function() {
        input.focus();
    });

    input.addEventListener("keyup", function(event) {
        if (event.keyCode === 13) {
            if (!input.readOnly) {
                check(id);
            }
        }
    });

    document.getElementById('submit').onclick = function() {
        console.log('flex'); // #TODO
        document.getElementById('submit').click();
    };
}

function request(link) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', link, false);
    xhr.send();
    return xhr.responseText;
}


function tab_error(id, message) {
    var console_ = document.getElementById('console');
    var txt = document.createElement('span');
    var br_ = document.createElement('br');
    var input_ = document.getElementById(id);

    txt.innerHTML = input_.value + ' -> ' + message;
    txt.classList.add("main-warning");
    console_.appendChild(txt);

    input_.outerHTML = "<span>" + input_.value + "</span><br>";
    console_.appendChild(br_);

    var script = document.getElementById('script');
    script.parentNode.removeChild(script);


    var input_ = document.createElement('input');
    var doll__ = document.createElement('span');
    doll__.classList.add("mr-1");
    input_.classList.add("main-input-auth");
    input_.classList.add("pl-0");
    input_.id = id;
    doll__.innerHTML = '$';

    console_.appendChild(doll__);
    console_.appendChild(input_);

    document.getElementById(id).focus();

    var script = document.createElement('script');
    script.innerHTML = 'tab("'+ id + '")';
    script.id = 'script';
    console_.appendChild(script);
}

function tab_success(id) {
    var console_ = document.getElementById('console');
    var txt = document.createElement('span');
    var br_ = document.createElement('br');
    var input_ = document.getElementById(id);

    txt.innerHTML = input_.value+' -> correct ' + id + '!';
    txt.classList.add("main-success");
    console_.appendChild(txt);

    input_.readOnly = true;;
    console_.appendChild(br_);

    var script = document.getElementById('script');
    script.parentNode.removeChild(script);


    var input_ = document.createElement('input');
    var doll__ = document.createElement('span');
    var text__ = document.createElement('span');
    var new_id;

    doll__.classList.add("mr-1");
    input_.classList.add("main-input-auth");
    input_.classList.add("pl-0");
    if (id == 'email') {
         new_id = 'login';
    }
    else if (id == 'login') {
         new_id = 'password';
    }
    else {
        text__.innerHTML = document.getElementById('email').value + ' successfully registered! ~<br>';
        text__.classList.add("main-success");
        console_.appendChild(text__);
    }
    if (id != 'password') {
        input_.id = new_id;
        text__.innerHTML = document.getElementById('email').value + ' ' + input_.id.toUpperCase() + ' ~<br>';
        doll__.innerHTML = '$';

        console_.appendChild(text__);
        console_.appendChild(doll__);
        console_.appendChild(input_);

        document.getElementById(new_id).focus();

        var script = document.createElement('script');
        script.innerHTML = 'tab("'+ new_id + '")';
        script.id = 'script';
        console_.appendChild(script);
    }
    else {
        console.log(123);
    }
}
