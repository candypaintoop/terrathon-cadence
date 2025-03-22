import gsap from "gsap";
import ScrollTrigger from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

// Animate the "Our Company" section
gsap.from("#our-company", {
  opacity: 0,
  y: 50,
  duration: 1,
  scrollTrigger: {
    trigger: "#our-company",
    start: "top 80%",
  }
});

// Animate the "Sustainability Goals" section
gsap.from("#sustainability-goals", {
  opacity: 0,
  x: 100,
  duration: 1,
  scrollTrigger: {
    trigger: "#sustainability-goals",
    start: "top 80%",
  }
});
