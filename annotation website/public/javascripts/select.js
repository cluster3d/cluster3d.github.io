var view, scene, renderer;

var windowWidth = window.innerWidth - 250;
var windowHeight = window.innerHeight - 56;

var camera = new THREE.PerspectiveCamera( 45, windowWidth / windowHeight, 0.1, 10000 );
camera.position.fromArray( [ 0, 0, 500 ] );
camera.up.fromArray( [0, 1, 0] );

var controls;

var raycaster = new THREE.Raycaster();
var mouse = new THREE.Vector2(), INTERSECTED;

var faceIndices = [ 'a', 'b', 'c', 'd' ];

init();
render();

function init() {

    scene = new THREE.Scene();

    var light = new THREE.DirectionalLight( 0xffffff );
    light.position.set( 100, 200, 300 );
    scene.add( light );

    renderer = new THREE.WebGLRenderer( { antialias: true } );

    renderer.setClearColor( 0x777777 );
    renderer.setPixelRatio( window.devicePixelRatio );
    renderer.setSize( windowWidth, windowHeight );

    renderer.domElement.addEventListener( 'mousemove', onMouseMove );

    controls = new THREE.OrbitControls( camera, renderer.domElement );
    controls.update()
    container = document.getElementById( 'main-container' );
    container.appendChild( renderer.domElement );
    
    var loader = new THREE.OBJLoader();
    loader.load(
        '../images/CAD/5.obj',
        function ( object ) {
            var geometry;
            object.traverse( function ( child ) {
                if ( child instanceof THREE.Mesh ) {
                    var geometry = new THREE.Geometry().fromBufferGeometry( child.geometry );

                    for ( var ii = 0; ii < geometry.vertices.length; ++ ii ) {
                        geometry.colors.push(new THREE.Color(0x80DEEA));
                    }
                    console.log(geometry)
                    for ( var i = 0; i < geometry.faces.length; i++ ) 
                    {
                        face = geometry.faces[ i ];
                        numberOfSides = ( face instanceof THREE.Face3 ) ? 3 : 4;
                        for( var j = 0; j < numberOfSides; j++ ) 
                        {
                            vertexIndex = face[ faceIndices[ j ] ];
                            face.vertexColors[ j ] = geometry.colors[ vertexIndex ];
                        }
                    }
                    console.log(geometry)
                    var material = new THREE.MeshPhongMaterial( {
                        // color: 0xff00ff,
                        flatShading: true,
                        vertexColors: THREE.VertexColors,
                        shininess: 0
                    } );
                    // material = new THREE.MeshBasicMaterial({ vertexColors: THREE.VertexColors });
                    var mesh = new THREE.Mesh( geometry, material )
                    mesh.geometry.verticesNeedUpdate = true
                    mesh.geometry.colorsNeedUpdate = true
                    mesh.geometry.elementsNeedUpdate = true;

                    scene.add( mesh );
                    // child.material.ambient.setHex(0xFF0000);
                    // child.material.color.setHex(0x00FF00);
                }
            } );

            object.position.y = 0;   
            // scene.add( object );
        },
        function ( xhr ) {

            console.log( ( xhr.loaded / xhr.total * 100 ) + '% loaded' );

        }
    );


}




function render() {

    requestAnimationFrame( render );
    raycaster.setFromCamera( mouse, camera );
    
    var intersects = raycaster.intersectObjects( scene.children, true );
    if ( intersects.length > 0 ) {
        if (!INTERSECTED) {
            console.log(intersects[ 0 ].object.geometry);
            geometry = intersects[ 0 ].object.geometry
            INTERSECTED = intersects[ 0 ].object;
            INTERSECTED.currentHex = intersects[ 0 ].object.geometry.colors.slice()
            console.log(INTERSECTED.currentHex, intersects[ 0 ].object.geometry.colors.slice())
            for ( var i = 0; i < geometry.faces.length; i++ ) 
            {
                face = geometry.faces[ i ];
                numberOfSides = ( face instanceof THREE.Face3 ) ? 3 : 4;
                for( var j = 0; j < numberOfSides; j++ ) 
                {
                    vertexIndex = face[ faceIndices[ j ] ];
                    face.vertexColors[ j ].set(new THREE.Color(0xff0000));
                }
            }
            geometry.colorsNeedUpdate = true;
        }
    } else {
        if ( INTERSECTED ) {
            geometry = INTERSECTED.geometry
            console.log(INTERSECTED.currentHex)
            for ( var i = 0; i < geometry.faces.length; i++ ) 
            {
                face = geometry.faces[ i ];
                
                numberOfSides = ( face instanceof THREE.Face3 ) ? 3 : 4;
                for( var j = 0; j < numberOfSides; j++ ) 
                {
                    vertexIndex = face[ faceIndices[ j ] ];
                    face.vertexColors[ j ].set(new THREE.Color(0x80DEEA));
                    face.vertexColors[ j ].set(INTERSECTED.currentHex[vertexIndex]);
                }
            }
            geometry.colorsNeedUpdate = true;
        }
        INTERSECTED = null;
    }


    renderer.render( scene, camera );


}



function onMouseMove( event ) {
	// calculate mouse position in normalized device coordinates
	// (-1 to +1) for both components
    mouse.x = ( event.clientX / windowWidth ) * 2 - 1;
    mouse.y = - ( (event.clientY-56) / windowHeight ) * 2 + 1;
}




//     var selectedObject = scene.getObjectByName(object.name);
//     scene.remove( selectedObject );
//     animate();
// }

// var myFile = document.getElementById('myFile');
// var parsed_geo;
// var input_geo;

// myFile.onchange = function() {
//     let input = this.files[0];
//     var reader = new FileReader();
//     reader.onload = (function() {
//         return function(e) {
//             var loader = new THREE.OBJLoader();
//             input_geo = e.target.result
//             parsed_geo = loader.parse(input_geo)
//             parsed_geo.name = "test_name";
//             scene.add( parsed_geo );
//         };
//     })(input);
//     reader.readAsText(input);
// };

// var myFile2 = document.getElementById('myFile2');
// myFile2.onchange = function() {
//     let input = this.files[0];
//     var reader = new FileReader();
//     reader.onload = (function() {
//         return function(e) {

//             var mtlLoader = new THREE.MTLLoader();
//             var matrial = mtlLoader.parse(e.target.result)
//             removeEntity(parsed_geo)

//             var loader = new THREE.OBJLoader();
//             loader.setMaterials(matrial);
//             scene.add( loader.parse(input_geo) );

//         };
//     })(input);
//     reader.readAsText(input);
// };