$(document).ready(function() {
    initFramework();
    function clearAllDrawingCanvases() {
        var canvas = document.getElementById('glRenderTarget');
        gl = canvas.getContext("webgl");
        gl.clearColor(0.0, 0, 0, 1.0);
        gl.clear(gl.COLOR_BUFFER_BIT);
        var canvas = document.getElementById('glViewportSmallClone');
        canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
    }

    //Function for clearing on reload
    function clear(callback, jsFileContents) {
        //reset app
        resetApp();
        //hide initial UI if necessary
        if ($("#setupTabs").data("ui-tabs")) {
            $("#setupTabs").tabs("destroy");
            $("#setupTabs").empty();
            $("#setupIntro").empty();
        }
        //reset all canvas objects
        clearAllDrawingCanvases();

        //remove codemirror instance
        if (UI.codemirrorInstances) {
            for (t = 0; t < UI.codemirrorInstances.length; ++t) {
                UI.codemirrorInstances[t].toTextArea();
            }
        }

        if (UI.tabs) {
            $("#implementationTabs").tabs("destroy");
            $("#implementationTabs").empty();
            $("#implementationTabs").append('<ul id="implementationTabsUL"></ul>');
        }
        UI.codemirrorInstances = [];
        UI = {};
        env = {};
        $("#implementationTabs").tabs({
            create: function (ui, event) {
                callback(jsFileContents);    // initFromJS
            },
            active: 0,
            collapsible: true,
        });
    }

    env = {};
    UI = {};

    //FRAMEWORK
    //experiment from js code
    function initFromJS(jsFileContents) {

        jsFileContents = jsFileContents.replace(`initGL(document.getElementById("glViewport"));`, "");

        //Try appending this file to the DOM
        try {
            var s = document.createElement('script');
            s.type = 'text/javascript';

            var code = jsFileContents;
            s.appendChild(document.createTextNode(code));
            document.body.appendChild(s);

        } catch (err) {
            alert("Your experiment template could not be loaded. Error: " + err.message);
            return;
        }

        //test whether this works
        UI = setup();
       
         //set canvas scale explicitly if defined
        if (UI.renderWidth && UI.renderHeight) {
            canvas = $("#glRenderTarget").get(0);
            canvas.width = Math.round(UI.renderWidth); //better be safe here
            canvas.height = Math.round(UI.renderHeight);
            initGL($("#glRenderTarget").get(0));
            $("#currentResolution").val(canvas.width + "x" + canvas.height);
        }
        //set frames if not available
        if (!UI.numFrames) {
            UI.numFrames = 1000;
            if (!UI.maxFPS) {
                UI.maxFPS = 24;
            }
        }

        $("#maxFramesInput").val(UI.numFrames);

        //set this to false at the start
        UI.showHidden = false;
        UI.codemirrorInstances = [];
        //Setup the UI as appropriate

        //show viewer
        $("#viewerRow").show(80, function () {
            $("#viewerControls").show(80, function () {

                //tabs
                $('#tabSpace').show(80, function () {

                    for (t = 0; t < UI.tabs.length; ++t) {
                        if (UI.tabs[t].visible == false) {
                            continue;
                        }
                        //Initial UL
                        $("div#implementationTabs ul").append(
                            "<li><a href='#implementationTabs-" + t + "'>" + UI.tabs[t].title + "</a></li>"
                        );
                        //Tab Detail
                        $("div#implementationTabs").append(
                            "<div id='implementationTabs-" + t + "'><p>" + UI.tabs[t].description + "</p><p class='consoleLike'>" + UI.tabs[t].wrapFunctionStart + "</p><div><textarea id='integratorTextArea-" + t + "'> </textarea></div><p class='consoleLike'>" + UI.tabs[t].wrapFunctionEnd + "</p></div>"
                        );
                    }
                    //Create code editors
                    var codeMirrorInstanceIdx = 0;
                    for (t = 0; t < UI.tabs.length; ++t) {
                        if (UI.tabs[t].visible == false) {
                            continue;
                        }

                        UI.codemirrorInstances.push(CodeMirror.fromTextArea($("#integratorTextArea-" + t).get(0), {
                            mode: "x-shader/x-fragment",
                            theme: "base16-dark",
                            lineNumbers: true,
                            lineWrapping: true,
                            styleActiveLine: true,
                            autoCloseBrackets: true,
                            matchBrackets: true,
                            indentUnit: 4,
                            indentWithTabs: true,
                            viewpointMargin: Infinity,
                            extraKeys: {
                                "Alt-F": "find", "Ctrl-F": "findPersistent", "Ctrl-Q": function (cm) {
                                    cm.foldCode(cm.getCursor());
                                }
                            },
                            foldGutter: true,
                            gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"]
                        }));


                        UI.codemirrorInstances[codeMirrorInstanceIdx].setValue(UI.tabs[t].initialValue);
                        UI.codemirrorInstances[codeMirrorInstanceIdx].refresh();
                        codeMirrorInstanceIdx += 1;
                    }

                    $("#implementationTabs").tabs("refresh");
                    $("#implementationTabs").tabs({ active: 0 });

                    // update
                    updateAllFunctions();
                    // init app
                    env = init();
                    CODE_CHANGED = true;
                    invokeCompute();
                    updateSmallViewerClone();

                });
            });
        });
    }

    function updateAllFunctions() {
        var codeMirrorInstanceIdx = 0;
        for (var t = 0; t < UI.tabs.length; ++t) {
            try {
                var oldScriptTag = $('#' + UI.tabs[t].id).get(0);

                if (oldScriptTag) {
                    oldScriptTag.parentElement.removeChild(oldScriptTag);
                }

                var s = document.createElement('script');

                s.id = UI.tabs[t].id;
                s.type = UI.tabs[t].type;
                var code = "";
                if (UI.tabs[t].visible) {
                    code = UI.tabs[t].wrapFunctionStart + UI.codemirrorInstances[codeMirrorInstanceIdx].getValue() + UI.tabs[t].wrapFunctionEnd;
                    codeMirrorInstanceIdx += 1;
                }
                else {
                    code = UI.tabs[t].wrapFunctionStart + UI.tabs[t].initialValue + UI.tabs[t].wrapFunctionEnd;
                }
                s.appendChild(document.createTextNode(code));
                document.body.appendChild(s);

            }
            catch (err) {
                alert("Your function failed to execute. Reported error: " + err.message);
            }
        }
    }

    function updateAll() {
        updateAllFunctions();
        if (CODE_CHANGED) {
            init();
        }
        CODE_CHANGED = true;
        invokeCompute();
        updateSmallViewerClone();
    }

    //How to load a new experiment
    function loadFile(fileName) {
        fetch(fileName)
        .then(response => response.text())
        .then(text => {
            clear(initFromJS, text);
        });
    }

    function saveFile(filename) {
        sessionStorage.setItem("currentFile", filename);
        window.location.reload();
    }

    loadFile(sessionStorage.getItem("currentFile") || "uclcg/RayTracerSimple.uclcg");
   
    $("#refreshButton").click(function () {
        CODE_CHANGED = true;
        updateAll();
    })

    $(".menuLoad").click(function (e) {
        saveFile(e.target.dataset.file)
    });


    $(document).scroll(function () {
        var y = $(this).scrollTop();
        if (y > 210) {
            $('#floatingPreview').fadeIn();
        } else {
            $('#floatingPreview').hide();
        }
    });

    //Button callbacks

    $("#toFirstFrameButton").click(function () {
        if (UI.numFrames && currentFrame > 0) {
            requestStopCB(function () {
                currentFrame = 0;
                updateAll();
            });
        }
    });

    $("#toLastFrameButton").click(function () {
        if (UI.numFrames && currentFrame < UI.numFrames) {
            requestStopCB(function () {
                currentFrame = UI.numFrames;
                updateAll();
            });
        }
    });

    $("#playButton").click(function () {
        if (UI.numFrames) {
            if (!isPlaying) {
                //reset some stuff
                requestStop = false;
                isPlaying = true;
                startPlayback();
            }
        }
    });

    //Stop on both stop and play button
    $("#stopButton").click(function () {
        if (UI.numFrames) {
            if (isPlaying) {
                stopPlayback();
            }
        }
    });

    //detect key changes on frame box
    $("#currentFrameInput").on("change paste keyup", function () {
        var currentValue = $(this).val();
        if (!isNaN(currentValue) && currentValue != '') {
            var newFrame = parseInt(currentValue);
            if (UI.numFrames && newFrame != currentFrame && newFrame >= 0 && newFrame <= UI.numFrames) {
                currentFrame = newFrame;
                updateAll();
            }
        }
    });
    //detect input for max frames
    $("#maxFramesInput").on("change paste keyup", function () {
        var currentValue = $(this).val();
        if (!isNaN(currentValue) && currentValue != '') {
            var newMaxFrames = parseInt(currentValue);
            if (UI.numFrames && newMaxFrames >= 0) {
                UI.numFrames = newMaxFrames;
            }
        }
    });


    $(document).keyup(function (e) {
        if (e.keyCode == 27) { // escape key maps to keycode `27`
            if (isPlaying) {
                stopPlayback();
            }
        }
    });

    //Resizing
    document.getElementById('decreaseResolutionButton').onclick = function () {
        decreaseCanvasResolution();
        canvas = $("#glRenderTarget").get(0)
        $("#currentResolution").val(canvas.width + "x" + canvas.height);
        currentFrame = 0;
        updateAll();
    };

    document.getElementById('increaseResolutionButton').onclick = function () {
        increaseCanvasResolution();
        canvas = $("#glRenderTarget").get(0)
        $("#currentResolution").val(canvas.width + "x" + canvas.height);
        currentFrame = 0;
        updateAll();
    };

});