<script>
let currentSlide = 0;
let count = document.querySelectorAll('.frame').length;
console.log(count)
const slideInput = document.getElementById("slideNumber");
const fullscreenBtn = document.getElementById("fullscreen");
let presentationMode = false;
let scrollLocked = false;
const SCROLL_DELAY = 300;

fullscreenBtn?.addEventListener("click", toggleFullscreen);

function toggleFullscreen() {
  const root = document.documentElement;

  if (!document.fullscreenElement) {
    root.requestFullscreen();
    root.classList.add("presentation");
    presentationMode = true;
    currentSlide = 0;
    goToSlide(0);
  } else {
    document.exitFullscreen();
    root.classList.remove("presentation");
    presentationMode = false;
    goToSlide(0);
    goToSlide(currentSlide);
  }
}

document.addEventListener("fullscreenchange", () => {
  const root = document.documentElement;

  if (!document.fullscreenElement) {
    root.classList.remove("presentation");
    presentationMode = false;
  }
});

function updateActiveSlide(n) {
  document.querySelectorAll(".frame.active")
    .forEach(f => f.classList.remove("active"));

  const frame = document.getElementById(String(n));
  if (frame) frame.classList.add("active");
}


// Find all slides with numeric IDs and sort them
const slides = Array.from(document.querySelectorAll("div[id]"))
  .filter(div => !isNaN(div.id))
  .sort((a, b) => Number(a.id) - Number(b.id));

// sleep func
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

// Function to go to a slide
const goToSlide = async (n) => {
  const slide = slides.find(s => Number(s.id) === n);
  if (!slide) return;

  if (presentationMode) {
    console.log(n);
    await updateActiveSlide(n);
    if (!document.getElementById(currentSlide).classList.contains("NoneOut")) {
      console.log("HERE WAIT");
      await sleep(300);
    } else {
      await sleep(1);
      console.log("NOT WAIT");
    }
    slide.scrollIntoView({ behavior: "instant", block: "center" });
  } else {
    slide.scrollIntoView({ behavior: "smooth", block: "center" });
  }
  currentSlide = n;
  slideInput.value = currentSlide;
};

// On page load, go to slide 0
goToSlide(0);

// Up/Down buttons
document.getElementById("start").addEventListener("click", () => goToSlide(0));
document.getElementById("up").addEventListener("click", () => goToSlide(currentSlide - 1));
document.getElementById("down").addEventListener("click", () => goToSlide(currentSlide + 1));
document.getElementById("end").addEventListener("click", () => goToSlide(count - 1));

// Input events
slideInput.addEventListener("change", () => goToSlide(Number(slideInput.value)));
window.addEventListener("keydown", e => {
  if (e.key === "ArrowDown") {e.preventDefault(); goToSlide(currentSlide + 1)};
  if (e.key === "ArrowUp") {e.preventDefault(); goToSlide(currentSlide - 1)};
});
window.addEventListener("wheel", e => {
  e.preventDefault();
  if (scrollLocked) return;
  scrollLocked = true;
  if (e.deltaY > 0) goToSlide(currentSlide+1) 
  else goToSlide(currentSlide-1);
  setTimeout(() => { scrollLocked = false; }, SCROLL_DELAY);
  }, { passive: false });
</script>
