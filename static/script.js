<script>
let currentSlide = 0;
const slideInput = document.getElementById("slideNumber");

// Find all slides with numeric IDs and sort them
const slides = Array.from(document.querySelectorAll("div[id]"))
  .filter(div => !isNaN(div.id))
  .sort((a, b) => Number(a.id) - Number(b.id));

// Function to go to a slide
const goToSlide = n => {
  const slide = slides.find(s => Number(s.id) === n);
  if (!slide) return;
  slide.scrollIntoView({ behavior: "smooth", block: "center" });
  currentSlide = n;
  slideInput.value = currentSlide;
};

// On page load, go to slide 0
goToSlide(0);

// Up/Down buttons
document.getElementById("up").addEventListener("click", () => goToSlide(currentSlide - 1));
document.getElementById("down").addEventListener("click", () => goToSlide(currentSlide + 1));

// Input events
slideInput.addEventListener("change", () => goToSlide(Number(slideInput.value)));
slideInput.addEventListener("keydown", e => {
  if (e.key === "ArrowUp") goToSlide(currentSlide + 1);
  if (e.key === "ArrowDown") goToSlide(currentSlide - 1);
});
</script>
