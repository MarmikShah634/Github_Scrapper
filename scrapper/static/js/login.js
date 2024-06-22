/* document.addEventListener("DOMContentLoaded", ()=>{
    document.getElementById("form").reset();
    let errorElement = document.getElementById('error');    
    let emailPasswordErrorElement = document.getElementById('emailPasswordError');    

    if (errorElement) {

    }

    if (emailPasswordErrorElement && emailPasswordErrorElement.style.visibility !== 'hidden') {
        emailPasswordErrorElement.style = "{% if emailPasswordErrorElement %}color: red;  display:none; visibility:hidden{% endif %}";
    }
}) */

/* window.onload = function(){
    document.getElementById("form").reset();
    let errorElement = document.getElementById('error');    
    let emailPasswordErrorElement = document.getElementById('emailPasswordError');    

    if (errorElement) {
        errorElement.style = "color: red;  display:none; visibility:hidden";
    }

    if (emailPasswordErrorElement) {
        emailPasswordErrorElement.style = "color: red;  display:inline; visibility:visible";
    }
}

document.getElementById("btn").addEventListener("click", ()=>{
    let errorElement = document.getElementById('error');    
    let emailPasswordErrorElement = document.getElementById('emailPasswordError');    

    if (errorElement) {
        errorElement = `{% if error %}
        <p id="error" style="color: red;">You don't have account with us. Please Sign in</p>
        {% endif %}`;
    }

    if (emailPasswordErrorElement) {
        emailPasswordErrorElement = `{% if emailPasswordError %}
        <p id="emailPasswordError" style="color: red;">Email or password is not correct. Please try again.</p>
        {% endif %}`;
    }
}) */