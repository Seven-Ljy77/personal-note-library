export function trans_obj_to_html(obj) {
    let str =  "<table>";
    
    let keys = Object.keys(obj);

    for (let x of keys) {
        str += `<tr>`;
        str += `<td> ${x} </td>`;
        str += `<td> ${obj[x]} </td>`;
        str += `</tr>`;
    }

    str += "</table>";

    return str;
}

export function trans_list_to_html(list) {
    let str = "<ol>";

    for (let x of list)
        str += `<li> ${trans_obj_to_html(x)} </li>`;
    
    str += "</ol>";

    return str;
}

export function display(str) {
    document.getElementById("display").innerHTML = str;
}