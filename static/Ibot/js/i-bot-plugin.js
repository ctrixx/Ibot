// I-bot HTML DOM Global Variables
{
    var miniChatStatus;
    var chatSession;
    var queryError=0;
    var openButton = document.getElementsByClassName('i-bot')[0];
    var mini = document.getElementsByClassName("mini-chat")[0];
    var chatContent = document.getElementsByClassName('chat-content')[0];
    var close = document.getElementsByClassName('close-chat')[0];
    var info = document.getElementsByClassName('bot-info')[0];
    var infobox = document.getElementsByClassName("info-box")[0];
    var full = document.getElementsByClassName('full-screen-page')[0];
    var submitBtn = document.getElementsByClassName('submit')[0];
    var queryInput = document.querySelector('input[name=query]');

    //Main Mini and Full Ibot containers
    var mC = document.getElementsByClassName('mini-chat')[0];
    var fC = document.getElementsByClassName('full-chat-box')[0];
}

//I-BOT MAIN FUNCTIONS


//Ajax function to submit query and get response
function poster(query,follow){
    $.get('/submit/?query='+query+'&follow='+follow,function(data,status){
        response_data = JSON.parse(data);
        response_string = response_data["response_string"];
        response_attachment = response_data["response_attachment"];
        response_follow = response_data["follow_up"];
        try {
            document.getElementsByClassName('follow-up')[0].className="msg-cont";
        }
        catch(err){
            var nott = 0;
        }
        var msgbox = messageBox('bot-msg',response_string,response_attachment);
        if(response_follow!="None"){
            msgbox.className= msgbox.className+" follow-up";
            msgbox.setAttribute("data-follow",response_follow);
        }
        chatContent.appendChild(msgbox)
        setTimeout(function () {
            chatContent.scrollTop = chatContent.scrollHeight;
        },100)
    })
}

//Check and Submit User's Query
function submit(){
    var userQuery = queryInput.value;

    //Check and Verify
    if(userQuery!=""){
        var format = /^[a-zA-Z0-9.,?-_ ]*$/;
        if(format.test(userQuery)==true){
            queryError=0;
        }else {
            queryError=1;
        }
    }else{
        queryInput.style.borderColor = "firebrick";
        queryError=1;
    }
    if(queryError==0){
        chatContent.appendChild(messageBox('user-msg',userQuery,0));

        try{
            var fup = document.getElementsByClassName('follow-up')[0];
            var follow = fup.getAttribute('data-follow');
        }
        catch(err){
            var follow = "";
        }

        poster(userQuery,follow);
        queryInput.value = "";
    }
    //Restore query input to default
    queryInput.addEventListener('focus',function () {
        queryInput.style.borderColor = "white";
        queryInput.value = "";
    })
}

// Create Default Message
function defaultMessage(){
    var message = "Hi There! What would you like to find out today?";
    var msgCont = document.createElement('div');
    msgCont.className = "msg-cont";
    var botMsg = document.createElement('div');
    var para = document.createElement("p");
    para.innerHTML = message;
    botMsg.appendChild(para)
    botMsg.className = "bot-msg";
    msgCont.appendChild(botMsg);
    return msgCont;
}

//Create Users Messages and  Bot Messages
function messageBox(classtype,message,attachment){
    var msgCont = document.createElement('div');
    msgCont.className = "msg-cont";
    var typeMsg = document.createElement('div');
    var para = document.createElement("p");
    para.innerHTML = message;
    typeMsg.appendChild(para)
    typeMsg.className = classtype;
    msgCont.appendChild(typeMsg);
    if(classtype=="bot-msg"){
        var msgOptions = document.createElement('div');
        msgOptions.className = "msg-options";
        var pict = document.createElement('i');
        pict.className = "fa fa-picture-o";
        var warn = document.createElement('i');
        warn.className = "fa fa-warning";
        if(attachment!=0) {
            msgOptions.appendChild(pict);
        }
        //msgOptions.appendChild(warn);
        msgCont.appendChild(msgOptions);
    }
    return msgCont;
}



// Animation Functions
var fadeIn = function(object,time){
    object.style.display = "block";
    object.style.transition = "opacity "+time+ "s";
    setTimeout(function(){
        object.style.opacity = "1";
    },100)
}
var fadeOut = function(object,time){
    object.style.transition = "opacity "+time+ "s";
    object.style.opacity = "0";
    setTimeout(function(){
        object.style.display = "none";
    },time*1000)
}
//Function that controls the mini-chat-box

var miniChat = function(){

    // Function to listen for open event of mini box
    openButton.addEventListener("click", function(){
        fadeIn(mini,1.5)
        miniChatStatus = 1;
        openButton.style.display = "none";

        //Print default message to user
        if(chatSession!="started"){
            setTimeout(function(){
                chatContent.appendChild(defaultMessage())
            },1000)
        }

        chatSession = "started";

    });

    //Function to listen for closing event of mini box

    close.addEventListener("click", function(){
        mini.style.display = "none";
        setTimeout(function(){
            mini.style.opacity = "0";
        },100)
        miniChatStatus = 0;
        openButton.style.display = "block";

    });
    
    //Function to listen for display of help information to user
    info.addEventListener("mouseenter",function(){
        fadeIn(infobox,0.2);
    })
    info.addEventListener("mouseleave",function(){
        fadeOut(infobox,0.2);
    })

    //Function to open full screen page
    full.addEventListener("click", function(){
        window.location.replace("/full-screen-chat");
    })

    //Call the submit function
    submitBtn.addEventListener('click',function(){
            submit();
    })

    //Check for overflow of mini chat and activate scroll
    setInterval(function () {
        var chatContentHeight = chatContent.scrollHeight;
        if(chatContentHeight > 280){
            chatContent.style.height = "280px";
            chatContent.style.overflowY = "scroll";
        }else{
            chatContent.style.height = "auto";
            chatContent.style.overflowY = "hidden";
        }
        //var tester = document.getElementById('test');
        //tester.innerHTML=chatContentHeight;
    },100)

    // Listen for use of Enter key for submitting the query
    queryInput.addEventListener('keydown',function(event){
        if(event.key == "Enter"){
            submit();
        }
    })

    //Extra function to open help page
    var binfo = document.getElementById("bot-info");
    binfo.addEventListener('click',function(){
        location.replace('/help')
    })

}

// Function that controls the full chat page
var fullChat = function(){

    //Print default message to user
    if(chatSession!="started"){
        setTimeout(function(){
            chatContent.appendChild(defaultMessage())
        },1000)
    }

    chatSession = "started";

    //Function to listen for display of help information to user
    info.addEventListener("mouseenter",function(){
        fadeIn(infobox,0.2);
    })
    info.addEventListener("mouseleave",function(){
        fadeOut(infobox,0.2);
    })

    //Check for overflow of full chat and activate scroll
    setInterval(function () {
        var fullChatBoxHeight = fC.scrollHeight;
        var chatContentHeight = chatContent.scrollHeight;
        if(chatContentHeight > fullChatBoxHeight-90){
            chatContent.style.height = "65vh";
            chatContent.style.overflowY = "scroll";
        }else{
            chatContent.style.height = "auto";
            chatContent.style.overflowY = "hidden";
        }
        //var tester = document.getElementById('test');
        //tester.innerHTML=chatContentHeight;
    },100)

    //Call the submit function
    submitBtn.addEventListener('click',function(){
            submit();
    })

    // Listen for use of Enter key for submitting the query
    queryInput.addEventListener('keydown',function(event){
        if(event.key == "Enter"){
            submit();
        }
    })

    //Extra function to open help page
    var binfo = document.getElementById("bot-info");
    binfo.addEventListener('click',function(){
        location.replace('/help')
    })

}
///Check if mini-chat or full-chat is present

if(mC!=null){
    miniChat();
}
if(fC!=null){
    fullChat();
}

