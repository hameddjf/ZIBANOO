import Swiper from "swiper";
import "swiper/css";
import { Autoplay } from "swiper/modules";
var swiper = new Swiper(".mySwiper", {
  slidesPerView: 1,
  spaceBetween: 10,
    autoplay: {
      delay: 2500,
      disableOnInteraction: false,
    },
  breakpoints: {
    500: {
      slidesPerView: 2,
      spaceBetween: 20,
    },
    768: {
      slidesPerView: 4,
      spaceBetween: 40,
    },
    1024: {
      slidesPerView: 4,
      spaceBetween: 50,
    },
  },
  modules: [Autoplay],
});
