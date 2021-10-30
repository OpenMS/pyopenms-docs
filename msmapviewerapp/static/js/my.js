//TODO dat gui still does not remove inbetween updates..
//TODO color does not reset after making a new selection. WE probably have to store the old height
//TODO reuse much more functions! Problem is the different data we sometimes use.
//TODO indent better
//TODO get maxInt only from mzs in range
// For the time now
Date.prototype.timeNow = function () {
     return ((this.getHours() < 10)?"0":"") + this.getHours() +":"+ ((this.getMinutes() < 10)?"0":"") + this.getMinutes() +":"+ ((this.getSeconds() < 10)?"0":"") + this.getSeconds();
}

console.clear();

var globaldata;
var globalrtminidx;
var globalrtmaxidx;
var gui = new dat.GUI({ autoPlace: false });

var stats = new Stats(1);
var scene = new THREE.Scene();
scene.background = new THREE.Color("white");
let camera = new THREE.PerspectiveCamera(60, innerWidth / innerHeight, 1, 1000);
camera.position.set(0, 70, 150);
let renderer = new THREE.WebGLRenderer({antialias: true}); //AA off for now for speed?
let light = new THREE.DirectionalLight(0xffffff, 1);
light.position.setScalar(1);
scene.add(light, new THREE.AmbientLight(0xffffff, 0.75));

$(document).ready(function(){
    $('.threedplot').append($(gui.domElement));
    $('.threedplot').append($(stats.dom));
    document.getElementById('threedplot').appendChild(renderer.domElement);
    var container = renderer.domElement.parentElement;
    renderer.setSize(container.getBoundingClientRect().width, container.getBoundingClientRect().height);
    camera.aspect = container.getBoundingClientRect().width/container.getBoundingClientRect().height;
    $.getJSON("bokehappfolder/static/data/feature.json", function(d) {
      renderAll(d);
    });
});


function GridGeometry(width = 1, height = 1, wSeg = 1, hSeg = 1, lExt = [0, 0]){

  let seg = new THREE.Vector2(width / wSeg, height / hSeg);
  let hlfSeg = seg.clone().multiplyScalar(0.5);

  let pts = [];

  for(let y = 0; y <= hSeg; y++){
  	pts.push(
    	new THREE.Vector2(0, y * seg.y),
      new THREE.Vector2(width + (hlfSeg.x * lExt[0]), y * seg.y)
    )
  }

  for(let x = 0; x <= wSeg; x++){
  	pts.push(
    	new THREE.Vector2(x * seg.x, 0),
      new THREE.Vector2(x * seg.x, height + (hlfSeg.y * lExt[1]))
    )
  }

  return new THREE.BufferGeometry().setFromPoints(pts);

}

function binarySearch(value, list, first, last) {
    let position = -1;
    let found = false;
    let middle;

    while (found === false && first <= last) {
        middle = Math.floor((first + last)/2);
        if (list[middle] === value) {
            found = true;
            position = middle;
        } else if (list[middle] > value) {
            last = middle - 1;
        } else {
            first = middle + 1;
        }
    }
    return position;
}

function closest (num, arr, lo, hi) {
    var mid;
    while (hi - lo > 1) {
        mid = Math.floor ((lo + hi) / 2);
        if (arr[mid] < num) {
            lo = mid;
        } else {
            hi = mid;
        }
    }
    if (num - arr[lo] <= arr[hi] - num) {
        return lo;
    }
    return hi;
}

// called from app, not here
function renderAllCDS(data, minRT, maxRT, minMZ, maxMZ) {
    globaldata = data;
    // We now assume that the data we get is already filtered for the RT range
    //let startrtidx = closest(minRT,data.data['RT'],0,data.data['RT'].length - 1)
    let startrtidx = 0;
    globalrtminidx = startrtidx;
    //let endrtidx = closest(maxRT,data.data['RT'],startrtidx,data.data['RT'].length - 1)
    let endrtidx = data.data['RT'].length - 1;
    globalrtmaxidx = endrtidx;
    console.log(startrtidx,endrtidx)
    let container = renderer.domElement.parentElement;
    let canvas = renderer.domElement
    let maxInt = 0;
    let minInt = 1000000000000;
    let mzPaintWidth = 500;
    let rtPaintWidth = 500;
    let intPaintWidth = 100;
    let scaleMZ = mzPaintWidth/(maxMZ - minMZ);
    let scaleRT = rtPaintWidth/(maxRT - minRT);
    let dotScale = 0.8;
    let cnt = 0;
    for (let i = startrtidx; i < endrtidx; i++)
    {
        let mz = data.data['mz'][i];
        // TODO if everything is sorted we should be able to do binary search inside the RT slice on mz level
        // With the new "only transfer what is visible mode" we do not need to check mz range
        //if (mz < minMZ || mz > maxMZ) continue;
        let pt = data.data['inty'][i];
        maxInt = Math.max(maxInt,pt)
        minInt = Math.min(minInt,pt)
        // if data is filtered already, cnt could be just length
        cnt++;
    }
    if (cnt > 300000)
    {
        alert("Too many points for 3D view. Please zoom in.")
        return;
    }

console.log(maxMZ,maxInt,maxRT,cnt);

scene = new THREE.Scene();
scene.background = new THREE.Color("white");

var points = [
  new THREE.Vector3(),
  new THREE.Vector3()
]
var clicks = 0;

//we do not need markers where we clicked the peaks
/*var markerA = new THREE.Mesh(
  new THREE.SphereGeometry(0.1, 10, 20),
  new THREE.MeshBasicMaterial({
    color: 0xff5555
  })
);
var markerB = markerA.clone();
var markers = [
  markerA, markerB
];
scene.add(markerA);
scene.add(markerB);
*/

var linepts = []
linepts.push(new THREE.Vector3());
linepts.push(new THREE.Vector3());
var lineGeometry = new THREE.BufferGeometry().setFromPoints(linepts);
var lineMaterial = new THREE.LineBasicMaterial({
  color: 0xff5555,
  linewidth: 3 // due to OpenGL limitations this mostly has no effect. We would need to use a tube or MeshLine. Performance impact?
});
var line = new THREE.Line(lineGeometry, lineMaterial);
scene.add(line);

function setLine(vectorA, vectorB) {
  let psts = line.geometry.attributes.position.array;
  psts[0] = vectorA.x;
  psts[1] = 0.1;
  psts[2] = vectorA.z;
  psts[3] = vectorB.x;
  psts[4] = 0.1;
  psts[5] = vectorB.z;
  line.geometry.computeBoundingSphere(); // to update it
  line.geometry.attributes.position.needsUpdate = true;
}

// Grids translated
/*let g1 = GridGeometry(maxRT-minRT, maxInt, 4, 3, [0, 0]);
    g1.translate(0,0,minRT);
let m1 = new THREE.LineBasicMaterial({color: "yellow"});
let grid1 = new THREE.LineSegments(g1, m1);
scene.add(grid1);

let g2 = GridGeometry(maxRT-minRT, maxMZ-minMZ, 4, 2, [0, 0]);

g2.rotateX(Math.PI * 0.5);
    g2.translate(minMZ,0,minRT);
let m2 = new THREE.LineBasicMaterial({color: "magenta"});
let grid2 = new THREE.LineSegments(g2, m2);
scene.add(grid2);

let g3 = GridGeometry(maxMZ-minMZ, maxInt, 2, 3, [0, 0]);

g3.rotateY(Math.PI * -0.5);
    g3.translate(minMZ,0,0);
let m3 = new THREE.LineBasicMaterial({color: "aqua"});
let grid3 = new THREE.LineSegments(g3, m3);
scene.add(grid3);*/

//Grids untranslated, data points moved to origin
let g1 = GridGeometry(rtPaintWidth, intPaintWidth, 1, 1, [0, 0]);
let m1 = new THREE.LineBasicMaterial({color: "gray"});
let grid1 = new THREE.LineSegments(g1, m1);
scene.add(grid1);

let g2 = GridGeometry(rtPaintWidth, mzPaintWidth, 1, 1, [0, 0]);
g2.rotateX(Math.PI * 0.5);
let m2 = new THREE.LineBasicMaterial({color: "gray"});
let grid2 = new THREE.LineSegments(g2, m2);
scene.add(grid2);

let g3 = GridGeometry(mzPaintWidth, intPaintWidth, 1, 1, [0, 0]);
g3.rotateY(Math.PI * -0.5);
let m3 = new THREE.LineBasicMaterial({color: "gray"});
let grid3 = new THREE.LineSegments(g3, m3);
scene.add(grid3);

let g = new THREE.BoxGeometry(dotScale,1,dotScale);

// extend material to color from bottom to top
let m = THREE.extendMaterial(THREE.MeshPhongMaterial, {

    header: 'varying vec3;',

    vertex: {
        '#include <fog_vertex>': `
        vec4 mypos = instanceMatrix * vec4( position, 1.0 );
        float h = mypos.y/(0.2*100.0);
        if(vColor == vec3(1.0,1.0,1.0))
        {
          vColor = vec3(pow(h, 1.0), 2.0*h, 1.0 - h);
        }
        `
    },
    fragment: {
        'gl_FragColor = vec4( outgoingLight, diffuseColor.a );' : 'gl_FragColor.rgb = vColor;'
    }

});

camera = new THREE.PerspectiveCamera(60, innerWidth / innerHeight, 1, 1000);
camera.position.set(250, 200, 250);
renderer.setSize(container.getBoundingClientRect().width, container.getBoundingClientRect().height);
camera.aspect = container.getBoundingClientRect().width/container.getBoundingClientRect().height;

const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2( 1, 1 );

let controls = new THREE.OrbitControls(camera, renderer.domElement);

let c1 = new THREE.Color(0, 0.5, 1);
let c2 = new THREE.Color(0.5, 0, 1);
let c = new THREE.Color();

let o = new THREE.InstancedMesh(g, m, cnt);
    o.name = "peaks";

let dummy = new THREE.Object3D();
let mat4 = new THREE.Matrix4();

function getIntersections(event) {
  var mouseVec = new THREE.Vector2();
  mouseVec.x = ( event.offsetX / canvas.clientWidth ) * 2 - 1;
  mouseVec.y = - ( event.offsetY / canvas.clientHeight ) * 2 + 1;

  var raycaster = new THREE.Raycaster();
  const o = scene.getObjectByName("peaks");
  raycaster.setFromCamera(mouseVec, camera);
  return raycaster.intersectObject( o );
}


function updatePeaks(instMesh, withHeight, dotSize)
{
  var cnt2 = 0;
  for (let i = globalrtminidx; i < globalrtmaxidx; i++)
  {
    let mz = globaldata.data['mz'][i];
    //if (mz < minMZ || mz > maxMZ) continue;
    let x = (mz - minMZ) * scaleMZ;

    let hData = globaldata.data['inty'][i]*intPaintWidth/maxInt;

    let y = (globaldata.data['RT'][i] - minRT) * scaleRT;
    if (withHeight)
    {
      dummy.position.set(y,hData/2,x);
      dummy.scale.set(1, hData ,1);
      // if color is empty, the custom renderer should define color by height.
      instMesh.setColorAt(cnt2, new THREE.Color(1.0,1.0,1.0))
    }
    else
    {
      dummy.position.set(y,0,x);
      dummy.scale.set(dotSize, 0.00001 ,dotSize); // 0 height does not let me select anymore
      instMesh.setColorAt(cnt2, c.lerpColors(c1, c2, Math.log(hData)/Math.log(100)))
    }
    dummy.updateMatrix();
    instMesh.setMatrixAt(cnt2, dummy.matrix);
    cnt2++;
  }
  instMesh.instanceMatrix.needsUpdate = true;
  instMesh.instanceColor.needsUpdate = true;
}

scene.add(o);
updatePeaks(o,true,dotScale);




renderer.setAnimationLoop( _ => {
  stats.begin()
  raycaster.setFromCamera( mouse, camera );

  let o = scene.getObjectByName("peaks");
  const intersection = raycaster.intersectObject( o );

  if ( intersection.length > 0 ) {

    info.style.display = "block";
    const instanceId = intersection[ 0 ].instanceId;

    o.getMatrixAt(instanceId, mat4);
    mat4.decompose(dummy.position, dummy.quaternion, dummy.scale);

    //TODO when Top view is active, we rescale the height to 0.0001 so using dummy.scale.y is wrong.
    // We probably need to save the intensity somewhere else in the instMesh array. Like a custom data field.
    info.innerText = `int: ${dummy.scale.y*maxInt},\n RT: ${(dummy.position.x / scaleRT) + minRT},\n mz: ${(dummy.position.z/scaleMZ) + minMZ}`;

  }
  else {
    info.style.display = "none";
  }

  renderer.render(scene, camera);
  stats.end();
})

var guiTopView = { topview:function(){
      let o = scene.getObjectByName( "peaks" );
      //scene.remove(o);
      //o = new THREE.InstancedMesh(g, m, cnt);
      //o.name = "peaks";
      //TODO we could actually just change the scales. No need to go through the data again.
      //make the peaks flat and wider for top view
      updatePeaks(o,false,2);

      camera.position.x = (maxRT-minRT)*scaleRT/2;
      camera.position.y = 200;
      camera.position.z = (maxMZ-minMZ)*scaleMZ/2;
      camera.lookAt((maxRT-minRT)*scaleRT/2,0,(maxMZ-minMZ)*scaleMZ/2);
      camera.updateProjectionMatrix();
      controls.target.set((maxRT-minRT)*scaleRT/2,0,(maxMZ-minMZ)*scaleMZ/2);
      controls.enableRotate = false;
      controls.update();
      renderer.render(scene, camera);
}};

var guiFreeView = { freeview:function(){
      let o = scene.getObjectByName( "peaks" );
      //scene.remove(o);
      //o = new THREE.InstancedMesh(g, m, cnt);
      //o.name = "peaks";
      //TODO we could actually just change the scales. No need to go through the data again.
      //make the peaks flat and wider for top view
      updatePeaks(o,true,dotScale);
      controls.enableRotate = true;
      controls.update();
      renderer.render(scene, camera);
}};

gui.destroy();
gui = new dat.GUI({ autoPlace: false });
gui.add(guiTopView,'topview');
gui.add(guiFreeView,'freeview');
$('.threedplot').append($(gui.domElement));


canvas.addEventListener( 'mousemove', onMouseMove );
canvas.addEventListener('mousedown', onDocumentMouseDown, false);
container.addEventListener('resize', onContainerResize);

function onMouseMove( event ) {
  event.preventDefault();

  mouse.x = ( event.offsetX / canvas.clientWidth ) * 2 - 1;
  mouse.y = - ( event.offsetY / canvas.clientHeight ) * 2 + 1;
  info.style.transform = `translate(${event.offsetX + 15}px, ${event.offsetY + 5}px)`;

}

function onDocumentMouseDown(event) {

  if (event.button === 2) {
  var intersects = getIntersections(event);

  //sets all colors
  //intersects[ 0 ].object.material.color.set( 0xff0000 );

  if (intersects.length > 0) {
    var o = scene.getObjectByName("peaks");
    console.log(intersects[ 0 ].instanceId);
    //TODO reset to old colors
    o.setColorAt(intersects[ 0 ].instanceId, new THREE.Color(0xff5555));
    o.instanceColor.needsUpdate = true;
    o.getMatrixAt(intersects[ 0 ].instanceId, mat4);
    mat4.decompose(dummy.position, dummy.quaternion, dummy.scale);
    points[clicks].copy(dummy.position);
    //markers[clicks].position.copy(intersects[0].point);
    setLine(dummy.position, dummy.position);
    clicks++;
    if (clicks > 1){
      var distancert = Math.abs(points[0].x - points[1].x);
      var distancemz = Math.abs(points[0].z - points[1].z);
      distanceMZPlace.innerText = "Distance MZ: " + distancemz/scaleMZ + " Da";
      distanceRTPlace.innerText = "Distance RT: " + distancert/scaleRT + " s";
      setLine(points[0], points[1]);
      clicks = 0;
    }
  }
  }
}

//function onWindowResize() {
//
//  camera.aspect = window.innerWidth / window.innerHeight;
//  camera.updateProjectionMatrix();

//  renderer.setSize( window.innerWidth, window.innerHeight );

//}

function onContainerResize() {
    var box = container.getBoundingClientRect();
    renderer.setSize(box.width, box.height);

    camera.aspect = box.width/box.height
    camera.updateProjectionMatrix()
    // optional animate/renderloop call put here for render-on-changes
}

}



function renderAll(data) {
    var container = renderer.domElement.parentElement;
    var canvas = renderer.domElement
    var cnt = 0;
    var maxMZ = 0;
    var maxInt = 0;
    var maxRT = data[data.length-1]["time"]; //assumes sorted
    var minMZ = 1000000000000;
    var minInt = 1000000000000;
    var minRT = data[0]["time"]; //assumes sorted
    var scaleMZ = 20;
    var scaleRT = 3;
    var dotScale = 0.3;
for (const spec of data)
  {
     cnt += spec["m/z array"].length;
     maxMZ = Math.max(maxMZ,
                      spec["m/z array"].reduce(
       function(a, b) {
         return Math.max(a, b);
       })
     );
     maxInt = Math.max(maxInt,
                       spec["intensity array"].reduce(
       function(a, b) {
        return Math.max(a, b);
       })
     );
     minMZ = Math.min(minMZ,
                      spec["m/z array"].reduce(
       function(a, b) {
         return Math.min(a, b);
       })
     );
     minInt = Math.min(minInt,
                       spec["intensity array"].reduce(
       function(a, b) {
        return Math.min(a, b);
       })
     );
  }

console.log(maxMZ,maxInt,maxRT,cnt);

scene = new THREE.Scene();
scene.background = new THREE.Color("white");

var points = [
  new THREE.Vector3(),
  new THREE.Vector3()
]
var clicks = 0;

//we do not need markers where we clicked the peaks
/*var markerA = new THREE.Mesh(
  new THREE.SphereGeometry(0.1, 10, 20),
  new THREE.MeshBasicMaterial({
    color: 0xff5555
  })
);
var markerB = markerA.clone();
var markers = [
  markerA, markerB
];
scene.add(markerA);
scene.add(markerB);
*/

var linepts = []
linepts.push(new THREE.Vector3());
linepts.push(new THREE.Vector3());
var lineGeometry = new THREE.BufferGeometry().setFromPoints(linepts);
var lineMaterial = new THREE.LineBasicMaterial({
  color: 0xff5555,
  linewidth: 3 // due to OpenGL limitations this mostly has no effect. We would need to use a tube or MeshLine. Performance impact?
});
var line = new THREE.Line(lineGeometry, lineMaterial);
scene.add(line);

function setLine(vectorA, vectorB) {
  let psts = line.geometry.attributes.position.array;
  psts[0] = vectorA.x;
  psts[1] = 0.1;
  psts[2] = vectorA.z;
  psts[3] = vectorB.x;
  psts[4] = 0.1;
  psts[5] = vectorB.z;
  line.geometry.computeBoundingSphere(); // to update it
  line.geometry.attributes.position.needsUpdate = true;
}

// Grids translated
/*let g1 = GridGeometry(maxRT-minRT, maxInt, 4, 3, [0, 0]);
    g1.translate(0,0,minRT);
let m1 = new THREE.LineBasicMaterial({color: "yellow"});
let grid1 = new THREE.LineSegments(g1, m1);
scene.add(grid1);

let g2 = GridGeometry(maxRT-minRT, maxMZ-minMZ, 4, 2, [0, 0]);

g2.rotateX(Math.PI * 0.5);
    g2.translate(minMZ,0,minRT);
let m2 = new THREE.LineBasicMaterial({color: "magenta"});
let grid2 = new THREE.LineSegments(g2, m2);
scene.add(grid2);

let g3 = GridGeometry(maxMZ-minMZ, maxInt, 2, 3, [0, 0]);

g3.rotateY(Math.PI * -0.5);
    g3.translate(minMZ,0,0);
let m3 = new THREE.LineBasicMaterial({color: "aqua"});
let grid3 = new THREE.LineSegments(g3, m3);
scene.add(grid3);*/

//Grids untranslated, data points moved to origin
let g1 = GridGeometry((maxRT-minRT)*scaleRT, 100, 1, 1, [0, 0]);
let m1 = new THREE.LineBasicMaterial({color: "gray"});
let grid1 = new THREE.LineSegments(g1, m1);
scene.add(grid1);

let g2 = GridGeometry((maxRT-minRT)*scaleRT, (maxMZ-minMZ)*scaleMZ, 1, 1, [0, 0]);
g2.rotateX(Math.PI * 0.5);
let m2 = new THREE.LineBasicMaterial({color: "gray"});
let grid2 = new THREE.LineSegments(g2, m2);
scene.add(grid2);

let g3 = GridGeometry((maxMZ-minMZ)*scaleMZ, 100, 1, 1, [0, 0]);
g3.rotateY(Math.PI * -0.5);
let m3 = new THREE.LineBasicMaterial({color: "gray"});
let grid3 = new THREE.LineSegments(g3, m3);
scene.add(grid3);

let g = new THREE.BoxGeometry(dotScale,1,dotScale);

// extend material to color from bottom to top
let m = THREE.extendMaterial(THREE.MeshPhongMaterial, {

    header: 'varying vec3;',

    vertex: {
        '#include <fog_vertex>': `
        vec4 mypos = instanceMatrix * vec4( position, 1.0 );
        float h = mypos.y/(0.2*100.0);
        if(vColor == vec3(1.0,1.0,1.0))
        {
          vColor = vec3(pow(h, 1.0), 2.0*h, 1.0 - h);
        }
        `
    },
    fragment: {
        'gl_FragColor = vec4( outgoingLight, diffuseColor.a );' : 'gl_FragColor.rgb = vColor;'
    }

});

camera = new THREE.PerspectiveCamera(60, innerWidth / innerHeight, 1, 1000);
camera.position.set(0, 70, 150);
renderer.setSize(container.getBoundingClientRect().width, container.getBoundingClientRect().height);
camera.aspect = container.getBoundingClientRect().width/container.getBoundingClientRect().height;

const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2( 1, 1 );

let controls = new THREE.OrbitControls(camera, renderer.domElement);

let c1 = new THREE.Color(0, 0.5, 1);
let c2 = new THREE.Color(0.5, 0, 1);
let c = new THREE.Color();

let o = new THREE.InstancedMesh(g, m, cnt);
    o.name = "peaks";

let dummy = new THREE.Object3D();
let mat4 = new THREE.Matrix4();

function getIntersections(event) {
  var mouseVec = new THREE.Vector2();
  mouseVec.x = ( event.offsetX / canvas.clientWidth ) * 2 - 1;
  mouseVec.y = - ( event.offsetY / canvas.clientHeight ) * 2 + 1;

  var raycaster = new THREE.Raycaster();
  const o = scene.getObjectByName("peaks");
  raycaster.setFromCamera(mouseVec, camera);
  return raycaster.intersectObject( o );
}



function updatePeaks(instMesh, withHeight, dotSize)
    {
      var cnt2 = 0;
      for (const spec of data){
        for (var i = 0; i < spec["m/z array"].length; i++) {
            let x = (spec["m/z array"][i] - minMZ)*scaleMZ;
            let y = (spec["time"] - minRT)*scaleRT;
            let hData = spec["intensity array"][i]*100/maxInt;
            if (withHeight)
            {
              dummy.position.set(y,hData/2,x);
              dummy.scale.set(1, hData ,1);
              instMesh.setColorAt(cnt2, new THREE.Color())
            }
            else
            {
              dummy.position.set(y,0,x);
              dummy.scale.set(dotSize, 0.00001 ,dotSize); // 0 height does not let me select anymore
              instMesh.setColorAt(cnt2, c.lerpColors(c1, c2, Math.log(hData)/Math.log(100)))
            }
            dummy.updateMatrix();
            instMesh.setMatrixAt(cnt2, dummy.matrix);
            cnt2++;
        }
      }
      instMesh.instanceMatrix.needsUpdate = true;
      instMesh.instanceColor.needsUpdate = true;
    }

scene.add(o);
updatePeaks(o,true,dotScale);


renderer.setAnimationLoop( _ => {
  stats.begin()
  raycaster.setFromCamera( mouse, camera );

  let o = scene.getObjectByName("peaks");
  const intersection = raycaster.intersectObject( o );

  if ( intersection.length > 0 ) {

    info.style.display = "block";
    const instanceId = intersection[ 0 ].instanceId;

    o.getMatrixAt(instanceId, mat4);
    mat4.decompose(dummy.position, dummy.quaternion, dummy.scale);

    info.innerText = `int: ${dummy.scale.y*maxInt},\n RT: ${(dummy.position.x / scaleRT) + minRT},\n mz: ${(dummy.position.z/scaleMZ) + minMZ}`;

  }
  else {
    info.style.display = "none";
  }

  renderer.render(scene, camera);
  stats.end();
})

var guiTopView = { topview:function(){
      let o = scene.getObjectByName( "peaks" );
      //scene.remove(o);
      //o = new THREE.InstancedMesh(g, m, cnt);
      //o.name = "peaks";
      //TODO we could actually just change the scales. No need to go through the data again.
      //make the peaks flat and wider for top view
      updatePeaks(o,false,2);

      camera.position.x = (maxRT-minRT)*scaleRT/2;
      camera.position.y = 100;
      camera.position.z = (maxMZ-minMZ)*scaleMZ/2;
			camera.lookAt((maxRT-minRT)*scaleRT/2,0,(maxMZ-minMZ)*scaleMZ/2);
      camera.updateProjectionMatrix();
      controls.target.set((maxRT-minRT)*scaleRT/2,0,(maxMZ-minMZ)*scaleMZ/2);
      controls.enableRotate = false;
      controls.update();
      renderer.render(scene, camera);
}};

var guiFreeView = { freeview:function(){
      let o = scene.getObjectByName( "peaks" );
      //scene.remove(o);
      //o = new THREE.InstancedMesh(g, m, cnt);
      //o.name = "peaks";
      //TODO we could actually just change the scales. No need to go through the data again.
      //make the peaks flat and wider for top view
      updatePeaks(o,true,1);
      controls.enableRotate = true;
      controls.update();
      renderer.render(scene, camera);
}};

gui.destroy();
gui = new dat.GUI({ autoPlace: false });
gui.add(guiTopView,'topview');
gui.add(guiFreeView,'freeview');
$('.threedplot').append($(gui.domElement));


canvas.addEventListener( 'mousemove', onMouseMove );
canvas.addEventListener('mousedown', onDocumentMouseDown, false);
container.addEventListener('resize', onContainerResize);

function onMouseMove( event ) {
  event.preventDefault();

  mouse.x = ( event.offsetX / canvas.clientWidth ) * 2 - 1;
  mouse.y = - ( event.offsetY / canvas.clientHeight ) * 2 + 1;
  info.style.transform = `translate(${event.offsetX + 15}px, ${event.offsetY + 5}px)`;

}

function onDocumentMouseDown(event) {

  if (event.button === 2) {
  var intersects = getIntersections(event);

  //sets all colors
  //intersects[ 0 ].object.material.color.set( 0xff0000 );

  if (intersects.length > 0) {
    var o = scene.getObjectByName("peaks");
    console.log(intersects[ 0 ].instanceId);
    //TODO reset to old colors
    o.setColorAt(intersects[ 0 ].instanceId, new THREE.Color(0xff5555));
    o.instanceColor.needsUpdate = true;
    o.getMatrixAt(intersects[ 0 ].instanceId, mat4);
    mat4.decompose(dummy.position, dummy.quaternion, dummy.scale);
    points[clicks].copy(dummy.position);
    //markers[clicks].position.copy(intersects[0].point);
    setLine(dummy.position, dummy.position);
    clicks++;
    if (clicks > 1){
      var distancert = Math.abs(points[0].x - points[1].x);
      var distancemz = Math.abs(points[0].z - points[1].z);
      distanceMZPlace.innerText = "Distance MZ: " + distancemz/scaleMZ + " Da";
      distanceRTPlace.innerText = "Distance RT: " + distancert/scaleRT + " s";
      setLine(points[0], points[1]);
      clicks = 0;
    }
  }
  }
}

//function onWindowResize() {
//
//  camera.aspect = window.innerWidth / window.innerHeight;
//  camera.updateProjectionMatrix();

//  renderer.setSize( window.innerWidth, window.innerHeight );

//}

function onContainerResize() {
    var box = container.getBoundingClientRect();
    renderer.setSize(box.width, box.height);

    camera.aspect = box.width/box.height
    camera.updateProjectionMatrix()
    // optional animate/renderloop call put here for render-on-changes
}

}



