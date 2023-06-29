
//获取登录/注册面板相关的 DOM 元素：
const container = document.getElementById('container');
const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
//为注册按钮添加点击事件处理程序，使点击时面板切换到注册状态：
signUpButton.onclick = function() {
    container.classList.add('penal-right-active');
}
//为登录按钮添加点击事件处理程序，使点击时面板切换到登录状态：
signInButton.onclick = function() {
    container.classList.remove('penal-right-active');
}

