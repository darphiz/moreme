jQuery(document).ready(function(a){"use strict";a(".js-clone-nav").each(function(){a(this).clone().attr("class","site-nav-wrap").appendTo(".site-mobile-menu-body")}),setTimeout(function(){var s=0;a(".site-mobile-menu .has-children").each(function(){var e=a(this);e.prepend('<span class="arrow-collapse collapsed">'),e.find(".arrow-collapse").attr({"data-toggle":"collapse","data-target":"#collapseItem"+s}),e.find("> ul").attr({class:"collapse",id:"collapseItem"+s}),s++})},1e3),a("body").on("click",".arrow-collapse",function(s){var e=a(this);e.closest("li").find(".collapse").hasClass("show")?e.removeClass("active"):e.addClass("active"),s.preventDefault()}),a(window).resize(function(){a(this).width()>768&&a("body").hasClass("offcanvas-menu")&&a("body").removeClass("offcanvas-menu")}),a("body").on("click",".js-menu-toggle",function(s){var e=a(this);s.preventDefault(),a("body").hasClass("offcanvas-menu")?(a("body").removeClass("offcanvas-menu"),e.removeClass("active")):(a("body").addClass("offcanvas-menu"),e.addClass("active"))}),a(document).mouseup(function(s){var e=a(".site-mobile-menu");e.is(s.target)||0!==e.has(s.target).length||a("body").hasClass("offcanvas-menu")&&a("body").removeClass("offcanvas-menu")});a(".image-popup").magnificPopup({type:"image",closeOnContentClick:!0,closeBtnInside:!1,fixedContentPos:!0,mainClass:"mfp-no-margins mfp-with-zoom",gallery:{enabled:!0,navigateByImgClick:!0,preload:[0,1]},image:{verticalFit:!0},zoom:{enabled:!0,duration:300}}),a(".popup-youtube, .popup-vimeo, .popup-gmaps").magnificPopup({disableOn:700,type:"iframe",mainClass:"mfp-fade",removalDelay:160,preloader:!1,fixedContentPos:!1});a(".nonloop-block-13").length>0&&a(".nonloop-block-13").owlCarousel({center:!1,items:1,loop:!0,stagePadding:0,margin:0,autoplay:!0,nav:!0,navText:['<span class="icon-arrow_back">','<span class="icon-arrow_forward">'],responsive:{600:{margin:0,nav:!0,items:2},1000:{margin:0,stagePadding:0,nav:!0,items:3},1200:{margin:0,stagePadding:0,nav:!0,items:4}}}),a(".slide-one-item").owlCarousel({center:!1,items:1,loop:!0,stagePadding:0,margin:0,autoplay:!0,pauseOnHover:!1,nav:!0,navText:['<span class="icon-keyboard_arrow_left">','<span class="icon-keyboard_arrow_right">']});a(window).stellar({responsive:!1,parallaxBackgrounds:!0,parallaxElements:!0,horizontalScrolling:!1,hideDistantElements:!1,scrollProperty:"scroll"});a("#date-countdown").countdown("2020/10/10",function(s){a(this).html(s.strftime('<span class="countdown-block"><span class="label">%w</span> weeks </span><span class="countdown-block"><span class="label">%d</span> days </span><span class="countdown-block"><span class="label">%H</span> hr </span><span class="countdown-block"><span class="label">%M</span> min </span><span class="countdown-block"><span class="label">%S</span> sec</span>'))});a(".datepicker").length>0&&a(".datepicker").datepicker()});