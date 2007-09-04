/**
 * Interface Elements for jQuery
 * ImageBox
 *
 * http://interface.eyecon.ro
 *
 * Copyright (c) 2006 Stefan Petre
 * Dual licensed under the MIT (MIT-LICENSE.txt)
 * and GPL (GPL-LICENSE.txt) licenses.
 *
 */

/**
 * This a jQuery equivalent for Lightbox2. Alternative to image popups that will display images in an overlay. All links that have attribute 'rel' starting with 'imagebox' and link to an image will display the image inside the page. Galleries can by build buy giving the value 'imagebox-galname' to attribute 'rel'. Attribute 'title' will be used as caption.
 * Keyboard navigation:
 *  -  next image: arrow right, page down, 'n' key, space
 *  -  previous image: arrow left, page up, 'p' key, backspace
 *  -  close: escape
 *
 * CSS
 *  #ImageBoxOverlay
 *  {
 *    background-color: #000;
 *  }
 *  #ImageBoxCaption
 *  {
 *    background-color: #F4F4EC;
 *  }
 *  #ImageBoxContainer
 *  {
 *    width: 250px;
 *    height: 250px;
 *    background-color: #F4F4EC;
 *  }
 *  #ImageBoxCaptionText
 *  {
 *    font-weight: bold;
 *    padding-bottom: 5px;
 *    font-size: 13px;
 *    color: #000;
 *  }
 *  #ImageBoxCaptionImages
 *  {
 *    margin: 0;
 *  }
 *  #ImageBoxNextImage
 *  {
 *    background-image: url(images/imagebox/spacer.gif);
 *    background-color: transparent;
 *  }
 *  #ImageBoxPrevImage
 *  {
 *    background-image: url(images/imagebox/spacer.gif);
 *    background-color: transparent;
 *  }
 *  #ImageBoxNextImage:hover
 *  {
 *    background-image: url(images/imagebox/next_image.jpg);
 *    background-repeat:  no-repeat;
 *    background-position: right top;
 *  }
 *  #ImageBoxPrevImage:hover
 *  {
 *    background-image: url(images/imagebox/prev_image.jpg);
 *    background-repeat:  no-repeat;
 *    background-position: left bottom;
 *  }
 *
 * @name Imagebox
 * @description This a jQuery equivalent for Lightbox2. Alternative to image popups that will display images in an overlay. All links that have attribute 'rel' starting with 'imagebox' and link to an image will display the image inside the page. Galleries can by build buy giving the value 'imagebox-galname' to attribute 'rel'. Attribute 'title' will be used as caption.
 * @param Hash hash A hash of parameters
 * @option Integer border border width
 * @option String loaderSRC path to loading image
 * @option String closeHTML path to close overlay image
 * @option Float overlayOpacity opacity for overlay
 * @option String textImage when a galalry it is build then the iteration is displayed
 * @option String textImageFrom when a galalry it is build then the iteration is displayed
 * @option Integer fadeDuration fade duration in miliseconds
 * @option Integer showTextImage 0/1 : show or not the text 'image n from z'
 *
 * @type jQuery
 * @cat Plugins/Interface
 * @author Stefan Petre
 */

var jQImageBox_imageEl=""; //rustine pour Safari

jQuery.ImageBox = {
  options : {
    border        : 10,
    loaderSRC     : '/images/loading.gif',
    closeHTML     : '<img src="/images/close.jpg" />',
    overlayOpacity    : 0,
    textImage     : 'Showing image',
    textImageFrom   : 'from',
    fadeDuration    : 0,
    showTextImage   : false,
    maxWidth        : 800
  },
  imageLoaded : false,
  firstResize : false,
  currentRel : null,
  animationInProgress : false,
  opened : false,
  minWidth : 0,
  heightClose : 0,

  keyPressed : function(event)
  {
    if(!jQuery.ImageBox.opened || jQuery.ImageBox.animationInProgress)
      return;
    var pressedKey = event.charCode || event.keyCode || -1;
    switch (pressedKey)
    {
      //end
      case 35:
        if (jQuery.ImageBox.currentRel)
          jQuery.ImageBox.start(null, jQuery('a[@rel=' + jQuery.ImageBox.currentRel+ ']:last').get(0));
      break;
      //home
      case 36:
        if (jQuery.ImageBox.currentRel)
          jQuery.ImageBox.start(null, jQuery('a[@rel=' + jQuery.ImageBox.currentRel+ ']:first').get(0));
      break;
      //left
      case 37:
      //backspace
      case 8:
      //page up
      case 33:
      //p
      case 80:
      case 112:
        var prevEl = jQuery('#ImageBoxPrevImage');
        if(prevEl.get(0).onclick != null) {
          prevEl.get(0).onclick.apply(prevEl.get(0));
        }
      break;
      //up
      case 38:
      break;
      //right
      case 39:
      //page down
      case 34:
      //space
      case 32:
      //n
      case 110:
      case 78:
        var nextEl = jQuery('#ImageBoxNextImage');
        if(nextEl.get(0).onclick != null) {
          nextEl.get(0).onclick.apply(nextEl.get(0));
        }
      break;
      //down;
      case 40:
      break;
      //escape
      case 27:
        jQuery.ImageBox.hideImage();
      break;
    }
  },

  init : function(options)
  {
    if (options)
      jQuery.extend(jQuery.ImageBox.options, options);
    if (window.event) {
      jQuery('body',document).bind('keyup', jQuery.ImageBox.keyPressed);
    } else {
      jQuery(document).bind('keyup', jQuery.ImageBox.keyPressed);
    }
    jQuery('a').each(
      function()
      {
        el        = jQuery(this);
        relAttr     = el.attr('rel')||'';
        hrefAttr    = el.attr('href')||'';
        imageTypes    = /\.jpg|\.jpeg|\.png|\.gif|\.bmp/g;
        if (hrefAttr.toLowerCase().match(imageTypes) != null && relAttr.toLowerCase().indexOf('imagebox') == 0) {
          el.bind('click', jQuery.ImageBox.start);
        }
      }
    );
    if (jQuery.browser.msie) {
      iframe = document.createElement('iframe');
      jQuery(iframe)
        .attr(
          {
            id      : 'ImageBoxIframe',
            src     : 'javascript:false;',
            frameborder : 'no',
            scrolling : 'no'
          }
        )
        .css (
          {
            display   : 'none',
            position  : 'absolute',
            top     : '0',
            left    : '0',
            filter    : 'progid:DXImageTransform.Microsoft.Alpha(opacity=0)'
          }
        );
      jQuery('body').append(iframe);
    }

    overlay = document.createElement('div');
    jQuery(overlay)
      .attr('id', 'ImageBoxOverlay')
      .css(
        {
          position  : 'absolute',
          display   : 'none',
          top     : '0',
          left    : '0',
          opacity   : 0
        }
      )
      .append(document.createTextNode(' '))
      .bind('click', jQuery.ImageBox.hideImage);

    captionText = document.createElement('div');
    jQuery(captionText)
      .attr('id', 'ImageBoxCaptionText')
      .css(
        {
          paddingLeft   : jQuery.ImageBox.options.border + 'px'
        }
      )
      .append(document.createTextNode(' '));

    captionImages = document.createElement('div');
    jQuery(captionImages)
      .attr('id', 'ImageBoxCaptionImages')
      .css(
        {
          paddingLeft   : jQuery.ImageBox.options.border + 'px',
          paddingBottom : jQuery.ImageBox.options.border + 'px'
        }
      )
      .append(document.createTextNode(' '));

    closeEl = document.createElement('a');
    jQuery(closeEl)
      .attr(
        {
          id      : 'ImageBoxClose',
          href    : '#'
        }
      )
      .css(
        {
          position  : 'absolute',
          right   : jQuery.ImageBox.options.border + 'px',
          top     : '0'
        }
      )
      .append(jQuery.ImageBox.options.closeHTML)
      .bind('click', jQuery.ImageBox.hideImage);

    captionEl = document.createElement('div');
    jQuery(captionEl)
      .attr('id', 'ImageBoxCaption')
      .css(
        {
          position  : 'relative',
          textAlign : 'left',
          margin    : '0 auto',
          zIndex    : 1
        }
      )
      .append(captionText)
      .append(captionImages)
      .append(closeEl);

    loader = document.createElement('img');
    loader.src = jQuery.ImageBox.options.loaderSRC;
    jQuery(loader)
      .attr('id', 'ImageBoxLoader')
      .css(
        {
          position  : 'absolute'
        }
      );

    prevImage = document.createElement('a');
    jQuery(prevImage)
      .attr(
        {
          id      : 'ImageBoxPrevImage',
          href    : '#'
        }
      )
      .css(
        {
          position    : 'absolute',
          display     : 'none',
          overflow    : 'hidden',
          textDecoration  : 'none'
        }
      )
      .append(document.createTextNode(' '));

    nextImage = document.createElement('a');
    jQuery(nextImage)
      .attr(
        {
          id      : 'ImageBoxNextImage',
          href    : '#'
        }
      )
      .css(
        {
          position    : 'absolute',
          overflow    : 'hidden',
          textDecoration  : 'none'
        }
      )
      .append(document.createTextNode(' '));

    container = document.createElement('div');
    jQuery(container)
      .attr('id', 'ImageBoxContainer')
      .css(
        {
          display   : 'none',
          position  : 'relative',
          overflow  : 'hidden',
          textAlign : 'left',
          margin    : '0 auto',
          top     : '0',
          left    : '0',
          zIndex    : 2
        }
      )
      .append([loader, prevImage, nextImage]);

    outerContainer = document.createElement('div');
    jQuery(outerContainer)
      .attr('id', 'ImageBoxOuterContainer')
      .css(
        {
          display   : 'none',
          position  : 'absolute',
          overflow  : 'hidden',
          top     : '0',
          left    : '0',
          textAlign : 'center',
          backgroundColor : 'transparent',
          lineHeigt : '0'
        }
      )
      .append([container,captionEl]);

    jQuery('body')
      .append(overlay)
      .append(outerContainer);


    //minimum width :
    prevImageEl = jQuery('#ImageBoxPrevImage');
    prevWidth = prevImageEl.css("width");
    if (!prevWidth) {
      prevWidth='';
    }
    else{
      if(prevWidth!=''){
        prevWidth = prevWidth.replace(/px/g,''); //on eleve le texte 'px' pour pouvoir faire des calculs
      }
    }
    nextImageEl = jQuery('#ImageBoxNextImage');
    nextWidth = nextImageEl.css("width");
    if (!nextWidth) {
      nextWidth='';
    }
    else{
      if(nextWidth!=''){
        nextWidth = nextWidth.replace(/px/g,''); //on eleve le texte 'px' pour pouvoir faire des calculs
      }
    }

    jQuery.ImageBox.minWidth=-(-(jQuery.ImageBox.options.border * 2)-nextWidth-prevWidth); //2*border+nextWidth+prevWidth


  },

  start : function(e, elm)
  {
    el = elm ? jQuery(elm) : jQuery(this);
    linkRel =  el.attr('rel');
    var totalImages, iteration, prevImage, nextImage;
    if (linkRel != 'imagebox') {
      jQuery.ImageBox.currentRel = linkRel;
      gallery = jQuery('a[@rel=' + linkRel + ']');
      totalImages = gallery.size();
      iteration = gallery.index(elm ? elm : this);
      prevImage = gallery.get(iteration - 1);
      nextImage = gallery.get(iteration + 1);
    }
    imageSrc =  el.attr('href');
    captionText = el.attr('title');
    caption2 = el.attr('content') || "";
    if (caption2!="") {
      captionText+="<br>"+caption2;
    }
    pageSize = jQuery.iUtil.getScroll();
    overlay = jQuery('#ImageBoxOverlay');
    if (!jQuery.ImageBox.opened) {
      jQuery.ImageBox.opened = true;
      if (jQuery.browser.msie) {
        jQuery('#ImageBoxIframe')
          .css ('height', Math.max(pageSize.ih,pageSize.h) + 'px')
          .css ('width', Math.max(pageSize.iw,pageSize.w) + 'px')
          .show();
      }
      overlay
        .css ('height', Math.max(pageSize.ih,pageSize.h) + 'px')
        .css ('width', '100%')
        .show()
        .fadeTo(
          300,
          jQuery.ImageBox.options.overlayOpacity,
          function()
          {
            jQuery.ImageBox.loadImage(
              imageSrc,
              captionText,
              pageSize,
              totalImages,
              iteration,
              prevImage,
              nextImage
            );
          }
        );
      jQuery('#ImageBoxOuterContainer').css ('width', Math.max(pageSize.iw,pageSize.w) + 'px');
    } else {
      jQuery('#ImageBoxPrevImage').get(0).onclick = null;
      jQuery('#ImageBoxNextImage').get(0).onclick = null;
      jQuery.ImageBox.loadImage(
        imageSrc,
        captionText,
        pageSize,
        totalImages,
        iteration,
        prevImage,
        nextImage
      );
    }
    return false;
  },

  loadImage : function(imageSrc, captiontext, pageSize, totalImages, iteration, prevImage, nextImage)
  {
    jQuery('#ImageBoxCurrentImage').remove();
    prevImageEl = jQuery('#ImageBoxPrevImage');
    prevImageEl.hide();
    nextImageEl = jQuery('#ImageBoxNextImage');
    nextImageEl.hide();
    loader = jQuery('#ImageBoxLoader');
    container = jQuery('#ImageBoxContainer');
    outerContainer = jQuery('#ImageBoxOuterContainer');
    captionEl = jQuery('#ImageBoxCaption').css('visibility', 'hidden');
    //Avoid safari Bug :
    //jQuery('#ImageBoxCaptionText').html(captionText);
    jQuery('#ImageBoxCaptionText').html("<div id='ImageBoxCaptextcontainer' style='padding-right:4px'>"+captionText+"</div>");
    jQuery.ImageBox.animationInProgress = true;
    if (totalImages && jQuery.ImageBox.options.showTextImage)
      jQuery('#ImageBoxCaptionImages').html(
        jQuery.ImageBox.options.textImage
        + ' ' + (iteration + 1) + ' '
        + jQuery.ImageBox.options.textImageFrom
        + ' ' + totalImages
      );
    if (prevImage) {
      prevImageEl.get(0).onclick = function()
      {
        this.blur();
        jQuery.ImageBox.start(null, prevImage);
        return false;
      };
    }
    if (nextImage) {
      nextImageEl.get(0).onclick =function()
      {
        this.blur();
        jQuery.ImageBox.start(null, nextImage);
        return false;
      };
    }
    loader.show();
    containerSize = jQuery.iUtil.getSize(container.get(0));
    containerW = Math.max(containerSize.wb, loader.get(0).width + jQuery.ImageBox.options.border * 2);
    containerH = Math.max(containerSize.hb, loader.get(0).height + jQuery.ImageBox.options.border * 2);
    loader
      .css(
        {
          left  : (containerW - loader.get(0).width)/2 + 'px',
          top   : (containerH - loader.get(0).height)/2 + 'px'
        }
      );
    container
      .css(
        {
          width : containerW + 'px',
          height  : containerH + 'px'
        }
      )
      .show();
    clientSize = jQuery.iUtil.getClient();
    outerContainer
      .css('top', pageSize.t +  (clientSize.h / 15) + 'px');
    if (outerContainer.css('display') == 'none') {
      outerContainer
        .show()
        .fadeIn(
          jQuery.ImageBox.options.fadeDuration
        );
    }
    imageEl = new Image;
    // avoid Safari bug :
    imageEl.id='ImageBoxCurrentImage';
    imageEl.onload = function(){

        if (jQuery.browser.safari) {
          containerW = jQImageBox_imageEl.width + jQuery.ImageBox.options.border * 2;
          containerH = jQImageBox_imageEl.height + jQuery.ImageBox.options.border * 2;
        }

        var maxWidth = jQuery.ImageBox.options.maxWidth;
        if ( jQuery.ImageBox.options.maxWidth > 0 && 
             imageEl.width > maxWidth && 
             !jQuery.browser.safari ) {
          var aspectHeight = imageEl.height/(imageEl.width/maxWidth);
          containerW = maxWidth + jQuery.ImageBox.options.border * 2;
          containerH = aspectHeight + jQuery.ImageBox.options.border * 2;
        } else {
          containerW = imageEl.width + jQuery.ImageBox.options.border * 2;
          containerH = imageEl.height + jQuery.ImageBox.options.border * 2;
        }

        //min width :
        if (jQuery.ImageBox.minWidth > containerW ) {
          containerW = jQuery.ImageBox.minWidth + jQuery.ImageBox.options.border * 2;
        }

        loader.hide();
        container.animate(
          {
            height    : containerH
          },
          containerSize.hb != containerH ? jQuery.ImageBox.options.fadeDuration : 1,
          function()
          {
            container.animate(
              {
                width   : containerW
              },
              containerSize.wb != containerW ? jQuery.ImageBox.options.fadeDuration : 1,
              function()
              {


                if (jQuery.browser.safari) {
                  var imgtoprepend="<img src='"+jQImageBox_imageEl.src+"' id='imgboxtmp' style='display:none' >";
                  container.prepend(imgtoprepend);
                  var jqi_width = jQuery('#imgboxtmp').width();
                  while(jqi_width==0){
                    jqi_width = jQuery('#imgboxtmp').width();
                  }
                  jqi_height = jQuery('#imgboxtmp').height();
                  jQuery('#imgboxtmp').remove();

                  jqi_width = jqi_width - 2* jQuery.ImageBox.options.border;

                  var imgtoprepend="<img src='"+jQImageBox_imageEl.src+"' id='"+jQImageBox_imageEl.id+"' >";
                  container.prepend(imgtoprepend); //pour safari...

                }
                else{
                  container.prepend(imageEl);
                }


                jQuery('#ImageBoxCurrentImage')
                  .css(
                    {
                      position  : 'absolute',
                      left    : (containerW-jQuery('#ImageBoxCurrentImage').width())/2+'px', //jQuery.ImageBox.options.border + 'px',
                      top     : jQuery.ImageBox.options.border + 'px'
                    }
                  )
                  .fadeIn(
                    jQuery.ImageBox.options.fadeDuration,
                    function()
                    {
                      captionSize = jQuery.iUtil.getSize(captionEl.get(0));

                      //min width :
                      if (jQuery.ImageBox.minWidth > containerW ) {
                         containerW = jQuery.ImageBox.minWidth;
                      }

                      if (prevImage) {
                        prevImageEl
                          .css(
                            {
                              left  : jQuery.ImageBox.options.border + 'px',
                              top   : jQuery.ImageBox.options.border + 'px',
                              width : containerW/2 ,//- jQuery.ImageBox.options.border * 3 + 'px',
                              height  : containerH - jQuery.ImageBox.options.border * 2 + 'px'
                            }
                          )
                          .show();
                      }
                      if (nextImage) {
                        nextImageEl
                          .css(
                            {
                              left  : containerW/2 + jQuery.ImageBox.options.border * 2 + 1 + 'px',
                              top   : jQuery.ImageBox.options.border + 'px',
                              width : containerW/2 - jQuery.ImageBox.options.border * 3 + 'px',
                              height  : containerH - jQuery.ImageBox.options.border * 2 + 'px'
                            }
                          )
                          .show();
                      }

                      jQuery("#ImageBoxCaptextcontainer").css('padding-top',jQuery("#ImageBoxClose").height());

                      captionEl
                        .css(
                          {
                            width   : containerW + 'px',
                            top     : - captionSize.hb + 'px',
                            visibility  : 'visible'
                          }
                        )
                        .animate(
                          {
                            top   : -1
                          },
                          jQuery.ImageBox.options.fadeDuration,
                          function()
                          {
                            jQuery.ImageBox.animationInProgress = false;
                          }
                        );
                    }
                  );
              }
            );
          }
        );
      }
    imageEl.src = imageSrc;

    jQImageBox_imageEl = imageEl;
  },

  hideImage : function()
  {
    jQuery('#ImageBoxCurrentImage').remove();
    jQuery('#ImageBoxOuterContainer').hide();
    jQuery('#ImageBoxCaption').css('visibility', 'hidden');
    jQuery('#ImageBoxOverlay').fadeTo(
      300,
      0,
      function(){
        jQuery(this).hide();
        if (jQuery.browser.msie) {
          jQuery('#ImageBoxIframe').hide();
        }
      }
    );
    jQuery('#ImageBoxPrevImage').get(0).onclick = null;
    jQuery('#ImageBoxNextImage').get(0).onclick = null;
    jQuery.ImageBox.currentRel = null;
    jQuery.ImageBox.opened = false;
    jQuery.ImageBox.animationInProgress = false;
    return false;
  }
};
