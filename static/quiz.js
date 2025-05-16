var currentSlide = NaN;
var remainingCards = [];
var completedCards = [];

async function getData() {
  var url = window.location.href + "/api/remCards";
  console.log(url);
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    remainingCards = await response.json();

    console.log(remainingCards);
  } catch (error) {
    console.error(error.message);
  }
}


async function startQuiz() {
    const quizContainer = document.getElementById("quiz-overlay");
    quizContainer.className = "d-flex justify-content-center align-items-center";
    quizContainer.classList.add('blurred')
    await getData()
}

function stopQuiz() {
    const quizContainer = document.getElementById("quiz-overlay");
    quizContainer.className = "d-none";
    quizContainer.classList.remove('blurred')
    logResult()
}

function addCompletedCard() {
    card = remainingCards[currentSlide];
    console.log(card);
    completedCards.push(card);
    console.log(completedCards);
}

async function logResult() {
    try {
        var url = window.location.href + "/api/update";
        const response = await fetch(url, {
        method: "PUT",
        body: JSON.stringify(completedCards),
        });
    } catch (error) {
        console.error(error.message);
    }

}

var myCarousel = document.querySelector('#cardCarousel')
var carousel = new bootstrap.Carousel(myCarousel, {
    wrap: false
})

document.querySelectorAll('#cardCarousel').forEach(function(carousel) {
    carousel.addEventListener('slide.bs.carousel', function(e) {
        var activeSlide = carousel.querySelector('.active');
        currentSlide = Array.prototype.indexOf.call(carousel.querySelectorAll('.carousel-item'), activeSlide);
        var slideTo = Array.prototype.indexOf.call(carousel.querySelectorAll('.carousel-item'), e.relatedTarget);
    });
});
