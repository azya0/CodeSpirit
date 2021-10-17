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
    });
}

function replaceText() {
    var flex = document.getElementById('text');
    div = document.getElementById('main-post-input');
    flex.value = div.innerHTML;
    console.log(flex.value);
}


function addImages() {
    $(function() {
            function readURL(input) {
                $('#main-post-images').empty();
                if (input.files.length > 8) {
                    alert('Слишком много изображений');
                    $("#image_input").val('');
                    document.getElementById('main-post-cancel-btn-div').style.display = "none";
                }
                else {
                    $(input.files).each(function(i, el) {
                        var reader = new FileReader();
                        reader.onload = function(e) {
                            img = $('<img>').attr('src', e.target.result).attr('class', 'main-post-image');
                            img.appendTo('#main-post-images');
                        };
                        reader.readAsDataURL(input.files[i]);
                    });
                }
                if (input.files.length > 0) {
                    document.getElementById('main-post-cancel-btn-div').style.display = "flex";
                    document.getElementById('main-post-cancel-btn-div').style.justifyContent = "flex-end";
                }
            }

            $("#image_input").change(function() {
                readURL(this);
            });
        });
}

function clearImagesBtn() {
    document.getElementById('main-post-cancel-btn-div').style.display = "none";
    $('#main-post-images').empty();
    $("#image_input").val('');
}