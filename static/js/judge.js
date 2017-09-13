/**
 * Created by kbsonlong on 2017/9/13.
 */

function check(){
    var usernameValue=window.document.getElementById("username").value;
    var password01=window.document.getElementById("password01").value;
    var password02=window.document.getElementById("password02").value;
    if (usernameValue == "") // 或者是!nameValue
    {
        window.alert("用户名不能为空!");
        return false;
    }
    else if (password01 == "")  // 或者是!nameValue
    {
        window.alert("密码不能为空!");
        return false;
    }

    else if (password01 != password02)  // 或者是!nameValue
    {
        window.alert("密码不一致!");
        return false;
    }

    return true;
}
