let color = "black";
let brushsize = 50;
let maxZoomPixelRatio = 4;
event_handlers["init-seadragon"] = function (id, value, event_name) {
    let config = value

    let viewerConfig = {
        id: id,
        prefixUrl: "/open_seadragon/images/",
        animationTime: 0,
        tileSources : {"type": "image","url": config.image},
        toolbar: config.buttonGroupId,
        showNavigationControl: false,
        maxZoomPixelRatio: maxZoomPixelRatio,
    };
    document.getElementById(id).innerHTML = "";

    let viewer = OpenSeadragon(viewerConfig);
    document.getElementById(id).viewer = viewer;


}
event_handlers["init-interactiveSeadragon"] = function (id, value, event_name) {

    let config = value

    let viewerConfig = {
        id: id,
        prefixUrl: "/open_seadragon/images/",
        animationTime: 0,
        tileSources : {"type": "image","url": config.image},
        showNavigationControl: false,
        maxZoomPixelRatio: maxZoomPixelRatio,
        autoHideControls: false,
        toolbar: config.buttonGroupId,
    
    };


    let viewer = OpenSeadragon(viewerConfig);
    document.getElementById(id).viewer = viewer;


    const overlay = viewer.fabricjsOverlay({"scale": 1000});
    document.getElementById(id).overlay = overlay;
    const generate_button = document.getElementById(generate_button_id);

    generate_button.addEventListener("click", function() {
        const viewportBounds = viewer.viewport.getBounds();
        const tiledImage = viewer.world.getItemAt(0); // Assuming you want the first (or only) image
        const imageBounds = tiledImage.viewportToImageRectangle(viewportBounds);
        const mergeCanvas = document.createElement('canvas');

        const mergeCtx = mergeCanvas.getContext('2d');
        mergeCtx.imageSmoothingEnabled = false;

        const originalImage = new Image();
        originalImage.src = viewer.world.getItemAt(0).source.url;

        originalImage.onload = function() {
            mergeCanvas.width = originalImage.width;
            mergeCanvas.height = originalImage.height;
            mergeCanvas.getContext('2d').drawImage(originalImage, 0, 0, mergeCanvas.width, mergeCanvas.height);

            const overlayImage = new Image();
            overlayImage.src = overlay.fabricCanvas().toDataURL("image/png", 1.0);

            overlayImage.onload = function() {

                mergeCtx.drawImage(overlayImage, imageBounds.x, imageBounds.y, imageBounds.width, imageBounds.height);

                const data = mergeCanvas.toDataURL("image/png", 1.0);
                const blob = dataURItoBlob(data);
                const imageUrl = URL.createObjectURL(blob);

                clientEmit(generate_button_id, {
                    "url": imageUrl,
                    "imageSize": blob.size,
                    "filename": "overlay.png"
                }, "click_generate");
            }};
        });
}





event_handlers["seadragon"] = function (id, command, event_name) {
    const viewer = document.getElementById(id).viewer;
    switch (command.action) {
        case "open":

            viewer.world.removeAll();
            viewer.open(command.value);
            console.log(viewer.viewport.getZoom(),"open",command.value);
            break;
        case 'close':
            viewer.close();
            break;
        case "set-scroll-zoom":
            const cmd = command.value === "true";
            viewer.gestureSettingsMouse.scrollToZoom = cmd;
            viewer.gestureSettingsMouse.clickToZoom = cmd;
            viewer.gestureSettingsMouse.dragToPan = cmd;
            break;

        case "zoomIn":
            console.log(viewer.viewport.getZoom()),"zoomIn";
      
            viewer.viewport.zoomBy(1.5);

            break;

        case "zoomOut":
            console.log(viewer.viewport.getZoom()),"zoomOut";

            viewer.viewport.zoomBy(0.5);
            
            break;

        case "home":
            viewer.viewport.goHome();
            break;

        case "fullscreen":
    
            if (viewer.isFullPage()) {
                viewer.setFullScreen(false);
                return;
            }
            viewer.setFullScreen(true);
            break;

        case "download":
            downloadFullImage();
            break;
    }
    function genRandomNumbers(){
        const array = new Uint32Array(10);
        crypto.getRandomValues(array);
        return Array.from(array).map(n => n.toString(16)).join('');
    };
    function downloadFullImage() {
        const viewer = document.getElementById(id).viewer;
        let tileSources = viewer.world.getItemAt(0).source;
        let imageUrl = tileSources.url || tileSources[0].url;

        if (!imageUrl) {
            console.error('Full image URL not found');
            return;
        }

        var link = document.createElement('a');
        link.href = imageUrl;
        const fileExtension = imageUrl.split('.').pop();
        link.download = `${genRandomNumbers()}.${fileExtension}`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

event_handlers["interactiveSeadragon"] = function (id, command, event_name) {
    const viewer = document.getElementById(id).viewer;

    const overlay = document.getElementById(id).overlay;
    switch (command.action) {

        case "open":
            viewer.world.removeAll();
            viewer.open(command.value);

            overlay.fabricCanvas().clear();


            break;

        case "open-edit-area":

            freeDraw(true, document.getElementById(id).overlay , viewer);
            const edit_area = document.getElementById(command.value);

   
            if(edit_area.classList.contains("active")){
                edit_area.classList.remove("active");
            }else{
                edit_area.classList.add("active");
            }
        

            // window.addEventListener("click", function(e) {
            //     if (!edit_area.contains(e.target)) {
            //         if (edit_area.classList.contains("active")) {
            //             edit_area.classList.remove("active");
            //         }
            //     }
            // });
            break;

        case "editBrush":
            color = hexToRgbA(command.value["color"], command.value["opacity"]);
            brushsize = command.value["brushSize"];
            freeDraw(true, document.getElementById(id).overlay , viewer);
            break;

        case "setPanMode":
            freeDraw(false, document.getElementById(id).overlay , viewer);
            break;

        case "eraserBrush":
            if (command.value["isChecked"]) {
                document.getElementById(id).overlay .fabricCanvas().freeDrawingBrush = new fabric.EraserBrush(document.getElementById(id).overlay .fabricCanvas());
                document.getElementById(id).overlay .fabricCanvas().freeDrawingBrush.width = command.value["brushSize"];}
            else {
                document.getElementById(id).overlay .fabricCanvas().freeDrawingBrush = new fabric.PencilBrush(document.getElementById(id).overlay .fabricCanvas());
                freeDraw(true, overlay, viewer);
            }

            break;
    }

    document.onkeydown = function(e) {
        if (e.key === "Delete") {
            if (document.getElementById(id).overlay .fabricCanvas().getActiveObject()) {
                document.getElementById(id).overlay .fabricCanvas().remove(document.getElementById(id).overlay .fabricCanvas().getActiveObject());
            }

        }
    }


}


function hexToRgbA(hex,opacity){
    var c;
    if(/^#([A-Fa-f0-9]{3}){1,2}$/.test(hex)){
        c= hex.substring(1).split('');
        if(c.length== 3){
            c= [c[0], c[0], c[1], c[1], c[2], c[2]];
        }
        c= '0x'+c.join('');
        return 'rgba('+[(c>>16)&255, (c>>8)&255, c&255].join(',')+',' + opacity + ')';
    }
    throw new Error('Bad Hex');
}

function dataURItoBlob(dataURI) {
    var byteString = atob(dataURI.split(',')[1]);
    var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
    var ab = new ArrayBuffer(byteString.length);
    var ia = new Uint8Array(ab);
    for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    return new Blob([ab], { type: mimeString });
}



function freeDraw(flag, over,viewer) {
    over.resizeCanvas();
    over.fabricCanvas().freeDrawingBrush.color = color;
    over.fabricCanvas().freeDrawingBrush.width = brushsize;
    if (flag) {
        viewer.setMouseNavEnabled(false);
        viewer.outerTracker.setTracking(true);
        over.fabricCanvas().isDrawingMode = true;
    } else {
        viewer.setMouseNavEnabled(true);
        viewer.outerTracker.setTracking(true);
        over.fabricCanvas().isDrawingMode = false;

    }

}
