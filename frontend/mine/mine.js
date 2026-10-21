import { trans_list_to_html, trans_obj_to_html , display } from "../utils.js";
import { request } from "./api.js";

export const base_url = "https://notes.desktop-pet.cn";

document.getElementById("user-profile-btn").addEventListener(
    "click" , 
    get_user_profile
);
document.getElementById("note-list-btn").addEventListener(
    "click",
    get_note_list
);
document.getElementById("create-note-btn").addEventListener(
    "click",
    create_note
);
document.getElementById("get-note-btn").addEventListener(
    "click",
    get_note
);
document.getElementById("patch-note-btn").addEventListener(
    "click",
    patch_note
);
document.getElementById("delete-note-btn").addEventListener(
    "click",
    delete_note
);
document.getElementById("change-pinned-status-btn").addEventListener(
    "click",
    change_pinned_status
);
document.getElementById("logout-btn").addEventListener(
    "click",
    logout
);

async function get_user_profile() {
    const response = await request(base_url + "/api/users/me" , {
        method : "GET",
        headers : {
            "content-type" : "application/json"
        }
    });

    if (response == -1) {
        window.alert("登录状态失效，请重新登陆 !");
        window.location.href = "../index/index.html"
        return;
    }
    if (!response.ok) {
        const result = await response.json();
        window.alert(result.detail || "错误 !");
        return;
    }

    const result = await response.json();

    display(trans_obj_to_html(result));
}

async function get_note_list() {
    const response = await request(base_url + "/api/notes" , {
        method : "GET",
        headers : {
            "content-type" : "application/json"
        }
    });

    if (response == -1) {
        window.alert("登录状态失效，请重新登陆 !");
        window.location.href = "../index/index.html"
        return;
    }
    if (!response.ok) {
        const result = await response.json();
        window.alert(result.detail || "错误 !");
        return;
    }

    const result = await response.json();

    if (result.length == 0) 
        display("Note List Is Empty");
    else
        display(trans_list_to_html(result));
}

async function create_note() {
    let title = document.getElementById("title-input").value;
    let content = document.getElementById("content-input").value;

    if (!title || !content) {
        window.alert("title 和 content 不能为空");
        return;
    }

    const response = await request(base_url + "/api/notes" , {
        method : "POST",
        headers : {
            "content-type" : "application/json"
        },
        body : JSON.stringify({
            "title" : title,
            "content" : content
        })
    });
    

    if (response == -1) {
        window.alert("登录状态失效，请重新登陆 !");
        window.location.href = "../index/index.html"
        return;
    }
    if (!response.ok) {
        const result = await response.json();
        window.alert(result.detail || "错误 !");
        return;
    }
    
    window.alert("创建文章成功 !");
}

async function get_note() {
    let note_id = document.getElementById("id-input").value;

    if (!note_id) {
        window.alert("note id 不能为空 !");
        return;
    }

    const response = await request(base_url + `/api/notes/${note_id}` , {
        method : "GET"
    });

    if (response == -1) {
        window.alert("登录状态失效，请重新登陆 !");
        window.location.href = "../index/index.html"
        return;
    }
    if (!response.ok) {
        const result = await response.json();
        window.alert(result.detail || "错误 !");
        return;
    }

    const result = await response.json();

    display(trans_obj_to_html(result));
}

async function patch_note() {
    let note_id = document.getElementById("id-input").value;
    let title = document.getElementById("title-input").value;
    let content = document.getElementById("content-input").value;

    if (!note_id) {
        window.alert("note id 不能为空");
        return;
    }

    if (!title && !content) {
        window.alert("title 和 content 不能同时为空 !");
        return;
    }

    const response = await request(base_url + `/api/notes/${note_id}` , {
        method : "PATCH",
        headers : {
            "content-type" : "application/json"
        },
        body : JSON.stringify({
            "title" : title,
            "content" : content
        })
    });
    

    if (response == -1) {
        window.alert("登录状态失效，请重新登陆 !");
        window.location.href = "../index/index.html"
        return;
    }
    if (!response.ok) {
        const result = await response.json();
        window.alert(result.detail || "错误 !");
        return;
    }
    
    window.alert("修改文章成功 !")
}

async function delete_note() {
    let note_id = document.getElementById("id-input").value;

    if (!note_id) {
        window.alert("note id 不能为空");
        return;
    }

    const response = await request(base_url + `/api/notes/${note_id}` , {
        method : "DELETE"
    });
    

    if (response == -1) {
        window.alert("登录状态失效，请重新登陆 !");
        window.location.href = "../index/index.html"
        return;
    }
    if (!response.ok) {
        const result = await response.json();
        window.alert(result.detail || "错误 !");
        return;
    }

    window.alert("删除文章成功 !");
}

async function change_pinned_status() {
    let note_id = document.getElementById("id-input").value;

    if (!note_id) {
        window.alert("note id 不能为空");
        return;
    }

    const response = await request(base_url + `/api/notes/${note_id}` , {
        method : "POST"
    });
    

    if (response == -1) {
        window.alert("登录状态失效，请重新登陆 !");
        window.location.href = "../index/index.html"
        return;
    }
    if (!response.ok) {
        const result = await response.json();
        window.alert(result.detail || "错误 !");
        return;
    }

    window.alert("修改文章置顶状态成功 !");
}

async function logout() {
    let refresh_token = localStorage.getItem("refresh_token");

    if (!refresh_token) {
        window.alert("登录状态失效，请重新登陆 !");
        window.location.href = "../index/index.html"
        return;
    }

    const response = await request(base_url + `/api/auth/logout` , {
        method : "POST",
        headers : {
            "content-type" : "application/json"
        },
        body : JSON.stringify({
            "refresh_token" : refresh_token
        })
    });
    

    if (response == -1) {
        window.alert("登录状态失效，请重新登陆 !");
        window.location.href = "../index/index.html"
        return;
    }
    if (!response.ok) {
        const result = await response.json();
        window.alert(result.detail || "错误 !");
        return;
    }

    window.alert("退出登录成功 !");
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("token_type");
    window.location.href = "../index/index.html"
}