// alert("Working Msg1")
// $(
//     function () {
//         $('#state').change(function() {
//             $("#district").empty();
//             $("#district").append("<option disabled selected value>-- select an option --</option>");
//             $("#district").attr('disabled',true);
//             var state_name = $(this).find('option:selected').val();
        
//             $.ajax({
//                 url: "/getDistricts",
//                 type: 'GET',
//                 data : {
//                     'state_name' : state_name
//                 },
//                 dataType : 'json',
//                 success: function(response) {
//                     $("#district").attr('disabled',false);
//                     response.forEach(element => {
//                         $("#district").append("<option value="+ element[1] +">" + element[1] + "</option>");
//                     });
            
//                 }
//             });
        
//         }
//         );
//     }
// );