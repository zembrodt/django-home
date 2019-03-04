$('div').filter(function() {
    return this.id.match(/id-photos-.*/);
}).each(function() {
    var count = $(this).find('#img-count').val();
    var interval = $(this).find('#img-interval').val();
    var is_background = parseInt($(this).find('#img-background').val());
    console.log('background: '+is_background);
    var images = [];
    var curr_image = 0;
    var is_transparent = false;
    
    for (var i = 0; i < count; i++) {
        images.push($(this).find('#img-' + i).val());
    }

    if (is_background === 1) {
        $(this).addClass('photo');
        var img = $(this).find('[id^=photo]');
        console.log('img: '+img)
        img.addClass('photo');
        img.removeAttr('width');
        img.removeAttr('height');
    }

    function display_next_image(img) {
        curr_image++;
        if (curr_image === images.length) {
            curr_image = 0;
        }
        var next_image = curr_image + 1;
        if (next_image === images.length) {
            next_image = 0;
        }
        var top = $('#' + img.attr('id') + '-top');
        top.toggleClass('transparent');
        img.toggleClass('transparent');
        is_transparent = !is_transparent;
        
        setTimeout(function() {
            if (is_transparent) {
                top.attr('src', images[next_image]);
            } else {
                $('#' + img.attr('id')).attr('src', images[next_image]);
            }
        }, 1000);
    }

    if (images.length > 0) {
        var img = $(this).find('[id^=photo]');
        img.attr('src', images[curr_image]);
        if (images.length > 1) {
            // If we have more than one image, duplicate img tag to create transitions
            img_top = img.clone().attr('id', img.attr('id') + '-top');
            $(this).append(img_top);
            img.attr('src', images[curr_image+1]);
            img.addClass('transparent');
            setInterval(function() { display_next_image(img) }, interval*1000);
        }
    } else {
        console.log('No images found for module ' + $(this).id);
    }
});


