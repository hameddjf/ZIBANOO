import Swiper from "swiper";
import "swiper/css";
// import 'swiper/css/navigation';
import { Autoplay, Navigation } from "swiper/modules";

var swiper = new Swiper(".mySwiper", {
  slidesPerView: 1,
  spaceBetween: 10,
  autoplay: {
    delay: 2500,
    disableOnInteraction: false,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  breakpoints: {
    "@0.00": {
      slidesPerView: 1,
      spaceBetween: 10,
    },
    "@0.75": {
      slidesPerView: 2,
      spaceBetween: 20,
    },
    "@1.00": {
      slidesPerView: 3,
      spaceBetween: 40,
    },
    // "@1.50": {
    //   slidesPerView: 4,
    //   spaceBetween: 50,
    // },
  },
  modules: [Autoplay, Navigation],
});
var swiper = new Swiper(".mySwiper2", {
  slidesPerView: 1,
  loop: true,
  centeredSlides: true,
  autoplay: {
    delay: 2500,
    disableOnInteraction: false,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  breakpoints: {
    "@0.00": {
      slidesPerView: 1,
      spaceBetween: 10,
    },
    "@0.75": {
      slidesPerView: 2,
      spaceBetween: 20,
    },
    "@1.00": {
      slidesPerView: 4,
      spaceBetween: 30,
    },
    // "@1.50": {
    //   slidesPerView: 4,
    //   spaceBetween: 50,
    // },
  },
  modules: [Navigation],
});
const sliderBtnPrevs = document.querySelectorAll(".swiper-button-prev");
const sliderBtnNexts = document.querySelectorAll(".swiper-button-next");

sliderBtnPrevs.forEach((sliderBtnPrev) => {
  swiper.on("slideChange", () => {
    if (!sliderBtnPrev.classList.contains("swiper-button-disabled")) {
      sliderBtnPrev.classList.add("bg-btnPrimary");
      sliderBtnPrev.classList.remove("bg-btnSecondary");
    } else {
      sliderBtnPrev.classList.remove("bg-btnPrimary");
      sliderBtnPrev.classList.add("bg-btnSecondary");
    }
  });
});

sliderBtnNexts.forEach((sliderBtnNext) => {
  swiper.on("slideChange", () => {
    if (sliderBtnNext.classList.contains("swiper-button-disabled")) {
      sliderBtnNext.classList.remove("bg-btnPrimary");
      sliderBtnNext.classList.add("bg-btnSecondary");
    } else {
      sliderBtnNext.classList.add("bg-btnPrimary");
      sliderBtnNext.classList.remove("bg-btnSecondary");
    }
  });
});
