var express = require('express');
var router = express.Router();
const Object_db = require('../models/object');
const Annotation = require('../models/annotation');
const checkAuthenticated = require('../middlewares/index').checkAuthenticated;

const yaml = require('js-yaml');
const fs   = require('fs');

var path = require('path');
// var abc_obj_path = './public/abc_dataset/chunk_000/obj/';
let abc_obj_root_path = '/obj/';
let abc_feat_root_path = '/abc_dataset/feat/';

function pad(num, size) {
  var s = String(num)+"";
  while (s.length < size) s = "0" + s;
  return s;
}

async function load_file(folder) {
  let abc_obj_path = abc_obj_root_path + 'chunk_' + pad(Math.floor(parseInt(folder)/10000), 3) + '/'
  let abc_feat_path = abc_feat_root_path + 'chunk_' + pad(Math.floor(parseInt(folder)/10000), 3) + '/'
  let parsed_feat = '';
  let obj_path = '';
  let decimated = false
  if (fs.statSync('/abc_dataset'+abc_obj_path+folder).isDirectory()) {
    var items = fs.readdirSync('/abc_dataset'+abc_obj_path+folder)
    for (let item of items) {
      if (item.endsWith('decimated.obj')) {
        obj_path = abc_obj_path+folder+'/'+item
        decimated = true
        break;
      }
      if (item.endsWith('.obj')) {
        // obj_path = fs.readFileSync(path.join(abc_feat_path, folder, item), 'utf8')
        obj_path = abc_obj_path+folder+'/'+item
      }
    }
  }
  if (fs.statSync(abc_feat_path+folder).isDirectory()) {
    var items = fs.readdirSync(abc_feat_path+folder)
    for (let item of items) {
      if (item.endsWith('decimated.yml')) {
        parsed_feat = yaml.safeLoad(fs.readFileSync(path.join(abc_feat_path, folder, item), 'utf8'));
        break;
      }
      if (item.endsWith('.yml')) {
        parsed_feat = yaml.safeLoad(fs.readFileSync(path.join(abc_feat_path, folder, item), 'utf8'));
      }
    }
  }
  if (obj_path == '' || parsed_feat == '') {
    throw Error('nothing to read')
  }
  const obj = new Object_db();
  let onShapeId;
  let onShapeURL;
  let onShapeURLPart;
  try {
    onShapeId = await obj.get_on_shape_id(folder)
    onShapeURL = await obj.get_on_shape_url(folder)
    onShapeURLPart = await obj.get_on_shape_url_part(folder)
  } catch(e) {
    throw Error('Cannot get Onshape ID')
  }
  return {objPath: obj_path, feat: parsed_feat.surfaces, onShapeId: onShapeId, onShapeURL: onShapeURL, onShapeURLPart: onShapeURLPart, decimated: decimated}
}

router.get('/filename/:folder', async (req, res) => {
  let obj_file;
  try {
    obj_file = await load_file(req.params.folder)
    res.json(obj_file)
    
  } catch(e) {
    console.log(e)
    res.status(400).send('failed to read file')
  }
});

router.get('/complete_model/:folder', async (req, res) => {
  const obj = new Object_db();
  try {
    object_list = await obj.get_same_assembly_obj(req.params.folder);
    console.log('COMPLETE:', object_list)
  } catch(e) {
    console.log(e);
  }
  let fileList = []
  for (const obj_id of object_list) {
    const data = await load_file(obj_id)
    fileList.push({...data, folderNmae: obj_id})
  }
  res.json(fileList)
})

router.post('/test', checkAuthenticated, async (req, res) => {
  const annotation = new Annotation();
  var my_data = req.body
  var annotation_data = {}
  annotation_data.objectId = my_data.objectId
  annotation_data.componentType = my_data.componentType
  annotation_data.modelType = my_data.modelType
  annotation_data.partDescription = my_data.partDescription
  annotation_data.productCategory = my_data.productCategory
  annotation_data.productClassification = [my_data.productClassification, my_data.firstCategory, my_data.secCategory, my_data.thirdCategory].filter(Boolean)
  annotation_data.wikiUrl = my_data.wikiUrl

  var my_material = []
  if (!my_data.materialCategory) {
    my_data.materialCategory = []
  } else if (!Array.isArray(my_data.materialCategory)) {
    my_data.materialCategory = [my_data.materialCategory]
    my_data.subMaterialCategory = [my_data.subMaterialCategory]
  }
  for (var i=0; i<my_data.materialCategory.length; i++) {
    let mat = {}
    mat[my_data.materialCategory[i]] = my_data.subMaterialCategory[i]
    my_material.push(mat)
  }
  annotation_data.materialCategory = my_material
  annotation_data.quantityProduced = my_data.quantityProduced
  annotation_data.precisionNeeded = my_data.precisionNeeded
  
  annotation_data.processCategory = []
  if (my_data.mainProcessCategory) {
    let process = {}
    process[my_data.mainProcessCategory] = my_data.subMainProcessCategory
    annotation_data.processCategory.push(process)
  }
  if (my_data.secondProcessCategory) {
    let process = {}
    process[my_data.secondProcessCategory] = my_data.subSecondProcessCategory
    annotation_data.processCategory.push(process)
  }
  annotation_data.goodQuality = my_data.goodQuality
  Object.keys(annotation_data).forEach(key => annotation_data[key] === undefined && delete annotation_data[key])
  annotation_data['annotator'] = req.user.id
  annotation_data['finishTime'] = new Date()
  annotation_data['done'] = true

  await annotation.update(req.user.id, annotation_data['objectId'], annotation_data)
  res.redirect('/');
});


router.post('/skip/:id', checkAuthenticated, async (req, res) => {
  const annotation = new Annotation();
  await annotation.delete(req.user.id, req.params.id)
  res.send("Success.");
});

router.get('/', checkAuthenticated, async (req, res) => {
  if (req.user.role == "admin") {
    res.redirect('/batch-assign');
    return
  }
  const obj = new Object_db();
  var object_list = []
  try {
    object_list = await obj.get_not_done(req.user.id);
  } catch(e) {
    console.log(e);
  }
  // surfaces: JSON.stringify(feat_doc.surfaces)
  res.render('index', { title: '3d-annotation', hello: object_list.sort(), admin: req.user.role=="admin" });

});

module.exports = router;
