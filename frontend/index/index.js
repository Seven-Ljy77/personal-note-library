const base_url = "https://notes.desktop-pet.cn";

document.getElementById("login-btn").addEventListener(
    "click",
    login
);

document.getElementById("register-btn").addEventListener(
    "click",
    register
);

async function login() {
    const username = document.getElementById("username-input").value;
    const password = document.getElementById("password-input").value;

    try {
        const response = await fetch(base_url + "/api/auth/login" , {
            method : "POST",
            headers : {
                "content-type" : "application/json"
            },
            body : JSON.stringify({
                "username" : username ,
                "password" : password
            })
        });

        if (!response.ok) {
            let result = await response.json();
            let detail = result.detail || "登陆失败请检查网络"
            throw new Error(detail);
        }

        let result = await response.json();

        localStorage.setItem("access_token" , result.access_token);
        localStorage.setItem("refresh_token" , result.refresh_token);
        localStorage.setItem("token_type" , result.token_type);

        window.alert("登录成功 !");

        document.getElementById("username-input").value = "";
        document.getElementById("password-input").value = "";

        window.location.href = "../mine/mine.html";
    } catch (error) {
        window.alert(error.message);
    }
}

async function register() {
    const username = document.getElementById("username-input").value;
    const password = document.getElementById("password-input").value;
    

    try {
        const response = await fetch(base_url + "/api/auth/register" , {
            method : "POST",
            headers : {
                "content-type" : "application/json"
            },
            body : JSON.stringify({
                "username" : username ,
                "password" : password
            })
        });

        if (!response.ok) {
            let result = await response.json();
            let detail = result.detail || "注册失败请检查网络";
            throw new Error(detail);
        }

        window.alert("注册成功");

        document.getElementById("login-btn").click();
    } catch(error) {
        window.alert(error.message);
    }
}