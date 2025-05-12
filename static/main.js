const downloadBtn = document.querySelector("button");
const inputBox = document.querySelector("input[type='text']")

const baseColor = "#b4befe";
const hoverColor = "#f38ba8";

downloadBtn.addEventListener("mouseover", () => {
    downloadBtn.style.backgroundColor = hoverColor;
    inputBox.style.borderColor = hoverColor;
});

downloadBtn.addEventListener("mouseout", () => {
    downloadBtn.style.backgroundColor = baseColor;
    inputBox.style.borderColor = baseColor;
});