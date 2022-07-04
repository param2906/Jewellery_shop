$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[1]
    $.ajax({
       type: "GET",
       url: "/shop/pluscart",
       data:{
           prod_id: id
       },
       success: function(data){
          eml.innerText = data.quantity
          document.getElementById("amount").innerText = data.amount
          document.getElementById("GST").innerText = data.GST
          document.getElementById("total_amount").innerText = data.total_amount
       }
    })
})

$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[1]
    $.ajax({
       type: "GET",
       url: "/shop/minuscart",
       data:{
           prod_id: id
       },
       success: function(data){
          eml.innerText = data.quantity
          document.getElementById("amount").innerText = data.amount
          document.getElementById("GST").innerText = data.GST
          document.getElementById("total_amount").innerText = data.total_amount
       }
    })
})

$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this
    $.ajax({
       type: "GET",
       url: "/shop/removecart",
       data:{
           prod_id: id
       },
       success: function(data){
          document.getElementById("amount").innerText = data.amount
          document.getElementById("GST").innerText = data.GST
          document.getElementById("total_amount").innerText = data.total_amount
          eml.parentNode.parentNode.parentNode.
          remove()
       }
    })
})
