
const pwShowHide = document.querySelectorAll(".eye-icon");
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

