
var category_first_options = {
    "Mechanical Sys and Components": ["Mechanical System", "Simple Machine Equipment", "Filters", "Fasteners", "Pipe, Tubing, Hose & Fittings", "Hinges, eyelets and joints", "Bearings", "Bushings", "Shafts and couplings", "Seals, glands", "Springs", "Gears", "Wheels", "Rotary-reciprocating mechanisms", "Enclosures"],
    "Electrical Systems": ["Electrical System", "Electrical wires and cables", "Insulation", "Components for electrical equipment", "Electrical accessories", "Lamps and related equipment", "Rotating machinery", "Transformers", "Reactors", "Rectifiers", "Converters", "Batteries"],
    "Electro-Mechanical Systems": ["Electro-Mechanical Assembly"],
}

var category_second_options = {
    "Simple Machine Equipment": ["Machine", "Lever", "Switch", "Hook", "Valve", "Actuators", "Mechanical Brakes", "Nozzles", "Plain Guidings", "Chain drives", "Belt drives"],
    "Filters": ["Air Filters", "Sieves", "Mesh Filters", "Masks"],
    "Fasteners": ["Bolt, Screws and Studs", "Nuts", "Pins", "Washers", "Clamps", "Plates"],
    "Pipe, Tubing, Hose & Fittings": ["Pipe Fittings", "Pipe Hangers", "Pipe Joints"],
    "Hinges, eyelets and joints": ["Hinges", "Articulations eyelets & joints", "Knobs", "Sockets"],
    "Bearings": ["Plain Bearings", "Thrust Bearings", "Roller Bearings", "Bearing accessories", "Bushes", "Flanged block bearing", "Flanged plain bearings", "Right angular gearings", "Radial contact ball bearings"],
    "Bushings": ["Bushings", "Bumpers", "Grommets", "Pads"],
    "Shafts and couplings": ["Shaft", "Couplings", "Spacers", "Keys and keyways splines", "collars"],
    "Seals, glands": ["Seals", "Edge Seals", "O-rings", "Gaskets", "Caps", "Plugs", "Tapes"],
    "Springs": ["Springs", "Spring washers", "Extension Springs", "Die Springs", "Strip Springs", "Linear Wave", "Rotor Springs"],
    "Gears": ["Gears", "Spur gears", "Sprockets", "Pulleys", "Timing Belts", "Gear Boxes", "Gear Rod Stock", "Ratcheting Gears", "Worm Gears", "Helical Gears", "Rack Gears"],
    "Wheels": ["Wheel", "Castor Wheels", "Roller Wheels"],
    "Rotary-reciprocating mechanisms": ["Rotary System", "Impeller", "Turbine", "Fan", "Motors"],
    "Enclosures": ["Shell", "Boxes", "Metal Casing Sheets", "Covers", "Flexible Covers", "Aluminum Extruded Frames"],
}

var category_third_options = {
    "Bolt, Screws and Studs": ["Bolt", "Screws", "Studs", "Screws & bolts \w countersunk head", "Screws & bolts \w hexagonal head", "Screws & bolts \w cylindrical head", "Tapping screws", "Studs", "Washer bolt", "Eye screws", "Set screw", "Threaded rods"],
    "Nuts": ["Nuts", "Castle nuts", "Locknuts", "Square nuts", "T-nut", "Hexagonal nuts", "Flange nut", "Rivet nut", "Slotted nuts", "Wingnuts", "Cap nuts"],
    "Pins": ["General Pins", "Locating pins", "Split pins", "Cylindrical pins", "Taper pins", "Grooved pins", "Roll pins", "Pivot pins", "Locking pins"],
    "Washers": ["Washer", "Lock washers", "Convex washer", "Thrust washers", "Knurled Washers"],
    "Clamps": ["Clamp", "Rivets", "Staples", "Snap Rings"],
    "Plates": ["Plates", "Rectangular Plates", "Circular Plates"],
    "Pipe Fittings": ["Elbow fitting", "T-shape fitting"],
    "Pipe Joints": ["Pipe Flanges", "Tube Fittings", "Hose", "Hose Fittings", "Tube Clamps"],
    "Roller Wheels": ["Roller Wheels", "Track Rollers", "V-Groove Track Rollers", "Flanged Track Rollers"],
}

init();

function init() {
    $('#submit-btn').click(function () {
        var checked = [];
        
        $('#checkboxes input:checked').each(function() {
            checked.push($(this).attr('id'));
        });

        // var cluser_name = [];
        // $('.form-control').each(function() {
        //     let name = $(this).val();
        //     if (name) {
        //         cluser_name.push(name);
        //     }
        // });

        if (checked.length > 1) {
            $('#submit-btn').prop('disabled', true);
            $.ajax({
                url: "/taxonomy/submit",
                method: "POST",
                data: {
                    oid: checked,
                    // cluster: cluser_name,
                    cluster_id: $(".id-text").attr('id')
                },
                success: function (res) {
                    console.log(res);
                    if(res.status === "Success.") {
                        window.location = '/taxonomy';
                    } else {
                        alert('You have already annotated this cluster!');
                        window.location = '/taxonomy';
                    }
                }
            })
        } else {
            alert('Please check at least two objects!')
        }
    })

    $('#skip-btn').click(function () {
        $('#submit-btn').prop('disabled', true);
        $('#skip-btn').prop('disabled', true);
        $.ajax({
            url: "/taxonomy/skip",
            method: "POST",
            data: {
                cluster_id: $(".id-text").attr('id')
            },
            success: function (res) {
                window.location = '/taxonomy';
            }
        })
    })

    $("#sec-level-category-selector").change(function () {
        var $dropdown = $(this);
        var key = $dropdown.val();
        var $thirdChoice = $("#third-level-category-selector")

        if (key in category_third_options){
            vals = category_third_options[key];
            $thirdChoice.css("display", "block");
            $thirdChoice.empty();
            $.each(vals, function(index, value) {
                $thirdChoice.append("<option>" + value + "</option>");
            });
        } else {
            $thirdChoice.css("display", "none");
            $thirdChoice.empty();
        }
    })

    $("#first-level-category-selector").change(function () {
        var $dropdown = $(this);
        var key = $dropdown.val();
        var $secondChoice = $("#sec-level-category-selector")

        if (key in category_second_options){
            vals = category_second_options[key];
            $secondChoice.css("display", "block");
            $secondChoice.empty();
            $.each(vals, function(index, value) {
                $secondChoice.append("<option>" + value + "</option>");
            });
            $("#sec-level-category-selector").trigger('change')
        } else {
            $secondChoice.css("display", "none");
            $secondChoice.empty();
        }


    })

    $('#product-classification-seletor').change(function () {
        var $dropdown = $(this);
        var key = $dropdown.val();
        var vals = [];
        var $firstChoice = $("#first-level-category-selector")
        var $secondChoice = $("#sec-level-category-selector")
        var $thirdChoice = $("#third-level-category-selector")

        $firstChoice.css("display", "none");
        $firstChoice.empty();
        $secondChoice.css("display", "none");
        $secondChoice.empty();
        $thirdChoice.css("display", "none");
        $thirdChoice.empty();


        vals = category_first_options[key];
        $firstChoice.css("display", "block");
        $firstChoice.empty();
        $.each(vals, function(index, value) {
            $firstChoice.append("<option>" + value + "</option>");
        });

        $("#first-level-category-selector").trigger('change')

    })

    $('#check-all-btn').click(function() {
        $('#checkboxes input').each(function() {
            $(this).prop('checked', true);
        });
    });
    $('#un-check-all-btn').click(function() {
        $('#checkboxes input').each(function() {
            $(this).prop('checked', false);
        });
    });
}