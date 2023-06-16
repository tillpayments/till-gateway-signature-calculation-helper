function get_current_utc_time() {
    time = new Date(Date());
    utctime = time.toUTCString();
    document.getElementById("timestamp").value = utctime;
}

function sig_generation() {
    // var apiKey = document.getElementById("apikey");
    var sharedSecret = document.getElementById("sharedsecret");
    var method = document.getElementById("requestmethod");
    var requestBody = document.getElementById("requestbody");
    var contentType = document.getElementById("content-type");
    var timestamp = document.getElementById("timestamp");
    var endpoint = document.getElementById("endpoint");
    var signedRequest = document.getElementById("signedrequest");
    if (endpoint.value.includes("://")) {
        var processedEndpoint = "/" + endpoint.value.split("/").slice(3).join("/");
    } else {
        var processedEndpoint = endpoint.value
    };
    // console.log(processedEndpoint);
    if (signedRequest.checked === true) {
        var hashedBody = CryptoJS.MD5(requestBody.value).toString();
    } else {
        var hashedBody = CryptoJS.SHA512(requestBody.value).toString();
    };
    var message = method.value + "\n" + hashedBody + "\n" + contentType.value + "\n" + timestamp.value + "\n" + processedEndpoint
    // console.log(hashedBody);
    // console.log(message);
    var signature = CryptoJS.HmacSHA512(message, sharedSecret.value).toString(CryptoJS.enc.Base64);
    // console.log(signature);
    document.getElementById("sig-generation").hidden = false;
    document.getElementById("hashedpayload").value = hashedBody;
    document.getElementById("concatenatedmessage").value = message;
    document.getElementById("signature").value = signature;
}