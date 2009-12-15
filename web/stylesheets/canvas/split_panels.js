
var g_iHeaderHeight;
var g_iLeftDivWidth = 200;		// Initial Width of the Left Div
var g_iBottomDivHeight = 200;	// Initial Height of the Bottom Div
var g_bBarMoving = false;
var g_bVert = false;

function OnLoadIndex()
{
	var title = document.getElementById("title");
	g_iHeaderHeight = parseInt(title.style.height);
	OnResizeIndex();
}

function OnResizeIndex()
{
	var divLeft = document.getElementById("divLeft");
	var divCanvas = document.getElementById("divCanvas");
    var canvas =  document.getElementById("top_viz");
	var code = document.getElementById("code");

	// Width
	var sWidth = new String();
	sWidth = g_iLeftDivWidth.toString();
	sWidth += "px";
	divLeft.style.width = sWidth;

	var iWidth = document.body.clientWidth - g_iLeftDivWidth - 20;
	sWidth = iWidth.toString();	
    canvas.width = iWidth;
    sWidth += "px";
	divCanvas.style.width = sWidth;
    
	code.style.width = sWidth;
	// Height
	var sHeight = new String();
	var iHeight = document.body.clientHeight - g_iHeaderHeight - 13;
	if (iHeight < g_iHeaderHeight + g_iBottomDivHeight - 23)
		iHeight = g_iHeaderHeight + g_iBottomDivHeight - 23;
	sHeight = iHeight.toString();
	sHeight += "px";
	divLeft.style.height = sHeight;

	iHeight = document.body.clientHeight - g_iHeaderHeight - g_iBottomDivHeight - 15;
	if (iHeight < 20)
		iHeight = 20;
	sHeight = iHeight.toString();
	sHeight += "px";
    canvas.height = iHeight;
	divCanvas.style.height = sHeight;

	sHeight = g_iBottomDivHeight.toString();
	sHeight += "px";
	code.style.height = sHeight;

	// VertBar
	var divVertBar = document.getElementById("divVertBar");
	iHeight = document.body.clientHeight - g_iHeaderHeight - 3;
	if (iHeight < g_iHeaderHeight + g_iBottomDivHeight - 10)
		iHeight = g_iHeaderHeight + g_iBottomDivHeight - 10;
	sHeight = iHeight.toString();
	sHeight += "px";
	divVertBar.style.height = sHeight;

	// left
	var sLeft = new String();
	var iLeft = g_iLeftDivWidth + 3;
	sLeft = iLeft.toString();
	sLeft += "px";
	divVertBar.style.left = sLeft;

	// HorzBar
	var divHorzBar = document.getElementById("divHorzBar");

	// width
	iWidth = document.body.clientWidth - g_iLeftDivWidth - 10;
	sWidth = iWidth.toString();
	sWidth += "px";
	divHorzBar.style.width = sWidth;

	iLeft = g_iLeftDivWidth + 3;
	sLeft = iLeft.toString();
	sLeft += "px";
	divHorzBar.style.left = sLeft;

	// top
	var sTop = new String();
	iHeight = document.body.clientHeight - g_iBottomDivHeight - 10;
	if (iHeight < g_iHeaderHeight + 25)
		iHeight = g_iHeaderHeight + 25;
	sTop = iHeight.toString();
	sTop += "px";
	divHorzBar.style.top = sTop;
    
    render();
    
}

function OnMouseDownBar(bVert, evt)
{
	g_bBarMoving = true;
	g_bVert = bVert;
	var e = (window.event) ? window.event : evt;
	e.returnValue = false;
	return false;
}

function OnMouseUpBar()
{
	if (g_bBarMoving)
	{
		g_bBarMoving = false;

		var divPhantomBar = document.getElementById("divPhantomBar");
		if (g_bVert)
		{
			g_iLeftDivWidth = parseInt(divPhantomBar.style.left) - 3;
			if (document.body.clientWidth - g_iLeftDivWidth < 50)
				g_iLeftDivWidth = document.body.clientWidth - 50;
		}
		else
		{	
			g_iBottomDivHeight = document.body.clientHeight - parseInt(divPhantomBar.style.top) - 10;
			if (g_iBottomDivHeight < 20)
				g_iBottomDivHeight = 20;
		}

		divPhantomBar.style.display = 'none';
		OnResizeIndex();
	}
}

function OnMouseMoveBar(evt)
{
	if (g_bBarMoving)
	{
		var e = (window.event) ? window.event : evt;
		ShowPhantomBar(e);
		e.returnValue = false;
		return false;
	}
}

function ShowPhantomBar(e)
{
	var divPhantomBar = document.getElementById("divPhantomBar");
	divPhantomBar.style.display = 'block';

	var sTop = new String();
	var sLeft = new String();
	var iLeft;
	if (g_bVert)
	{
		var iHeight = document.body.clientHeight - g_iHeaderHeight - 3;
		if (iHeight < g_iHeaderHeight + g_iBottomDivHeight - 10)
		iHeight = g_iHeaderHeight + g_iBottomDivHeight - 10;

		var sHeight = new String();
		sHeight = iHeight.toString();
		sHeight += "px";
		divPhantomBar.style.height = sHeight;

		iLeft = e.clientX - 5;
		if (iLeft < 30)
			iLeft = 30;
		sLeft = iLeft.toString();
		sLeft += "px";
		divPhantomBar.style.left = sLeft;
		divPhantomBar.style.width = '5px';

		sTop = g_iHeaderHeight.toString();
		sTop += "px";
		divPhantomBar.style.top = sTop;
	}
	else
	{	
		var iTop = e.clientY - 5;
		if (iTop < g_iHeaderHeight + 20)
			iTop = g_iHeaderHeight + 20;
		sTop = iTop.toString();
		sTop += "px";
		divPhantomBar.style.top = sTop;

		iLeft = g_iLeftDivWidth + 3;
		if (iLeft < 30)
			iLeft = 30;
		sLeft = iLeft.toString();
		sLeft += "px";
		divPhantomBar.style.left = sLeft;

		var sWidth = new String();
		var iWidth = document.body.clientWidth - g_iLeftDivWidth - 10;
		sWidth = iWidth.toString();
		sWidth += "px";
		divPhantomBar.style.width = sWidth;
		divPhantomBar.style.height = '5px';
	}
}
