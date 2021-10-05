function postClicked () {
    window.addEventListener('click',function(elm){

        var input = document.getElementById("main-post-ask-btn");
        var flex = document.getElementById('main-post-bottom-panel');
        const target = elm.target;

        if (target == input) {
            var input = document.getElementById("main-post-ask-btn");
            var div = document.createElement('div');
            div.setAttribute("contentEditable", true);
            div.id = "main-post-input";
            div.class = "main-post-item";
            input.replaceWith(div);
            div.focus();
            var flex = document.getElementById('main-post-bottom-panel');
            flex.hidden = !flex.hidden;
            var cont = document.getElementById('main-post-container');
            cont.style.borderRadius = '6px 6px 0 0';
        }

        else if (!flex.hidden && !target.closest('#main-post-bottom-panel') && !target.closest('#main-post-container')) { // если этот элемент или его родительские элементы не окно навигации и не кнопка
            var flex = document.getElementById('main-post-bottom-panel');
            flex.hidden = !flex.hidden;

            var cont = document.getElementById('main-post-container');
            cont.style.borderRadius = '6px';

            var new_input = document.createElement('input');
            new_input.id = 'main-post-ask-btn';
            new_input.classList.add("main-post-item", "main-white-font-color");
            new_input.type = 'button';
            new_input.value = "What's new?";
            console.log(new_input);
            div = document.getElementById('main-post-input');
            div.replaceWith(new_input);
        }
    });
}

function replaceText() {
    var flex = document.getElementById('text');
    div = document.getElementById('main-post-input');
    flex.value = div.innerHTML;
    console.log(flex.value);
}
// TO POST console.log(div.innerHTML);