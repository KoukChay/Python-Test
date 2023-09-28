
const forms = document.querySelector(".forms"),
    login = document.getElementById('login'),
    signUp = document.getElementById('signUp'),
    pwShowHide = document.querySelectorAll(".eye-icon"),
    error = document.getElementById('error'),
    passMatch = document.getElementById("spass2"),
    passError = document.getElementById("p-error"),
    popUp = document.getElementById("pop"),
    okButton = document.getElementById("ok"),
    links = document.querySelectorAll(".link");
let smail = "";
let pss1 = "";
let pss2 = "";
let lmail = "";
let lpass = "";
let no = 0;
let user = {};
passMatch.addEventListener("input", passwordMatch);
function passwordMatch() {
    smail = document.getElementById("semail").value;
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

links.forEach(link => {
    link.addEventListener("click", e => {
        e.preventDefault();
        forms.classList.toggle("show-hide");

    });
});

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

// localStorage.clear();
// sessionStorage.clear();


//signUp.addEventListener("submit", function (e) {
//    e.preventDefault();
//    let isMatch = passwordMatch();
//    let storedUser = localStorage.getItem('user');
//    user = JSON.parse(storedUser) || {};
//    if (isMatch) {
//
//
//        if (user.length === 0) {
//            no = 0;
//            newUser = { email: smail, password: pss1, money: 0 };
//            user[no] = newUser;
//            localStorage.setItem('user', JSON.stringify(user));
//            forms.classList.toggle("pop-up");
////            popUp.innerHTML = "You are Signed Up!";
//        }
//        else {
//            for (let i in user) {
//                let n_email = user[i]["email"];
//                if (n_email == smail) {
//                    forms.classList.toggle("pop-up");
//                    popUp.innerHTML = "Email already exist!";
//                    return;
//                }
//                no = parseInt(`${i}`);
//            };
//            no += 1;
//            newUser = { email: smail, password: pss1, money: 0 };
//            user[no] = newUser;
//            localStorage.setItem('user', JSON.stringify(user));
//            forms.classList.toggle("pop-up");
////            popUp.innerHTML = "You are Signed Up!";
//            return;
//
//        }
//    }
//
//
//
//});
//
//login.addEventListener("submit", function (e) {
//    e.preventDefault();
//    let lmail = document.getElementById("linput").value;
//    let lpass = document.getElementById("lpss").value;
//    let storedUser = localStorage.getItem('user');
//    if (storedUser) {
//        user = JSON.parse(storedUser);
//        for (let i in user) {
//            let email = user[i]["email"];
//            let password = user[i]["password"];
//            if (email == lmail && password == lpass) {
//                sessionStorage.setItem('luser', JSON.stringify(user[i]));
//                window.location.href = 'userpf/';
//
//                return;
//            }
//            error.innerHTML = "Email or password incorrect!";
//        }
//    }
//    else {
//        error.innerHTML = "Email or password incorrect!";
//    }
//
//});
//
//const f_pass = document.querySelector('.forgot-pass');
//f_pass.addEventListener("click", () => {
//    forms.classList.toggle("lpop-up");
//
//    okButton.addEventListener("click", function (e) {
//        e.preventDefault();
//        let c_email = document.getElementById("cemail").value;
//        let npass = document.getElementById("npass").value;
//        let storedUser = localStorage.getItem('user');
//        user = JSON.parse(storedUser);
//        for (let i in user) {
//            if (user[i]["email"] == c_email) {
//                user[i]["password"] = npass;
//                localStorage.setItem('user', JSON.stringify(user));
//                forms.classList.toggle("pop-up");
//                popUp.innerHTML = "Yor password has been changed!";
//                return;
//            }
//
//        };
//        forms.classList.toggle("pop-up");
//        popUp.innerHTML = "Email doesn't Exist!";
//
//    });
//
//});
