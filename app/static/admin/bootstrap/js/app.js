/**
 * Created by chenjl on 2018/1/29.
 */

$(document).ready(function(){
    $("#tableSort tr").each(function(){
        $(this).find("td:nth-child(1)").css({"width":"16%"});
        $(this).find("td:nth-child(2)").css({"text-align":"left","padding":"18px 0px","width":"25%"});
        $(this).find("td:nth-child(3)").css({"font-weight":"bold","font-size":"14px","padding":"0px","width":"40%"});
        $(this).find("td:nth-child(2)").addClass("icon-zhandian");
        $(this).find("td:nth-child(4)").html("<i class='iconfont fontsize' onclick='qingling(this)'>&#xe62f;</i>");
        $(this).find("td:nth-child(4)").css({"color":"#ccc","font-size":"18px","padding":"4px 0px 0px 16px"});
    })
    $(".rleft").addClass('icon-xianlu');
    $('.list-top span i:first-child').addClass('icon-zhi');
    $(".list-top span:nth-child(2)").css({"font-weight":"bold"});


    $("#moren").click(function(){
        $(this).addClass("Selected");
        $(this).removeClass("kong");
        $("#site").addClass("kong");
        $("#number").addClass("kong");
    });
    $("#site").click(function(){
        $(this).addClass("Selected");
        $(this).removeClass("kong");
        $("#moren").addClass("kong");
        $("#number").addClass("kong");
    });
    $("#number").click(function(){
        $(this).addClass("Selected");
        $(this).removeClass("kong");
        $("#moren").addClass("kong");
        $("#site").addClass("kong");
    });

    $("input").focus(function(){
        $(this).css("background-color","#f5f5f5");
    });
    $("input").blur(function(){
        $(this).css("background-color","#ffffff");
    });

    $(".spinnerExample").focus(function(){
        $(this).text("");
    });

});


    function jian(a){
        var nextnode = a.nextElementSibling;//��ȡ��һ���ڵ�
              //alert(nextnode.className);
    //    alert(nextnode.className);
        var a = parseInt(nextnode.value);//parseInt()�����ɽ���һ���ַ�����������һ������
        a = a-0.5;//����   a -= 1;
    //            a = a > 0 ? a : 0;//��ֹ��Ϊ������
        if(a<0.5){
            a = 0
        };//��ֹ��Ϊ������
        nextnode.value = a;
    };
    function jia(a){
        var previousnode = a.previousElementSibling;
        var a = parseInt(previousnode.value)//parseInt()�����ɽ���һ���ַ�����������һ������
        a = a+1;//����   a -= 1;
        previousnode.value = a;
    };



