
// var field = document.getElementById("field");
// var discription=document.getElementById("discription");
// // var resume_area=document.getElementById("resume_area");
// var button=document.getElementById("button");
// var main_area=document.getElementById("main_area");
// var hr=document.getElementById("hr");
// var ans_sub_but=document.getElementById("sub");
// var next=document.getElementById("next");
// var area=document.getElementById("area");
// button.addEventListener('click',function(event){
//     event.preventDefault()
//     var question=document.getElementById('qn')
//     var form=document.getElementById('job_detail_form')
//     var formData = new FormData(form);
//     fetch( generateQuestionUrl , { // Django will replace this with the correct URL
//         method: "POST",
//         body: formData,
//         headers: {
//             "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value // Correct the case to .value
//         }
//     })
//     .then(response=>response.json())
//     .then(data=>
//     {question.value=data.question});

    
//     field.style.display = "none";
//     // resume_area.style.display = "none";
//     discription.style.display = "none";
//     button.style.display = "none";
//     hr.style.display = "none";
//     main_area.style.display = "flex";
//     })

// var feedbacke=document.getElementById("feedback-card");
// var answere=document.getElementById("answer-card");
// function feedback()
// {
//     if(feedbacke.style.display == "flex")
//     {
//         feedbacke.style.display = "none";
//     }
//     else{
//         feedbacke.style.display = "flex";
//     }
// }
// function answer()
// {
//     if(answere.style.display == "flex")
//         {
//             answere.style.display = "none";
//         }
//         else{
//             answere.style.display = "flex";
//         }
// }
// var aud = document.getElementById("audio-upload");
// var tex = document.getElementById("textarea");

// function showAudio() {
//     aud.style.display = "block";
//     tex.style.display = "none";
// }

// function showTextarea() 
// {
//     aud.style.display = "none";
//     tex.style.display = "block";
// // }
// function feedback_ans()
// {
//     feedbacke.style.display = "flex";
//     answere.style.display = "flex"; 
//     ans_sub_but.style.display="none";
//     next.style.display="block";
// }
// function next_ans()
// {
//     next.style.display="none";
//     ans_sub_but.style.display="block";
//     feedbacke.style.display = "none";
//     answere.style.display = "none"; 
//    area.scrollIntoView({
//         behavior: "smooth",
//         block: "center"
//     });
// }