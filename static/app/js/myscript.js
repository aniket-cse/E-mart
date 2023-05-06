$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})
$('.plus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children['2']
    console.log(id) //debug ke liye
    //ajax ka use karke humid ko bhegenge taki humara page refresh na ho
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id:id
        },
        //sending success hoga to success function call hoga humlog ajax me padh chuke hai
        //jo data server se ayega o function ko mil jayega data nam ka variable me
        success:function(data){
            console.log(data)
            console.log("success")
            //addtocart.html me {{cart.quantity }} ko update karwana hai
            //element(cart.quantity) isko update karne ke liye current object(plus-cart ka) uska parentnode ka second element par jo chield hai o humara usper update 
            //karwana hai innerText karke to up date hokar dikhai dega
            eml.innerText=data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("total_amount").innerText=data.total_amount

        }
    })
})
$('.minus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children['2']
    console.log(id) //debug ke liye
    //ajax ka use karke humid ko bhegenge taki humara page refresh na ho
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id:id
        },
        //sending success hoga to success function call hoga humlog ajax me padh chuke hai
        //jo data server se ayega o function ko mil jayega data nam ka variable me
        success:function(data){
            console.log(data)
            console.log("success")
            //addtocart.html me {{cart.quantity }} ko update karwana hai
            //element(cart.quantity) isko update karne ke liye current object(plus-cart ka) uska parentnode ka second element par jo chield hai o humara usper update 
            //karwana hai innerText karke to up date hokar dikhai dega
            eml.innerText=data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("total_amount").innerText=data.total_amount

        }
    })
})
$('.remove-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this
    console.log(id) //debug ke liye
    //ajax ka use karke humid ko bhegenge taki humara page refresh na ho
    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id:id
        },
        //sending success hoga to success function call hoga humlog ajax me padh chuke hai
        //jo data server se ayega o function ko mil jayega data nam ka variable me
        success:function(data){
            console.log(data)
            console.log("delete")
            //addtocart.html me {{cart.quantity }} ko update karwana hai
            //element(cart.quantity) isko update karne ke liye current object(plus-cart ka) uska parentnode ka second element par jo chield hai o humara usper update 
            //karwana hai innerText karke to up date hokar dikhai dega
            document.getElementById("amount").innerText=data.amount
            document.getElementById("total_amount").innerText=data.total_amount
            //4 div hai isliye 4 parentnode
            eml.parentNode.parentNode.parentNode.parentNode.remove()

        }
    })
})
