
const forms = document.querySelector(".forms"),
    pwShowHide = document.querySelectorAll(".eye-icon"),
    error = document.getElementById('error'),
    passMatch = document.getElementById("spass2"),
    passError = document.getElementById("p-error");
passMatch.addEventListener("input", passwordMatch);

function passwordMatch() {
    smail = document.getElementById("smail").value;
    pss1 = document.getElementById("spass1").value;
    pss2 = document.getElementById("spass2").value;

    if (pss2.length != 0) {
        if (pss1 != pss2) {
            passError.innerHTML = "Passwords don't match";
            return false;

        }
        passError.innerHTML = "";
        return true;
    };
};


pwShowHide.forEach(eye => {
    eye.addEventListener("click", () => {

        let pwState = eye.parentElement.querySelectorAll(".password");
        pwState.forEach(password => {
            if (password.type === "password") {
                password.type = "text";
                eye.classList.replace("bxs-hide", "bxs-show");
                return;
            }
            password.type = "password";
            eye.classList.replace("bxs-show", "bxs-hide");
        });

    });
});

