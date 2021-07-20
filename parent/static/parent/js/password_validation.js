var checkPassword = (newPass) => {
    // 6-20 chars, at least one numeric, one special
    var paswd=  /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{7,15}$/;
    if(newPass.value.match(paswd)) { 
        return true;
    }
    else { 
        return false;
    }
}

pass = document.getElementById("pass");
repeat = document.getElementById("repeatPass");
submit = document.getElementById("submitBtn");


pass.addEventListener("change", ()=>{
    console.log(checkPassword(pass));
});

// console.log(pass);

// console.log(repeat);
// console.log(checkPassword(pass));
