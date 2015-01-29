// JavaScript Document
function HelloWorld(n, o)
{
	alert(o);
}

function AjaxGET(url, fn)
{
  $.get(url, function(data) {
    var args = new Array();	
    //for (var i = 1; i < arguments.length; i++)
    //    args.push(arguments[i]);
    args.push(arguments[0]);
    window[fn].apply(this, args);

  });
}

function ShowInfo(msg)
{
  AjaxGET('/Staff/login', HelloWorld(10, 20));
  /*$('#AlertMessage').html("Hello World");
  $('#Alert').toggle();
  mainfunc(HelloWorld());*/
}

