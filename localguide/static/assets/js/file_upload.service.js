
function upload(formData) {
    axios({
        method: 'POST',
        url: URL + 'tour/uploadTourPhoto',
        data: formData, 
        headers: {'Content-Type': 'multipart/form-data'} 
    })
    /*
    .then(function (response) {
        //handle success
        //console.log(response.data)
    })
    .catch(function (response) {
        //handle error
        console.log(response);
    });
    */
    const photos = formData.getAll('photos');
    const promises = photos.map((x) => getImage(x)
        .then(img => ({
            id: img,
            originalName: x.name,
            fileName: x.name,
            url: img
        })));    
    return Promise.all(promises);
}

function allImage(formData) {
    const photos = formData.getAll('photos');
    const promises = photos.map((x) => getImage(x)
        .then(img => ({
            id: img,
            originalName: x.name,
            fileName: x.name,
            url: img
        })));
    return Promise.all(promises);
}

function getImage(file) {
    return new Promise((resolve, reject) => {
        const fReader = new FileReader();
        const img = document.createElement('img');

        fReader.onload = () => {
            img.src = fReader.result;
            resolve(getBase64Image(img));
        }

        fReader.readAsDataURL(file);
    })
}

function getBase64Image(img) {
    const canvas = document.createElement('canvas');
    canvas.width = img.width;
    canvas.height = img.height;

    const ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0);
    const dataURL = img.src;
    return dataURL;
}
