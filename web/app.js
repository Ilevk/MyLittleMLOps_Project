const canvas = document.getElementById("jsCanvas");
const ctx = canvas.getContext("2d");
const colors = document.getElementsByClassName("jsColor");
const range = document.getElementById("jsRange");
const mode = document.getElementById("jsMode");
const erase = document.getElementById("jsErase");
const palette = document.getElementById("palette");
const url = 'http://20.194.38.80:35000/draw';
let file;

canvas.width = 500;
canvas.height = 500;
// 기본 설정
ctx.fillStyle = "black";
ctx.fillRect(0, 0, canvas.width, canvas.height);

ctx.strokeStyle = "#2c2c2c"; // strokeStyle 은 예약어임.'
ctx.fillStyle = "#2c2c2c";
ctx.lineWidth = 5;
ctx.lineCap = 'round'

background = "black";

let painting = false;
let filling = false;

stopPainting = () => {
  painting = false;
};

onMouseMove = e => {
  console.log(e);
  const x = e.offsetX;
  const y = e.offsetY;
  if (!painting) {
    ctx.beginPath();
    ctx.moveTo(x, y);
  } else {
    ctx.lineTo(x, y);
    ctx.stroke();
  }
};

startPainting = () => {
  painting = true;
};

handleCanvasClick = () => {
  if (filling) {
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    background = ctx.fillStyle;
  }
};

handleCM = e => {
  e.preventDefault();
};

function setPredictUpload(){
  file = document.getElementById('imageUpload').files[0]
}

function setPredictCanvas(){
  // predict can take in an image, video or canvas html element
  const imgDataUrl = canvas.toDataURL('image/png');
  var blobBin = atob(imgDataUrl.split(',')[1]);	// base64 데이터 디코딩
  var array = [];
  for (var i = 0; i < blobBin.length; i++) {
      array.push(blobBin.charCodeAt(i));
  }
  file = new Blob([new Uint8Array(array)], {type: 'image/png'});	// Blob 생성
}


async function predict() {
  var form = new FormData();
  form.append("input_file", file, "tmp.png");

  $.ajax({
    "url": url,
    "method": "POST",
    "timeout": 0,
    "processData": false,
    "mimeType": "multipart/form-data",
    "contentType": false,
    "data": form,
    "responsetype": "blob"
  })
    .done(function (data) {
      $('#drawimagePreview').attr('display', `inherit`);
      $('#drawimagePreview').attr('src', `data:image/jpeg;base64,${data}`);
      $('#drawimagePreview').fadeIn(650);
      $('#subjectDraw').attr('display', `inherit`);
      $('#subjectDraw').hide();
      $('#subjectDraw').fadeIn(650);
    })

}

if (canvas) {
  canvas.addEventListener("mousemove", onMouseMove);
  canvas.addEventListener("mousedown", startPainting);
  canvas.addEventListener("mouseup", stopPainting);
  canvas.addEventListener("mouseleave", stopPainting);
  canvas.addEventListener("click", handleCanvasClick);
  canvas.addEventListener("contextmenu", handleCM);
}

changeColor = e => {
  const color = e.target.style.backgroundColor;
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
};

handleRangeChange = e => {
  const brushWidth = e.target.value;
  ctx.lineWidth = brushWidth;
};

Array.from(colors).forEach(color =>
  color.addEventListener("click", changeColor)
);

if (range) {
  range.addEventListener("input", handleRangeChange);
}

handleModeClick = e => {
  if (filling) {
    filling = false;
    mode.innerText = "배경색";
  } else {
    filling = true;
    mode.innerText = "선";
  }
};

handleEraseClick = e => {
  ctx.fillStyle = "black";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
};

changeColorByPalette = e => {
  const color = e.target.value;
  ctx.strokeStyle = "#" + color;
  ctx.fillStyle = "#" + color;
};

if (mode) {
  mode.addEventListener("click", handleModeClick);
}

if (erase) {
  erase.addEventListener("click", handleEraseClick);
}

if (palette) {
  palette.addEventListener("blur", changeColorByPalette);
}
