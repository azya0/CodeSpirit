last = -1;


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
            div.setAttribute("placeholder", "What's new?");
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
    flex.value = div.innerText.replace(/\r?\n|\r/g, "\\n");
}


function replaceCommentText(post_id) {
    var flex = document.getElementById('comments-hidden-input-' + post_id);
    var div = document.getElementById('comment-post-' + post_id);
    flex.value = div.innerText.replace(/\r?\n|\r/g, "\\n");
}


function moreButton(comment_id) {
    var button = document.getElementById('text-a-' + comment_id);
    var br = document.getElementById('text-br-' + comment_id);
    var hidden_text = document.getElementById('text-hidden-' + comment_id);
    var points = document.getElementById('points-' + comment_id);

    button.style.display = 'none';
    br.style.display = 'none';
    points.style.display = 'none';
    hidden_text.style.display = 'contents';
}


function moreButtonN(comment_id) {
    var button = document.getElementById('text-n-' + comment_id);
    var points = document.getElementById('points-n-' + comment_id);
    var hidden_text = document.getElementsByClassName('text-n-hidden-' + comment_id);

    for (let item of hidden_text) {
        item.style.display = 'block';
    }
    button.style.display = 'none';
    points.style.display = 'none';
}


function moreButtonP(comment_id) {
    var button = document.getElementById('p-text-a-' + comment_id);
    var br = document.getElementById('p-text-br-' + comment_id);
    var hidden_text = document.getElementById('p-text-hidden-' + comment_id);
    var points = document.getElementById('p-points-' + comment_id);

    button.style.display = 'none';
    br.style.display = 'none';
    points.style.display = 'none';
    hidden_text.style.display = 'contents';
}


function moreButtonPP(comment_id) {
    var button = document.getElementById('text-p-' + comment_id);
    var points = document.getElementById('points-p-' + comment_id);
    var hidden_text = document.getElementsByClassName('text-p-hidden-' + comment_id);

    for (let item of hidden_text) {
        item.style.display = 'block';
    }
    button.style.display = 'none';
    points.style.display = 'none';
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
    document.addEventListener('mouseover', EasyTogglerHandler);
    function EasyTogglerHandler(event){
        const EY_BTN = event.target.closest('[data-easy-toggle]');
        if(EY_BTN)
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

        if (!EY_BTN)
        {
            let ey_rcoe_block_targets = document.querySelectorAll('[data-easy-rcoe]');

            Array.from(ey_rcoe_block_targets).forEach.call(ey_rcoe_block_targets, function(ey_rcoe_block_target){
                let ey_rcoe_block = ey_rcoe_block_target.getAttribute('data-easy-toggle'),
                    ey_rcoe_block_class = ey_rcoe_block_target.getAttribute('data-easy-class');

                    if(!event.target.closest(ey_rcoe_block))
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


$(document).ready(function () {
    $(".comment-form").submit(function(event) {
        addComment(jQuery(this).attr('_post'));
        event.preventDefault();
    });

    $("#qaa-answer-form").submit(function(event) {
        addAnswer($("#qaa-answer-form").attr('_question'));
        event.preventDefault();
    });

    $(".qaa-comment-form").submit(function(event) {
        answer_id = $(event.currentTarget).attr('__answer');
        addQAAComment(answer_id);
        event.preventDefault();
    });

    $(".main-comment-union").hover(
        function() {
            if ($(this).attr('comment_liked') == 'False') {
                $ ('#main-likes-' + $(this).attr('comment_id')).css({'visibility': 'visible', 'opacity': '1'})
                }
            $ ('#delete-' + $(this).attr('comment_id')).css({'visibility': 'visible', 'opacity': '1'})
        }, function() {
            if ($(this).attr('comment_liked') == 'False') {
                $ ('#main-likes-' + $(this).attr('comment_id')).css({'visibility': 'hidden', 'opacity': '0'})
            }
            $ ('#delete-' + $(this).attr('comment_id')).css({'visibility': 'hidden', 'opacity': '0'})
        }
       );
});

function addComment(post_id) {
    var curScroll = $(window).scrollTop(),
    curHeight = $('body').height(), newHeight;
    var form = $("#comment-form-" + post_id);
    $.ajax({
        url: '/add_comment/' + post_id,
        type: 'POST',
        data: form.serialize(),
        success: function(response) {
            if (response.result == 'success') {
                post =  $("#post-" + post_id);
                comments = $('.main-post-comments:first');
                new_hr = $('<hr class="main-hr-for-comments">');
                string = `
                <div id='comment-${response.id}' comment_id="${response.id}" comment_liked='False' class="main-comment-union">
                    <div class="main-post-comment">
                        <i class="fa fa-user-circle main-comment-a-ava main-white-font-color" aria-hidden="true"></i>
                        <div class="main-comment-data">
                            <div class='df-jc-sb'>
                                <b class="main-comment-username main-strong">${response.author}</b>
                                <i id="delete-${response.id}" class="fas fa-times main-white-font-color" style="visibility: hidden; opacity: 0;" onclick="deleteComment(${response.id})"></i>
                            </div>
                            <b class="main-comment-text"></b>
                        </div>
                    </div>
                    <div class="main-comment-content">
                        <p style="color: #e6e9ed70;margin-bottom: 0em;font-size: 0.85em;">${response.datetime}</p>
                        <a id='main-likes-${response.id}' class="main-likes" onclick="likeComment(${response.id})" style="visibility: hidden;opacity: 0;">
                            <span id="likes-${response.id}" class="main-likes-num"></span>
                            <i id='heart-${response.id}' class="fa fa-heart main-like-icon"></i>
                        </a>
                    </div>
                 </div>
                `
                var new_comment = $(string);
                $('.main-comment-text', new_comment).text(response.text.replace(/\r?\n|\r/g, "<br>"));
                var hr = $('<hr class="main-hr-for-comments">');
                if (!response.is_first) {
                    hr.appendTo('#main-post-comments-' + post_id);
                }
                new_comment.appendTo('#main-post-comments-' + post_id);
                document.getElementById('comment-post-' + post_id).innerHTML = '';

                newHeight = $('body').height();

                $('[comment_id=' + response.id + ']').hover(
                    function() {
                        if ($(this).attr('comment_liked') == 'False') {
                            $ ('#main-likes-' + $(this).attr('comment_id')).css({'visibility': 'visible', 'opacity': '1'})
                        }
                            $ ('#delete-' + $(this).attr('comment_id')).css({'visibility': 'visible', 'opacity': '1'})
                    }, function() {
                        if ($(this).attr('comment_liked') == 'False') {
                            $ ('#main-likes-' + $(this).attr('comment_id')).css({'visibility': 'hidden', 'opacity': '0'})
                        }
                            $ ('#delete-' + $(this).attr('comment_id')).css({'visibility': 'hidden', 'opacity': '0'})
                    }
               );
                scrollTo(0, curScroll + (newHeight - curHeight));
            }
        }
    });
}


function replaceQaaCommentText(qaa_answer_id) {
    var flex = document.getElementById('qaa-answer-comments-hidden-input-' + qaa_answer_id);
    var div = document.getElementById('qaa-answer-comment-input-' + qaa_answer_id);
    flex.value = div.innerText.replace(/\r?\n|\r/g, "\\n");
}


function addAnswer(question_id) {
    var curScroll = $(window).scrollTop(),
    curHeight = $('body').height(), newHeight;
    var form = $("#qaa-answer-form");
    $.ajax({
        url: '/add_answer/' + question_id,
        type: 'POST',
        data: form.serialize(),
        success: function(response) {
            if (response.result == 'success') {
                $('.main-qaa-error').hide();
                string = `
                <div id="qaa-answer-${response.id}">
                    <div class="main-qaa-user-data-comment">
                        <a href="/profile/${response.author}">
                            <i class="fa fa-user-circle main-post-item i-post man-qaa-ava-b" style="margin: 0 auto" aria-hidden="true"></i>
                            <span>${response.name}</span>
                        </a>
                    </div>
                    <div class="grid-answer">
                        <div class="main-comment-vote">
                            <i id='up-arrow-c-${response.id}' class="fa fa-arrow-up main-arrow-c" aria-hidden="true" onclick="qaa_vote_a_c(${response.id}, true)"></i>
                            <span id="rating-qaa-span-c-${response.id}">${response.rating}</span>
                            <i id="down-arrow-c-${response.id}" class="fa fa-arrow-down main-arrow-c" aria-hidden="true" onclick="qaa_vote_a_c(${response.id}, false)"></i>
                        </div>
                        <div class="grid-answer-data">
                            <span class="answers-pre"></span>
                        </div>
                    </div>
                    <div class="qaa-answers-comments">
                    </div>
                    <form id='qaa-comment-${response.id}' class="qaa-comment-form" method="post" enctype=multipart/form-data action="/add_qaa_comment/${response.id}">
                        <input id="csrf_token" name="csrf_token" type="hidden" value="IjFiMWE4ZDBhNDNlOTgwODdjMTU3ZWM0ZjM2OGQ4ODlhNDBiODRkYTAi.YZqT-w.rg4mJCYR1ypsfiGOqsqko_otl1Y">
                        <input id="qaa-answer-comments-hidden-input-${response.id}" name="text" required="" style="display: none" type="text">
                        <div id='qaa-answer-comment-input-${response.id}' contenteditable="true" class="main-qaa-comment-input" placeholder="write comment..."></div>
                        <input class="qaa-comment-btn" id="submit" name="submit" onclick="replaceQaaCommentText(${response.id})" type="submit" value="Comment">
                        <small id="main-qaa-c-error-${response.id}" class='main-qaa-c-error'></small>
                    </form>
                </div>
                `
                var new_answer = $(string);
                $('.answers-pre', new_answer).text(response.text.replace(/\r?\n|\r/g, "<br>"));
                if (response.author_of_qaa) {
                    fa_check = $("<i id='fa-check-${response.id}' class='fa fa-check' aria-hidden='true' onclick='mark_as_right(${response.q_id},${response.id})'></i>")
                    $('.main-comment-vote', new_answer).append(fa_check);
                }
                new_answer.appendTo('#main-answers');
                $('#answer-form').val('');
            }
            else {
                $('.main-qaa-error').show();
                $('.main-qaa-error').text(response.result);
            }
            newHeight = $('body').height();
            scrollTo(0, curScroll + (newHeight - curHeight));
        }
    });
}

function addQAAComment(answer_id) {
    var curScroll = $(window).scrollTop(),
    curHeight = $('body').height(), newHeight;
    var form = $("#qaa-comment-" + answer_id);
    $.ajax({
        url: '/add_qaa_comment/' + answer_id,
        type: 'POST',
        data: form.serialize(),
        success: function(response) {
            if (response.result == 'success') {
                $('#main-qaa-c-error-' + answer_id).hide()
                $('#s-a-b-' + answer_id).click();
                string = `
                <div class="qaa-comment">
                    <span class='qaa-c-t'></span>
                    <a href="/profile/${response.author}" class="qaa-comment-data">
                        <small>${response.datetime} commented by &mdash;&ensp;</small>
                        <span>${response.user}</span>
                    </a>
                </div>
                `
                var new_comment = $(string);
                $('.qaa-c-t', new_comment).text(response.text.replace(/\r?\n|\r/g, "<br>"));
                new_comment.appendTo('#qaa-comments-' + answer_id);
                $('#qaa-answer-comment-input-' + answer_id).text('');
            }
            else {
                $('#main-qaa-c-error-' + answer_id).show()
                $('#main-qaa-c-error-' + answer_id).text(response.result);
            }
            newHeight = $('body').height();
            scrollTo(0, curScroll + (newHeight - curHeight));
        }
    });
}

function show_hidden_qaa_comments(id) {
    $(".qaa-comment-hidden").each(function (i, elm){
        if ($(elm).attr('answer') == id) {
            $(elm).removeClass('qaa-comment-hidden');
        }
    });
    $('#s-a-b-' + id).hide()
}

function qaa_vote_a_c(id, bool_) {
    if (bool_) {
        var rating = 1
    }
    else {
        var rating = 0
    }
    $.ajax({
        url: '/like/qaa_comment/' + id + '/' + rating,
        type: 'GET',
        success: function(response) {
            if (response.result == 'success') {
                span = document.getElementById('rating-qaa-span-c-' + id);
                span.innerHTML = response.rating;
                if (response.cancel == 'True') {
                    if (response.double == 'True') {
                        if (rating) {
                            arrow_up = document.getElementById('up-arrow-c-' + id);
                            arrow_dn = document.getElementById('down-arrow-c-' + id);
                            arrow_up.classList.add('main-qaa-selected');
                            arrow_dn.classList.remove('main-qaa-selected');
                        }
                        else {
                            arrow_up = document.getElementById('up-arrow-c-' + id);
                            arrow_dn = document.getElementById('down-arrow-c-' + id);
                            arrow_dn.classList.add('main-qaa-selected');
                            arrow_up.classList.remove('main-qaa-selected');
                        }
                    }
                    else {
                        if (rating) {
                            arrow = document.getElementById('up-arrow-c-' + id);
                            arrow.classList.remove('main-qaa-selected');
                        }
                        else {
                            arrow = document.getElementById('down-arrow-c-' + id);
                            arrow.classList.remove('main-qaa-selected');
                        }
                    }
                }
                else {
                    if (rating) {
                        arrow = document.getElementById('up-arrow-c-' + id);
                        arrow.classList.add('main-qaa-selected');
                    }
                    else {
                        arrow = document.getElementById('down-arrow-c-' + id);
                        arrow.classList.add('main-qaa-selected');
                    }
                }
            }
        }
    });
}


function mark_as_right(question_id, answer_id) {
    $.ajax({
        url: '/mark_as_right/' + question_id + '/' + answer_id,
        type: 'GET',
        success: function(response) {
            if (response.result == 'success') {
                if (response.canceled == 'False') {
                    $('.fa-check').each(function (i, elm) {
                        if ($(elm).attr('id') != 'fa-check-' + answer_id) {
                            $(elm).hide();
                        }
                        else {
                            $(elm).addClass('fa-check-right')
                        }
                    });
                    $('#qaa-answer-' + answer_id).addClass('right-answer');
                    }
                else {
                    $('.fa-check').each(function (i, elm) {
                        if ($(elm).attr('id') != 'fa-check-' + answer_id) {
                            $(elm).show();
                        }
                        else {
                            $(elm).removeClass('fa-check-right')
                        }
                    });
                    $('#qaa-answer-' + answer_id).removeClass('right-answer');
                }
                }
        }
    });
}


function deletePost(post_id) {
    $.ajax({
        url: '/delete_post/' + post_id,
        type: 'DELETE',
        success: function() {
            post = document.getElementById('post-' + post_id);
            var div = document.createElement('div');
            div.classList.add("main-deleted-post");

            span = document.createElement('span');
            span.innerHTML = 'Once, a long time ago, there was a post here...'
            span.classList.add('main-deleted-span');

            div.appendChild(span)

            post.replaceWith(div);

            last = -1;
        }
    });
}

function deleteComment(id) {
    $.ajax({
        url: '/delete_comment/' + id,
        type: 'DELETE',
        success: function() {
            post = document.getElementById('comment-' + id);
            var div = document.createElement('div');
            div.classList.add("main-deleted-post");

            span = document.createElement('span');
            span.innerHTML = 'Once, a long time ago, there was a comment here...'
            span.classList.add('main-deleted-span');

            div.appendChild(span)

            post.replaceWith(div);
        }
    });
}

function likeComment(id) {
    $.ajax({
        url: '/like/comment/' + id,
        type: 'GET',
        success: function(response) {
            heart = document.getElementById('heart-' + id);
            span = document.getElementById('likes-' + id);
            if (response.result == 'add') {
                if (!span.innerHTML) {
                    span.innerHTML = '1';
                }
                else {
                    span.innerHTML = parseInt(span.innerHTML) + 1;
                }
                span.classList.add('main-already-liked');
                heart.classList.add('main-already-liked');
                $('[comment_id=' + id + ']').attr('comment_liked', 'True');
            }
            else if (response.result == 'cancel') {
                if (parseInt(span.innerHTML) - 1 == 0) {
                    span.innerHTML = '';
                }
                else {
                    span.innerHTML = parseInt(span.innerHTML) - 1;
                }
                span.classList.remove('main-already-liked');
                heart.classList.remove('main-already-liked');
                $('[comment_id=' + id + ']').attr('comment_liked', 'False');
            }
        }
    });
}

function from_text_to_tags() {
    var text = document.getElementById('main-qaa-content').innerText.trim();
    const regex = /(?:^|[^\\])```(.*?)```/gs;
    const searchRegExp = /\\```/g;
    const replaceWith_ = '```';
    let new_arr = [];
    var last_num = 0;
    var arr = Array.from(text.matchAll(regex), (x) => x[1]);
    arr.forEach(function(item, i, arr) {
        span = document.createElement('span');
        index = text.indexOf("```" + item + "```");
        span.innerText = text.substring(last_num, index).replace(searchRegExp, replaceWith_);
        last_num = index + item.length + 6;
        if (span.innerText.trim()) {
            new_arr.push(span);
        }
        code = document.createElement('p');
        code.classList.add('code');
        code.classList.add('main-w-w');
        code.innerText = item.trim();
        new_arr.push(code);
    });
    span = document.createElement('span');
    span.innerText = text.substring(last_num).replace(searchRegExp, replaceWith_);
    new_arr.push(span);
    document.getElementById('main-qaa-content').innerHTML = '';
    new_arr.forEach(function(item, i, arr) {
        document.getElementById('main-qaa-content').appendChild(item);
    });

}

function qaa_vote(id, bool_) {
    if (bool_) {
        var rating = 1
    }
    else {
        var rating = 0
    }
    $.ajax({
        url: '/like/qaa_post/' + id + '/' + rating,
        type: 'GET',
        success: function(response) {
            if (response.result == 'success') {
                span = document.getElementById('rating-qaa-span-' + id);
                span.innerHTML = response.rating;
                if (response.cancel == 'True') {
                    if (response.double == 'True') {
                        if (rating) {
                            arrow_up = document.getElementById('up-arrow-' + id);
                            arrow_dn = document.getElementById('down-arrow-' + id);
                            arrow_up.classList.add('main-qaa-selected');
                            arrow_dn.classList.remove('main-qaa-selected');
                        }
                        else {
                            arrow_up = document.getElementById('up-arrow-' + id);
                            arrow_dn = document.getElementById('down-arrow-' + id);
                            arrow_dn.classList.add('main-qaa-selected');
                            arrow_up.classList.remove('main-qaa-selected');
                        }
                    }
                    else {
                        if (rating) {
                            arrow = document.getElementById('up-arrow-' + id);
                            arrow.classList.remove('main-qaa-selected');
                        }
                        else {
                            arrow = document.getElementById('down-arrow-' + id);
                            arrow.classList.remove('main-qaa-selected');
                        }
                    }
                }
                else {
                    if (rating) {
                        arrow = document.getElementById('up-arrow-' + id);
                        arrow.classList.add('main-qaa-selected');
                    }
                    else {
                        arrow = document.getElementById('down-arrow-' + id);
                        arrow.classList.add('main-qaa-selected');
                    }
                }
            }
        }
    });
}