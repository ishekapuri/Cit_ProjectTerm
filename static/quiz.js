var currentSlide = 0;
var currentIndex = 0;
var carouselLength = 0;
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

    var cards = await response.json();
    remainingCards = JSON.parse(cards.remainingCards);

    console.log(cards);
  } catch (error) {
    console.error(error.message);
  }
}

async function startQuiz() {
    const quizContainer = document.getElementById("quiz-overlay");
    quizContainer.classList.remove("d-none");
    quizContainer.classList.add("d-flex");
    await getData();
    carouselLength = remainingCards.length;
}

async function stopQuiz() {
    const quizContainer = document.getElementById("quiz-overlay");
    quizContainer.classList.add("d-none");
    quizContainer.classList.remove('blurred')
    alert(`Quiz Completed! Your score is ${completedCards.length} out of ${carouselLength}`);
    await logResult();
    location.reload();
}

function disableButton() {
    document.querySelectorAll('.quiz-btn').forEach(btn => btn.disabled = true);
    setTimeout(() => {
        document.querySelectorAll('.quiz-btn').forEach(btn => btn.disabled = false);
    }
    , 1000);
}

function addCompletedCard(buttonElement) {
    console.log(`Carousel Length: ${carouselLength}`);
    console.log(`Current Slide: ${currentSlide}`);

    card = remainingCards[currentSlide];
    console.log(`Card: ${JSON.stringify(card)}`);
    completedCards.push(JSON.stringify(card));
    console.log(`Completed Cards: ${JSON.stringify(completedCards)}`);

    disableButton();

    currentIndex++;

    if(currentIndex == carouselLength) {
        stopQuiz();
    }
}

function forgotCard(buttonElement) {
    disableButton();
    currentIndex++;

    if(currentIndex == carouselLength) {
        stopQuiz();
    }
}


async function logResult() {
    try {
        var url = window.location.href + "/api/update";
        const response = await fetch(url, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(completedCards),
        });
    } catch (error) {
        console.error(error.message);
    }
}

async function shuffleCards() {
    try {
        var url = window.location.href + "/api/shuffle";
        const response = await fetch(url, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(completedCards),
        });
    } catch (error) {
        console.error(error.message);
    }
    location.reload();
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
