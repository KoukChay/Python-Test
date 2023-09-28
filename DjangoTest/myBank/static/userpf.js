
const container = document.querySelector(".container"),
    showMoney = document.querySelector('.wc');
let menu = document.querySelector(".menu");
let toggle = document.querySelector(".toggle");
let storedUser = JSON.parse(localStorage.getItem('user'));
let loggedInUser = JSON.parse(sessionStorage.getItem('luser'));


if (loggedInUser["money"] == null) {
    showMoney.innerHTML = "Welcome Boss-$" + String(0);
}
else {
    showMoney.innerHTML = "Welcome Boss-$" + String(loggedInUser["money"]);
};


toggle.onclick = function () {
    menu.classList.toggle("active");
};


let deposit = document.querySelector('.deposit');
const popUp = document.getElementById("pop");
const popErr = document.getElementById("pop-err");
deposit.onclick = function () {
    popUp.innerHTML = '<input type="number" placeholder="Enter amount to deposit...."min="1000" step="1000" max="100000" name="amount" id="amount" required></input>';
    container.classList.toggle("pop-up");
    const okButton = document.querySelector('.ok');
    okButton.addEventListener("click", () => {
        let amount = parseInt(document.getElementById('amount').value);
        if (amount || amount > 0) {
            for (let i in storedUser) {
                if (storedUser[i]["email"] == loggedInUser["email"]) {
                    storedUser[i]["money"] += amount;
                    loggedInUser["money"] += amount;
                    localStorage.setItem('user', JSON.stringify(storedUser));
                    sessionStorage.setItem('luser', JSON.stringify(loggedInUser));
                    window.location.href = '../userpf/usrpf.html';
                }
            }
        }
        else {
            popErr.innerHTML = "Please Enter Amount!"
        }
    });
    
};

let userDel = document.querySelector('.fa-user-xmark');
// const popUp = document.getElementById("pop");
// const popErr = document.getElementById("pop-err");
userDel.onclick = function () {
    popUp.innerHTML = '<div style="color: chartreuse;font-size: 18px;">Press "Ok" to delete your account.</div>';
    container.classList.toggle("pop-up");
    const okButton = document.querySelector('.ok');
    okButton.addEventListener("click", () => {
        for (let key in storedUser) {
            if (storedUser[key]["email"] == loggedInUser["email"]) {
                delete storedUser[key];
                localStorage.setItem('user', JSON.stringify(storedUser));
                window.location.href = '../Home/file.html';
            }


        }
    }
    );
    const cancleButton = document.querySelector('.cancle');
    cancleButton.addEventListener("click", () => {
        menu.classList.toggle("active");
    });
};
// localStorage.clear();
// sessionStorage.clear();
const tpopUp = document.getElementById("tpop");
const tpopErr = document.getElementById("tpop-err");
let transFer = document.querySelector('.fa-money-bill-transfer');
transFer.onclick = function () {
    popUp.innerHTML = "Choose Email you want to transfer...";
    container.classList.toggle("pop-up");
    let radioContainer = document.getElementById("radioContainer");

    for (let key in storedUser) {
        if (storedUser[key]["email"] !== loggedInUser["email"]) {
            let radioInput = document.createElement('input');
            radioInput.type = 'radio';
            radioInput.name = 'email';
            radioInput.value = storedUser[key]["email"];
            radioInput.id = `option_${key}`;

            let label = document.createElement('label');
            label.htmlFor = `option_${key}`;
            label.textContent = storedUser[key].email;

            let br = document.createElement('br')

            radioContainer.appendChild(radioInput);
            radioContainer.appendChild(label);
            radioContainer.appendChild(br);
        }
    };

    const okButton = document.querySelector('.ok');
    okButton.addEventListener("click", () => {
        let selectedOption = document.querySelector('input[name="email"]:checked');

        if (selectedOption) {
            let selectedValue = selectedOption.value;
            tpopUp.innerHTML = '<input type="number" placeholder="Enter money to Transfer..."min="1000" step="1000" max="1000000" name="amount" id="amount" required></input>';
            container.classList.toggle("tpop-up");

            const okButton = document.querySelector('.tok');
            okButton.addEventListener("click", () => {
                let amount = parseInt(document.getElementById('amount').value);

                if (amount && amount < loggedInUser["money"]) {
                    for (let i in storedUser) {
                        if (storedUser[i]["email"] == selectedValue) {
                            storedUser[i]["money"] += amount;
                            loggedInUser["money"] -= amount;
                            sessionStorage.setItem('luser', JSON.stringify(loggedInUser));
                        }
                        if (storedUser[i]["email"] == loggedInUser["email"]) {
                            storedUser[i]["money"] -= amount;
                            localStorage.setItem('user', JSON.stringify(storedUser));
                            window.location.href = '../userpf/usrpf.html';
                        }
                    }
                } else {
                    tpopErr.innerHTML = "Not enough money to transfer!"
                }
            });

        } else {
            popErr.innerHTML = "No option selected!"
        }
    });
};



