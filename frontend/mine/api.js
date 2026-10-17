import { base_url } from "./mine.js";

export const login_status_invalid = -1;
export const request_success = 1;

function if_token_exist() {
    let access_token = localStorage.getItem("access_token");
    let refresh_token = localStorage.getItem("refresh_token");
    let token_type = localStorage.getItem("token_type");

    if (access_token && refresh_token && token_type)
        return true;
    else
        return false;
}

async function refresh() {
    if (!if_token_exist())
        return false;

    let refresh_token = localStorage.getItem("refresh_token");

    const response = await fetch(base_url + "/api/auth/refresh" , {
        method : "POST",
        headers : {
            "content-type" : "application/json"
        },
        body : JSON.stringify({
            "refresh_token" : refresh_token
        })
    });

    if (!response.ok) 
        return false;

    const result = await response.json();

    localStorage.setItem("access_token" , result.access_token);
    localStorage.setItem("token_type" , result.token_type);

    return true
}

// 用于请求受保护的接口
export async function request(url , obj) {
    if (!if_token_exist())
        return -1;

    let token_type = localStorage.getItem("token_type");
    let access_token = localStorage.getItem("access_token");

    // 如果没有 headers 字段就添加
    if(!obj.headers)
        obj.headers = {};

    obj["headers"]["Authorization"] = `${token_type} ${access_token}`;

    const response = await fetch(url , obj);

    if (response.ok)
        return response;
    else if (response.status == 401) {
        const status = await refresh();

        if (!status)
            return -1

        return request(url , obj);
    }
    else
        return response;
}