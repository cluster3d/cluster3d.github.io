var views, scene, renderer;
var controls;

scene = new THREE.Scene();

var windowWidth = window.innerWidth - 350;
var windowHeight = window.innerHeight - 56;

var view_mode = 0;

var faceIndices = [ 'a', 'b', 'c', 'd' ];
var feat_surfaces = [];


var manager = new THREE.LoadingManager();
manager.onStart = function ( url, itemsLoaded, itemsTotal ) {

	console.log( 'Started loading file: ' + url + '.\nLoaded ' + itemsLoaded + ' of ' + itemsTotal + ' files.' );
    $('#loading').show()
};

manager.onLoad = function ( ) {

    console.log( 'Loading complete!');
    $('#loading').hide()

};

manager.onProgress = function ( url, itemsLoaded, itemsTotal ) {

	console.log( 'Loading file: ' + url + '.\nLoaded ' + itemsLoaded + ' of ' + itemsTotal + ' files.' );

};

manager.onError = function ( url ) {

	console.log( 'There was an error loading ' + url );

};

var loader = new THREE.OBJLoader(manager);

var patch_colors = [
    new THREE.Color( 0xFF0000 ),
    new THREE.Color( 0xFF0000 ),
    new THREE.Color( 0xFF0000 ),
    new THREE.Color( 0xFF0000 ),
    new THREE.Color( 0xFF0000 ),
]
var colors = {}
let cur_obj = []

var views = [
    {
        left: 0,
        bottom: 0.5,
        width: [0, 0.5],
        height: [0, 0.5],
        background: new THREE.Color( 0.35, 0.35, 0.35 ),
        eye: [ 0, 0, 250 ],
        up: [ 0, 1, 0 ],
        fov: 45,
        camera: null,
        updateCamera: function ( camera, scene, mouseX ) {
            camera.position.x -= mouseX * 0.05;
            camera.position.x = Math.max( Math.min( camera.position.x, 2000 ), - 2000 );
            camera.lookAt( camera.position.clone().setY( 0 ) );
          }
    },
    {
        left: 0.5,
        bottom: 0.5,
        width: [0, 0.5],
        height: [0, 0.5],
        background: new THREE.Color( 0.5, 0.5, 0.5 ),
        eye: [ 0, 300, 0 ],
        up: [ 0, 1, 0 ],
        fov: 45,
        camera: null,
        updateCamera: function ( camera, scene, mouseX ) {
          camera.position.x -= mouseX * 0.05;
          camera.position.x = Math.max( Math.min( camera.position.x, 2000 ), - 2000 );
          camera.lookAt( camera.position.clone().setY( 0 ) );
        }
    },
    {
        left: 0,
        bottom: 0,
        width: [1, 0.5],
        height: [1, 0.5],
        background: new THREE.Color( 0.7, 0.7, 0.7 ),
        eye: [ 0, -250, 200 ],
        up: [ 0, 1, 0 ],
        fov: 45,
        camera: null,
        updateCamera: function ( camera, scene, mouseX ) {
          camera.position.y -= mouseX * 0.05;
          camera.position.y = Math.max( Math.min( camera.position.y, 1600 ), - 1600 );
          camera.lookAt( scene.position );
        },
    },
    {
        left: 0.5,
        bottom: 0,
        width: [0, 0.5],
        height: [0, 0.5],
        background: new THREE.Color( 0.8, 0.8, 0.8 ),
        eye: [ 0, 500, -250 ],
        up: [ 0, 1, 0 ],
        fov: 45,
        camera: null,
        updateCamera: function ( camera, scene, mouseX ) {
          camera.position.y -= mouseX * 0.05;
          camera.position.y = Math.max( Math.min( camera.position.y, 1600 ), - 1600 );
          camera.lookAt( scene.position );
        }
    }
];

var material_options = {
    "Metals": ["Aluminum Alloys", "Brass", "Copper Alloys", "Iron", "Nickel Alloys", "Other Metal Alloys", "Precious Metals (Gold, Silver, Platinum)", "Steel", "Titanium Alloys", "Zinc Alloys"],
    "Polymers & Plastics": ["ABS", "Acrylic", "Epoxy", "Nylon", "Other Polymers & Plastics", "PTFE (Teflon)", "PVC", "Polyacrylamide", "Polycarbonate", "Polyester", "Polyethylene (HD) - High Density", "Polyethylene (LD) - Low Density", "Polystyrene"]
}

var sub_options = {
    "Casting": ["Centrifugal casting", "Continuous casting", "Die casting", "Evaporative-pattern casting", "Investment casting", "Low pressure die casting", "Permanent mold casting", "Plastic mold casting", "Resin casting", "Sand casting", "Shell molding", "Slush casting", "Vacuum molding"],
    "Coating": ["Chemical vapor deposition", "Inkjet printing", "Laser engraving", "Plating", "Sputter deposition", "Thermal spraying"],
    "Molding": ["Blow molding", "Compaction plus sintering", "Compression molding", "Dip moulding", "Expandable bead", "Extrusion", "Foam", "Hot isostatic pressing", "Injection", "Laminating", "Matched mould", "Metal injection moulding", "Pressure plug assist", "Rotational molding", "Shrink wrapping", "Spray forming", "Thermoforming", "Transfer", "Vacuum plug assist"],
    "Forming": ["Blanking", "Blanking and piercing", "Bulging", "Coining", "Cold rolling", "Cold sizing", "Cored", "Cross-rolling", "Cryorolling", "Curling (metalworking)", "Cutoff", "Decambering", "Deep drawing (sinks, auto body)", "Dinking", "Drawing (manufacturing) (pulling sheet metal, wire, bar, or tube", "Drop forge", "Electroforming", "Embossing", "Explosive forming", "Flanging", "Flattening", "Guerin process", "Hammer forge", "Hemming", "High-energy-rate", "Hot metal gas forming", "Hot rolling", "Hubbing", "Hydroforming", "Impact (see also Extrusion)", "Impact extrusion", "Incremental", "Ironing", "Lancing", "Leather", "Magnetic pulse", "Metal", "Necking", "Nibbling", "No draft", "Nosing", "Notching", "Orbital", "Peening", "Perforating", "Powder", "Press", "Progressive", "Redrawing", "Ring", "Screw thread", "Seaming", "Shape", "Shaving", "Sheet metal", "Slitting", "Smith", "Spinning", "Staking", "Stamping", "Straight shearing", "Straightening", "Stretch forming", "Swaging", "Thread rolling", "Transverse", "Trimming", "Tube beading", "Upset", "Wheelon process"],
    "CNC Machining": ["Abrasive belt", "Abrasive blasting (sand blasting)", "Abrasive jet machining", "Annealing", "Ball mill", "Biomachining", "Blast furnace", "Boring (also Single pass bore finishing)", "Broaching", "Buffing", "Buhrstone mill", "Burnishing", "Chemical", "Coating", "Countersinking", "Cutoff (parting)", "Disc mill", "Double housing", "Drilling", "Edge or plate", "Electrical discharge", "Electrical discharge machining (EDM)", "Electro-chemical grinding", "Electrochemical machining", "Electron beam machining", "Electroplating", "Electropolishing", "Etching", "Facing", "Filing", "Finishing & industrial finishing", "Friction drilling", "Gashing", "Grinding", "Grist mill", "Hammer mill", "Hard turning", "High stock removal", "Hobbing", "Honing (Sharpening)", "Horizontal", "Knurling", "Laser cutting", "Laser drilling", "Lathe", "Linishing", "Magnetic field-assisted finishing", "Mass finishing", "Milling", "Mills", "Open-side", "Passivate", "Photochemical", "Photochemical machining", "Pickling", "Pit-type", "Planing", "Plating", "Polishing", "Reaming", "Reduction mill", "Refining", "Routing", "Saw mill", "Sawing", "Shaping", "Smelting", "Special purpose", "Spindle finishing", "Spinning (flow turning)", "Steel mill", "Superfinishing", "Tapping", "Tumbling (barrel finishing)", "Turning", "Ultrasonic machining", "Vertical", "Vibratory finishing", "Water jet cutting", "Wire brushing"],
    "Joining": ['Adhesive alloys', 'Adhesive bonding (incomplete)', 'Air-acetylene', 'Arc', 'Atomic hydrogen', 'Box head', 'Brazing', 'Butt welding', 'By material fastened', 'By shape', 'By slot type', 'CO2', 'Carbon arc', 'Clinching', 'Cold', 'Cotter', 'Dielectric', 'Diffusion', 'Dip', 'Electrogas', 'Electromagnetic', 'Electron beam welding', 'Electroslag', 'Epoxy', 'Explosive', 'Fastening wood and metal', 'Flash butt welding', 'Flat head', 'Flow', 'Flux-cored', 'Forge', 'Friction welding', 'Furnace', 'Gas metal', 'Gas tungsten', 'Groove', 'Heated metal plate', 'Hex', 'High frequency (induction resistance; 200–450 kHz)', 'High frequency resistance', 'Hot plate', 'Hot press', 'Hot-air-welding', 'Impregnated tape', 'Induction', 'Induction brazing', 'Inertia', 'Infrared', 'Iron', 'Isostatic hot gas', 'Lag', 'Laser welding', 'Low frequency (50–450 Hz)', 'Machine (Metal)', 'Magnetic pulse welding', 'Manual metal', 'Methylacetylene propadiene (MAPP)', 'Miscellaneous other powders, liquids, solids, and tapes', 'Modified epoxy', 'Nailing', 'Nut and bolts', 'Others', 'Oven', 'Oxy-acetylene gas', 'Oxyfuel gas', 'Oxyhydrogen', 'Percussion (manufacturing)', 'Phenolics', 'Phillips', 'Pinning', 'Plasma arc', 'Plasma-MIG (metal inert gas)', 'Polyurethane', 'Press fitting', 'Pressure gas', 'Projection welding', 'Pulsed', 'Quick release skewer', 'Radio frequency welding', 'Regulated Metal Deposition', 'Resistance', 'Retaining rings', 'Riveting', 'Roll', 'Round head', 'Screwing', 'Seam', 'Shielded metal', 'Short circuit', 'Shot welding', 'Sintering', 'Soldering', 'Solid state welding', 'Solvent', 'Spot welding', 'Spray transfer', 'Stapling', 'Stitching', 'Straight', 'Stud', 'Submerged', 'Tapered', 'Thermite', 'Thermo-setting and thermoplastic', 'Torch', 'Ultrasonic', 'Upset welding', 'Vacuum', 'Vacuum furnace', 'Wave', 'Welding', 'Wood Screws'],
    "Additive Manufacturing": ["3D printing", "Direct metal laser sintering", "Filament winding, produces composite pipes, tanks, etc.", "Fused deposition modeling", "Laminated object manufacturing", "Laser engineered net shaping", "Selective laser sintering", "Stereolithography"]    
}

var category_first_options = {
    "Mechanical Sys and Components": ["Mechanical System", "Simple Machine Equipment", "Filters", "Fasteners", "Pipe, Tubing, Hose & Fittings", "Hinges, eyelets and joints", "Bearings", "Bushings", "Shafts and couplings", "Seals, glands", "Springs", "Gears", "Wheels", "Rotary-reciprocating mechanisms", "Enclosures"],
    "Electrical Systems": ["Electrical System", "Electrical wires and cables", "Insulation", "Components for electrical equipment", "Electrical accessories", "Lamps and related equipment", "Rotating machinery", "Transformers", "Reactors", "Rectifiers", "Converters", "Batteries"],
    "Electro-Mechanical Systems": ["Electro-Mechanical Assembly"],
}

var category_second_options = {
    "Simple Machine Equipment": ["Machine", "Lever", "Switch", "Valve", "Actuators", "Mechanical Brakes"],
    "Filters": ["Air Filters", "Sieves", "Mesh Filters", "Masks"],
    "Fasteners": ["Bolt, Screws and Studs", "Nuts", "Pins", "Washers", "Clamps"],
    "Pipe, Tubing, Hose & Fittings": ["Pipe Fittings", "Pipe Hangers", "Pipe Joints"],
    "Hinges, eyelets and joints": ["Hinges", "Articulations eyelets & joints", "Knobs", "Sockets"],
    "Bearings": ["Plain Bearings", "Thrust Bearings", "Roller Bearings", "Bearing accessories", "Bushes", "Flanged block bearing", "Flanged plain bearings", "Right angular gearings", "Radial contact ball bearings"],
    "Bushings": ["Bushings", "Bumpers", "Grommets", "Pads"],
    "Shafts and couplings": ["Shaft", "Couplings", "Spacers", "Keys and keyways splines"],
    "Seals, glands": ["Seals", "Edge Seals", "O-rings", "Gaskets", "Caps", "Plugs", "Tapes"],
    "Springs": ["Springs", "Spring washers", "Extension Springs", "Die Springs", "Strip Springs", "Linear Wave", "Rotor Springs"],
    "Gears": ["Gears", "Spur gears", "Sprockets", "Pulleys", "Timing Belts", "Gear Boxes", "Gear Rod Stock", "Ratcheting Gears", "Worm Gears", "Helical Gears", "Rack Gears"],
    "Wheels": ["Wheel", "Castor Wheels"],
    "Rotary-reciprocating mechanisms": ["Rotary System", "Impeller", "Turbine", "Fan", "Motors"],
    "Enclosures": ["Shell", "Boxes", "Metal Casings", "Covers"],
}

var category_third_options = {
    "Bolt, Screws and Studs": ["Bolt", "Screws", "Studs", "Screws & bolts \w countersunk head", "Screws & bolts \w hexagonal head", "Screws & bolts \w cylindrical head", "Tapping screws", "Studs", "Washer bolt", "Eye screws", "Set screw", "Threaded rods"],
    "Nuts": ["Nuts", "Castle nuts", "Locknuts", "Square nuts", "T-nut", "Hexagonal nuts", "Flange nut", "Rivet nut", "Slotted nuts", "Wingnuts"],
    "Pins": ["General Pins", "Locating pins", "Split pins", "Cylindrical pins", "Taper pins", "Grooved pins", "Roll pins", "Pivot pins", "Locking pins"],
    "Washers": ["Washer", "Lock washers", "Convex washer", "Thrust washers", "Knurled Washers"],
    "Clamps": ["Clamp", "Rivets", "Staples", "Rings", "Plates"],
    "Pipe Fittings": ["Elbow fitting", "T-shape fitting"],
    "Pipe Joints": ["Pipe Flanges", "Tube Fittings", "Hose", "Hose Fittings", "Tube Clamps"],
}


init();
animate();



function loadObjFromFileName(key) {
    $.ajax({ 
        url: '/filename/' + key,
        type: 'GET',
        cache: false, 
        success: function(data){
            removeEntity(cur_obj)
            if (data.decimated) {
                $('#decimated-txt').show()
            } else {
                $('#decimated-txt').hide()
            }
            feat_surfaces = data['feat']
            colors[key] = []
            for ( var i = 0; i < feat_surfaces.length; i ++) {
                var patch_color = new THREE.Color( Math.random() * 0xffffff )
                for ( var j = 0; j < feat_surfaces[i]['face_indices'].length ; ++ j) {
                    colors[key].push(patch_color)
                }
            }
            $('#file-id-txt').text('File ID: '+data['onShapeId'])
            $('#file-link').attr("href", data['onShapeURL']);
            $('#file-link-2').attr("href", data['onShapeURLPart']);
            console.log(data['onShapeURL'])
            console.log(data['onShapeURLPart'])
            addEntity(data['objPath'], key)   
        }
        , error: function(jqXHR, textStatus, err){
            alert('No file to show!')
            removeEntity(cur_obj)
        }
    })
}

function loadAnnotation(key) {
    $.ajax({
        url: "/assign/annotator",
        data: {
            oid: key
        },
        method: "POST",
        success: function (res) {
            const done = res.annotators.filter(annot => annot.done);
            const undone = res.annotators.filter(annot => !annot.done);
            $('#finish-set').find("a").remove();
            done.forEach(annotation => {
                $('#finish-set').append("<a href='#' class='modal-trigger' data-toggle='modal' data-target='#exampleModal' data-uid='" + annotation.annotator.id + "'>" + annotation.annotator['first-name'] + ' ' + "</a>")
            });
            $('#inprogress-set').find('a').remove();
            undone.forEach(annotation => {
                $('#inprogress-set').append("<a href='#' class='modal-trigger' data-toggle='modal' data-target='#exampleModal' data-uid='" + annotation.annotator.id + "'>" + annotation.annotator['first-name']  + ' ' + "</a>")
            });
            $('#user-dropdown').find("option").remove();
            res.dropdownUsers.forEach(user => {
                $('#user-dropdown').append("<option value='" + user.id + "'>" + user['first-name'] + "</option>")
            });
        }
    })
}

function handleSubmit(e) {
    console.log(e)
}

var material_cnt = 1

function init() {
    $('#skip-btn').click(function () {
        $.ajax({
            url: "/skip/" + $('#file-selector').val(),
            method: "POST",
            success: function (res) {
                window.location = '/';
            }
        })
    })

    $('#btn-toggle input').change(function () {
        view_mode = $(this).data("viewmode");
    })

    $('#loading').show()
    $('#decimated-txt').hide()

    $('#btn-toggle-model input').change(function () {
        let modelmode = $(this).data("modelmode")
        if (modelmode == "complete") {
            $.ajax({ 
                url: '/complete_model/' + $('#file-selector').val(),
                type: 'GET',
                cache: false, 
                success: function(data){
                    console.log(data)
                    data.forEach(obj => {                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
                        if (obj.folderNmae != cur_obj[0]) {
                            colors[obj.folderNmae] = []
                            feat_surfaces = obj.feat
                            for ( var i = 0; i < feat_surfaces.length; i ++) {
                                var patch_color = new THREE.Color( Math.random() * 0xffffff )
                                for ( var j = 0; j < feat_surfaces[i]['face_indices'].length ; ++ j) {
                                    colors[obj.folderNmae].push(patch_color)
                                }
                            }
                            addEntity(obj.objPath, obj.folderNmae) 
                        }
                    }) 
                }
                , error: function(jqXHR, textStatus, err){
                    console.log(err)
                }
            })
        } else {
            let del_list = cur_obj.slice()
            var index = del_list.indexOf($('#file-selector').val());
            if (index > -1) {
                del_list.splice(index, 1);
            }
            removeEntity(del_list)
        }
    })

    var urlParams = new URLSearchParams(window.location.search);

    const file_param = urlParams.get('file');

    $('#add-mat-btn').click(function () {
        var str_material_cnt = material_cnt.toString()
        var material_select = `<hr id=\"line-divider-${str_material_cnt}\"><select class=\"form-control material-selector\" id=\"material-selector-`+ material_cnt.toString() + "\"name=\"materialCategory\">"
        var ops = [
            "<option value=\"\" selected disabled>Please select</option>",
            "<option value=\"Ceramics\">Ceramics</option>",
            "<option value=\"Composites\">Composites</option>",
            "<option value=\"Concrete\">Concrete</option>",
            "<option value=\"Electronic/Optical\">Electronic/Optical</option>",
            "<option value=\"Glass\">Glass</option>",
            "<option value=\"Metals\">Metals</option>",
            "<option value=\"Polymers & Plastics\">Polymers & Plastics</option>",
            "<option value=\"Wood\">Wood</option>",
            "<option value=\"Rubber\">Rubber</option>",
            "<option value=\"Silicone\">Silicone</option>",
        ].join('')
        var sub_material = "</select><select class=\"form-control\" id=\"sub-material-selector-"+ material_cnt.toString()+"\" value=\"\" name=\"subMaterialCategory\" style=\"display:none\"><option value selected disabled>Please select</option></select>"
    
        $("#add-mat-dropdown-div").append($(material_select+ops+sub_material))
        material_cnt += 1
    })

    $('#del-mat-btn').click(function () {
        
        if (material_cnt != 1){
            console.log('wwww')
            $('#line-divider-'+(material_cnt-1).toString()).remove();
            $('#material-selector-'+(material_cnt-1).toString()).remove();
            $('#sub-material-selector-'+(material_cnt-1).toString()).remove();
            material_cnt -= 1
        }
    })
    
    $("#file-selector option").filter(function() {
        return $(this).text() == file_param;
    }).prop('selected', true);

    loadObjFromFileName($('#file-selector').val())
    loadAnnotation($('#file-selector').val())

    $('#file-selector').change(function () {
        $('#loading').show()
        var $dropdown = $(this);
        window.history.pushState(null, null, window.location.pathname + "?file=" + $dropdown.val());
        loadObjFromFileName($dropdown.val());
        loadAnnotation($dropdown.val())

        $('#toggle-single').trigger("click")
        
    });

    $(document).on('change', '.material-selector', function () {
        var $dropdown = $(this);
        var key = $dropdown.val();
        var vals = [];
        var material_id = $dropdown.attr('id').split('-').pop()


        var $secondChoice = $("#sub-material-selector-"+material_id);
        if (key in material_options) {
            vals = material_options[key];
            $secondChoice.css("display", "block");
            $secondChoice.empty();
            $.each(vals, function(index, value) {
                $secondChoice.append("<option value=\"" + value + "\">" + value + "</option>");
            });
        } else {
            $secondChoice.css("display", "none");
            $secondChoice.empty();
            $secondChoice.append("<option value=\"\">" + 'none' + "</option>");
        }
    })

    $('.process-selector').change(function () {
        var $dropdown = $(this);
        var key = $dropdown.val();
        var vals = [];
        var $secondChoice;
        if ($dropdown.attr('id') == 'first-process-selector') {
            $secondChoice = $("#first-sub-process-selector");
        } else {
            $secondChoice = $("#second-sub-process-selector");
        }
        if (key in sub_options) {
            vals = sub_options[key];
            $secondChoice.css("display", "block");
            $secondChoice.empty();
            $.each(vals, function(index, value) {
                $secondChoice.append("<option>" + value + "</option>");
            });
        } else {
            $secondChoice.css("display", "none");
            $secondChoice.empty();
            $secondChoice.append("<option value=\"\">" + 'none' + "</option>");
        }
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

    create_camera()
    
    var light = new THREE.DirectionalLight( 0xffffff );
    light.position.set( 100, 200, 300 );
    scene.add( light );
    var light_2 = new THREE.DirectionalLight( 0xffffff );
    light_2.position.set( -300, -200, -300 );
    scene.add( light_2 );

    renderer = new THREE.WebGLRenderer( { antialias: true } );
    renderer.setPixelRatio( window.devicePixelRatio );
    renderer.setSize( windowWidth, windowHeight );

    // controls = new THREE.OrbitControls( views[0].camera, renderer.domElement );
    // controls = new THREE.OrbitControls( views[1].camera, renderer.domElement );
    controls = new THREE.OrbitControls( views[2].camera, renderer.domElement );
    // controls = new THREE.OrbitControls( views[3].camera, renderer.domElement );
    controls.update();
    container = document.getElementById( 'main-container' );
    container.appendChild( renderer.domElement );

}

function create_camera() {
    for ( var ii = 0; ii < views.length; ++ ii ) {
        var view = views[ ii ];
        var camera = new THREE.PerspectiveCamera( view.fov, windowWidth / windowHeight, 0.1, 10000 );
        camera.position.fromArray( view.eye );
        camera.up.fromArray( view.up );
        view['camera'] = camera;
    }
}

function addEntity(path, file_name) {
    controls.reset();
    loader.load(
        path,
        function ( object ) {
            object.traverse( function ( child ) {
                if ( child instanceof THREE.Mesh ) {
                    var geometry = new THREE.Geometry().fromBufferGeometry( child.geometry );
                    for ( var i = 0; i < geometry.faces.length; i++ ) {
                        face = geometry.faces[ i ];
                        numberOfSides = ( face instanceof THREE.Face3 ) ? 3 : 4;
                        for ( var j = 0; j < numberOfSides; j++ )  {
                            face.vertexColors[ j ] = colors[file_name][i]
                        }
                    }
                    var material = new THREE.MeshPhongMaterial( {
                        flatShading: true,
                        vertexColors: THREE.VertexColors,
                        shininess: 0
                    } );
                    var mesh = new THREE.Mesh( geometry, material )
                    mesh.geometry.colorsNeedUpdate = true
                    mesh.name = file_name
                    scene.add( mesh );
                    cur_obj.push(file_name)
                }
            } );
            object.position.y = 0;   
        },
    );
    animate();
    
}


function removeEntity(obj_name_list) {
    cur_obj = cur_obj.filter(cur => obj_name_list.indexOf(cur) === -1);

    for (let ii = 0; ii < obj_name_list.length; ii ++) {
        let selectedObject = scene.getObjectByName(obj_name_list[ii]);
        
        selectedObject.traverse(function (item) {
            if (item instanceof THREE.Mesh) {
                item.geometry.dispose();
                item.material.dispose();
                item = undefined
            }
        });
        scene.remove( selectedObject );
    }

    animate();
}

function animate() {

    requestAnimationFrame( animate );

    for ( var ii = 0; ii < views.length; ++ ii ) {
        
        var view = views[ ii ];
        var camera = view.camera;
        var left = Math.floor( windowWidth * view.left );
        var bottom = Math.floor( windowHeight * view.bottom );
        var width = Math.floor( windowWidth * view.width[view_mode] );
        var height = Math.floor( windowHeight * view.height[view_mode] );
        renderer.setViewport( left, bottom, width, height );
        renderer.setScissor( left, bottom, width, height );
        renderer.setScissorTest( true );
        renderer.setClearColor( view.background );
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.render( scene, camera );
    }

}
