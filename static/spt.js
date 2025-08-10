const chatBody=document.querySelector(".chat-body");
const messageInput=document.querySelector(".message-input");
const sendMessageButton=document.querySelector("#send-message");
async function getData() {
  try {
    
    const response =  fetch('http://127.0.0.1:5000/xyz');
    const data = await response.json();
    try{ 
    const apiResponseText=response ;
    MessageElement.innerText=apiResponseText; 
    }
    catch(error){
    console.log(error);
    MessageElement.innerText=error.message;
    MessageElement.style.color="#ff0000";

    }
    finally{
    chatBody.scrollTo({top:chatBody.scrollHeight,behavior:"smooth"}); 
    }
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}
getData();