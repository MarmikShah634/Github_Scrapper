let link = document.getElementById("link");
const pattern = /^https:\/\/github\.com\/[^\/]+$/;

document.getElementById("btn").addEventListener("click", (e)=>{
    e.preventDefault();
    let linkValue = link.value;
    if (!pattern.test(linkValue)){
        alert("Enter Valid Github Profile URL.");
        link.focus();
        return false;
    }
    else{
        document.getElementById("profileForm").submit();
    }
})
