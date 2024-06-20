/*! uclcg 2024-06-20 */

var CODE_CHANGED = !1;

function hasCodeChanged() {
    return CODE_CHANGED;
}

var currentFrame, requestStop, isPlaying, requestCallback, startPlaybackTime, endPlaybackTime, gl = null, GL_EXTENSIONS_UNAVAILABLE = !0, GL_EXTENSIONS_MISSING = !1, browserPrefixes = [ "", "MOZ_", "OP_", "WEBKIT_" ], getExtensionWithKnownPrefixes = function(e) {
    for (var t = 0; t < browserPrefixes.length; ++t) {
        var n = browserPrefixes[t] + e, a = gl.getExtension(n);
        if (a) return a;
    }
};

function initGL(e) {
    try {
        (gl = e.getContext("webgl")).viewportWidth = e.width, gl.viewportHeight = e.height;
    } catch (e) {}
    gl ? GL_EXTENSIONS_UNAVAILABLE = !1 : alert(```Could not initialise WebGL. This means that the app will not work.
        Please consider updating your drivers and chrome, as well as using a computer with a discrete GPU.```);
}

function invokeCompute() {
    $("#currentFrameInput").val(currentFrame), $("body").css("cursor", "progress"), 
    appData.it += 1;
    var e, t, n = $("#glRenderTarget").get(0);
    if (GL_EXTENSIONS_UNAVAILABLE) return $("#performanceChartDiv").html("<p>This feature does not work without WebGL Extensions</p>"), 
    compute(n), (t = (e = $("#glViewport").get(0)).getContext("2d")).mozImageSmoothingEnabled = !1, 
    t.msImageSmoothingEnabled = !1, t.imageSmoothingEnabled = !1, t.drawImage(n, 0, 0, n.width, n.height, 0, 0, e.width, e.height), 
    $("body").css("cursor", "default"), void (CODE_CHANGED = !1);
    compute(n), (t = (e = $("#glViewport").get(0)).getContext("2d")).mozImageSmoothingEnabled = !1, 
    t.msImageSmoothingEnabled = !1, t.imageSmoothingEnabled = !1, t.drawImage(n, 0, 0, n.width, n.height, 0, 0, e.width, e.height), 
    $("body").css("cursor", "default"), CODE_CHANGED = !1;
}

function resetPlayback() {
    currentFrame = 0, requestStop = !1, isPlaying = !1;
}

function stopPlayback() {
    requestStopCB(function() {
        endPlaybackTime = new Date().getTime();
    });
}

function startPlayback() {
    startPlaybackTime = new Date().getTime(), play();
}

function play() {
    if (requestStop) return requestStop = !1, isPlaying = !1, void requestCallback();
    if (currentFrame >= UI.numFrames) return requestStop = !1, void (isPlaying = !1);
    if (requestStop) return requestStop = !1, isPlaying = !1, void requestCallback();
    var e = 1 / UI.maxFPS * 1e3, t = playFrame();
    t < e ? setTimeout(play, e - t) : window.requestAnimationFrame(play);
}

function playFrame() {
    currentFrame += 1;
    var e = new Date().getTime();
    invokeCompute();
    var t = new Date().getTime() - e;
    return updateSmallViewerClone(), t;
}

function requestStopCB(e) {
    isPlaying ? (requestCallback = e, requestStop = !0) : e();
}

function getCurrentFrame() {
    return currentFrame;
}

function getCurrentTime() {
    return isPlaying ? new Date().getTime() - startPlaybackTime : endPlaybackTime - startPlaybackTime;
}

function increaseCanvasResolution() {
    canvas = $("#glRenderTarget").get(0), canvas.width < 1600 && (oldWidth = canvas.width, 
    oldHeight = canvas.height, canvas.width = Math.round(2 * oldWidth), canvas.height = Math.round(2 * oldHeight), 
    UI.renderHeight = canvas.height, UI.renderWidth = canvas.width, initGL($("#glRenderTarget").get(0)));
}

function decreaseCanvasResolution() {
    canvas = $("#glRenderTarget").get(0), canvas.width > 100 && (oldWidth = canvas.width, 
    oldHeight = canvas.height, canvas.width = Math.round(oldWidth / 2), canvas.height = Math.round(oldHeight / 2), 
    UI.renderHeight = canvas.height, UI.renderWidth = canvas.width, initGL($("#glRenderTarget").get(0)));
}

function getRenderTargetWidth() {
    return $("#glRenderTarget").get(0).width;
}

function getRenderTargetHeight() {
    return $("#glRenderTarget").get(0).height;
}

function updateSmallViewerClone() {
    var e = $("#glViewportSmallClone").get(0).getContext("2d"), t = $("#glViewportSmallClone").get(0).width, n = $("#glViewportSmallClone").get(0).height, a = $("#glRenderTarget").get(0).width, r = $("#glRenderTarget").get(0).height;
    e.drawImage($("#glRenderTarget").get(0), 0, 0, a, r, 0, 0, t, n);
}

var appData = null;

function resetApp() {
    MAX_ROWS_PERF_BUFFER = 200, logIt = 0, logRenderingPerformanceBuffer = [], logRenderingPerformanceBufferAvg = 0, 
    resetPlayback(), startPlaybackTime = 0, endPlaybackTime = 0;
}

function initFramework() {
    appData = {}, resetApp(), initGL($("#glRenderTarget").get(0)), appData.it = 0;
}