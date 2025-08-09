const chatBody=document.querySelector(".chat-body");
const messageInput=document.querySelector(".message-input");
const sendMessageButton=document.querySelector("#send-message");
const queries = []; 
const userData={
    message:null
}

const createMessageElement=(content,...classes)=>{
    const div=document.createElement("div");
    div.classList.add("message",...classes);
    div.innerHTML=content;
    return div;
}


const generateBotResponse=async(incomingMessageDiv)=>{
    const MessageElement=incomingMessageDiv.querySelector(".message-text");
    const requestOptions={
        method:"POST",
       headers:{"Content-Type":"application/json" },
       body:JSON.stringify({
        contents:[{
            parts:[{text: userData.message}]
            }]
       })  
    }
  try{ 
    const response= await fetch(API_URL,requestOptions);
    const data=await response.json();
    if(!response.ok) throw new Error(data.error.message);
    
    const apiResponseText= data.candidates[0].content.parts[0].text.replace(/\*\*(.*?)\*\*/g, "$1").trim();
    MessageElement.innerText=apiResponseText; 
}
  catch(error){
    console.log(error);
    MessageElement.innerText=error.message;
    MessageElement.style.color="#ff0000";

}
  finally{
    incomingMessageDiv.classList.remove("thinking");
    
    chatBody.scrollTo({top:chatBody.scrollHeight,behavior:"smooth"}); 
  }
}


const handleuserMessage =(sam)=>{
    sam.preventDefault();
    userData.message=messageInput.value.trim();
    messageInput.value="";

      console.log(userData)
        chatBody.scrollTo({top:chatBody.scrollHeight,behavior:"smooth"});

    setTimeout(()=>{
        const messageContent=`  <img src="aireply.png" alt="Description" height="20px>
             <div class="message-text">
                <div class="thinking-indicator">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                </div> `
        const incomingMessageDiv = createMessageElement(messageContent,"bot-message","thinking");
        chatBody.appendChild(incomingMessageDiv);
        
        chatBody.scrollTo({top:chatBody.scrollHeight,behavior:"smooth"});
        generateBotResponse(incomingMessageDiv);  

    },600);

}
messageInput.addEventListener("keydown",(sam)=>{
    const userMessage=sam.target.value.trim();
    if(sam.key=="Enter" && userMessage){
        handleuserMessage(sam);
    }
});

sendMessageButton.addEventListener("click",(sam)=>handleuserMessage(sam)) 