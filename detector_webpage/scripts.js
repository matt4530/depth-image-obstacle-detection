function getPHPscript(scriptName, paramString, callback) {
  var phphttp = new XMLHttpRequest();

  phphttp.onreadystatechange = function() {
    
    if (phphttp.readyState === 4 && phphttp.status === 200) {
      if (typeof callback === 'function') {
        console.info('response', phphttp.responseText);
        callback(phphttp.responseText);
      }
    }
    
  };
  phphttp.open('GET', scriptName+'?'+paramString, true);
  phphttp.send();
}

function getFiles(set_type) {
  
  getPHPscript('getfiles.php', 'set_type=' + set_type, (data) => {
    imageNames = JSON.parse(data).filter((fileName) => {
      return fileName.substring(0, 9) === 'depth_viz';
    });
    console.log(imageNames);
    
    setImages(imageNames[0]);
    
  });
}

function setImages(imageName) {
  document.getElementById('rgb_image').src = FOLDER_DIR  + imageName.replace('depth_viz', 'rbg');
  document.getElementById('depth_image').src = FOLDER_DIR + imageName;
}


function setClass(currentImageName, classification) {
  results[currentImageName.replace('depth_viz', 'depth').replace('.jpg', '.txt')] = classification;
}

function yesClick() {
  setClass(imageNames[currentImageIndex], 'yes');
  nextImage();
}

function noClick() {
  setClass(imageNames[currentImageIndex], 'no');
  nextImage();
}

function nextImage() {
  console.log('results so far', results);
  currentImageIndex++;
  setImages(imageNames[currentImageIndex]);
  display();
}

function display() {
  document.getElementById('results').value = JSON.stringify(results, null, 3);
  console.log('hi');
}

/*
 *  
 * TO CHANGE DATA SETS, CHANGE THIS VARIABLE
 * 
 */
const SET_TYPE = 'train';


const FOLDER_DIR = 'datasets/' + SET_TYPE +'/';
document.getElementById('data_set_type').innerHTML = SET_TYPE + ' set';

let currentImageIndex = 0;
let imageNames = [];
let results = {};
getFiles(SET_TYPE);

document.addEventListener('keypress', (event) => {
  if (event.key === 'y') {
    yesClick();
  }
  else if (event.key === 'n') {
    noClick();
  }
});


