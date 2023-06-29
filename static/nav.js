var that;
class AsideNav {//定义 AsideNav 类并传入类名作为参数：
    constructor(className) {
        this.nav = document.querySelector(className);

        this.lis = this.nav.querySelectorAll('.nav-list .item');
        this.parentNav = this.nav.querySelectorAll('.nav-list .item .parentNav');
        that = this;
        this.init();
    }
    //初始化 AsideNav 类的实例，并为每个具有子菜单的导航项添加点击事件处理程序：
    init() {
        for (var i = 0; i < this.parentNav.length; i++) {
            this.parentNav[i].onclick = this.toggleNav;
        }
    }//定义 clearClass 方法，用于清除所有导航项的激活状态
    clearClass() {
        for (var i = 0; i < this.lis.length; i++) {
            this.lis[i].className = "item";
        }
    }//定义 toggleNav 方法，用于切换导航项的激活状态
    toggleNav() {
        var li = this.parentNode;
        if (li.classList.contains('active')) {
            li.classList.remove('active');
        } else {
            that.clearClass();
            li.classList.add('active');
        }
    }
}//创建一个 AsideNav 类的实例，并传入对应的选择器
var asideNav = new AsideNav('.aside-nav');