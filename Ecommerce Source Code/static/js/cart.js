
var updatebtns = document.getElementsByClassName('update-cart')

for(var i=0; i < updatebtns.length ; i++){
    updatebtns[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log(productId)
        console.log(action)

        console.log(user)
        if(user === "AnonymousUser"){
            addCookieItems(productId,action)
            // console.log("it is not an authenticated user" , user)
        }
        else{
            UpdateUserItems(productId,action)
//            console.log("it is an authenticated user" , user)
        }
    })
}

function addCookieItems(productId,action){
    console.log("it is un-authenticated user" )

    if(action == "add"){
        if(cart[productId] == undefined){
            cart[productId] = {"quantity" : 1}
        }
        else{
            cart[productId]['quantity'] += 1
        }
    }
    else if(action == "remove"){
        cart[productId]['quantity'] -= 1
        if(cart[productId]['quantity'] <= 0){
            console.log("Remove item..")
            delete cart[productId]
        }
    }
    console.log("cart:",cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
            
}


function UpdateUserItems(productId,action)
{
    var url = "/update_item/"

    // fetch api is used
    // if we use
    fetch( url ,{
        method : "POST",
        headers : {
            // since we are sending json file
            "Content-Type" : "application/json",
            "X-CSRFToken" : csrftoken,
        },
        body : JSON.stringify({"productId":productId,"action":action})
    })

    // to get the response if it is successful => ( promise() concept is used )
    .then(res => {
        return res.json()
    })

    // to display the data
    .then(data => {
        console.log("data",data)
        location.reload();
    })
}



