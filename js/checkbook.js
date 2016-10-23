//Load css fro button

var Checkbook;
Checkbook || (Checkbook = {}),
    Checkbook = function() {
        var data_key, amountVal,
        host = "https://www.checkbook.io/";
        checkout_host = "https://www.checkbook.io/api/v1/checkout"; //FOR PRODUCTION
        var checkbook_iframe;
        var merchantOrigin = window.location.href;

        var _createButton = function() {
            var button, form, iframe;
            var body = document.getElementsByTagName('body')[0];
            var data = document.getElementById("checkbook_var");

            if (data.getAttribute("data-env") != null && data.getAttribute("data-env") == "sandbox") {
                host = "https://sandbox.checkbook.io/";
                checkout_host = "https://sandbox.checkbook.io/api/v1/checkout"; //FOR SANDBOX
            } else if (data.getAttribute("data-env") != null && data.getAttribute("data-env") == "local") {
                host = "http://0.0.0.0:8000/";
                checkout_host = "http://0.0.0.0:8000/api/v1/checkout"; //FOR LOCAL
            } else if (data.getAttribute("data-env") != null && data.getAttribute("data-env") == "stage") {
                host = "https://stage.checkbook.io/";
                checkout_host = "https://stage.checkbook.io/api/v1/checkout"; //FOR STAGE
            } else if (data.getAttribute("data-env") != null && data.getAttribute("data-env") == "dev") {
                host = "https://dev.checkbook.io/";
                checkout_host = "https://dev.checkbook.io/api/v1/checkout"; //FOR STAGE
            }else {
                host = "https://www.checkbook.io/";
                checkout_host = "https://www.checkbook.io/api/v1/checkout"; //FOR PRODUCTION
            }

            _loadcssfile(host + "static/css/button.css", "css") ////dynamically load and add this .css file

            if (document.getElementById("checkbook_btn_")) {
                //Make it better in future so if user removes the button, you can fix it 
            } else {
                button = document.createElement("button");
                button.setAttribute("type", "button");
                button.setAttribute("id", "checkbook_btn_");
                button.setAttribute("value", "submit");
                button.className = "checkbook-button-el";
                button.appendChild(document.createTextNode("Pay by Digital Check"));
            }



            form = document.getElementById("checkbook_io");
            if (!form) {
                alert("checkbook form needs to have an id 'checkbook_io' ");
            } else {

                if (button) {
                    form.appendChild(button);
                }


                iframe = document.createElement("iframe");
                iframe.style.display = "none";
                iframe.style.border = 0;
                iframe.id = "__checkbook_frame";
                iframe.className = "checkbook_iframe";
                iframe.name = "__checkbook_frame";
                iframe.src = checkout_host;


                iframe.setAttribute("data-key", data.getAttribute("data-key"));
                iframe.setAttribute("data-amount", data.getAttribute("data-amount"));
                iframe.setAttribute("data-name", data.getAttribute("data-name"));
                iframe.setAttribute("data-for", data.getAttribute("data-for"));
                iframe.setAttribute("data-description", data.getAttribute("data-description"));
                iframe.setAttribute("data-user-email", data.getAttribute("data-user-email"));
                iframe.setAttribute("data-businessName", data.getAttribute("data-businessName"));
                iframe.setAttribute("data-firstName", data.getAttribute("data-firstName"));
                iframe.setAttribute("data-lastName", data.getAttribute("data-lastName"));
                iframe.setAttribute("data_isBusiness", data.getAttribute("data_isBusiness"));                
                iframe.setAttribute("data-addr1", data.getAttribute("data-addr1"));
                iframe.setAttribute("data-addr2", data.getAttribute("data-addr2"));
                iframe.setAttribute("data-city", data.getAttribute("data-city"));
                iframe.setAttribute("data-state", data.getAttribute("data-state"));
                iframe.setAttribute("data-country", data.getAttribute("data-country"));
                iframe.setAttribute("data-env", data.getAttribute("data-env"));

                



                amountVal = data.getAttribute("data-amount");

                form.appendChild(iframe);



                checkbook_iframe = document.getElementById('__checkbook_frame');

                //When button is clicked , show the iframe
                document.getElementById("checkbook_btn_").onclick = function() {
                    document.getElementById('__checkbook_frame').style.display = "block";
                    //document.getElementById('__checkbook_frame').src = checkout_host;
                    //Posting Data
                    var postObj = {};
                    postObj["data-key"] = data.getAttribute("data-key");
                    postObj["data-amount"] = data.getAttribute("data-amount");
                    postObj["data-name"] = data.getAttribute("data-name");
                    postObj["data-for"] = data.getAttribute("data-for");
                    postObj["data-description"] = data.getAttribute("data-description");
                    //postObj["data-user-email"] = data.getAttribute("data-user-email") ;
                    if (document.getElementById("email_id_from_parent")) {
                        postObj["data-user-email"] = document.getElementById("email_id_from_parent").value;
                    } else {
                        postObj["data-user-email"] = data.getAttribute("data-user-email");
                    }
                    postObj["data-redirect-url"] = data.getAttribute("data-redirect-url");
                    postObj["data-businessName"] = data.getAttribute("data-businessName");
                    postObj["data-interval"] = data.getAttribute("data-interval");
                    postObj["data-duration"] = data.getAttribute("data-duration");                    
                    postObj["data-firstName"] = data.getAttribute("data-firstName");
                    postObj["data-lastName"] = data.getAttribute("data-lastName");
                    postObj["data-isBusiness"] = data.getAttribute("data-isBusiness");
                    postObj["data-addr1"] = data.getAttribute("data-addr1");
                    postObj["data-addr2"] = data.getAttribute("data-addr2");
                    postObj["data-city"] = data.getAttribute("data-city");
                    postObj["data-state"] = data.getAttribute("data-state");
                    postObj["data-zip"] = data.getAttribute("data-zip");
                    postObj["data-country"] = data.getAttribute("data-country");
                    postObj["data-env"] = data.getAttribute("data-env");
                    postObj["data-merchantOrigin"] = merchantOrigin;

                    checkbook_iframe.contentWindow.postMessage(JSON.stringify(postObj), checkout_host);

                    // Create IE + others compatible event handler
                    var eventMethod = window.addEventListener ? "addEventListener" : "attachEvent";
                    var eventer = window[eventMethod];
                    var messageEvent = eventMethod == "attachEvent" ? "onmessage" : "message";

                    // Listen to message from child window
                    eventer(messageEvent, function(e) {
                        var data = JSON.parse(e.data);
                        if (data["data-token"]) {
                            form = document.getElementById("checkbook_io");
                            if (!form) {
                                alert("checkbook form needs to have an id 'checkbook_io' ");
                            } else {

                                form.action = data["data-redirect-url"];

                                var token = document.createElement("input");
                                token.setAttribute("type", "hidden");
                                token.setAttribute("name", "token");
                                token.setAttribute("value", data["data-token"]);
                                form.appendChild(token);

                                var amount = document.createElement("input");
                                amount.setAttribute("type", "hidden");
                                amount.setAttribute("name", "amountVal");
                                amount.setAttribute("value", amountVal);
                                form.appendChild(amount);

                                form.submit();
                            }
                        } else if (data['msg'] == 'closeIframe'){
                            console.log("This is the message from cbIframe");
                            document.getElementById('__checkbook_frame').style.display = 'none';
                        } else {
                            console.log("no message");
                        }

                    }, false);

                }

            }
        }

        var _loadcssfile = function(filename, filetype) {

            if (filetype == "css") { //if filename is an external CSS file
                var fileref = document.createElement("link")
                fileref.setAttribute("rel", "stylesheet")
                fileref.setAttribute("type", "text/css")
                fileref.setAttribute("href", filename)
            }
            if (typeof fileref != "undefined") {
                document.getElementsByTagName("head")[0].appendChild(fileref);
            }
        }

        //CALL
        _createButton();

    }();
