const cards = document.querySelectorAll('.flashcardcontent');
for (let i = 0; i < cards.length; i++) {
    cards[i].addEventListener('click', function() {
        const innerCard = cards[i].querySelector('.card-inner');
        innerCard.classList.toggle('flipped');
    });
}


function toggleButtons() {
    const show = document.getElementById('editToggle').checked;
    const editButtons = document.querySelectorAll('.edit-button');
    const deleteButtons = document.querySelectorAll('.delete-button');

    editButtons.forEach(btn => { btn.classList.toggle('hidden', !show)});
    deleteButtons.forEach(btn => {btn.classList.toggle('hidden', !show)});

    }
  
