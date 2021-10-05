function addPost() {
    var input = document.getElementById("main-post-ask-btn");
    var div = document.createElement('div');
    div.setAttribute("contentEditable", true);
    div.id = "main-post-input";
    div.class = "main-post-item";
    input.replaceWith(div);
    div.focus();
}
