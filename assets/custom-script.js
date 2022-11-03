(function($)
{
    var baseDivCSS;
    $(document).ready( function()
    {
        var checkExist = setInterval(() => {
            console.log("check div");
            div = $('#dropdiv');
            if (div.length) {
                console.log("Div initialised");
                scroll(div);
                clearInterval(checkExist);
            }
        }, 100)
    });

    function scroll(div) {
        var elementPosTop = div.offset().top;
        $(window).scroll(function()
        {
            var wintop = $(window).scrollTop(), docheight = $(document).height(), winheight = $(window).height();
            //if top of element is in view
            if (wintop > elementPosTop)
            {
                //always in view
//                div.css({ "position":"fixed", "top":"0px", "z-index": 9999, "width": "100%",
//                    "background-color": "lightgrey", "padding": "20px"
//                });
                div.removeClass("select-normal");
                 div.addClass("select-hang");
            }
            else
            {
                //reset back to normal viewing
                //div.css({ "position":"inherit" });
                 div.addClass("select-normal");
                 div.removeClass("select-hang");
            }
        });
    }
})(jQuery);