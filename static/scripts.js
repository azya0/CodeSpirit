function postClicked () {
    window.addEventListener('click',function(elm){

        var input = document.getElementById("main-post-ask-btn");
        var flex = document.getElementById('main-post-bottom-panel');
        var img_input = document.getElementById('image_input');

        const target = elm.target;

        if ((target == input) | (target == image_input)) {
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
    var div = document.getElementById('main-post-input');
    flex.value = div.innerHTML;
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
                    document.getElementById('main-post-bottom-panel').style.borderRadius = '0';
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
    document.getElementById('main-post-bottom-panel').style = null;
}

(function() {
    var last = -1;
    document.addEventListener('mouseover', EasyTogglerHandler);
    function EasyTogglerHandler(event){
        const EY_BTN = event.target.closest('[data-easy-toggle]');
        if( EY_BTN )
        {
            event.preventDefault();
            let ey_target = EY_BTN.getAttribute('data-easy-toggle');
            let ey_class = EY_BTN.getAttribute('data-easy-class');

            try
            {
                document.querySelectorAll('[data-easy-toggle]').forEach(easyBlock => {
                    if(!easyBlock.hasAttribute('data-easy-parallel') && easyBlock !== EY_BTN){
                        document.querySelector(easyBlock.getAttribute('data-easy-toggle')).classList.remove(easyBlock.getAttribute('data-easy-class'));
                    }
                    else if (easyBlock.hasAttribute('data-easy-parallel') && easyBlock == EY_BTN) {
                        if ((last != -1)) {
                            console.log(12, last);
                            var block_list = document.querySelectorAll(ey_target);
                            block_list[last].classList.remove('show');
                        }

                        var block_list = document.querySelectorAll(ey_target);
                        var array = Array.from(document.querySelectorAll('[data-easy-toggle]'));
                        var index = array.indexOf(easyBlock);
                        var flex = array[index]
                        block_list[index].classList.toggle(ey_class);
                        last = index;
                    }
                });
            }
            catch (ey_error)
            {
                console.warn(ey_error);
            }
        }

        if ( !EY_BTN )
        {
            let ey_rcoe_block_targets = document.querySelectorAll('[data-easy-rcoe]');

            Array.from(ey_rcoe_block_targets).forEach.call(ey_rcoe_block_targets, function(ey_rcoe_block_target){
                let ey_rcoe_block = ey_rcoe_block_target.getAttribute('data-easy-toggle'),
                    ey_rcoe_block_class = ey_rcoe_block_target.getAttribute('data-easy-class');

                    if( !event.target.closest(ey_rcoe_block) )
                    {
                        try
                        {
                            document.querySelectorAll(ey_rcoe_block)[last].classList.remove(ey_rcoe_block_class);
                            last = -1;
                        }
                        catch (ey_error)
                        {
                        }
                    }

            });
        }

    }

  })()
