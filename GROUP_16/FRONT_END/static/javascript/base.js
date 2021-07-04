$(
    function () {
        // For selection of state depending on the state
        $('#state').change(function() {
            if ($("#district").length <= 0) {
                return;
            }
            $("#district").empty();
            $("#district").append("<option disabled selected value>-- select district --</option>");
            $("#district").attr('disabled',true);
            var state_name = $(this).find('option:selected').val();
        
            $.ajax({
                url: "/getDistricts",
                type: 'GET',
                data : {
                    'state_name' : state_name
                },
                dataType : 'json',
                success: function(response) {
                    $("#district").attr('disabled',false);
                    response.forEach(element => {
                        $("#district").append("<option value="+ element[0] +">" + element[1] + "</option>");
                    });
            
                }
            });
        
        }
        );

        $('#state_id').change(function() {
            if ($("#district_id").length <= 0) {
                return;
            }
            $("#district_id").empty();
            $("#district_id").append("<option disabled selected value>-- select district --</option>");
            $("#district_id").attr('disabled',true);
            var state_name = $(this).find('option:selected').val();
        
            $.ajax({
                url: "/getDistricts",
                type: 'GET',
                data : {
                    'state_name' : state_name
                },
                dataType : 'json',
                success: function(response) {
                    $("#district_id").attr('disabled',false);
                    response.forEach(element => {
                        $("#district_id").append("<option value="+ element[0] +">" + element[1] + "</option>");
                    });
            
                }
            });
        
        }
        );

        // For selecting variety for a given commodity
        $('#commodity').change(function() {
            if ($("#variety").length <= 0) {
                return;
            }
            $("#variety").empty();
            $("#variety").append("<option disabled selected value>-- select variety --</option>");
            $("#variety").attr('disabled',true);
            var commodity_name = $(this).find('option:selected').val();
        
            $.ajax({
                url: "/getVariety",
                type: 'GET',
                data : {
                    'commodity_name' : commodity_name
                },
                dataType : 'json',
                success: function(response) {
                    $("#variety").attr('disabled',false);
                    $("#variety").append("<option value=\"All\">All</option>");
                    response.forEach(element => {
                        $("#variety").append("<option value=\""+ element[1] +"\">" + element[1] + "</option>");
                    });
            
                }
            });
        
        }
        );

        $('#commodity_id').change(function() {
            if ($("#variety_id").length <= 0) {
                return;
            }
            $("#variety_id").empty();
            $("#variety_id").append("<option disabled selected value>-- select variety --</option>");
            $("#variety_id").attr('disabled',true);
            var commodity_name = $(this).find('option:selected').val();
        
            $.ajax({
                url: "/getVariety",
                type: 'GET',
                data : {
                    'commodity_name' : commodity_name
                },
                dataType : 'json',
                success: function(response) {
                    $("#variety_id").attr('disabled',false);
                    response.forEach(element => {
                        $("#variety_id").append("<option value="+ element[0] +">" + element[1] + "</option>");
                    });
            
                }
            });
        
        }
        );

        $('#district').change(function() {
            if (!$("#market").length) {
                return;
            }
            $("#market").empty();
            $("#market").append("<option disabled selected value>-- select market --</option>");
            $("#market").attr('disabled',true);
            var state_name = $('#state').find('option:selected').val();
            var district_name = $(this).find('option:selected').val();
            $.ajax({
                url: "/getMarkets",
                type: 'GET',
                data : {
                    'state_name' : state_name,
                    'district_name' : district_name
                },
                dataType : 'json',
                success: function(response) {
                    $("#market").attr('disabled',false);
                    response.forEach(element => {
                        $("#market").append("<option value="+ element[1] +">" + element[1] + "</option>");
                    });
            
                }
            });
        
        }
        );

        $('#district_id').change(function() {
            if (!$("#market_id").length) {
                return;
            }
            $("#market_id").empty();
            $("#market_id").append("<option disabled selected value>-- select market --</option>");
            $("#market_id").attr('disabled',true);
            var state_name = $('#state_id').find('option:selected').val();
            var district_name = $(this).find('option:selected').val();
            $.ajax({
                url: "/getMarkets",
                type: 'GET',
                data : {
                    'state_name' : state_name,
                    'district_name' : district_name
                },
                dataType : 'json',
                success: function(response) {
                    $("#market_id").attr('disabled',false);
                    response.forEach(element => {
                        $("#market_id").append("<option value="+ element[0] +">" + element[1] + "</option>");
                    });
            
                }
            });
        
        }
        );
    }
);