

var URL = "https://localhost:8000/"

/** Upload Image for Quill Editor */
/* Step 1: Select local file */
function imageHandler() {
    //alert("Select Image")
    const input = document.createElement('input');
    input.setAttribute('type', 'file');
    input.click();

    // Listen upload local image and save to server
    input.onchange = () => {
        const file = input.files[0];
        //alert(file.type);
        // file type is only image.
        if (/^image\//.test(file.type)) {
            //console.log('Save file');
            //console.log(this.quill)
            saveToServer(this.quill, file);
        } else {
            console.warn('You could only upload images.');
        }
    };
}

/* Step2: Save to server */
function saveToServer(quill, file) {
    var uploadFile = file;
    //alert("Save To Server" + uploadFile);
    const formData = new FormData();
    formData.append('photo', uploadFile);

    axios({
        method: 'POST',
        url: URL + 'common/uploadEditorImage',
        data: formData, 
        headers: {'Content-Type': 'multipart/form-data'},
    })
    .then(res => {
        if(res.status == '200' && res.statusText == 'OK'){
            var Delta = Quill.import('delta');
            let range = quill.getSelection(true);
            quill.updateContents(new Delta()
                .retain(range.index)
                .delete(range.length)
                .insert({ image: res.data.url })
            , Quill.sources.USER);
        } else {
            console.error(res);
        }
    })
    .catch(e => {
        console.error(e);
    });
}

// utils to delay promise
function wait(ms) {
    return (x) => {
        return new Promise(resolve => setTimeout(() => resolve(x), ms));
    };
}
//get url parameter
function getUrlParameter(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}