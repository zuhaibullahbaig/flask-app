out_style = document.getElementById('out-style');
in_style = document.getElementById('in-style');
dots_style = document.getElementById('dots-style');



function createQRcode(){

    document.getElementById('canvas').innerHTML = '';
    container = document.getElementById('generated-qr');
    container.classList.remove('generated-qr-active');
    qrcodemain = document.getElementById('qrcodemain');
    qrcodemain.classList.add('options-active')
    forecolor = document.getElementById('forecolor').value;
    backcolor = document.getElementById('backcolor').value;

    url = document.getElementById('url').value;

    if (url==""){
        url = 'random'
    }
    let newqrCode = new QRCodeStyling({
        width: 300,
        height: 300,
        type: "png",
        data: String(url),
        // image: "https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg",
        dotsOptions: {
            color: forecolor,
            type: dots_style.value,
        },
        backgroundOptions: {
            color: backcolor,
        },
        cornersSquareOptions : {
            type: out_style.value,
        },
        cornersDotOptions : {
            type: in_style.value,
        },
        imageOptions: {
            crossOrigin: "anonymous",
            margin: 20
        }
    });
    newqrCode.append(document.getElementById("canvas"));

}

function download_Qr(){

  
    document.getElementById('canvas').innerHTML = '';
    container = document.getElementById('generated-qr');
    container.classList.remove('generated-qr-active');
    forecolor = document.getElementById('forecolor').value;
    backcolor = document.getElementById('backcolor').value;

    url = document.getElementById('url').value;

    if (url==""){
        url = 'random'
    }
    let newqrCode = new QRCodeStyling({
        width: 300,
        height: 300,
        type: "png",
        data: String(url),
        image: '',
        dotsOptions: {
            color: forecolor,
            type: dots_style.value,
        },
        backgroundOptions: {
            color: backcolor,
        },
        cornersSquareOptions : {
            type: out_style.value,
        },
        cornersDotOptions : {
            type: in_style.value,
        },
        imageOptions: {
            crossOrigin: "anonymous",
            margin: 20
        }
    });
    newqrCode.append(document.getElementById("canvas"));

    download_type = document.getElementById('download-type').value;
    console.log(download_type);
    if (download_type == 'jpg'){
        newqrCode.download({ name: "qr", extension: "jpg" });
    }
    else if (download_type == 'svg'){
        newqrCode.download({ name: 'qr', extension: "svg"});
    } else {
        newqrCode.download({ name: 'qr', extension: "png"});
    }
}

function remove_class(){
    container = document.getElementById('generated-qr');
    container.classList.add('generated-qr-active');
    qrcodemain = document.getElementById('qrcodemain');
    qrcodemain.classList.remove('options-active')
}
document.getElementById('download').addEventListener('click', download_Qr);
document.getElementById('generate').addEventListener('click', createQRcode);
document.getElementById('cross').addEventListener('click', remove_class);


// 

// DOTS
// 
dots_extra_rounded= document.getElementById('dots-extra-rounded');
dots_dot = document.getElementById('dots-dot');
dots_square = document.getElementById('dots-square');
dots_rounded = document.getElementById('dots-rounded');

function dots_extra_rounded_updated(){
    dots_style.value = 'extra-rounded';
    dots_extra_rounded.classList.add('img-active');
    dots_square.classList.remove('img-active');
    dots_rounded.classList.remove('img-active');
    dots_dot.classList.remove('img-active');
}

function dots_dot_updated(){
    dots_style.value = 'dots';
    dots_square.classList.remove('img-active');
    dots_rounded.classList.remove('img-active');
    dots_dot.classList.add('img-active');
    dots_extra_rounded.classList.remove('img-active');

}

function dots_square_updated(){
    dots_style.value = 'square';
    dots_square.classList.add('img-active');
    dots_rounded.classList.remove('img-active');
    dots_dot.classList.remove('img-active');
    dots_extra_rounded.classList.remove('img-active');


}

function dots_rounded_updated(){
    dots_style.value = 'rounded';
    dots_dot.classList.remove('img-active');
    dots_rounded.classList.add('img-active');
    dots_square.classList.remove('img-active');
    dots_extra_rounded.classList.remove('img-active');

}

dots_dot.addEventListener('click', dots_dot_updated)
dots_square.addEventListener('click', dots_square_updated)
dots_rounded.addEventListener('click', dots_rounded_updated)
dots_extra_rounded.addEventListener('click', dots_extra_rounded_updated)

// DOTS
// 

out_dot = document.getElementById('out-dots');
out_square = document.getElementById('out-square');
out_rounded = document.getElementById('out-rounded');

function out_dot_updated(){
    out_style.value = 'dots';
    out_dot.classList.add('img-active');
    out_rounded.classList.remove('img-active');
    out_square.classList.remove('img-active');

}

function out_square_updated(){
    out_style.value = 'square';
    out_dot.classList.remove('img-active');
    out_rounded.classList.remove('img-active');
    out_square.classList.add('img-active');

}

function out_rounded_updated(){
    out_style.value = 'extra-rounded';
    out_dot.classList.remove('img-active');
    out_rounded.classList.add('img-active');
    out_square.classList.remove('img-active');
}

out_dot.addEventListener('click', out_dot_updated)
out_square.addEventListener('click', out_square_updated)
out_rounded.addEventListener('click', out_rounded_updated)


// in

in_dots = document.getElementById('in-dots');
in_square = document.getElementById('in-square');

function in_dots_updated(){
    in_style.value = 'dot';
    in_dots.classList.add('img-active');
    in_square.classList.remove('img-active');
}

function in_square_updated(){
    in_style.value = 'square';
    in_dots.classList.remove('img-active');
    in_square.classList.add('img-active');
}

in_dots.addEventListener('click', in_dots_updated);
in_square.addEventListener('click', in_square_updated);
